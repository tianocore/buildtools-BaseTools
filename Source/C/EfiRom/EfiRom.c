/*++

Copyright (c)  1999-2007 Intel Corporation. All rights reserved
This program and the accompanying materials are licensed and made available 
under the terms and conditions of the BSD License which accompanies this 
distribution.  The full text of the license may be found at
http://opensource.org/licenses/bsd-license.php

THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.

Module Name:

  EfiRom.c
  
Abstract:

  Utility program to create an EFI option ROM image from binary and 
  EFI PE32 files.


--*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include <Common/UefiBaseTypes.h>
#include <IndustryStandard/PeImage.h> // for PE32 structure definitions

#include <IndustryStandard/pci22.h>  // for option ROM header structures
#include <IndustryStandard/pci30.h>

#include "Compress.h"
#include "CommonLib.h"

//
// Version of this utility
//
#define UTILITY_NAME "EfiRom"
#define UTILITY_MAJOR_VERSION 0
#define UTILITY_MINOR_VERSION 1

//
// Define some status return values
//
#define STATUS_SUCCESS  0
#define STATUS_WARNING  1
#define STATUS_ERROR    2

//
// Define the max length of a filename
//
#define MAX_PATH                  200

#define DEFAULT_OUTPUT_EXTENSION  ".rom"

//
// Max size for an option ROM image
//
#define MAX_OPTION_ROM_SIZE (1024 * 1024 * 16)  // 16MB
//
// Values for the indicator field in the PCI data structure
//
#define INDICATOR_LAST  0x80  // last file in series of files
//
// Masks for the FILE_LIST.FileFlags field
//
#define FILE_FLAG_BINARY    0x01
#define FILE_FLAG_EFI       0x02
#define FILE_FLAG_COMPRESS  0x04

//
// Use this linked list structure to keep track of all the filenames
// specified on the command line.
//
typedef struct _FILE_LIST {
  struct _FILE_LIST *Next;
  INT8              *FileName;
  UINT32            FileFlags;
  UINT32            ClassCode;
  UINT16            CodeRevision;
} FILE_LIST;

//
// Use this to track our command-line options
//
typedef struct {
  INT8      OutFileName[MAX_PATH];
  INT8      NoLast;
  INT8      Verbose;
  INT8      DumpOption;
  INT8      Pci23;
  UINT8     DevIdValid;
  UINT8     VendIdValid;
  UINT16    VendId;
  UINT16    DevId;
  FILE_LIST *FileList;
} OPTIONS;

//
// Make a global structure to keep track of command-line options
//
static OPTIONS  mOptions;

//
// Use these to convert from machine type value to a named type
//
typedef struct {
  UINT16  Value;
  char    *Name;
} STRING_LOOKUP;

static STRING_LOOKUP  mMachineTypes[] = {
  EFI_IMAGE_MACHINE_IA32,
  "IA32",
  EFI_IMAGE_MACHINE_IA64,
  "IA64",
  EFI_IMAGE_MACHINE_EBC,
  "EBC",
  0,
  NULL
};

static STRING_LOOKUP  mSubsystemTypes[] = {
  EFI_IMAGE_SUBSYSTEM_EFI_APPLICATION,
  "EFI application",
  EFI_IMAGE_SUBSYSTEM_EFI_BOOT_SERVICE_DRIVER,
  "EFI boot service driver",
  EFI_IMAGE_SUBSYSTEM_EFI_RUNTIME_DRIVER,
  "EFI runtime driver",
  0,
  NULL
};

static char* mCodeTypeStr[] = {
  "PCAT Image",
  "Open Firmware Image",
  "HP PA RISC Image",
  "EFI Image",
  "Undefined"
};

//
//  Function prototypes
//
static
void
Version (
  VOID
  );

static
void
Usage (
  VOID
  );

static
int
ParseCommandLine (
  int       Argc,
  char      *Argv[],
  OPTIONS   *Options
  );

static
int
CheckPE32File (
  FILE      *Fptr,
  UINT16    *MachineType,
  UINT16    *SubSystem
  );

static
int
ProcessEfiFile (
  FILE      *OutFptr,
  FILE_LIST *InFile,
  UINT16    VendId,
  UINT16    DevId,
  UINT32    *Size
  );

static
int
ProcessBinFile (
  FILE      *OutFptr,
  FILE_LIST *InFile,
  UINT32    *Size
  );

static
void
DumpImage (
  INT8 *InFileName
  );

char                  *
GetMachineTypeStr (
  UINT16    MachineType
  );

static
char                  *
GetSubsystemTypeStr (
  UINT16  SubsystemType
  );

int
main (
  int   Argc,
  char  *Argv[]
  )
/*++

Routine Description:
  
  Given an EFI image filename, create a ROM-able image by creating an option 
  ROM header and PCI data structure, filling them in, and then writing the
  option ROM header + PCI data structure + EFI image out to the output file.

Arguments:

  Argc            - standard C main() argument count

  Argv            - standard C main() argument list

Returns:

  0             success
  non-zero      otherwise

--*/
{
  INT8      *Ext;
  FILE      *FptrOut;
  UINT32    Status;
  FILE_LIST *FList;
  UINT32    TotalSize;
  UINT32    Size;

  SetUtilityName(UTILITY_NAME);
  Status  = STATUS_SUCCESS;
  FptrOut = NULL;

  //
  // Parse the command line arguments
  //
  if (ParseCommandLine (Argc, Argv, &mOptions)) {
    return STATUS_ERROR;
  }

  if (mOptions.Verbose) {
    fprintf (stdout, "%s tool start.\n", UTILITY_NAME);
  }
  //
  // If dumping an image, then do that and quit
  //
  if (mOptions.DumpOption) {
    for (FList = mOptions.FileList; FList != NULL; FList = FList->Next) {
      DumpImage (FList->FileName);
      goto BailOut;
    }
  }

  //
  // Determine the output filename. Either what they specified on
  // the command line, or the first input filename with a different extension.
  //
  if (!mOptions.OutFileName[0]) {
    strcpy (mOptions.OutFileName, mOptions.FileList->FileName);
    //
    // Find the last . on the line and replace the filename extension with
    // the default
    //
    for (Ext = mOptions.OutFileName + strlen (mOptions.OutFileName) - 1;
         (Ext >= mOptions.OutFileName) && (*Ext != '.') && (*Ext != '\\');
         Ext--
        )
      ;
    //
    // If dot here, then insert extension here, otherwise append
    //
    if (*Ext != '.') {
      Ext = mOptions.OutFileName + strlen (mOptions.OutFileName);
    }

    strcpy (Ext, DEFAULT_OUTPUT_EXTENSION);
  }
  //
  // Make sure we don't have the same filename for input and output files
  //
  for (FList = mOptions.FileList; FList != NULL; FList = FList->Next) {
    if (stricmp (mOptions.OutFileName, FList->FileName) == 0) {
      Status = STATUS_ERROR;
      Error(NULL, 0, 1002, "Conflicting options", "Input and output file names must be different - %s = %s", FList->FileName, mOptions.OutFileName);
      goto BailOut;
    }
  }
  //
  // Now open our output file
  //
  if ((FptrOut = fopen (mOptions.OutFileName, "wb")) == NULL) {
    Error(NULL, 0, 0001, "Error opening file", mOptions.OutFileName);
    goto BailOut;
  }
  //
  // Process all our files
  //
  TotalSize = 0;
  for (FList = mOptions.FileList; FList != NULL; FList = FList->Next) {
    Size = 0;
    if (FList->FileFlags & FILE_FLAG_EFI) {
      if (mOptions.Verbose) {
        fprintf (stdout, "Processing EFI file    %s\n", FList->FileName);
      }

      Status = ProcessEfiFile (FptrOut, FList, mOptions.VendId, mOptions.DevId, &Size);
    } else if (FList->FileFlags & FILE_FLAG_BINARY) {
      if (mOptions.Verbose) {
        fprintf (stdout, "Processing binary file %s\n", FList->FileName);
      }

      Status = ProcessBinFile (FptrOut, FList, &Size);
    } else {
      Error(NULL, 0, 2000, "Invalid parameter", "File not specified as EFI or binary: %s", FList->FileName);
      Status = STATUS_ERROR;
    }

    if (mOptions.Verbose) {
      fprintf (stdout, "  Output size = 0x%X\n", Size);
    }

    if (Status != STATUS_SUCCESS) {
      break;
    }

    TotalSize += Size;
  }
  //
  // Check total size
  //
  if (TotalSize > MAX_OPTION_ROM_SIZE) {
    Error(NULL, 0, 2000, "Invalid parameter", "Option ROM image size exceeds limit 0x%X bytes", MAX_OPTION_ROM_SIZE);
    Status = STATUS_ERROR;
  }

BailOut:
  if (FptrOut != NULL) {
    fclose (FptrOut);
  }
  //
  // Clean up our file list
  //
  while (mOptions.FileList != NULL) {
    FList = mOptions.FileList->Next;
    free (mOptions.FileList);
    mOptions.FileList = FList;
  }

  if (mOptions.Verbose) {
    fprintf (stdout, "%s tool done with return code is 0x%x.\n", UTILITY_NAME, GetUtilityStatus ());  
  }

  return GetUtilityStatus (); 
}

UINT8
CheckSumPadff (
  UINT8  *Buffer, 
  UINT32 DataSize,
  UINT32 PaddingSize
  )
/*++
Routine Description:
  Calculate checksum from DataSize of Buffer and Add pad 0xff

Arguments:
  Buffer      - pointer to data buffer
  DataSize    - size of data buffer in bytes

Return:
  UINT8       - checksum
--*/
{
  UINT8 Checksum = 0;
  while (DataSize-- != 0) {
    Checksum = Checksum + Buffer[DataSize];
  }
  while (PaddingSize-- != 0) {
    Checksum = Checksum + 0xff;
  }
  return Checksum;
}

char *
GetCodeTypeStr (
  UINT8     CodeType
  )
{
  if (CodeType >= sizeof (mCodeTypeStr) / sizeof (*mCodeTypeStr)) {
    CodeType = sizeof (mCodeTypeStr) / sizeof (*mCodeTypeStr) - 1;
  }
  return mCodeTypeStr[CodeType];
}

static
int
ProcessBinFile (
  FILE      *OutFptr,
  FILE_LIST *InFile,
  UINT32    *Size
  )
/*++

Routine Description:
  
  Process a binary input file.

Arguments:

  OutFptr     - file pointer to output binary ROM image file we're creating
  InFile      - structure contains information on the binary file to process
  Size        - pointer to where to return the size added to the output file

Returns:

  0 - successful

--*/
{
  FILE                      *InFptr;
  UINT32                    TotalSize;
  UINT32                    FileSize;
  UINT32                    DataSize;
  UINT32                    PaddingSize;
  UINT8                     *Buffer;
  UINT32                    Status;
  PCI_EXPANSION_ROM_HEADER  *RomHdr;
  PCI_3_0_DATA_STRUCTURE    *PciDs30;
  UINT8                     ByteCheckSum;

  Status = STATUS_SUCCESS;

  //
  // Try to open the input file
  //
  if ((InFptr = fopen (InFile->FileName, "rb")) == NULL) {
    Error (NULL, 0, 0001, "Error opening file", InFile->FileName);
    return STATUS_ERROR;
  }
  //
  // Seek to the end of the input file and get the file size. Then allocate
  // a buffer to read it in to.
  //
  fseek (InFptr, 0, SEEK_END);
  FileSize = ftell (InFptr);
  if (mOptions.Verbose) {
    fprintf (stdout, "  File size   = 0x%X\n", FileSize);
  }

  fseek (InFptr, 0, SEEK_SET);
  Buffer = (INT8 *) malloc (FileSize);
  if (Buffer == NULL) {
    Error (NULL, 0, 4003, "Resource", "Out of memory resources.");
    Status = STATUS_ERROR;
    goto BailOut;
  }

  if (fread (Buffer, FileSize, 1, InFptr) != 1) {
    Error(NULL, 0, 2000, "Invalid parameter", "Failed to read all bytes from input file");
    Status = STATUS_ERROR;
    goto BailOut;
  }

  
  RomHdr  = (PCI_EXPANSION_ROM_HEADER *) Buffer;
  PciDs30 = (PCI_3_0_DATA_STRUCTURE *) (Buffer + RomHdr->PcirOffset);

  //
  // Crude check to make sure it's a legitimate ROM image
  //
  if (RomHdr->Signature != PCI_EXPANSION_ROM_HEADER_SIGNATURE) {
    Error(NULL, 0, 2000, "Invalid parameter", "ROM image file has invalid ROM signature");
    Status = STATUS_ERROR;
    goto BailOut;
  }
  //
  // Make sure the pointer to the PCI data structure is within the size of the image.
  // Then check it for valid signature.
  //
  if ((RomHdr->PcirOffset > FileSize) || (RomHdr->PcirOffset == 0)) {
    Error (NULL, 0, 2000, "Invalid parameter", "Invalid PCI data structure offset");
    Status = STATUS_ERROR;
    goto BailOut;
  }

  if (PciDs30->Signature != PCI_DATA_STRUCTURE_SIGNATURE) {
    Error (NULL, 0, 2000, "Invalid parameter", "PCI data structure has invalid signature\n");
    Status = STATUS_ERROR;
    goto BailOut;
  }

  if ((UINT32) (PciDs30->ImageLength * 512) == FileSize) {
    //
    // ImageLength reflects the actual file size correctly.
    //
    DataSize    = FileSize - 1;
    PaddingSize = 0;
    TotalSize   = FileSize;
  } else {
    //
    // ImageLength doesn't reflect the actual file size,
    // 1). add additional 512 bytes if actual file size is multiple of 512
    // 2). add additional X (X <= 512) bytes so that the result size is multiple of 512
    //
    fprintf (stdout, "WARNING: ImageLength in PCI data structure != Actual File Size\n"
                     "         --> add additional padding bytes\n"
                     "         --> adjust ImageLength\n"
            );
    TotalSize   = (FileSize + 0x200) & ~0x1ff;
    DataSize    = FileSize;
    PaddingSize = TotalSize - DataSize - 1;
    PciDs30->ImageLength = (UINT16) (TotalSize / 512);
  }

  //
  // Check size
  //
  if (TotalSize > MAX_OPTION_ROM_SIZE) {
    Error (NULL, 0, 2000, "Invalid parameter", "Option ROM image %s size exceeds limit 0x%X bytes\n",
      InFile->FileName, MAX_OPTION_ROM_SIZE
      );
    Status = STATUS_ERROR;
    goto BailOut;
  }

  //
  // Return the size to the caller so they can keep track of the running total.
  //
  *Size = TotalSize;

  //
  // If this is the last image, then set the LAST bit unless requested not
  // to via the command-line -l argument. Otherwise, make sure you clear it.
  //
  if ((InFile->Next == NULL) && (mOptions.NoLast == 0)) {
    PciDs30->Indicator |= INDICATOR_LAST;
  } else {
    PciDs30->Indicator &= ~INDICATOR_LAST;
  }

  ByteCheckSum = -CheckSumPadff (Buffer, DataSize, PaddingSize);

  //
  // Now copy the input file contents out to the output file
  // Add 0xff as pad byte, and fill checksum in the last byte.
  //
  if (fwrite (Buffer, DataSize, 1, OutFptr) != 1) {
    Error(NULL, 0, 0002, "Error writing file", "Failed to write all file bytes to output file");
    Status = STATUS_ERROR;
    goto BailOut;
  }

  while (PaddingSize-- != 0) {
    putc (~0, OutFptr);
  }
  putc (ByteCheckSum, OutFptr);

BailOut:
  if (InFptr != NULL) {
    fclose (InFptr);
  }

  if (Buffer != NULL) {
    free (Buffer);
  }
  //
  // Print the file name if errors occurred
  //
  if (Status != STATUS_SUCCESS) {
    Error (NULL, 0, 0003, "Error parsing file", InFile->FileName);
  }

  return Status;
}

static
int
ProcessEfiFile (
  FILE      *OutFptr,
  FILE_LIST *InFile,
  UINT16    VendId,
  UINT16    DevId,
  UINT32    *Size
  )
/*++

Routine Description:
  
  Process a PE32 EFI file.

Arguments:

  OutFptr     - file pointer to output binary ROM image file we're creating
  InFile      - structure contains information on the PE32 file to process
  VendId      - vendor ID as required in the option ROM header
  DevId       - device ID as required in the option ROM header
  Size        - pointer to where to return the size added to the output file

Returns:

  0 - successful

--*/
{
  UINT32                        Status;
  FILE                          *InFptr;
  EFI_PCI_EXPANSION_ROM_HEADER  RomHdr;
  PCI_DATA_STRUCTURE            PciDs23;
  PCI_3_0_DATA_STRUCTURE        PciDs30;
  UINT32                        FileSize;
  UINT32                        CompressedFileSize;
  UINT8                         *Buffer;
  UINT8                         *CompressedBuffer;
  UINT8                         *TempBufferPtr;
  UINT32                        TotalSize;
  UINT32                        HeaderSize;
  UINT16                        MachineType;
  UINT16                        SubSystem;
  UINT32                        HeaderPadBytes;

  //
  // Try to open the input file
  //
  if ((InFptr = fopen (InFile->FileName, "rb")) == NULL) {
    Error(NULL, 0, 0001, "Error opening file", InFile->FileName);
    return STATUS_ERROR;
  }
  //
  // Initialize our buffer pointers to null.
  //
  Buffer            = NULL;
  CompressedBuffer  = NULL;

  //
  // Double-check the file to make sure it's what we expect it to be
  //
  Status = CheckPE32File (InFptr, &MachineType, &SubSystem);
  if (Status != STATUS_SUCCESS) {
    goto BailOut;
  }
  //
  // Seek to the end of the input file and get the file size
  //
  fseek (InFptr, 0, SEEK_END);
  FileSize = ftell (InFptr);

  //
  // Get the size of the headers we're going to put in front of the image. The
  // EFI header must be aligned on a 4-byte boundary, so pad accordingly.
  //
  if (sizeof (RomHdr) & 0x03) {
    HeaderPadBytes = 4 - (sizeof (RomHdr) & 0x03);
  } else {
    HeaderPadBytes = 0;
  }
  
  if (mOptions.Pci23 == 1) {
    HeaderSize = sizeof (PCI_DATA_STRUCTURE) + HeaderPadBytes + sizeof (EFI_PCI_EXPANSION_ROM_HEADER);
  } else {
    HeaderSize = sizeof (PCI_3_0_DATA_STRUCTURE) + HeaderPadBytes + sizeof (EFI_PCI_EXPANSION_ROM_HEADER);
  }
  
  if (mOptions.Verbose) {
    fprintf (stdout, "  File size   = 0x%X\n", FileSize);
  }
  //
  // Allocate memory for the entire file (in case we have to compress), then
  // seek back to the beginning of the file and read it into our buffer.
  //
  Buffer = (INT8 *) malloc (FileSize);
  if (Buffer == NULL) {
    Error (NULL, 0, 4001, "Resouce", "memory cannot be allocated");
    Status = STATUS_ERROR;
    goto BailOut;
  }

  fseek (InFptr, 0, SEEK_SET);
  if (fread (Buffer, FileSize, 1, InFptr) != 1) {
    Error(NULL, 0, 0004, "Error reading file", InFptr);
    Status = STATUS_ERROR;
    goto BailOut;
  }
  //
  // Now determine the size of the final output file. It's either the header size
  // plus the file's size, or the header size plus the compressed file size.
  //
  if (InFile->FileFlags & FILE_FLAG_COMPRESS) {
    //
    // Allocate a buffer into which we can compress the image, compress it,
    // and use that size as the new size.
    //
    CompressedBuffer = (INT8 *) malloc (FileSize);
    if (CompressedBuffer == NULL) {
      Error (NULL, 0, 4001, "Resouce", "memory cannot be allocated");
      Status = STATUS_ERROR;
      goto BailOut;
    }

    CompressedFileSize  = FileSize;
    Status              = EfiCompress (Buffer, FileSize, CompressedBuffer, &CompressedFileSize);
    if (Status != STATUS_SUCCESS) {
      Error(NULL, 0, 0007, "Error compressing file");
      goto BailOut;
    }
    //
    // Now compute the size, then swap buffer pointers.
    //
    if (mOptions.Verbose) {
      fprintf (stdout, "  Comp size   = 0x%X\n", CompressedFileSize);
    }

    TotalSize         = CompressedFileSize + HeaderSize;
    FileSize          = CompressedFileSize;
    TempBufferPtr     = Buffer;
    Buffer            = CompressedBuffer;
    CompressedBuffer  = TempBufferPtr;
  } else {
    TotalSize = FileSize + HeaderSize;
  }
  //
  // Total size must be an even multiple of 512 bytes
  //
  if (TotalSize & 0x1FF) {
    TotalSize = (TotalSize + 0x200) &~0x1ff;
  }
  //
  // Check size
  //
  if (TotalSize > MAX_OPTION_ROM_SIZE) {
    Error(NULL, 0, 2000, "Invalid parameter", "Option ROM image %s size exceeds limit 0x%X bytes", InFile->FileName, MAX_OPTION_ROM_SIZE);  
    Status = STATUS_ERROR;
    goto BailOut;
  }
  //
  // Return the size to the caller so they can keep track of the running total.
  //
  *Size = TotalSize;

  //
  // Now fill in the ROM header. These values come from chapter 18 of the
  // EFI 1.02 specification.
  //
  memset (&RomHdr, 0, sizeof (RomHdr));
  RomHdr.Signature            = PCI_EXPANSION_ROM_HEADER_SIGNATURE;
  RomHdr.InitializationSize   = (UINT16) (TotalSize / 512);
  RomHdr.EfiSignature         = EFI_PCI_EXPANSION_ROM_HEADER_EFISIGNATURE;
  RomHdr.EfiSubsystem         = SubSystem;
  RomHdr.EfiMachineType       = MachineType;
  RomHdr.EfiImageHeaderOffset = (UINT16) HeaderSize;
  RomHdr.PcirOffset           = (UINT16) (sizeof (RomHdr) + HeaderPadBytes);
  //
  // Set image as compressed or not
  //
  if (InFile->FileFlags & FILE_FLAG_COMPRESS) {
    RomHdr.CompressionType = EFI_PCI_EXPANSION_ROM_HEADER_COMPRESSED;
  }
  //
  // Fill in the PCI data structure
  //
  if (mOptions.Pci23 == 1) {
    memset (&PciDs23, 0, sizeof (PCI_DATA_STRUCTURE));
  } else {
    memset (&PciDs30, 0, sizeof (PCI_3_0_DATA_STRUCTURE));
  }

  if (mOptions.Pci23 == 1) {
  PciDs23.Signature = PCI_DATA_STRUCTURE_SIGNATURE;
  PciDs23.VendorId  = VendId;
  PciDs23.DeviceId  = DevId;
  PciDs23.Length    = (UINT16) sizeof (PCI_DATA_STRUCTURE);
  PciDs23.Revision  = 2;
  //
  // Class code and code revision from the command line (optional)
  //
  PciDs23.ClassCode[0]  = (UINT8) InFile->ClassCode;
  PciDs23.ClassCode[1]  = (UINT8) (InFile->ClassCode >> 8);
  PciDs23.ClassCode[2]  = (UINT8) (InFile->ClassCode >> 16);
  PciDs23.ImageLength   = RomHdr.InitializationSize;
  PciDs23.CodeRevision  = InFile->CodeRevision;
  PciDs23.CodeType      = PCI_CODE_TYPE_EFI_IMAGE;
  } else {
  PciDs30.Signature = PCI_DATA_STRUCTURE_SIGNATURE;
  PciDs30.VendorId  = VendId;
  PciDs30.DeviceId  = DevId;
  PciDs30.DeviceListOffset = 0; // to be fixed
  PciDs30.Length    = (UINT16) sizeof (PCI_3_0_DATA_STRUCTURE);
  PciDs30.Revision  = 3;
  //
  // Class code and code revision from the command line (optional)
  //
  PciDs30.ClassCode[0]  = (UINT8) InFile->ClassCode;
  PciDs30.ClassCode[1]  = (UINT8) (InFile->ClassCode >> 8);
  PciDs30.ClassCode[2]  = (UINT8) (InFile->ClassCode >> 16);
  PciDs30.ImageLength   = RomHdr.InitializationSize;
  PciDs30.CodeRevision  = InFile->CodeRevision;
  PciDs30.CodeType      = PCI_CODE_TYPE_EFI_IMAGE;
  PciDs30.MaxRuntimeImageLength = 0; // to be fixed
  PciDs30.ConfigUtilityCodeHeaderOffset = 0; // to be fixed
  PciDs30.DMTFCLPEntryPointOffset = 0; // to be fixed
  }
  //
  // If this is the last image, then set the LAST bit unless requested not
  // to via the command-line -n argument.
  //
  if ((InFile->Next == NULL) && (mOptions.NoLast == 0)) {
    if (mOptions.Pci23 == 1) {
      PciDs23.Indicator |= INDICATOR_LAST;
    } else {
      PciDs30.Indicator |= INDICATOR_LAST;
    }
  } else {
    if (mOptions.Pci23 == 1) {
      PciDs23.Indicator &= ~INDICATOR_LAST;
    } else {
      PciDs30.Indicator &= ~INDICATOR_LAST;
    }
  }
  //
  // Write the ROM header to the output file
  //
  if (fwrite (&RomHdr, sizeof (RomHdr), 1, OutFptr) != 1) {
    Error(NULL, 0, 0002, "Error writing file", "Failed to write ROM header to output file");
    Status = STATUS_ERROR;
    goto BailOut;
  }

  //
  // Write pad bytes to align the PciDs
  //
  while (HeaderPadBytes > 0) {
    if (putc (0, OutFptr) == EOF) {
      Error(NULL, 0, 0002, "Error writing file", "Failed to write ROM header pad bytes to output file");
      Status = STATUS_ERROR;
      goto BailOut;
    }

    HeaderPadBytes--;
  }
  //
  // Write the PCI data structure header to the output file
  //
  if (mOptions.Pci23 == 1) {
    if (fwrite (&PciDs23, sizeof (PciDs23), 1, OutFptr) != 1) {
      Error(NULL, 0, 0002, "Error writing file", "Failed to write PCI ROM header to output file");
      Status = STATUS_ERROR;
      goto BailOut;
    } 
  } else {
    if (fwrite (&PciDs30, sizeof (PciDs30), 1, OutFptr) != 1) {
      Error(NULL, 0, 0002, "Error writing file", "Failed to write PCI ROM header to output file");
      Status = STATUS_ERROR;
      goto BailOut;
    } 
  }
  //
  // Keep track of how many bytes left to write
  //
  TotalSize -= HeaderSize;

  //
  // Now dump the input file's contents to the output file
  //
  if (fwrite (Buffer, FileSize, 1, OutFptr) != 1) {
    Error(NULL, 0, 0002, "Error writing file", "Failed to write all file bytes to output file");
    Status = STATUS_ERROR;
    goto BailOut;
  }

  TotalSize -= FileSize;
  //
  // Pad the rest of the image to make it a multiple of 512 bytes
  //
  while (TotalSize > 0) {
    if (putc (~0, OutFptr) == EOF) {
      Error(NULL, 0, 2000, "Invalid parameter", "Failed to write trailing pad bytes output file");
      Status = STATUS_ERROR;
      goto BailOut;
    }

    TotalSize--;
  }

BailOut:
  if (InFptr != NULL) {
    fclose (InFptr);
  }

  //
  // Free up our buffers
  //
  if (Buffer != NULL) {
    free (Buffer);
  }

  if (CompressedBuffer != NULL) {
    free (CompressedBuffer);
  }
  //
  // Print the file name if errors occurred
  //
  if (Status != STATUS_SUCCESS) {
    Error(NULL, 0 , 0003, "Error parsing file", InFile->FileName);
  }

  return Status;
}

static
int
CheckPE32File (
  FILE      *Fptr,
  UINT16    *MachineType,
  UINT16    *SubSystem
  )
/*++

Routine Description:
  
  Given a file pointer to a supposed PE32 image file, verify that it is indeed a
  PE32 image file, and then return the machine type in the supplied pointer.

Arguments:

  Fptr          File pointer to the already-opened PE32 file
  MachineType   Location to stuff the machine type of the PE32 file. This is needed
                because the image may be Itanium-based, IA32, or EBC.

Returns:

  0             success
  non-zero      otherwise

--*/
{
  EFI_IMAGE_DOS_HEADER      DosHeader;
  EFI_IMAGE_FILE_HEADER     FileHdr;
  EFI_IMAGE_OPTIONAL_HEADER OptionalHdr;
  UINT32                    PESig;

  //
  // Position to the start of the file
  //
  fseek (Fptr, 0, SEEK_SET);

  //
  // Read the DOS header
  //
  if (fread (&DosHeader, sizeof (DosHeader), 1, Fptr) != 1) {
    Error(NULL, 0, 0004, "Error reading file", "Failed to read the DOS stub from the input file");
    return STATUS_ERROR;
  }
  //
  // Check the magic number (0x5A4D)
  //
  if (DosHeader.e_magic != EFI_IMAGE_DOS_SIGNATURE) {
    Error(NULL, 0, 2000, "Invalid parameter", "Input file does not appear to be a PE32 image (magic number)");
    return STATUS_ERROR;
  }
  //
  // Position into the file and check the PE signature
  //
  fseek (Fptr, (long) DosHeader.e_lfanew, SEEK_SET);
  if (fread (&PESig, sizeof (PESig), 1, Fptr) != 1) {
    Error(NULL, 0, 0004, "Error reading file", "Failed to read PE signature bytes from input file");
    return STATUS_ERROR;
  }
  //
  // Check the PE signature in the header "PE\0\0"
  //
  if (PESig != EFI_IMAGE_NT_SIGNATURE) {
    Error(NULL, 0, 2000, "Invalid parameter", "Input file does not appear to be a PE32 image (signature)");
    return STATUS_ERROR;
  }
  //
  // Read the file header and stuff their MachineType
  //
  if (fread (&FileHdr, sizeof (FileHdr), 1, Fptr) != 1) {
    Error(NULL, 0, 0004, "Error reading file", "Failed to read PE file header from input file");
    return STATUS_ERROR;
  }

  memcpy ((char *) MachineType, &FileHdr.Machine, 2);

  //
  // Read the optional header so we can get the subsystem
  //
  if (fread (&OptionalHdr, sizeof (OptionalHdr), 1, Fptr) != 1) {
    Error(NULL, 0, 0004, "Error reading file", "Failed to read COFF optional header from input file");
    return STATUS_ERROR;
  }

  *SubSystem = OptionalHdr.Subsystem;
  if (mOptions.Verbose) {
    fprintf (stdout, "  Got subsystem = 0x%X from image\n", (int) *SubSystem);
  }
  //
  // Good to go
  //
  return STATUS_SUCCESS;
}

static
int
ParseCommandLine (
  int         Argc,
  char        *Argv[],
  OPTIONS     *Options
  )
/*++

Routine Description:
  
  Given the Argc/Argv program arguments, and a pointer to an options structure,
  parse the command-line options and check their validity.


Arguments:

  Argc            - standard C main() argument count
  Argv[]          - standard C main() argument list
  Options         - pointer to a structure to store the options in

Returns:

  STATUS_SUCCESS    success
  non-zero          otherwise

--*/
{
  FILE_LIST *FileList;

  FILE_LIST *PrevFileList;
  UINT32    FileFlags;
  UINT32    ClassCode;
  UINT32    CodeRevision;

  FileFlags = 0;

  //
  // Clear out the options
  //
  memset ((char *) Options, 0, sizeof (OPTIONS));

  //
  // To avoid compile warnings
  //
  FileList                = PrevFileList = NULL;

  ClassCode               = 0;
  CodeRevision            = 0;
  //
  // Skip over the program name
  //
  Argc--;
  Argv++;

  //
  // If no arguments, assume they want usage info
  //
  if (Argc == 0) {
    Usage ();
    return STATUS_ERROR;
  }
  
  if ((strcmp(Argv[0], "-h") == 0) || (strcmp(Argv[0], "--help") == 0) ||
      (strcmp(Argv[0], "-?") == 0) || (strcmp(Argv[0], "/?") == 0)) {
    Usage();
    return STATUS_ERROR;
  }
  
  if ((strcmp(Argv[0], "--version") == 0)) {
    Version();
    return STATUS_ERROR;
  }

  //
  // Process until no more arguments
  //
  while (Argc > 0) {
    if ((Argv[0][0] == '-') || (Argv[0][0] == '/')) {
      //
      // To simplify string comparisons, replace slashes with dashes
      //
      Argv[0][0] = '-';
      
      //
      // Vendor ID specified with -f
      //
      if (stricmp (Argv[0], "-f") == 0) {
        //
        // Make sure there's another parameter
        //
        //printf("\nvendor id specified!\n");
        if (Argc > 1) {
          Options->VendId       = (UINT16) strtol (Argv[1], NULL, 16);
          Options->VendIdValid  = 1;
        } else {
          Error (NULL, 0, 2000, "Invalid parameter", "Missing Vendor ID with %s", Argv[0]);
          Usage ();
          return STATUS_ERROR;
        }

        Argv++;
        Argc--;
      } else if (stricmp (Argv[0], "-i") == 0) {
        //
        // Device ID specified with -i
        // Make sure there's another parameter
        //
        //printf("\nDevice id specified!\n");
        if (Argc > 1) {
          Options->DevId      = (UINT16) strtol (Argv[1], NULL, 16);
          Options->DevIdValid = 1;
        } else {
          Error (NULL, 0, 2000, "Invalid parameter", "Missing Device ID with %s", Argv[0]);
          Usage ();
          return STATUS_ERROR;
        }

        Argv++;
        Argc--;
      } else if ((stricmp (Argv[0], "-o") == 0) || (stricmp (Argv[0], "--output") == 0)) {
        //
        // Output filename specified with -o
        // Make sure there's another parameter
        //
        if (Argc > 1) {
          strcpy (Options->OutFileName, Argv[1]);
        } else {
          Error (NULL, 0, 2000, "Invalid parameter", "Missing output file name with %s", Argv[0]);
          Usage ();
          return STATUS_ERROR;
        }

        Argv++;
        Argc--;
      } else if ((stricmp (Argv[0], "-h") == 0) || (strcmp (Argv[0], "-?") == 0)) {
        //
        // Help option
        //
        Usage ();
        return STATUS_ERROR;
      } else if (stricmp (Argv[0], "-b") == 0) {
        //
        // Specify binary files with -b
        //
        FileFlags = (FileFlags &~FILE_FLAG_EFI) | FILE_FLAG_BINARY;
      } else if ((stricmp (Argv[0], "-e") == 0) || (stricmp (Argv[0], "-ec") == 0)) {
        //
        // Specify EFI files with -e. Specify EFI-compressed with -c.
        //
        FileFlags = (FileFlags &~FILE_FLAG_BINARY) | FILE_FLAG_EFI;
        if ((Argv[0][2] == 'c') || (Argv[0][2] == 'C')) {
          FileFlags |= FILE_FLAG_COMPRESS;
        }
        //
        // Specify not to set the LAST bit in the last file with -n
        //
      } else if (stricmp (Argv[0], "-n") == 0) {
        Options->NoLast = 1;
      } else if (((stricmp (Argv[0], "-v") == 0)) || ((stricmp (Argv[0], "--verbose") == 0))) {
        //
        // -v for verbose
        //
        Options->Verbose = 1;
      } else if ((stricmp (Argv[0], "--dump") == 0) || (stricmp (Argv[0], "-d") == 0)) {
        //
        // -dump for dumping a ROM image. In this case, say that the device id
        // and vendor id are valid so we don't have to specify bogus ones on the
        // command line.
        //
        Options->DumpOption   = 1;

        Options->VendIdValid  = 1;
        Options->DevIdValid   = 1;
        FileFlags             = FILE_FLAG_BINARY;
      } else if ((stricmp (Argv[0], "-l") == 0) || (stricmp (Argv[0], "--class-code") == 0)) {
        //
        // Class code value for the next file in the list.
        // Make sure there's another parameter
        //
        if (Argc > 1) {
          //
          // No error checking on the return value. Could check for LONG_MAX,
          // LONG_MIN, or 0 class code value if desired. Check range (3 bytes)
          // at least.
          //
          ClassCode = (UINT32) strtol (Argv[1], NULL, 16);
          if (ClassCode & 0xFF000000) {
            Error (NULL, 0, 2000, "Invalid parameter", "Class code %s out of range", Argv[1]);
            return STATUS_ERROR;
          }
        } else {
          Error (NULL, 0, 2000, "Invalid parameter", "Missing class code value with %s", Argv[0]);
          Usage ();
          return STATUS_ERROR;
        }

        Argv++;
        Argc--;
      } else if ((stricmp (Argv[0], "-r") == 0) || (stricmp (Argv[0], "--Revision") == 0)) {
        //
        // Code revision in the PCI data structure. The value is for the next
        // file in the list.
        // Make sure there's another parameter
        //
        if (Argc > 1) {
          //
          // No error checking on the return value. Could check for LONG_MAX,
          // LONG_MIN, or 0 value if desired. Check range (2 bytes)
          // at least.
          //
          CodeRevision = (UINT32) strtol (Argv[1], NULL, 16);
          if (CodeRevision & 0xFFFF0000) {
            Error (NULL, 0, 2000, "Invalid parameter", "Code revision %s out of range", Argv[1]);
            return STATUS_ERROR;
          }
        } else {
          Error (NULL, 0, 2000, "Invalid parameter", "Missing code revision value with %s", Argv[0]);
          Usage ();
          return STATUS_ERROR;
        }

        Argv++;
        Argc--;
      } else if ((stricmp (Argv[0], "-p") == 0) || (stricmp (Argv[0], "--pci23") == 0)) {
        //
        // Default layout meets PCI 3.0 specifications, specifying this flag will for a PCI 2.3 layout.
        //
        mOptions.Pci23 = 1; 
      } else {
        Error (NULL, 0, 2000, "Invalid parameter", "Invalid option specified: %s", Argv[0]);
        Usage ();
        return STATUS_ERROR;
      }
    } else {
      //
      // Not a slash-option argument. Must be a file name. Make sure they've specified
      // -e or -b already.
      //
      if ((FileFlags & (FILE_FLAG_BINARY | FILE_FLAG_EFI)) == 0) {
        Error (NULL, 0, 2000, "Invalid parameter", "Missing -e or -b with input file %s", Argv[0]);
        return STATUS_ERROR;
      }
      //
      // Create a new file structure
      //
      FileList = (FILE_LIST *) malloc (sizeof (FILE_LIST));
      if (FileList == NULL) {
        Error (NULL, 0, 4001, "Resource", "memory cannot be allcoated");
        return STATUS_ERROR;
      }

      memset ((char *) FileList, 0, sizeof (FILE_LIST));
      FileList->FileName  = Argv[0];
      FileList->FileFlags = FileFlags;
      if (Options->FileList == NULL) {
        Options->FileList = FileList;
      } else {
        if (PrevFileList == NULL) {
          PrevFileList = FileList;
        } else {          
          PrevFileList->Next = FileList;
        }
      }

      PrevFileList = FileList;
      //
      // Set the class code and code revision for this file, then reset the values.
      //
      FileList->ClassCode     = ClassCode;
      FileList->CodeRevision  = (UINT16) CodeRevision;
      ClassCode               = 0;
      CodeRevision            = 0;
    }
    //
    // Next argument
    //
    Argv++;
    Argc--;
  }
  //
  // Make sure they specified a device ID and vendor ID
  //
/*  
  if (!Options->VendIdValid) {
    Error(NULL, 0, 2000, "Invalid parameter", "Missing Vendor ID in command line");
    Usage ();
    return STATUS_ERROR;
  }

  if (!Options->DevIdValid) {
    Error(NULL, 0, 2000, "Invalid parameter", "Missing Device ID in command line");
    Usage ();
    return STATUS_ERROR;
  }
*/  
  //
  // Must have specified some files
  //
  if (Options->FileList == NULL) {
    Error (NULL, 0, 2000, "Invalid parameter", "Missing input file name");
    Usage ();
    return STATUS_ERROR;
  }

  return 0;
}

static
void
Version (
  VOID
  )
/*++

Routine Description:
  
  Print version information for this utility.

Arguments:

  None.

Returns:

  Nothing.
--*/
{
 fprintf (stdout, "%s Version %d.%d\n", UTILITY_NAME, UTILITY_MAJOR_VERSION, UTILITY_MINOR_VERSION);
}
   
static
void
Usage (
  VOID
  )
/*++

Routine Description:
  
  Print usage information for this utility.

Arguments:

  None.

Returns:

  Nothing.

--*/
{
  //
  // Summary usage
  //
  fprintf (stdout, "Usage: %s [options] <-e input_file>|<-b input_file> \n\n", UTILITY_NAME);
  
  //
  // Copyright declaration
  // 
  fprintf (stdout, "Copyright (c) 2007, Intel Corporation. All rights reserved.\n\n");

  //
  // Details Option
  //
  fprintf (stdout, "Options:\n");
  fprintf (stdout, "  -o FileName, --output FileName\n\
            File will be created to store the ouput content.\n");
  fprintf (stdout, "  -e EfiFileName\n\
            EFI PE32 image files.\n");
  fprintf (stdout, "  -ec EfiFileName\n\
            EFI PE32 image files and will be compressed.\n");
  fprintf (stdout, "  -b BinFileName\n\
            Legacy binary files.\n");
  fprintf (stdout, "  -l ClassCode\n\
            Hex ClassCode in the PCI data structure header.\n");
  fprintf (stdout, "  -r Rev\n\
            hex Revision in the PCI data structure header.\n");
  fprintf (stdout, "  -n\n\
            not to automatically set the LAST bit in the last file.\n");
  fprintf (stdout, "  -f VendorId\n\
            Hex PCI Vendor ID for the device OpROM.\n");
  fprintf (stdout, "  -i DeviceId\n\
            Hex PCI Device ID for the device OpROM.\n");
  fprintf (stdout, "  -p, --pci23\n\
            Default layout meets PCI 3.0 specifications, specifying this flag will for a PCI 2.3 layout.\n");
  fprintf (stdout, "  -d, --dump\n\
            Dump the headers of an existing option ROM image.\n");
  fprintf (stdout, "  -v, --verbose\n\
            Turn on verbose output with informational messages.\n");
  fprintf (stdout, "  --version\n\
            Show program's version number and exit.\n");
  fprintf (stdout, "  -h, --help\n\
            Show this help message and exit.\n");
}

static
void
DumpImage (
  INT8 *InFileName
  )
/*++

Routine Description:

  Dump the headers of an existing option ROM image

Arguments:

  InFileName  - the file name of an existing option ROM image

Returns:

  none

--*/
{
  PCI_EXPANSION_ROM_HEADER      PciRomHdr;
  FILE                          *InFptr;
  UINT32                        ImageStart;
  UINT32                        ImageCount;
  EFI_PCI_EXPANSION_ROM_HEADER  EfiRomHdr;
  PCI_3_0_DATA_STRUCTURE        PciDs30;
  UINT16                        DeviceId;  

  //
  // Open the input file
  //
  if ((InFptr = fopen (InFileName, "rb")) == NULL) {
    Error (NULL, 0, 0001, "Error opening file", InFileName);
    return ;
  }
  fprintf (stdout, "\nThe dumped option ROM image : %s.\n", InFileName);
  //
  // Go through the image and dump the header stuff for each
  //
  ImageCount = 0;
  for (;;) {
    //
    // Save our postition in the file, since offsets in the headers
    // are relative to the particular image.
    //
    ImageStart = ftell (InFptr);
    ImageCount++;

    //
    // Read the option ROM header. Have to assume a raw binary image for now.
    //
    if (fread (&PciRomHdr, sizeof (PciRomHdr), 1, InFptr) != 1) {
      if (ImageStart == 0) {
        Error (NULL, 0, 3001, "Not supported", "Failed to read PCI ROM header from file");
        goto BailOut;
      } else {
        goto BailOut;
      }
    }

    //
    // Dump the contents of the header
    //
    fprintf (stdout, "Image %d -- Offset 0x%X\n", ImageCount, ImageStart);
    fprintf (stdout, "  ROM header contents\n");
    fprintf (stdout, "    Signature              0x%04X\n", (UINT32) PciRomHdr.Signature);
    fprintf (stdout, "    PCIR offset            0x%04X\n", (UINT32) PciRomHdr.PcirOffset);
    //
    // Find PCI data structure
    //
    if (fseek (InFptr, ImageStart + PciRomHdr.PcirOffset, SEEK_SET)) {
      Error (NULL, 0, 3001, "Not supported", "Failed to seek to PCI data structure");
      goto BailOut;
    }
    //
    // Read and dump the PCI data structure
    //
    if (fread (&PciDs30, sizeof (PciDs30), 1, InFptr) != 1) {
      Error (NULL, 0, 3001, "Not supported", "Failed to read PCI data structure from file");
      goto BailOut;
    }

    fprintf (stdout, "  PCI Data Structure\n");
    fprintf (
      stdout,
      "    Signature              %c%c%c%c\n",
      (char) PciDs30.Signature,
      (char) (PciDs30.Signature >> 8),
      (char) (PciDs30.Signature >> 16),
      (char) (PciDs30.Signature >> 24)
      );
    fprintf (stdout, "    Vendor ID              0x%04X\n", PciDs30.VendorId);
    fprintf (stdout, "    Device ID              0x%04X\n", PciDs30.DeviceId);
    fprintf (stdout, "    Length                 0x%04X\n", PciDs30.Length);
    fprintf (stdout, "    Revision               0x%04X\n", PciDs30.Revision);
    fprintf (
      stdout,
      "    Class Code             0x%06X\n",
      (UINT32) (PciDs30.ClassCode[0] | (PciDs30.ClassCode[1] << 8) | (PciDs30.ClassCode[2] << 16))
      );
    fprintf (stdout, "    Image size             0x%X\n", PciDs30.ImageLength * 512);
    fprintf (stdout, "    Code revision:         0x%04X\n", PciDs30.CodeRevision);
    fprintf (stdout, "    Indicator              0x%02X\n", (UINT32) PciDs30.Indicator);
    //
    // Print the code type. If EFI code, then we can provide more info.
    //
    fprintf (stdout, "    Code type              0x%02X   (%s)\n", (UINT32) PciDs30.CodeType, GetCodeTypeStr(PciDs30.CodeType));

    //
    // Dump additional information for PCI 3.0 OpROM
    //
    if (PciDs30.Revision >= 3) {
      fprintf (stdout, "  Extended for PCI 3.0\n");
      
      if (PciDs30.DeviceListOffset != 0) {
        if (fseek (InFptr, ImageStart + PciRomHdr.PcirOffset + PciDs30.DeviceListOffset, SEEK_SET)) {
          Error (NULL, 0, 3001, "Not supported", "Failed to seek to supported Device List");
          goto BailOut;
        }
        fprintf (stdout, "    Device ID List         ");
        while (TRUE) {
          if (fread (&DeviceId, sizeof (DeviceId), 1, InFptr) != 1) {
            Error (NULL, 0, 3001, "Not supported", "Failed to read supported DeviceId from DeviceId List");
            goto BailOut;
          }
          if (DeviceId == 0) {
            break;
          }
          fprintf (stdout, "0x%04X ", DeviceId);
        }
        fprintf (stdout, "\n");
      }
      fprintf (stdout, "    Max Runtime Image Length 0x%08X\n", PciDs30.MaxRuntimeImageLength * 512);
      if (PciDs30.Length == sizeof (PCI_3_0_DATA_STRUCTURE)) {
        fprintf (stdout, "    Config Utility Header  0x%04X\n", PciDs30.ConfigUtilityCodeHeaderOffset);
        fprintf (stdout, "    DMTF CLP Entry Point   0x%04X\n", PciDs30.DMTFCLPEntryPointOffset);
      } else {
        fprintf (stdout, "WARNING: Oprom declars 3.0 revision with wrong structure length 0x%04X\n", PciDs30.Length);
      }
    }

    if (PciDs30.CodeType == PCI_CODE_TYPE_EFI_IMAGE) {
      //
      // Re-read the header as an EFI ROM header, then dump more info
      //
      fprintf (stdout, "  EFI ROM header contents\n");
      memcpy (&EfiRomHdr, &PciRomHdr, sizeof (EfiRomHdr));
      //
      // Now dump more info
      //
      fprintf (stdout, "    EFI Signature          0x%04X\n", EfiRomHdr.EfiSignature);
      fprintf (
        stdout,
        "    Compression Type       0x%04X ",
        (UINT32) EfiRomHdr.CompressionType
        );
      if (EfiRomHdr.CompressionType == EFI_PCI_EXPANSION_ROM_HEADER_COMPRESSED) {
        fprintf (stdout, "(compressed)\n");
      } else {
        fprintf (stdout, "(not compressed)\n");
      }

      fprintf (
        stdout,
        "    Machine type           0x%04X (%s)\n",
        EfiRomHdr.EfiMachineType,
        GetMachineTypeStr (EfiRomHdr.EfiMachineType)
        );
      fprintf (
        stdout,
        "    Subsystem              0x%04X (%s)\n",
        EfiRomHdr.EfiSubsystem,
        GetSubsystemTypeStr (EfiRomHdr.EfiSubsystem)
        );
      fprintf (
        stdout,
        "    EFI image offset       0x%04X (@0x%X)\n",
        (UINT32) EfiRomHdr.EfiImageHeaderOffset,
        (UINT32) (EfiRomHdr.EfiImageHeaderOffset + ImageStart)
        );
    }

    //
    // If last image, then we're done
    //
    if ((PciDs30.Indicator & INDICATOR_LAST) == INDICATOR_LAST) {
      fprintf (stdout, "  (last image)\n");
      goto BailOut;
    }
    //
    // Seek to the start of the next image
    //
    if (fseek (InFptr, ImageStart + (PciDs30.ImageLength * 512), SEEK_SET)) {
      Error (NULL, 0, 3001, "Not supported", "Failed to seek to next image");
      goto BailOut;
    }
  }

BailOut:
  fclose (InFptr);
}

char *
GetMachineTypeStr (
  UINT16    MachineType
  )
/*++

Routine Description:

  GC_TODO: Add function description

Arguments:

  MachineType - GC_TODO: add argument description

Returns:

  GC_TODO: add return values

--*/
{
  int Index;

  for (Index = 0; mMachineTypes[Index].Name != NULL; Index++) {
    if (mMachineTypes[Index].Value == MachineType) {
      return mMachineTypes[Index].Name;
    }
  }

  return "unknown";
}

static
char *
GetSubsystemTypeStr (
  UINT16  SubsystemType
  )
/*++

Routine Description:

  GC_TODO: Add function description

Arguments:

  SubsystemType - GC_TODO: add argument description

Returns:

  GC_TODO: add return values

--*/
{
  int Index;

  for (Index = 0; mSubsystemTypes[Index].Name != NULL; Index++) {
    if (mSubsystemTypes[Index].Value == SubsystemType) {
      return mSubsystemTypes[Index].Name;
    }
  }

  return "unknown";
}
