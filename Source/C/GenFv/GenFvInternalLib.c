/*++

Copyright (c) 2004, Intel Corporation                                                         
All rights reserved. This program and the accompanying materials                          
are licensed and made available under the terms and conditions of the BSD License         
which accompanies this distribution.  The full text of the license may be found at        
http://opensource.org/licenses/bsd-license.php                                            
                                                                                          
THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,                     
WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.             

Module Name:

  GenFvInternalLib.c

Abstract:

  This file contains functions required to generate a Firmware Volume.

--*/

//
// Include files
//
#ifdef __GNUC__
#include <uuid/uuid.h>
#include <sys/stat.h>
#endif
#include <string.h>
#ifndef __GNUC__
#include <io.h>
#endif
#include <assert.h>

#include "GenFvInternalLib.h"
#include "PeCoffLib.h"
#include "WinNtInclude.h"

STATIC UINT32   MaxFfsAlignment = 0;

EFI_GUID  mEfiFirmwareFileSystem2Guid = EFI_FIRMWARE_FILE_SYSTEM2_GUID;
EFI_GUID  mEfiFirmwareVolumeTopFileGuid = EFI_FFS_VOLUME_TOP_FILE_GUID;
EFI_GUID  mFileGuidArray [MAX_NUMBER_OF_FILES_IN_FV] = {0};

CHAR8      *mFvbAttributeName[] = {
  EFI_FVB2_READ_DISABLED_CAP_STRING, 
  EFI_FVB2_READ_ENABLED_CAP_STRING,  
  EFI_FVB2_READ_STATUS_STRING,       
  EFI_FVB2_WRITE_DISABLED_CAP_STRING,
  EFI_FVB2_WRITE_ENABLED_CAP_STRING, 
  EFI_FVB2_WRITE_STATUS_STRING,      
  EFI_FVB2_LOCK_CAP_STRING,          
  EFI_FVB2_LOCK_STATUS_STRING,       
  NULL,
  EFI_FVB2_STICKY_WRITE_STRING,      
  EFI_FVB2_MEMORY_MAPPED_STRING,     
  EFI_FVB2_ERASE_POLARITY_STRING,    
  EFI_FVB2_READ_LOCK_CAP_STRING,     
  EFI_FVB2_READ_LOCK_STATUS_STRING,  
  EFI_FVB2_WRITE_LOCK_CAP_STRING,    
  EFI_FVB2_WRITE_LOCK_STATUS_STRING 
};

CHAR8      *mFvbAlignmentName[] = {
  EFI_FVB2_ALIGNMENT_1_STRING,   
  EFI_FVB2_ALIGNMENT_2_STRING,   
  EFI_FVB2_ALIGNMENT_4_STRING,   
  EFI_FVB2_ALIGNMENT_8_STRING,   
  EFI_FVB2_ALIGNMENT_16_STRING,  
  EFI_FVB2_ALIGNMENT_32_STRING,  
  EFI_FVB2_ALIGNMENT_64_STRING,  
  EFI_FVB2_ALIGNMENT_128_STRING, 
  EFI_FVB2_ALIGNMENT_256_STRING, 
  EFI_FVB2_ALIGNMENT_512_STRING, 
  EFI_FVB2_ALIGNMENT_1K_STRING,  
  EFI_FVB2_ALIGNMENT_2K_STRING,  
  EFI_FVB2_ALIGNMENT_4K_STRING,  
  EFI_FVB2_ALIGNMENT_8K_STRING,  
  EFI_FVB2_ALIGNMENT_16K_STRING, 
  EFI_FVB2_ALIGNMENT_32K_STRING, 
  EFI_FVB2_ALIGNMENT_64K_STRING, 
  EFI_FVB2_ALIGNMENT_128K_STRING,
  EFI_FVB2_ALIGNMENT_256K_STRING,
  EFI_FVB2_ALIGNMNET_512K_STRING,
  EFI_FVB2_ALIGNMENT_1M_STRING,  
  EFI_FVB2_ALIGNMENT_2M_STRING,  
  EFI_FVB2_ALIGNMENT_4M_STRING,  
  EFI_FVB2_ALIGNMENT_8M_STRING,  
  EFI_FVB2_ALIGNMENT_16M_STRING, 
  EFI_FVB2_ALIGNMENT_32M_STRING, 
  EFI_FVB2_ALIGNMENT_64M_STRING, 
  EFI_FVB2_ALIGNMENT_128M_STRING,
  EFI_FVB2_ALIGNMENT_256M_STRING,
  EFI_FVB2_ALIGNMENT_512M_STRING,
  EFI_FVB2_ALIGNMENT_1G_STRING,  
  EFI_FVB2_ALIGNMENT_2G_STRING
};

//
// This data array will be located at the base of the Firmware Volume Header (FVH)
// in the boot block.  It must not exceed 14 bytes of code.  The last 2 bytes
// will be used to keep the FVH checksum consistent.
// This code will be run in response to a starutp IPI for HT-enabled systems.
//
#define SIZEOF_STARTUP_DATA_ARRAY 0x10

UINT8                                   m128kRecoveryStartupApDataArray[SIZEOF_STARTUP_DATA_ARRAY] = {
  //
  // EA D0 FF 00 F0               ; far jmp F000:FFD0
  // 0, 0, 0, 0, 0, 0, 0, 0, 0,   ; Reserved bytes
  // 0, 0                         ; Checksum Padding
  //
  0xEA,
  0xD0,
  0xFF,
  0x0,
  0xF0,
  0x00,
  0x00,
  0x00,
  0x00,
  0x00,
  0x00,
  0x00,
  0x00,
  0x00,
  0x00,
  0x00
};

UINT8                                   m64kRecoveryStartupApDataArray[SIZEOF_STARTUP_DATA_ARRAY] = {
  //
  // EB CE                               ; jmp short ($-0x30)
  // ; (from offset 0x0 to offset 0xFFD0)
  // 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ; Reserved bytes
  // 0, 0                                ; Checksum Padding
  //
  0xEB,
  0xCE,
  0x00,
  0x00,
  0x00,
  0x00,
  0x00,
  0x00,
  0x00,
  0x00,
  0x00,
  0x00,
  0x00,
  0x00,
  0x00,
  0x00
};

EFI_STATUS
ParseFvInf (
  IN  MEMORY_FILE  *InfFile,
  OUT FV_INFO      *FvInfo
  )
/*++

Routine Description:

  This function parses a FV.INF file and copies info into a FV_INFO structure.

Arguments:

  InfFile         Memory file image.
  FvInfo          Information read from INF file.

Returns:

  EFI_SUCCESS       INF file information successfully retrieved.
  EFI_ABORTED       INF file has an invalid format.
  EFI_NOT_FOUND     A required string was not found in the INF file.
--*/
{
  CHAR8       Value[_MAX_PATH];
  UINT64      Value64;
  UINTN       Index;
  EFI_STATUS  Status;

  //
  // Initialize FV info
  //
  memset (FvInfo, 0, sizeof (FV_INFO));

  //
  // Read the FV base address
  //
  Status = FindToken (InfFile, OPTIONS_SECTION_STRING, EFI_FV_BASE_ADDRESS_STRING, 0, Value);
  if (Status == EFI_SUCCESS) {
    //
    // Get the base address
    //
    Status = AsciiStringToUint64 (Value, FALSE, &Value64);
    if (EFI_ERROR (Status)) {
      Error (NULL, 0, 2000, "Invalid parameter", "%s = %s", EFI_FV_BASE_ADDRESS_STRING, Value);
      return EFI_ABORTED;
    }
    DebugMsg (NULL, 0, 9, "rebase address", "%s = %s", EFI_FV_BASE_ADDRESS_STRING, Value);

    FvInfo->BaseAddress = Value64;
  }

  //
  // Read the FV Guid
  //
  Status = FindToken (InfFile, OPTIONS_SECTION_STRING, EFI_FV_GUID_STRING, 0, Value);
  if (Status == EFI_SUCCESS) {
    //
    // Get the guid value
    //
    Status = StringToGuid (Value, &FvInfo->FvGuid);
    if (EFI_ERROR (Status)) {
      memcpy (&FvInfo->FvGuid, &mEfiFirmwareFileSystem2Guid, sizeof (EFI_GUID));
    }
  } else {
    memcpy (&FvInfo->FvGuid, &mEfiFirmwareFileSystem2Guid, sizeof (EFI_GUID));
  }
  DebugMsg (NULL, 0, 9, "FV File Guid", "%08X-%04X-%04X-%02X%02X-%02X%02X%02X%02X%02X%02X", 
                FvInfo->FvGuid.Data1,
                FvInfo->FvGuid.Data2,
                FvInfo->FvGuid.Data3,
                FvInfo->FvGuid.Data4[0],
                FvInfo->FvGuid.Data4[1],
                FvInfo->FvGuid.Data4[2],
                FvInfo->FvGuid.Data4[3],
                FvInfo->FvGuid.Data4[4],
                FvInfo->FvGuid.Data4[5],
                FvInfo->FvGuid.Data4[6],
                FvInfo->FvGuid.Data4[7]);

  //
  // Read the FV file name
  //
  Status = FindToken (InfFile, OPTIONS_SECTION_STRING, EFI_FV_FILE_NAME_STRING, 0, Value);
  if (Status == EFI_SUCCESS) {
    //
    // copy the file name
    //
    strcpy (FvInfo->FvName, Value);
  }
  
  //
  // Read Fv Attribute
  //
  for (Index = 0; Index < sizeof (mFvbAttributeName)/sizeof (CHAR8 *); Index ++) {
    if ((mFvbAttributeName [Index] != NULL) && \
        (FindToken (InfFile, ATTRIBUTES_SECTION_STRING, mFvbAttributeName [Index], 0, Value) == EFI_SUCCESS)) {
      if ((strcmp (Value, TRUE_STRING) == 0) || (strcmp (Value, ONE_STRING) == 0)) {
        FvInfo->FvAttributes |= 1 << Index;
      } else if ((strcmp (Value, FALSE_STRING) != 0) && (strcmp (Value, ZERO_STRING) != 0)) {
        Error (NULL, 0, 2000, "Invalid parameter", "%s expected %s | %s", mFvbAttributeName [Index], TRUE_STRING, FALSE_STRING);
        return EFI_ABORTED;
      }
    }
  }

  //
  // Read Fv Alignment
  //
  for (Index = 0; Index < sizeof (mFvbAlignmentName)/sizeof (CHAR8 *); Index ++) {
    if (FindToken (InfFile, ATTRIBUTES_SECTION_STRING, mFvbAlignmentName [Index], 0, Value) == EFI_SUCCESS) {
      if (strcmp (Value, TRUE_STRING) == 0) {
        FvInfo->FvAttributes |= Index << 16;
        DebugMsg (NULL, 0, 9, "FV file alignment", "Align = %s", mFvbAlignmentName [Index]);
        break;
      }
    }
  }

  //
  // Read block maps
  //
  for (Index = 0; Index < MAX_NUMBER_OF_FV_BLOCKS; Index++) {
    //
    // Read block size
    //
    Status = FindToken (InfFile, OPTIONS_SECTION_STRING, EFI_BLOCK_SIZE_STRING, Index, Value);

    if (Status == EFI_SUCCESS) {
      //
      // Update the size of block
      //
      Status = AsciiStringToUint64 (Value, FALSE, &Value64);
      if (EFI_ERROR (Status)) {
        Error (NULL, 0, 2000, "Invalid parameter", "%s = %s", EFI_BLOCK_SIZE_STRING, Value);
        return EFI_ABORTED;
      }

      FvInfo->FvBlocks[Index].Length = (UINT32) Value64;
      DebugMsg (NULL, 0, 9, "FV Block Size", "%s = %s", EFI_BLOCK_SIZE_STRING, Value);
    } else {
      //
      // If there is no blocks size, but there is the number of block, then we have a mismatched pair
      // and should return an error.
      //
      Status = FindToken (InfFile, OPTIONS_SECTION_STRING, EFI_NUM_BLOCKS_STRING, Index, Value);
      if (!EFI_ERROR (Status)) {
        Error (NULL, 0, 2000, "Invalid parameter", "both %s and %s must be specified.", EFI_NUM_BLOCKS_STRING, EFI_BLOCK_SIZE_STRING);
        return EFI_ABORTED;
      } else {
        //
        // We are done
        //
        break;
      }
    }

    //
    // Read blocks number
    //
    Status = FindToken (InfFile, OPTIONS_SECTION_STRING, EFI_NUM_BLOCKS_STRING, Index, Value);

    if (Status == EFI_SUCCESS) {
      //
      // Update the number of blocks
      //
      Status = AsciiStringToUint64 (Value, FALSE, &Value64);
      if (EFI_ERROR (Status)) {
        Error (NULL, 0, 2000, "Invalid parameter", "%s = %s", EFI_NUM_BLOCKS_STRING, Value);
        return EFI_ABORTED;
      }

      FvInfo->FvBlocks[Index].NumBlocks = (UINT32) Value64;
      DebugMsg (NULL, 0, 9, "FV Block Number", "%s = %s", EFI_NUM_BLOCKS_STRING, Value);
    }
  }

  if (Index == 0) {
    Error (NULL, 0, 2001, "Missing required argument", "block size.");
    return EFI_ABORTED;
  }

  //
  // Read files
  //
  for (Index = 0; Index < MAX_NUMBER_OF_FILES_IN_FV; Index++) {
    //
    // Read the number of blocks
    //
    Status = FindToken (InfFile, FILES_SECTION_STRING, EFI_FILE_NAME_STRING, Index, Value);

    if (Status == EFI_SUCCESS) {
      //
      // Add the file
      //
      strcpy (FvInfo->FvFiles[Index], Value);
      DebugMsg (NULL, 0, 9, "FV component file", "the %dth name is %s", Index, Value);
    } else {
      break;
    }
  }

  if (Index == 0) {
    Warning (NULL, 0, 0, "FV components are not specified.", NULL);
  }
  //
  // Compute size for easy access later
  //
  FvInfo->Size = 0;
  for (Index = 0; FvInfo->FvBlocks[Index].NumBlocks; Index++) {
    FvInfo->Size += FvInfo->FvBlocks[Index].NumBlocks * FvInfo->FvBlocks[Index].Length;
  }

  return EFI_SUCCESS;
}

VOID
UpdateFfsFileState (
  IN EFI_FFS_FILE_HEADER          *FfsFile,
  IN EFI_FIRMWARE_VOLUME_HEADER   *FvHeader
  )
/*++

Routine Description:

  This function changes the FFS file attributes based on the erase polarity
  of the FV. Update the reserved bits of State to EFI_FVB2_ERASE_POLARITY. 

Arguments:

  FfsFile   File header.
  FvHeader  FV header.

Returns:

  None

--*/
{
  if (FvHeader->Attributes & EFI_FVB2_ERASE_POLARITY) {
    FfsFile->State = (UINT8)~(FfsFile->State);
    // FfsFile->State |= ~(UINT8) EFI_FILE_ALL_STATE_BITS;
  }
}

EFI_STATUS
ReadFfsAlignment (
  IN EFI_FFS_FILE_HEADER    *FfsFile,
  IN OUT UINT32             *Alignment
  )
/*++

Routine Description:

  This function determines the alignment of the FFS input file from the file
  attributes.

Arguments:

  FfsFile       FFS file to parse
  Alignment     The minimum required alignment offset of the FFS file

Returns:

  EFI_SUCCESS              The function completed successfully.
  EFI_INVALID_PARAMETER    One of the input parameters was invalid.
  EFI_ABORTED              An error occurred.

--*/
{
  //
  // Verify input parameters.
  //
  if (FfsFile == NULL || Alignment == NULL) {
    return EFI_INVALID_PARAMETER;
  }

  switch ((FfsFile->Attributes >> 3) & 0x07) {

  case 0:
    //
    // 8 byte alignment, mini alignment requirement for FFS file. 
    //
    *Alignment = 3;
    break;

  case 1:
    //
    // 16 byte alignment
    //
    *Alignment = 4;
    break;

  case 2:
    //
    // 128 byte alignment
    //
    *Alignment = 7;
    break;

  case 3:
    //
    // 512 byte alignment
    //
    *Alignment = 9;
    break;

  case 4:
    //
    // 1K byte alignment
    //
    *Alignment = 10;
    break;

  case 5:
    //
    // 4K byte alignment
    //
    *Alignment = 12;
    break;

  case 6:
    //
    // 32K byte alignment
    //
    *Alignment = 15;
    break;

  case 7:
    //
    // 64K byte alignment
    //
    *Alignment = 16;
    break;

  default:
    break;
  }

  return EFI_SUCCESS;
}

EFI_STATUS
AddPadFile (
  IN OUT MEMORY_FILE  *FvImage,
  IN UINT32           DataAlignment
  )
/*++

Routine Description:

  This function adds a pad file to the FV image if it required to align the
  data of the next file.

Arguments:

  FvImage         The memory image of the FV to add it to.  The current offset
                  must be valid.
  DataAlignment   The data alignment of the next FFS file.

Returns:

  EFI_SUCCESS              The function completed successfully.
  EFI_INVALID_PARAMETER    One of the input parameters was invalid.
  EFI_OUT_OF_RESOURCES     Insufficient resources exist in the FV to complete
                           the pad file add.

--*/
{
  EFI_FFS_FILE_HEADER *PadFile;
  UINTN               PadFileSize;

  //
  // Verify input parameters.
  //
  if (FvImage == NULL) {
    return EFI_INVALID_PARAMETER;
  }

  //
  // Check if a pad file is necessary
  //
  if (((UINTN) FvImage->CurrentFilePointer - (UINTN) FvImage->FileImage + sizeof (EFI_FFS_FILE_HEADER)) % DataAlignment == 0) {
    return EFI_SUCCESS;
  }

  //
  // Write pad file header
  //
  PadFile = (EFI_FFS_FILE_HEADER *) FvImage->CurrentFilePointer;

  //
  // Verify that we have enough space for the file header
  //
  if ((UINTN) (PadFile + sizeof (EFI_FFS_FILE_HEADER)) >= (UINTN) FvImage->Eof) {
    return EFI_OUT_OF_RESOURCES;
  }

  //
  // write PadFile FFS header with PadType, don't need to set PAD file guid in its header.
  //
  PadFile->Type       = EFI_FV_FILETYPE_FFS_PAD;
  PadFile->Attributes = 0;

  //
  // Calculate the pad file size
  //
  //
  // This is the earliest possible valid offset (current plus pad file header
  // plus the next file header)
  //
  PadFileSize = (UINTN) FvImage->CurrentFilePointer - (UINTN) FvImage->FileImage + (sizeof (EFI_FFS_FILE_HEADER) * 2);

  //
  // Add whatever it takes to get to the next aligned address
  //
  while ((PadFileSize % DataAlignment) != 0) {
    PadFileSize++;
  }
  //
  // Subtract the next file header size
  //
  PadFileSize -= sizeof (EFI_FFS_FILE_HEADER);

  //
  // Subtract the starting offset to get size
  //
  PadFileSize -= (UINTN) FvImage->CurrentFilePointer - (UINTN) FvImage->FileImage;
  
  //
  // Write pad file size (calculated size minus next file header size)
  //
  PadFile->Size[0]  = (UINT8) (PadFileSize & 0xFF);
  PadFile->Size[1]  = (UINT8) ((PadFileSize >> 8) & 0xFF);
  PadFile->Size[2]  = (UINT8) ((PadFileSize >> 16) & 0xFF);

  //
  // Fill in checksums and state, they must be 0 for checksumming.
  //
  PadFile->IntegrityCheck.Checksum.Header = 0;
  PadFile->IntegrityCheck.Checksum.File   = 0;
  PadFile->State                          = 0;
  PadFile->IntegrityCheck.Checksum.Header = CalculateChecksum8 ((UINT8 *) PadFile, sizeof (EFI_FFS_FILE_HEADER));
  if (PadFile->Attributes & FFS_ATTRIB_CHECKSUM) {
    PadFile->IntegrityCheck.Checksum.File = CalculateChecksum8 ((UINT8 *) PadFile, PadFileSize);
  } else {
    PadFile->IntegrityCheck.Checksum.File = FFS_FIXED_CHECKSUM;
  }

  PadFile->State = EFI_FILE_HEADER_CONSTRUCTION | EFI_FILE_HEADER_VALID | EFI_FILE_DATA_VALID;
  UpdateFfsFileState (
    (EFI_FFS_FILE_HEADER *) PadFile,
    (EFI_FIRMWARE_VOLUME_HEADER *) FvImage->FileImage
    );

  //
  // Verify that we have enough space (including the padding
  //
  if ((UINTN) (PadFile + PadFileSize) >= (UINTN) FvImage->Eof) {
    return EFI_OUT_OF_RESOURCES;
  }
  //
  // Update the current FV pointer
  //
  FvImage->CurrentFilePointer += PadFileSize;

  return EFI_SUCCESS;
}

BOOLEAN
IsVtfFile (
  IN EFI_FFS_FILE_HEADER    *FileBuffer
  )
/*++

Routine Description:

  This function checks the header to validate if it is a VTF file

Arguments:

  FileBuffer     Buffer in which content of a file has been read.

Returns:

  TRUE    If this is a VTF file
  FALSE   If this is not a VTF file

--*/
{
  if (!memcmp (&FileBuffer->Name, &mEfiFirmwareVolumeTopFileGuid, sizeof (EFI_GUID))) {
    return TRUE;
  } else {
    return FALSE;
  }
}

EFI_STATUS
AddFile (
  IN OUT MEMORY_FILE          *FvImage,
  IN FV_INFO                  *FvInfo,
  IN UINTN                    Index,
  IN OUT EFI_FFS_FILE_HEADER  **VtfFileImage,
  IN FILE                     *FvMapFile  
  )
/*++

Routine Description:

  This function adds a file to the FV image.  The file will pad to the
  appropriate alignment if required.

Arguments:

  FvImage       The memory image of the FV to add it to.  The current offset
                must be valid.
  FvInfo        Pointer to information about the FV.
  Index         The file in the FvInfo file list to add.
  VtfFileImage  A pointer to the VTF file within the FvImage.  If this is equal
                to the end of the FvImage then no VTF previously found.
  FvMapFile     Pointer to FvMap File

Returns:

  EFI_SUCCESS              The function completed successfully.
  EFI_INVALID_PARAMETER    One of the input parameters was invalid.
  EFI_ABORTED              An error occurred.
  EFI_OUT_OF_RESOURCES     Insufficient resources exist to complete the add.

--*/
{
  FILE                  *NewFile;
  UINTN                 FileSize;
  UINT8                 *FileBuffer;
  UINTN                 NumBytesRead;
  UINT32                CurrentFileAlignment;
  EFI_STATUS            Status;
  EFI_PHYSICAL_ADDRESS  CurrentFileBaseAddress;
  UINT8                 VtfHeaderChecksum;
  UINT8                 VtfFileChecksum;
  UINT8                 FileState;
  UINTN                 Index1;
  
  Index1 = 0;
  //
  // Verify input parameters.
  //
  if (FvImage == NULL || FvInfo == NULL || FvInfo->FvFiles[Index][0] == 0 || VtfFileImage == NULL) {
    return EFI_INVALID_PARAMETER;
  }

  //
  // Read the file to add
  //
  NewFile = fopen (FvInfo->FvFiles[Index], "rb");

  if (NewFile == NULL) {
    Error (NULL, 0, 0001, "Error opening file", FvInfo->FvFiles[Index]);
    return EFI_ABORTED;
  }

  //
  // Get the file size
  //
  FileSize = _filelength (fileno (NewFile));

  //
  // Read the file into a buffer
  //
  FileBuffer = malloc (FileSize);
  if (FileBuffer == NULL) {
    Error (NULL, 0, 4001, "Resouce", "memory cannot be allocated!");
    return EFI_OUT_OF_RESOURCES;
  }

  NumBytesRead = fread (FileBuffer, sizeof (UINT8), FileSize, NewFile);

  //
  // Done with the file, from this point on we will just use the buffer read.
  //
  fclose (NewFile);
  
  //
  // Verify read successful
  //
  if (NumBytesRead != sizeof (UINT8) * FileSize) {
    free  (FileBuffer);
    Error (NULL, 0, 0004, "Error reading file", FvInfo->FvFiles[Index]);
    return EFI_ABORTED;
  }
  
  //
  // Verify Ffs file
  //
  Status = VerifyFfsFile (FileBuffer);
  if (EFI_ERROR (Status)) {
    free (FileBuffer);
    Error (NULL, 0, 3000, "Invalid", "%s is a FFS file.", FvInfo->FvFiles[Index]);
    return EFI_INVALID_PARAMETER;
  }

  //
  // Verify space exists to add the file
  //
  if (FileSize > (UINTN) ((UINTN) *VtfFileImage - (UINTN) FvImage->CurrentFilePointer)) {
    free (FileBuffer);
    Error (NULL, 0, 4002, "Resource", "FV space is full, not enough room to add file %s.", FvInfo->FvFiles[Index]);
    return EFI_OUT_OF_RESOURCES;
  }

  //
  // Verify the input file is the duplicated file in this Fv image
  //
  for (Index1 = 0; Index1 < Index; Index1 ++) {
    if (CompareGuid ((EFI_GUID *) FileBuffer, &mFileGuidArray [Index1]) == 0) {
      Error (NULL, 0, 2000, "Invalid parameter", "the %dth file and %dth file have the same file GUID.", Index1 + 1, Index + 1);
      PrintGuid ((EFI_GUID *) FileBuffer);
      return EFI_INVALID_PARAMETER;
    }
  }
  CopyMem (&mFileGuidArray [Index], FileBuffer, sizeof (EFI_GUID));

  //
  // Update the file state based on polarity of the FV.
  //
  UpdateFfsFileState (
    (EFI_FFS_FILE_HEADER *) FileBuffer,
    (EFI_FIRMWARE_VOLUME_HEADER *) FvImage->FileImage
    );

  //
  // Check if alignment is required
  //
  ReadFfsAlignment ((EFI_FFS_FILE_HEADER *) FileBuffer, &CurrentFileAlignment);
  
  //
  // Find the largest alignment of all the FFS files in the FV
  //
  if (CurrentFileAlignment > MaxFfsAlignment) {
    MaxFfsAlignment = CurrentFileAlignment;
  }
  //
  // If we have a VTF file, add it at the top.
  //
  if (IsVtfFile ((EFI_FFS_FILE_HEADER *) FileBuffer)) {
    if ((UINTN) *VtfFileImage == (UINTN) FvImage->Eof) {
      //
      // No previous VTF, add this one.
      //
      *VtfFileImage = (EFI_FFS_FILE_HEADER *) (UINTN) ((UINTN) FvImage->FileImage + FvInfo->Size - FileSize);
      //
      // Sanity check. The file MUST align appropriately
      //
      if (((UINTN) *VtfFileImage + sizeof (EFI_FFS_FILE_HEADER) - (UINTN) FvImage->FileImage) % (1 << CurrentFileAlignment)) {
        Error (NULL, 0, 3000, "Invalid", "VTF file cannot be aligned on a %d-byte boundary.", 1 << CurrentFileAlignment);
        free (FileBuffer);
        return EFI_ABORTED;
      }
      //
      // Rebase the PE or TE image in FileBuffer of FFS file for XIP 
      // Rebase for the debug genfvmap tool
      //
      FfsRebase (FvInfo, FvInfo->FvFiles[Index], (EFI_FFS_FILE_HEADER *) FileBuffer, (UINTN) *VtfFileImage - (UINTN) FvImage->FileImage, FvMapFile);
      //
      // copy VTF File
      //
      memcpy (*VtfFileImage, FileBuffer, FileSize);
      free (FileBuffer);
      DebugMsg (NULL, 0, 9, "Add VTF FFS file in FV image", NULL);
      return EFI_SUCCESS;
    } else {
      //
      // Already found a VTF file.
      //
      Error (NULL, 0, 3000, "Invalid", "multiple VTF files are not permitted within a single FV.");
      free (FileBuffer);
      return EFI_ABORTED;
    }
  }

  //
  // Add pad file if necessary
  //
  Status = AddPadFile (FvImage, 1 << CurrentFileAlignment);
  if (EFI_ERROR (Status)) {
    Error (NULL, 0, 4002, "Resource", "FV space is full, could not add pad file for data alignment property.");
    free (FileBuffer);
    return EFI_ABORTED;
  }
  //
  // Add file
  //
  if ((FvImage->CurrentFilePointer + FileSize) < FvImage->Eof) {
    //
    // Rebase the PE or TE image in FileBuffer of FFS file for XIP. 
    // Rebase Bs and Rt drivers for the debug genfvmap tool.
    //
    FfsRebase (FvInfo, FvInfo->FvFiles[Index], (EFI_FFS_FILE_HEADER *) FileBuffer, (UINTN) FvImage->CurrentFilePointer - (UINTN) FvImage->FileImage, FvMapFile);
    //
    // Copy the file
    //
    memcpy (FvImage->CurrentFilePointer, FileBuffer, FileSize);
    FvImage->CurrentFilePointer += FileSize;
  } else {
    Error (NULL, 0, 4002, "Resource", "FV space is full, cannot add file %s.", FvInfo->FvFiles[Index]);
    free (FileBuffer);
    return EFI_ABORTED;
  }
  //
  // Make next file start at QWord Boundry
  //
  while (((UINTN) FvImage->CurrentFilePointer & (EFI_FFS_FILE_HEADER_ALIGNMENT - 1)) != 0) {
    FvImage->CurrentFilePointer++;
  }

  //
  // Free allocated memory.
  //
  free (FileBuffer);

  return EFI_SUCCESS;
}

EFI_STATUS
PadFvImage (
  IN MEMORY_FILE          *FvImage,
  IN EFI_FFS_FILE_HEADER  *VtfFileImage
  )
/*++

Routine Description:

  This function places a pad file between the last file in the FV and the VTF
  file if the VTF file exists.

Arguments:

  FvImage       Memory file for the FV memory image
  VtfFileImage  The address of the VTF file.  If this is the end of the FV
                image, no VTF exists and no pad file is needed.

Returns:

  EFI_SUCCESS             Completed successfully.
  EFI_INVALID_PARAMETER   One of the input parameters was NULL.

--*/
{
  EFI_FFS_FILE_HEADER *PadFile;
  UINTN               FileSize;

  //
  // If there is no VTF or the VTF naturally follows the previous file without a
  // pad file, then there's nothing to do
  //
  if ((UINTN) VtfFileImage == (UINTN) FvImage->Eof || \
      ((UINTN) VtfFileImage == (UINTN) FvImage->CurrentFilePointer)) {
    return EFI_SUCCESS;
  }

  //
  // Pad file starts at beginning of free space
  //
  PadFile = (EFI_FFS_FILE_HEADER *) FvImage->CurrentFilePointer;

  //
  // write PadFile FFS header with PadType, don't need to set PAD file guid in its header. 
  //
  PadFile->Type       = EFI_FV_FILETYPE_FFS_PAD;
  PadFile->Attributes = 0;

  //
  // FileSize includes the EFI_FFS_FILE_HEADER
  //
  FileSize          = (UINTN) VtfFileImage - (UINTN) FvImage->CurrentFilePointer;
  PadFile->Size[0]  = (UINT8) (FileSize & 0x000000FF);
  PadFile->Size[1]  = (UINT8) ((FileSize & 0x0000FF00) >> 8);
  PadFile->Size[2]  = (UINT8) ((FileSize & 0x00FF0000) >> 16);

  //
  // Fill in checksums and state, must be zero during checksum calculation.
  //
  PadFile->IntegrityCheck.Checksum.Header = 0;
  PadFile->IntegrityCheck.Checksum.File   = 0;
  PadFile->State                          = 0;
  PadFile->IntegrityCheck.Checksum.Header = CalculateChecksum8 ((UINT8 *) PadFile, sizeof (EFI_FFS_FILE_HEADER));
  if (PadFile->Attributes & FFS_ATTRIB_CHECKSUM) {
    PadFile->IntegrityCheck.Checksum.File = CalculateChecksum8 ((UINT8 *) PadFile, FileSize);
  } else {
    PadFile->IntegrityCheck.Checksum.File = FFS_FIXED_CHECKSUM;
  }

  PadFile->State = EFI_FILE_HEADER_CONSTRUCTION | EFI_FILE_HEADER_VALID | EFI_FILE_DATA_VALID;

  UpdateFfsFileState (
    (EFI_FFS_FILE_HEADER *) PadFile,
    (EFI_FIRMWARE_VOLUME_HEADER *) FvImage->FileImage
    );
  //
  // Update the current FV pointer
  //
  FvImage->CurrentFilePointer = FvImage->Eof;

  return EFI_SUCCESS;
}

EFI_STATUS
UpdateResetVector (
  IN MEMORY_FILE            *FvImage,
  IN FV_INFO                *FvInfo,
  IN EFI_FFS_FILE_HEADER    *VtfFile
  )
/*++

Routine Description:

  This parses the FV looking for the PEI core and then plugs the address into
  the SALE_ENTRY point of the BSF/VTF for IPF and does BUGBUG TBD action to
  complete an IA32 Bootstrap FV.

Arguments:

  FvImage       Memory file for the FV memory image
  FvInfo        Information read from INF file.
  VtfFile       Pointer to the VTF file in the FV image.

Returns:

  EFI_SUCCESS             Function Completed successfully.
  EFI_ABORTED             Error encountered.
  EFI_INVALID_PARAMETER   A required parameter was NULL.
  EFI_NOT_FOUND           PEI Core file not found.

--*/
{
  EFI_FFS_FILE_HEADER       *PeiCoreFile;
  EFI_FFS_FILE_HEADER       *SecCoreFile;
  EFI_STATUS                Status;
  EFI_FILE_SECTION_POINTER  Pe32Section;
  UINT32                    EntryPoint;
  UINT32                    BaseOfCode;
  UINT16                    MachineType;
  EFI_PHYSICAL_ADDRESS      PeiCorePhysicalAddress;
  EFI_PHYSICAL_ADDRESS      SecCorePhysicalAddress;
  EFI_PHYSICAL_ADDRESS      *SecCoreEntryAddressPtr;
  INT32                     Ia32SecEntryOffset;
  UINT32                    *Ia32ResetAddressPtr;
  UINT8                     *BytePointer;
  UINT8                     *BytePointer2;
  UINT16                    *WordPointer;
  UINT16                    CheckSum;
  UINTN                     Index;
  EFI_FFS_FILE_STATE        SavedState;
  UINT64                    FitAddress;
  FIT_TABLE                 *FitTablePtr;
  UINT32                    IpiVector;

  //
  // Verify input parameters
  //
  if (FvImage == NULL || FvInfo == NULL || VtfFile == NULL) {
    return EFI_INVALID_PARAMETER;
  }
  //
  // Initialize FV library
  //
  InitializeFvLib (FvImage->FileImage, FvInfo->Size);

  //
  // Verify VTF file
  //
  Status = VerifyFfsFile (VtfFile);
  if (EFI_ERROR (Status)) {
    return EFI_INVALID_PARAMETER;
  }

  //
  // Find the Sec Core
  //
  Status = GetFileByType (EFI_FV_FILETYPE_SECURITY_CORE, 1, &SecCoreFile);
  if (EFI_ERROR (Status) || SecCoreFile == NULL) {
    Error (NULL, 0, 3000, "Invalid", "could not find the SEC core file in the FV.");
    return EFI_ABORTED;
  }
  //
  // Sec Core found, now find PE32 section
  //
  Status = GetSectionByType (SecCoreFile, EFI_SECTION_PE32, 1, &Pe32Section);
  if (Status == EFI_NOT_FOUND) {
    Status = GetSectionByType (SecCoreFile, EFI_SECTION_TE, 1, &Pe32Section);
  }

  if (EFI_ERROR (Status)) {
    Error (NULL, 0, 3000, "Invalid", "could not find a PE32 section in the SEC core file.");
    return EFI_ABORTED;
  }

  Status = GetPe32Info (
            (VOID *) ((UINTN) Pe32Section.Pe32Section + sizeof (EFI_SECTION_PE32)),
            &EntryPoint,
            &BaseOfCode,
            &MachineType
            );

  if (EFI_ERROR (Status)) {
    Error (NULL, 0, 3000, "Invalid", "could not get the PE32 entry point for the SEC core.");
    return EFI_ABORTED;
  }
  //
  // Physical address is FV base + offset of PE32 + offset of the entry point
  //
  SecCorePhysicalAddress = FvInfo->BaseAddress;
  SecCorePhysicalAddress += (UINTN) Pe32Section.Pe32Section + sizeof (EFI_SECTION_PE32) - (UINTN) FvImage->FileImage;
  SecCorePhysicalAddress += EntryPoint;
  DebugMsg (NULL, 0, 9, "SecCore physical entry point address", "Address = 0x%X", SecCorePhysicalAddress); 

  //
  // Find the PEI Core
  //
  Status = GetFileByType (EFI_FV_FILETYPE_PEI_CORE, 1, &PeiCoreFile);
  if (EFI_ERROR (Status) || PeiCoreFile == NULL) {
    Error (NULL, 0, 3000, "Invalid", "could not find the PEI core in the FV.");
    return EFI_ABORTED;
  }
  //
  // PEI Core found, now find PE32 or TE section
  //
  Status = GetSectionByType (PeiCoreFile, EFI_SECTION_PE32, 1, &Pe32Section);
  if (Status == EFI_NOT_FOUND) {
    Status = GetSectionByType (PeiCoreFile, EFI_SECTION_TE, 1, &Pe32Section);
  }

  if (EFI_ERROR (Status)) {
    Error (NULL, 0, 3000, "Invalid", "could not find either a PE32 or a TE section in PEI core file.");
    return EFI_ABORTED;
  }

  Status = GetPe32Info (
            (VOID *) ((UINTN) Pe32Section.Pe32Section + sizeof (EFI_SECTION_PE32)),
            &EntryPoint,
            &BaseOfCode,
            &MachineType
            );

  if (EFI_ERROR (Status)) {
    Error (NULL, 0, 3000, "Invalid", "could not get the PE32 entry point for the PEI core.");
    return EFI_ABORTED;
  }
  //
  // Physical address is FV base + offset of PE32 + offset of the entry point
  //
  PeiCorePhysicalAddress = FvInfo->BaseAddress;
  PeiCorePhysicalAddress += (UINTN) Pe32Section.Pe32Section + sizeof (EFI_SECTION_PE32) - (UINTN) FvImage->FileImage;
  PeiCorePhysicalAddress += EntryPoint;
  DebugMsg (NULL, 0, 9, "PeiCore physical entry point address", "Address = 0x%X", PeiCorePhysicalAddress);

  if (MachineType == EFI_IMAGE_MACHINE_IA64) {
    //
    // Update PEI_CORE address
    //
    //
    // Set the uncached attribute bit in the physical address
    //
    PeiCorePhysicalAddress |= 0x8000000000000000ULL;

    //
    // Check if address is aligned on a 16 byte boundary
    //
    if (PeiCorePhysicalAddress & 0xF) {
      Error (NULL, 0, 3000, "Invalid",
        "PEI_CORE entry point is not aligned on a 16 byte boundary, address specified is %Xh.",
        PeiCorePhysicalAddress
        );
      return EFI_ABORTED;
    }
    //
    // First Get the FIT table address
    //
    FitAddress  = (*(UINT64 *) (FvImage->Eof - IPF_FIT_ADDRESS_OFFSET)) & 0xFFFFFFFF;

    FitTablePtr = (FIT_TABLE *) (FvImage->FileImage + (FitAddress - FvInfo->BaseAddress));

    Status      = UpdatePeiCoreEntryInFit (FitTablePtr, PeiCorePhysicalAddress);

    if (!EFI_ERROR (Status)) {
      UpdateFitCheckSum (FitTablePtr);
    }

    //
    // Update SEC_CORE address
    //
    //
    // Set the uncached attribute bit in the physical address
    //
    SecCorePhysicalAddress |= 0x8000000000000000ULL;
    //
    // Check if address is aligned on a 16 byte boundary
    //
    if (SecCorePhysicalAddress & 0xF) {
      Error (NULL, 0, 3000, "Invalid",
        "SALE_ENTRY entry point is not aligned on a 16 byte boundary, address specified is %Xh.",
        SecCorePhysicalAddress
        );
      return EFI_ABORTED;
    }
    //
    // Update the address
    //
    SecCoreEntryAddressPtr  = (EFI_PHYSICAL_ADDRESS *) ((UINTN) FvImage->Eof - IPF_SALE_ENTRY_ADDRESS_OFFSET);
    *SecCoreEntryAddressPtr = SecCorePhysicalAddress;

  } else if (MachineType == EFI_IMAGE_MACHINE_IA32) {
    //
    // Get the location to update
    //
    Ia32ResetAddressPtr  = (UINT32 *) ((UINTN) FvImage->Eof - IA32_PEI_CORE_ENTRY_OFFSET);

    //
    // Write lower 32 bits of physical address for Pei Core entry
    //
    *Ia32ResetAddressPtr = (UINT32) PeiCorePhysicalAddress;
    
    //
    // Write SecCore Entry point relative address into the jmp instruction in reset vector.
    // 
    Ia32ResetAddressPtr  = (UINT32 *) ((UINTN) FvImage->Eof - IA32_SEC_CORE_ENTRY_OFFSET);
    
    Ia32SecEntryOffset   = SecCorePhysicalAddress - (FV_IMAGES_TOP_ADDRESS - IA32_SEC_CORE_ENTRY_OFFSET + 2);
    if (Ia32SecEntryOffset <= -65536) {
      Error (NULL, 0, 3000, "Invalid", "The SEC EXE file size is too large, it must be less than 64K.");
      return STATUS_ERROR;
    }
    
    *(UINT16 *) Ia32ResetAddressPtr = (UINT16) Ia32SecEntryOffset;

    //
    // Update the BFV base address
    //
    Ia32ResetAddressPtr   = (UINT32 *) ((UINTN) FvImage->Eof - 4);
    *Ia32ResetAddressPtr  = (UINT32) (FvInfo->BaseAddress);
    DebugMsg (NULL, 0, 9, "update BFV base address in the top FV image", "BFV base address = 0x%X.", FvInfo->BaseAddress);

    //
    // Update the Startup AP in the FVH header block ZeroVector region.
    //
    BytePointer   = (UINT8 *) ((UINTN) FvImage->FileImage);
    if (FvInfo->Size == 0x10000) {
      BytePointer2 = m64kRecoveryStartupApDataArray;
    } else if (FvInfo->Size == 0x20000) {
      BytePointer2 = m128kRecoveryStartupApDataArray;
    } else if (FvInfo->Size > 0x20000) {
      BytePointer2 = m128kRecoveryStartupApDataArray;
      //
      // Find the position to place Ap reset vector, the offset
      // between the position and the end of Fvrecovery.fv file
      // should not exceed 128kB to prevent Ap reset vector from
      // outside legacy E and F segment
      //
      Status = FindApResetVectorPosition (FvImage, &BytePointer);
      if (EFI_ERROR (Status)) {
        Error (NULL, 0, 3000, "Invalid", "Cannot find the appropriate location in FvImage to add Ap reset vector!");
        return EFI_ABORTED;
      }
    }

    for (Index = 0; Index < SIZEOF_STARTUP_DATA_ARRAY; Index++) {
      BytePointer[Index] = BytePointer2[Index];
    }
    //
    // Calculate the checksum
    //
    CheckSum              = 0x0000;
    WordPointer = (UINT16 *) (BytePointer);
    for (Index = 0; Index < SIZEOF_STARTUP_DATA_ARRAY / 2; Index++) {
      CheckSum = (UINT16) (CheckSum + ((UINT16) *WordPointer));
      WordPointer++;
    }
    //
    // Update the checksum field
    //
    WordPointer   = (UINT16 *) (BytePointer + SIZEOF_STARTUP_DATA_ARRAY - 2);
    *WordPointer  = (UINT16) (0x10000 - (UINT32) CheckSum);
    
    //
    // IpiVector at the 4k aligned address in the top 2 blocks in the PEI FV. 
    //
    IpiVector  = FV_IMAGES_TOP_ADDRESS - ((UINTN) FvImage->Eof - (UINTN) BytePointer);
    DebugMsg (NULL, 0, 9, "Startup AP Vector address", "IpiVector at 0x%X", IpiVector);
    IpiVector  = IpiVector >> 12;
    IpiVector  = IpiVector & 0xFF;

    //
    // Write IPI Vector at Offset FvrecoveryFileSize - 8
    //
    Ia32ResetAddressPtr   = (UINT32 *) ((UINTN) FvImage->Eof - 8);
    *Ia32ResetAddressPtr  = IpiVector;
  } else {
    Error (NULL, 0, 3000, "Invalid", "machine type=0x%X in PEI core.", (UINT32) MachineType);
    return EFI_ABORTED;
  }

  //
  // Now update file checksum
  //
  SavedState  = VtfFile->State;
  VtfFile->IntegrityCheck.Checksum.File = 0;
  VtfFile->State                        = 0;
  if (VtfFile->Attributes & FFS_ATTRIB_CHECKSUM) {
    VtfFile->IntegrityCheck.Checksum.File = CalculateChecksum8 (
                                              (UINT8 *) VtfFile,
                                              GetLength (VtfFile->Size)
                                              );
  } else {
    VtfFile->IntegrityCheck.Checksum.File = FFS_FIXED_CHECKSUM;
  }

  VtfFile->State = SavedState;

  return EFI_SUCCESS;
}

EFI_STATUS
GetPe32Info (
  IN UINT8                  *Pe32,
  OUT UINT32                *EntryPoint,
  OUT UINT32                *BaseOfCode,
  OUT UINT16                *MachineType
  )
/*++

Routine Description:

  Retrieves the PE32 entry point offset and machine type from PE image or TeImage.  
  See EfiImage.h for machine types.  The entry point offset is from the beginning 
  of the PE32 buffer passed in.

Arguments:

  Pe32          Beginning of the PE32.
  EntryPoint    Offset from the beginning of the PE32 to the image entry point.
  BaseOfCode    Base address of code.
  MachineType   Magic number for the machine type.

Returns:

  EFI_SUCCESS             Function completed successfully.
  EFI_ABORTED             Error encountered.
  EFI_INVALID_PARAMETER   A required parameter was NULL.
  EFI_UNSUPPORTED         The operation is unsupported.

--*/
{
  EFI_IMAGE_DOS_HEADER  *DosHeader;
  EFI_IMAGE_NT_HEADERS  *NtHeader;
  EFI_TE_IMAGE_HEADER   *TeHeader;

  //
  // Verify input parameters
  //
  if (Pe32 == NULL) {
    return EFI_INVALID_PARAMETER;
  }

  //
  // First check whether it is one TE Image.
  //
  TeHeader = (EFI_TE_IMAGE_HEADER *) Pe32;
  if (TeHeader->Signature == EFI_TE_IMAGE_HEADER_SIGNATURE) {
    //
    // By TeImage Header to get output
    //
    *EntryPoint   = TeHeader->AddressOfEntryPoint + sizeof (EFI_TE_IMAGE_HEADER) - TeHeader->StrippedSize;
    *BaseOfCode   = TeHeader->BaseOfCode + sizeof (EFI_TE_IMAGE_HEADER) - TeHeader->StrippedSize;
    *MachineType  = TeHeader->Machine;
  } else {
  
    //
    // Then check whether 
    // First is the DOS header
    //
    DosHeader = (EFI_IMAGE_DOS_HEADER *) Pe32;
  
    //
    // Verify DOS header is expected
    //
    if (DosHeader->e_magic != EFI_IMAGE_DOS_SIGNATURE) {
      Error (NULL, 0, 3000, "Invalid", "Unknown magic number in the DOS header, 0x%04X.", DosHeader->e_magic);
      return EFI_UNSUPPORTED;
    }
    //
    // Immediately following is the NT header.
    //
    NtHeader = (EFI_IMAGE_NT_HEADERS *) ((UINTN) Pe32 + DosHeader->e_lfanew);
  
    //
    // Verify NT header is expected
    //
    if (NtHeader->Signature != EFI_IMAGE_NT_SIGNATURE) {
      Error (NULL, 0, 3000, "Invalid", "Unrecognized image signature 0x%08X.", NtHeader->Signature);
      return EFI_UNSUPPORTED;
    }
    //
    // Get output
    //
    *EntryPoint   = NtHeader->OptionalHeader.AddressOfEntryPoint;
    *BaseOfCode   = NtHeader->OptionalHeader.BaseOfCode;
    *MachineType  = NtHeader->FileHeader.Machine;
  }

  //
  // Verify machine type is supported
  //
  if (*MachineType != EFI_IMAGE_MACHINE_IA32 && *MachineType != EFI_IMAGE_MACHINE_IA64 && *MachineType != EFI_IMAGE_MACHINE_X64 && *MachineType != EFI_IMAGE_MACHINE_EBC) {
    Error (NULL, 0, 3000, "Invalid", "Unrecognized machine type in the PE32 file.");
    return EFI_UNSUPPORTED;
  }

  return EFI_SUCCESS;
}

EFI_STATUS
GenerateFvImage (
  IN CHAR8                *InfFileImage,
  IN UINTN                InfFileSize,
  IN CHAR8                *FvFileName,
  IN CHAR8                *MapFileName,
  IN EFI_PHYSICAL_ADDRESS XipBaseAddress,
  IN EFI_PHYSICAL_ADDRESS *BtBaseAddress,
  IN EFI_PHYSICAL_ADDRESS *RtBaseAddress
  )
/*++

Routine Description:

  This is the main function which will be called from application.

Arguments:

  InfFileImage   Buffer containing the INF file contents.
  InfFileSize    Size of the contents of the InfFileImage buffer.
  FvFileName     Requested name for the FV file.
  MapFileName    Fv map file to log fv driver information.
  XipBaseAddress BaseAddress is to be rebased.
  BtBaseAddress  Pointer to BaseAddress is to set the prefer loaded image start address for boot drivers.
  RtBaseAddress  Pointer to BaseAddress is to set the prefer loaded image start address for runtime drivers.

Returns:

  EFI_SUCCESS             Function completed successfully.
  EFI_OUT_OF_RESOURCES    Could not allocate required resources.
  EFI_ABORTED             Error encountered.
  EFI_INVALID_PARAMETER   A required parameter was NULL.

--*/
{
  EFI_STATUS                  Status;
  MEMORY_FILE                 InfMemoryFile;
  MEMORY_FILE                 FvImageMemoryFile;
  FV_INFO                     FvInfo;
  UINTN                       Index;
  EFI_FIRMWARE_VOLUME_HEADER  *FvHeader;
  EFI_FFS_FILE_HEADER         *VtfFileImage;
  UINT8                       *FvBufferHeader; // to make sure fvimage header 8 type alignment.
  UINT8                       *FvImage;
  UINTN                       FvImageSize;
  FILE                        *FvFile;
  CHAR8                       FvMapName [_MAX_PATH];
  FILE                        *FvMapFile;

  FvBufferHeader = NULL;
  FvFile         = NULL;
  FvMapFile      = NULL;
  //
  // Check for invalid parameter
  //
  if (InfFileImage == NULL) {
    return EFI_INVALID_PARAMETER;
  }

  //
  // Initialize file structures
  //
  InfMemoryFile.FileImage           = InfFileImage;
  InfMemoryFile.CurrentFilePointer  = InfFileImage;
  InfMemoryFile.Eof                 = InfFileImage + InfFileSize;

  //
  // Parse the FV inf file for header information
  //
  Status = ParseFvInf (&InfMemoryFile, &FvInfo);
  if (EFI_ERROR (Status)) {
    Error (NULL, 0, 0003, "Error parsing file", "the input INF file.");
    return Status;
  }

  //
  // Update the file name return values
  //
  if (FvFileName == NULL && FvInfo.FvName[0] != '\0') {
    FvFileName = FvInfo.FvName;
  }

  if (FvFileName == NULL) {
    Error (NULL, 0, 1001, "Missing option", "Output file name");
    return EFI_ABORTED;
  }
  
  //
  // FvMap file to log the function address of all modules in one Fvimage
  //
  if (MapFileName != NULL) {
    strcpy (FvMapName, MapFileName);
  } else {
    strcpy (FvMapName, FvFileName);
    strcat (FvMapName, ".map");
  }
  VerboseMsg ("FV Map file name is %s", FvMapName);

  FvMapFile = fopen (FvMapName, "w");
  if (FvMapFile == NULL) {
    Error (NULL, 0, 0001, "Error opening file", FvMapName);
    return EFI_ABORTED;
  }
  
  //
  // Update FvImage Base Address, XipBase not same to BtBase, RtBase address.
  //
  if (XipBaseAddress != 0) {
    FvInfo.BaseAddress = XipBaseAddress;
  }
  if (*BtBaseAddress != 0) {
    FvInfo.BootBaseAddress = *BtBaseAddress;
  }
  if (*RtBaseAddress != 0) {
    FvInfo.RuntimeBaseAddress = *RtBaseAddress;
  }

  //
  // Calculate the FV size and Update Fv Size based on the actual FFS files.
  // And Update FvInfo data.
  //
  Status = CalculateFvSize (&FvInfo);
  if (EFI_ERROR (Status)) {
    return Status;    
  }
  VerboseMsg ("the generated FV image size is %d bytes", FvInfo.Size);
  
  //
  // support fv image and empty fv image
  //
  FvImageSize = FvInfo.Size;

  //
  // Allocate the FV, assure FvImage Header 8 byte alignment
  //
  FvBufferHeader = malloc (FvImageSize + sizeof (UINT64));
  if (FvBufferHeader == NULL) {
    return EFI_OUT_OF_RESOURCES;
  }
  FvImage = (UINT8 *) (((UINTN) FvBufferHeader + 7) & ~7);

  //
  // Initialize the FV to the erase polarity
  //
  if (FvInfo.FvAttributes & EFI_FVB2_ERASE_POLARITY) {
    memset (FvImage, -1, FvImageSize);
  } else {
    memset (FvImage, 0, FvImageSize);
  }

  //
  // Initialize FV header
  //
  FvHeader = (EFI_FIRMWARE_VOLUME_HEADER *) FvImage;

  //
  // Initialize the zero vector to all zeros.
  //
  memset (FvHeader->ZeroVector, 0, 16);

  //
  // Copy the FFS GUID
  //
  memcpy (&FvHeader->FileSystemGuid, &FvInfo.FvGuid, sizeof (EFI_GUID));

  FvHeader->FvLength        = FvImageSize;
  FvHeader->Signature       = EFI_FVH_SIGNATURE;
  FvHeader->Attributes      = FvInfo.FvAttributes;
  FvHeader->Revision        = EFI_FVH_REVISION;
  FvHeader->ExtHeaderOffset = 0;
  FvHeader->Reserved[0]     = 0;
  
  //
  // Copy firmware block map
  //
  for (Index = 0; FvInfo.FvBlocks[Index].Length != 0; Index++) {
    FvHeader->BlockMap[Index].NumBlocks   = FvInfo.FvBlocks[Index].NumBlocks;
    FvHeader->BlockMap[Index].Length      = FvInfo.FvBlocks[Index].Length;
  }

  //
  // Add block map terminator
  //
  FvHeader->BlockMap[Index].NumBlocks   = 0;
  FvHeader->BlockMap[Index].Length      = 0;

  //
  // Complete the header
  //
  FvHeader->HeaderLength  = (UINT16) (((UINTN) &(FvHeader->BlockMap[Index + 1])) - (UINTN) FvImage);
  FvHeader->Checksum      = 0;
  FvHeader->Checksum      = CalculateChecksum16 ((UINT16 *) FvHeader, FvHeader->HeaderLength / sizeof (UINT16));

  //
  // If there is no FFS file, generate one empty FV
  //
  if (FvInfo.FvFiles[0][0] == 0) {
    goto WriteFile;
  }

  //
  // Initialize our "file" view of the buffer
  //
  FvImageMemoryFile.FileImage           = FvImage;
  FvImageMemoryFile.CurrentFilePointer  = FvImage + FvHeader->HeaderLength;
  FvImageMemoryFile.Eof                 = FvImage + FvImageSize;

  //
  // Initialize the FV library.
  //
  InitializeFvLib (FvImageMemoryFile.FileImage, FvImageSize);

  //
  // Initialize the VTF file address.
  //
  VtfFileImage = (EFI_FFS_FILE_HEADER *) FvImageMemoryFile.Eof;

  //
  // Add files to FV
  //
  for (Index = 0; FvInfo.FvFiles[Index][0] != 0; Index++) {
    //
    // Add the file
    //
    Status = AddFile (&FvImageMemoryFile, &FvInfo, Index, &VtfFileImage, FvMapFile);

    //
    // Exit if error detected while adding the file
    //
    if (EFI_ERROR (Status)) {
      goto Finish;
    }
  }

  //
  // If there is a VTF file, some special actions need to occur.
  //
  if ((UINTN) VtfFileImage != (UINTN) FvImageMemoryFile.Eof) {
    //
    // Pad from the end of the last file to the beginning of the VTF file.
    // If the left space is less than sizeof (EFI_FFS_FILE_HEADER)?
    //
    Status = PadFvImage (&FvImageMemoryFile, VtfFileImage);
    if (EFI_ERROR (Status)) {
      Error (NULL, 0, 4002, "Resource", "FV space is full, cannot add pad file between the last file and the VTF file.");
      goto Finish;
    }
    //
    // Update reset vector (SALE_ENTRY for IPF)
    // Now for IA32 and IA64 platform, the fv which has bsf file must have the 
    // EndAddress of 0xFFFFFFFF. Thus, only this type fv needs to update the   
    // reset vector. If the PEI Core is found, the VTF file will probably get  
    // corrupted by updating the entry point.                                  
    //
    if ((FvInfo.BaseAddress + FvInfo.Size) == FV_IMAGES_TOP_ADDRESS) {       
      Status = UpdateResetVector (&FvImageMemoryFile, &FvInfo, VtfFileImage);
      if (EFI_ERROR(Status)) {                                               
        Error (NULL, 0, 3000, "Invalid", "Could not update the reset vector.");
        goto Finish;                                              
      }
      DebugMsg (NULL, 0, 9, "Update Reset vector in VTF file", NULL);
    }
  } 
  
  //
  // Update FV Alignment attribute to the largest alignment of all the FFS files in the FV
  //
  if ((((FvHeader->Attributes & EFI_FVB2_ALIGNMENT) >> 16)) < MaxFfsAlignment) {
    FvHeader->Attributes = ((MaxFfsAlignment << 16) | (FvHeader->Attributes & 0xFFFF));
    //
    // Update Checksum for FvHeader
    //
    FvHeader->Checksum      = 0;
    FvHeader->Checksum      = CalculateChecksum16 ((UINT16 *) FvHeader, FvHeader->HeaderLength / sizeof (UINT16));
  }

WriteFile: 
  //
  // Write fv file
  //
  FvFile = fopen (FvFileName, "wb");
  if (FvFile == NULL) {
    Error (NULL, 0, 0001, "Error opening file", FvFileName);
    Status = EFI_ABORTED;
    goto Finish;
  }

  if (fwrite (FvImage, 1, FvImageSize, FvFile) != FvImageSize) {
    Error (NULL, 0, 0002, "Error writing file", FvFileName);
    Status = EFI_ABORTED;
    goto Finish;
  }

Finish:
  if (FvBufferHeader != NULL) {
    free (FvBufferHeader);
  }
  
  if (FvFile != NULL) {
    fclose (FvFile);
  }
  
  if (FvMapFile != NULL) {
    fclose (FvMapFile);
  }

  //
  // Update BootAddress and RuntimeAddress
  //
  *BtBaseAddress = FvInfo.BootBaseAddress;
  *RtBaseAddress = FvInfo.RuntimeBaseAddress;

  return Status;
}

EFI_STATUS
UpdatePeiCoreEntryInFit (
  IN FIT_TABLE     *FitTablePtr,
  IN UINT64        PeiCorePhysicalAddress
  )
/*++

Routine Description:

  This function is used to update the Pei Core address in FIT, this can be used by Sec core to pass control from
  Sec to Pei Core

Arguments:

  FitTablePtr             - The pointer of FIT_TABLE.
  PeiCorePhysicalAddress  - The address of Pei Core entry.

Returns:

  EFI_SUCCESS             - The PEI_CORE FIT entry was updated successfully.
  EFI_NOT_FOUND           - Not found the PEI_CORE FIT entry.

--*/
{
  FIT_TABLE *TmpFitPtr;
  UINTN     Index;
  UINTN     NumFitComponents;

  TmpFitPtr         = FitTablePtr;
  NumFitComponents  = TmpFitPtr->CompSize;

  for (Index = 0; Index < NumFitComponents; Index++) {
    if ((TmpFitPtr->CvAndType & FIT_TYPE_MASK) == COMP_TYPE_FIT_PEICORE) {
      TmpFitPtr->CompAddress = PeiCorePhysicalAddress;
      return EFI_SUCCESS;
    }

    TmpFitPtr++;
  }

  return EFI_NOT_FOUND;
}

VOID
UpdateFitCheckSum (
  IN FIT_TABLE   *FitTablePtr
  )
/*++

Routine Description:

  This function is used to update the checksum for FIT.


Arguments:

  FitTablePtr             - The pointer of FIT_TABLE.

Returns:

  None.

--*/
{
  if ((FitTablePtr->CvAndType & CHECKSUM_BIT_MASK) >> 7) {
    FitTablePtr->CheckSum = 0;
    FitTablePtr->CheckSum = CalculateChecksum8 ((UINT8 *) FitTablePtr, FitTablePtr->CompSize * 16);
  }
}

EFI_STATUS
CalculateFvSize (
  FV_INFO *FvInfoPtr
  )
/*++
Routine Description:
  Calculate the FV size and Update Fv Size based on the actual FFS files.
  And Update FvInfo data.

Arguments:
  FvInfoPtr     - The pointer to FV_INFO structure.

Returns:
  EFI_ABORTED   - Ffs Image Error
  EFI_SUCCESS   - Successfully update FvSize
--*/
{
  UINTN               CurrentOffset;
  UINTN               Index;
  FILE                *fpin;
  UINTN               FfsFileSize;
  UINT32              FfsAlignment;
  EFI_FFS_FILE_HEADER FfsHeader;
  EFI_STATUS          Status;
  BOOLEAN             VtfFileFlag;
  
  VtfFileFlag = FALSE;
  fpin  = NULL;
  Index = 0;
  CurrentOffset = sizeof (EFI_FIRMWARE_VOLUME_HEADER);
  
  for (Index = 1;; Index ++) {
    CurrentOffset += sizeof (EFI_FV_BLOCK_MAP_ENTRY);
    if (FvInfoPtr->FvBlocks[Index].NumBlocks == 0 && FvInfoPtr->FvBlocks[Index].Length == 0) {
      break;
    }
  }

  //
  // Accumlate every FFS file size.
  //
  for (Index = 0; FvInfoPtr->FvFiles[Index][0] != 0; Index++) {
    //
    // Open FFS file
    //
    fpin = NULL;
    fpin = fopen (FvInfoPtr->FvFiles[Index], "rb");
    if (fpin == NULL) {
      Error (NULL, 0, 0001, "Error opening file", FvInfoPtr->FvFiles[Index]);
      return EFI_ABORTED;
    }
    //
    // Get the file size
    //
    FfsFileSize = _filelength (fileno (fpin));
    //
    // Read Ffs File header
    //
    fread (&FfsHeader, sizeof (UINT8), sizeof (EFI_FFS_FILE_HEADER), fpin);
    //
    // close file
    //
    fclose (fpin);
    //
    // Check whether this ffs file is vtf file
    //
    if (IsVtfFile (&FfsHeader)) {
      if (VtfFileFlag) {
        //
        // One Fv image can't have two vtf files.
        //
        return EFI_ABORTED;
      }
      VtfFileFlag = TRUE;
      //
      // The space between Vft File and the latest file must be able to contain 
      // one ffs file header in order to add one pad file.
      //
      CurrentOffset += sizeof (EFI_FFS_FILE_HEADER);
    }
    //
    // Get the alignment of FFS file 
    //
    ReadFfsAlignment (&FfsHeader, &FfsAlignment);
    FfsAlignment = 1 << FfsAlignment;
    //
    // Add Pad file
    //
    if (((CurrentOffset + sizeof (EFI_FFS_FILE_HEADER)) % FfsAlignment) != 0) {
      CurrentOffset = (CurrentOffset + sizeof (EFI_FFS_FILE_HEADER) * 2 + FfsAlignment - 1) & ~(FfsAlignment - 1);
      CurrentOffset -= sizeof (EFI_FFS_FILE_HEADER);
    }
    //
    // Add ffs file size
    //
    CurrentOffset += FfsFileSize;    
    //
    // Make next ffs file start at QWord Boundry
    //
    CurrentOffset = (CurrentOffset + EFI_FFS_FILE_HEADER_ALIGNMENT - 1) & ~(EFI_FFS_FILE_HEADER_ALIGNMENT - 1);
  }
  
  DebugMsg (NULL, 0, 9, "FvImage size", "The caculated fv image size is 0x%x and the current set fv image size is 0x%x", CurrentOffset, FvInfoPtr->Size);
  
  if (FvInfoPtr->Size < CurrentOffset) { 
    //
    // Update FvInfo data
    //
    FvInfoPtr->FvBlocks[0].NumBlocks = CurrentOffset / FvInfoPtr->FvBlocks[0].Length + ((CurrentOffset % FvInfoPtr->FvBlocks[0].Length)?1:0);
    FvInfoPtr->Size = FvInfoPtr->FvBlocks[0].NumBlocks * FvInfoPtr->FvBlocks[0].Length;
    FvInfoPtr->FvBlocks[1].NumBlocks = 0;
    FvInfoPtr->FvBlocks[1].Length = 0;
  }

  return EFI_SUCCESS;
}

EFI_STATUS
FfsRebaseImageRead (
  IN     VOID    *FileHandle,
  IN     UINTN   FileOffset,
  IN OUT UINT32  *ReadSize,
  OUT    VOID    *Buffer
  )
/*++

Routine Description:

  Support routine for the PE/COFF Loader that reads a buffer from a PE/COFF file

Arguments:

  FileHandle - The handle to the PE/COFF file

  FileOffset - The offset, in bytes, into the file to read

  ReadSize   - The number of bytes to read from the file starting at FileOffset

  Buffer     - A pointer to the buffer to read the data into.

Returns:

  EFI_SUCCESS - ReadSize bytes of data were read into Buffer from the PE/COFF file starting at FileOffset

--*/
{
  CHAR8   *Destination8;
  CHAR8   *Source8;
  UINT32  Length;

  Destination8  = Buffer;
  Source8       = (CHAR8 *) ((UINTN) FileHandle + FileOffset);
  Length        = *ReadSize;
  while (Length--) {
    *(Destination8++) = *(Source8++);
  }

  return EFI_SUCCESS;
}

EFI_STATUS
FfsRebase ( 
  IN OUT  FV_INFO               *FvInfo, 
  IN      CHAR8                 *FileName,           
  IN OUT  EFI_FFS_FILE_HEADER   *FfsFile,
  IN      UINTN                 XipOffset,
  IN      FILE                  *FvMapFile
  )
/*++

Routine Description:

  This function determines if a file is XIP and should be rebased.  It will
  rebase any PE32 sections found in the file using the base address.

Arguments:
  
  FvInfo            A pointer to FV_INFO struture.
  FileName          Ffs File PathName
  FfsFile           A pointer to Ffs file image.
  XipOffset         The offset address to use for rebasing the XIP file image.
  FvMapFile         FvMapFile to record the function address in one Fvimage

Returns:

  EFI_SUCCESS             The image was properly rebased.
  EFI_INVALID_PARAMETER   An input parameter is invalid.
  EFI_ABORTED             An error occurred while rebasing the input file image.
  EFI_OUT_OF_RESOURCES    Could not allocate a required resource.
  EFI_NOT_FOUND           No compressed sections could be found.

--*/
{
  EFI_STATUS                            Status;
  PE_COFF_LOADER_IMAGE_CONTEXT          ImageContext;
  EFI_PHYSICAL_ADDRESS                  XipBase;
  EFI_PHYSICAL_ADDRESS                  NewPe32BaseAddress;
  EFI_PHYSICAL_ADDRESS                  *BaseToUpdate;
  UINTN                                 Index;
  EFI_FILE_SECTION_POINTER              CurrentPe32Section;
  EFI_FFS_FILE_STATE                    SavedState;
  EFI_IMAGE_NT_HEADERS                  *PeHdr;
  EFI_IMAGE_OPTIONAL_HEADER32           *Optional32;
  EFI_IMAGE_OPTIONAL_HEADER64           *Optional64;
  EFI_TE_IMAGE_HEADER                   *TEImageHeader;
  UINT8                                 Flags;
  UINT8                                 *MemoryImagePointer;
  EFI_IMAGE_SECTION_HEADER              *SectionHeader;
  CHAR8                                 PeFileName [_MAX_PATH];
  CHAR8                                 *Cptr;
  FILE                                  *PeFile;
  UINT8                                 *PeFileBuffer;
  UINT32                                PeFileSize;

  Index              = 0;  
  MemoryImagePointer = NULL;
  BaseToUpdate       = NULL;
  TEImageHeader      = NULL;
  PeHdr              = NULL;
  Optional32         = NULL;
  Optional64         = NULL;
  SectionHeader      = NULL;
  Cptr               = NULL;
  PeFile             = NULL;
  PeFileBuffer       = NULL;
  //
  // Check XipAddress, BootAddress and RuntimeAddress
  //
  Flags = 0;

  if (FvInfo->BaseAddress != 0) {
    Flags  |= REBASE_XIP_FILE;
    XipBase = FvInfo->BaseAddress + XipOffset;
  }
  if (FvInfo->BootBaseAddress != 0) {
    Flags  |= REBASE_BOOTTIME_FILE;
  }
  if (FvInfo->RuntimeBaseAddress != 0) {
    Flags  |= REBASE_RUNTIME_FILE;
  }
  //
  // Don't Rebase this FFS.
  //
  if (Flags == 0) {
    return EFI_SUCCESS;
  }

  //
  // We only process files potentially containing PE32 sections.
  //
  switch (FfsFile->Type) {
    case EFI_FV_FILETYPE_SECURITY_CORE:
    case EFI_FV_FILETYPE_PEI_CORE:
    case EFI_FV_FILETYPE_PEIM:
    case EFI_FV_FILETYPE_COMBINED_PEIM_DRIVER:
    case EFI_FV_FILETYPE_DRIVER:
    case EFI_FV_FILETYPE_DXE_CORE:
      break;
    default:
      return EFI_SUCCESS;
  }

  //
  // Rebase each PE32 section
  //
  Status      = EFI_SUCCESS;
  for (Index = 1;; Index++) {
    Status = GetSectionByType (FfsFile, EFI_SECTION_PE32, Index, &CurrentPe32Section);
    if (EFI_ERROR (Status)) {
      break;
    }

    //
    // Initialize context
    //
    memset (&ImageContext, 0, sizeof (ImageContext));
    ImageContext.Handle     = (VOID *) ((UINTN) CurrentPe32Section.Pe32Section + sizeof (EFI_PE32_SECTION));
    ImageContext.ImageRead  = (PE_COFF_LOADER_READ_FILE) FfsRebaseImageRead;
    Status                  = PeCoffLoaderGetImageInfo (&ImageContext);
    if (EFI_ERROR (Status)) {
      Error (NULL, 0, 3000, "Invalid", "GetImageInfo() call failed on rebase %s.", FileName);
      return Status;
    }

    //
    // Get PeHeader pointer
    //
    PeHdr = (EFI_IMAGE_NT_HEADERS *)((UINTN) CurrentPe32Section.Pe32Section + sizeof (EFI_PE32_SECTION) + ImageContext.PeCoffHeaderOffset);

    //
    // Calculate the PE32 base address, based on file type
    //
    switch (FfsFile->Type) {
      case EFI_FV_FILETYPE_SECURITY_CORE:
      case EFI_FV_FILETYPE_PEI_CORE:
      case EFI_FV_FILETYPE_PEIM:
      case EFI_FV_FILETYPE_COMBINED_PEIM_DRIVER:
        if ((Flags & REBASE_XIP_FILE) == 0) {
          //
          // We aren't relocating XIP code, so skip it.
          //
          return EFI_SUCCESS;
        }
        
        //
        // Check if section-alignment and file-alignment match or not
        //
        if ((PeHdr->OptionalHeader.SectionAlignment != PeHdr->OptionalHeader.FileAlignment)) {
          //
          // Xip module has the same section alignment and file alignment.
          //
          Error (NULL, 0, 3000, "Invalid", "Section-Alignment and File-Alignment do not match : %s.", FileName);
          return EFI_ABORTED;
        }
        //
        // PeImage has no reloc section. It will try to get reloc data from the original EFI image. 
        //
        if (ImageContext.RelocationsStripped) {
          //
          // Construct the original efi file Name 
          //
          strcpy (PeFileName, FileName);
          Cptr = PeFileName + strlen (PeFileName);
          while (*Cptr != '.') {
            Cptr --;
          }
          if (*Cptr != '.') {
            Error (NULL, 0, 3000, "Invalid", "The file %s has no .reloc section.", FileName);
            return EFI_ABORTED;
          } else {
            *(Cptr + 1) = 'e';
            *(Cptr + 2) = 'f';
            *(Cptr + 3) = 'i';
            *(Cptr + 4) = '\0';
          }
          PeFile = fopen (PeFileName, "rb");
          if (PeFile == NULL) {
            Error (NULL, 0, 3000, "Invalid", "The file %s has no .reloc section.", FileName);
            return EFI_ABORTED;
          }
          //
          // Get the file size
          //
          PeFileSize = _filelength (fileno (PeFile));
          PeFileBuffer = (UINT8 *) malloc (PeFileSize);
          if (PeFileBuffer == NULL) {
            Error (NULL, 0, 4001, "Resource", "memory cannot be allocated on rebase of %s", FileName);
            return EFI_OUT_OF_RESOURCES;
          }
          //
          // Read Pe File
          //
          fread (PeFileBuffer, sizeof (UINT8), PeFileSize, PeFile);
          //
          // close file
          //
          fclose (PeFile);
          //
          // Handle pointer to the original efi image.
          //
          ImageContext.Handle = PeFileBuffer;
          Status              = PeCoffLoaderGetImageInfo (&ImageContext);
          if (EFI_ERROR (Status)) {
            Error (NULL, 0, 3000, "Invalid", "GetImageInfo() call failed on rebase of %s", FileName);
            return Status;
          }
          ImageContext.RelocationsStripped = FALSE;
        }

        NewPe32BaseAddress = XipBase + (UINTN) CurrentPe32Section.Pe32Section + sizeof (EFI_PE32_SECTION) - (UINTN)FfsFile;
        BaseToUpdate = &XipBase;
        break;

      case EFI_FV_FILETYPE_DRIVER:
        switch (PeHdr->OptionalHeader.Subsystem) {
          case EFI_IMAGE_SUBSYSTEM_EFI_RUNTIME_DRIVER:
            if ((Flags & REBASE_RUNTIME_FILE) == 0) {
              //
              // RT drivers aren't supposed to be relocated
              //
              continue;
            }
            //
            // make sure image base address at the section alignment
            //
            FvInfo->RuntimeBaseAddress = (FvInfo->RuntimeBaseAddress - ImageContext.ImageSize) & (~(ImageContext.SectionAlignment - 1));
            FvInfo->RuntimeBaseAddress = FvInfo->RuntimeBaseAddress & (~(EFI_PAGE_SIZE - 1));
            NewPe32BaseAddress = FvInfo->RuntimeBaseAddress;
            BaseToUpdate = &(FvInfo->RuntimeBaseAddress);
            break;

          default:
            //
            // We treat all other subsystems the same as BS_DRIVER
            //
            if ((Flags & REBASE_BOOTTIME_FILE) == 0) {
              //
              // Skip all BS_DRIVER's
              //
              continue;
            }
            //
            // make sure image base address at the Section and Page alignment
            //
            FvInfo->BootBaseAddress = (FvInfo->BootBaseAddress - ImageContext.ImageSize) & (~(ImageContext.SectionAlignment - 1));
            FvInfo->BootBaseAddress = FvInfo->BootBaseAddress & (~(EFI_PAGE_SIZE - 1));
            NewPe32BaseAddress = FvInfo->BootBaseAddress;
            BaseToUpdate = &(FvInfo->BootBaseAddress);
            break;
        }
        break;

      case EFI_FV_FILETYPE_DXE_CORE:
        if ((Flags & REBASE_BOOTTIME_FILE) == 0) {
          //
          // Skip DXE core, DxeCore only contain one PE image.
          //
          return EFI_SUCCESS;
        }
        //
        // make sure image base address at the Section and Page alignment
        //
        FvInfo->BootBaseAddress = (FvInfo->BootBaseAddress - ImageContext.ImageSize) & (~(ImageContext.SectionAlignment - 1));
        FvInfo->BootBaseAddress = FvInfo->BootBaseAddress & (~(EFI_PAGE_SIZE - 1));
        NewPe32BaseAddress = FvInfo->BootBaseAddress;
        BaseToUpdate = &(FvInfo->BootBaseAddress);
        break;

      default:
        //
        // Not supported file type
        //
        return EFI_SUCCESS;
    }

    //
    // Load and Relocate Image Data
    //
    MemoryImagePointer = (UINT8 *) malloc ((UINTN) ImageContext.ImageSize + ImageContext.SectionAlignment);
    if (MemoryImagePointer == NULL) {
      Error (NULL, 0, 4001, "Resource", "memory cannot be allocated on rebase of %s", FileName);
      return EFI_OUT_OF_RESOURCES;
    }
    memset ((VOID *) MemoryImagePointer, 0, (UINTN) ImageContext.ImageSize + ImageContext.SectionAlignment);
    ImageContext.ImageAddress = ((UINTN) MemoryImagePointer + ImageContext.SectionAlignment - 1) & (~(ImageContext.SectionAlignment - 1));
    
    Status =  PeCoffLoaderLoadImage (&ImageContext);
    if (EFI_ERROR (Status)) {
      Error (NULL, 0, 3000, "Invalid", "LocateImage() call failed on rebase of %s", FileName);
      free ((VOID *) MemoryImagePointer);
      return Status;
    }
         
    ImageContext.DestinationAddress = NewPe32BaseAddress;
    Status                          = PeCoffLoaderRelocateImage (&ImageContext);
    if (EFI_ERROR (Status)) {
      Error (NULL, 0, 3000, "Invalid", "RelocateImage() call failed on rebase of %s", FileName);
      free ((VOID *) MemoryImagePointer);
      return Status;
    }

    //
    // Copy Relocated data to raw image file.
    //
    if (PeHdr->FileHeader.Machine == EFI_IMAGE_MACHINE_IA32) {
      Optional32 = (EFI_IMAGE_OPTIONAL_HEADER32 *) &(PeHdr->OptionalHeader);
      Optional32->ImageBase     = (UINT32) NewPe32BaseAddress;
    } else if (PeHdr->FileHeader.Machine == EFI_IMAGE_MACHINE_IA64 || 
               PeHdr->FileHeader.Machine == EFI_IMAGE_MACHINE_X64) {
      Optional64 = (EFI_IMAGE_OPTIONAL_HEADER64 *) &(PeHdr->OptionalHeader);
      Optional64->ImageBase     = NewPe32BaseAddress;
    } else {
      Error (NULL, 0, 3000, "Invalid", "unknown machine type %X in PE32 image %s", 
        (UINT32) PeHdr->FileHeader.Machine,
        FileName
        );
      free ((VOID *) MemoryImagePointer);
      return EFI_ABORTED;
    }

    SectionHeader = (EFI_IMAGE_SECTION_HEADER *) (
                       (UINTN) PeHdr +
                       sizeof (UINT32) + 
                       sizeof (EFI_IMAGE_FILE_HEADER) +  
                       PeHdr->FileHeader.SizeOfOptionalHeader
                       );
    
    for (Index = 0; Index < PeHdr->FileHeader.NumberOfSections; Index ++, SectionHeader ++) {
      CopyMem (
        (UINT8 *) CurrentPe32Section.Pe32Section + sizeof (EFI_COMMON_SECTION_HEADER) + SectionHeader->PointerToRawData, 
        (VOID*) (UINTN) (ImageContext.ImageAddress + SectionHeader->VirtualAddress), 
        SectionHeader->SizeOfRawData
        );
    }

    free ((VOID *) MemoryImagePointer);
    MemoryImagePointer = NULL;
    if (PeFileBuffer != NULL) {
      free (PeFileBuffer);
      PeFileBuffer = NULL;
    }

    //
    // Update BASE address by add one page size.
    //
    *BaseToUpdate -= EFI_PAGE_SIZE;

    //
    // Now update file checksum
    //
    if (FfsFile->Attributes & FFS_ATTRIB_CHECKSUM) {
      SavedState  = FfsFile->State;
      FfsFile->IntegrityCheck.Checksum.File = 0;
      FfsFile->State                        = 0;
      if (FfsFile->Attributes & FFS_ATTRIB_CHECKSUM) {
        FfsFile->IntegrityCheck.Checksum.File = CalculateChecksum8 (
                                                  (UINT8 *) FfsFile,
                                                  GetLength (FfsFile->Size)
                                                  );
      } else {
        FfsFile->IntegrityCheck.Checksum.File = FFS_FIXED_CHECKSUM;
      }

      FfsFile->State = SavedState;
    }

    //
    // Get this module function address from ModulePeMapFile and add them into FvMap file
    //
    WriteMapFile (FvMapFile, FileName, ImageContext.DestinationAddress, PeHdr->OptionalHeader.AddressOfEntryPoint, 0);
  }

  if ((Flags & 1) == 0 || (
      FfsFile->Type != EFI_FV_FILETYPE_SECURITY_CORE &&
      FfsFile->Type != EFI_FV_FILETYPE_PEI_CORE &&

      FfsFile->Type != EFI_FV_FILETYPE_PEIM &&
      FfsFile->Type != EFI_FV_FILETYPE_COMBINED_PEIM_DRIVER
      )) {
    //
    // Only XIP code may have a TE section
    //
    return EFI_SUCCESS;
  }
  
  //
  // Now process TE sections
  //
  for (Index = 1;; Index++) {
    Status = GetSectionByType (FfsFile, EFI_SECTION_TE, Index, &CurrentPe32Section);
    if (EFI_ERROR (Status)) {
      break;
    }

    //
    // Calculate the TE base address, the FFS file base plus the offset of the TE section less the size stripped off
    // by GenTEImage
    //
    TEImageHeader = (EFI_TE_IMAGE_HEADER *) ((UINT8 *) CurrentPe32Section.Pe32Section + sizeof (EFI_COMMON_SECTION_HEADER));

    //
    // Initialize context, load image info.
    //
    memset (&ImageContext, 0, sizeof (ImageContext));
    ImageContext.Handle     = (VOID *) TEImageHeader;
    ImageContext.ImageRead  = (PE_COFF_LOADER_READ_FILE) FfsRebaseImageRead;

    Status                  = PeCoffLoaderGetImageInfo (&ImageContext);

    if (EFI_ERROR (Status)) {
      Error (NULL, 0, 3000, "Invalid", "GetImageInfo() call failed on rebase of TE image %s", FileName);
      return Status;
    }
    //
    // if reloc is stripped, try to get the original efi image to get reloc info.
    //
    if (ImageContext.RelocationsStripped == TRUE) {
      //
      // Construct the original efi file name 
      //
      strcpy (PeFileName, FileName);
      Cptr = PeFileName + strlen (PeFileName);
      while (*Cptr != '.') {
        Cptr --;
      }
      if (*Cptr != '.') {
        Error (NULL, 0, 3000, "Invalid", "The file %s has no .reloc section.", FileName);
        return EFI_ABORTED;
      } else {
        *(Cptr + 1) = 'e';
        *(Cptr + 2) = 'f';
        *(Cptr + 3) = 'i';
        *(Cptr + 4) = '\0';
      }
      PeFile = fopen (PeFileName, "rb");
      if (PeFile == NULL) {
        Error (NULL, 0, 3000, "Invalid", "The file %s has no .reloc section.", FileName);
        return EFI_ABORTED;
      }
      //
      // Get the file size
      //
      PeFileSize = _filelength (fileno (PeFile));
      PeFileBuffer = (UINT8 *) malloc (PeFileSize);
      if (PeFileBuffer == NULL) {
        Error (NULL, 0, 4001, "Resource", "memory cannot be allocated on rebase of %s", FileName);
        return EFI_OUT_OF_RESOURCES;
      }
      //
      // Read Pe File
      //
      fread (PeFileBuffer, sizeof (UINT8), PeFileSize, PeFile);
      //
      // close file
      //
      fclose (PeFile);
      //
      // Append reloc section into TeImage
      //
      ImageContext.Handle = PeFileBuffer;
      Status              = PeCoffLoaderGetImageInfo (&ImageContext);
      if (EFI_ERROR (Status)) {
        Error (NULL, 0, 3000, "Invalid", "GetImageInfo() call failed on rebase of TE image %s", FileName);
        return Status;
      }
      ImageContext.RelocationsStripped = FALSE;
    }

    //
    // Load and Relocate Image Data
    //
    MemoryImagePointer = (UINT8 *) malloc ((UINTN) ImageContext.ImageSize + ImageContext.SectionAlignment);
    if (MemoryImagePointer == NULL) {
      Error (NULL, 0, 4001, "Resource", "memory cannot be allocated on rebase of %s", FileName);
      return EFI_OUT_OF_RESOURCES;
    }
    memset ((VOID *) MemoryImagePointer, 0, (UINTN) ImageContext.ImageSize + ImageContext.SectionAlignment);
    ImageContext.ImageAddress = ((UINTN) MemoryImagePointer + ImageContext.SectionAlignment - 1) & (~(ImageContext.SectionAlignment - 1));

    Status =  PeCoffLoaderLoadImage (&ImageContext);
    if (EFI_ERROR (Status)) {
      Error (NULL, 0, 3000, "Invalid", "LocateImage() call failed on rebase of %s", FileName);
      free ((VOID *) MemoryImagePointer);
      return Status;
    }
    //
    // Reloacate TeImage
    // 
    ImageContext.DestinationAddress = XipBase + (UINTN) TEImageHeader + sizeof (EFI_TE_IMAGE_HEADER) \
                                      - TEImageHeader->StrippedSize - (UINTN) FfsFile;
    Status                          = PeCoffLoaderRelocateImage (&ImageContext);
    if (EFI_ERROR (Status)) {
      Error (NULL, 0, 3000, "Invalid", "RelocateImage() call failed on rebase of TE image %s", FileName);
      free ((VOID *) MemoryImagePointer);
      return Status;
    }
    
    //
    // Copy the relocated image into raw image file.
    //
    TEImageHeader->ImageBase = ImageContext.DestinationAddress;
    SectionHeader = (EFI_IMAGE_SECTION_HEADER *) (TEImageHeader + 1);
    for (Index = 0; Index < TEImageHeader->NumberOfSections; Index ++, SectionHeader ++) {
      if (!ImageContext.IsTeImage) {
        CopyMem (
          (UINT8 *) TEImageHeader + sizeof (EFI_TE_IMAGE_HEADER) - TEImageHeader->StrippedSize + SectionHeader->PointerToRawData, 
          (VOID*) (UINTN) (ImageContext.ImageAddress + SectionHeader->VirtualAddress), 
          SectionHeader->SizeOfRawData
          );
      } else {
        CopyMem (
          (UINT8 *) TEImageHeader + sizeof (EFI_TE_IMAGE_HEADER) - TEImageHeader->StrippedSize + SectionHeader->PointerToRawData, 
          (VOID*) (UINTN) (ImageContext.ImageAddress + sizeof (EFI_TE_IMAGE_HEADER) - TEImageHeader->StrippedSize + SectionHeader->VirtualAddress), 
          SectionHeader->SizeOfRawData
          );
      }
    }
    
    //
    // Free the allocated memory resource
    //
    free ((VOID *) MemoryImagePointer);
    MemoryImagePointer = NULL;
    if (PeFileBuffer != NULL) {
      free (PeFileBuffer);
      PeFileBuffer = NULL;
    }

    //
    // Now update file checksum
    //
    if (FfsFile->Attributes & FFS_ATTRIB_CHECKSUM) {
      SavedState  = FfsFile->State;
      FfsFile->IntegrityCheck.Checksum.File = 0;
      FfsFile->State                        = 0;
      if (FfsFile->Attributes & FFS_ATTRIB_CHECKSUM) {
        FfsFile->IntegrityCheck.Checksum.File = CalculateChecksum8 (
                                                  (UINT8 *) FfsFile,
                                                  GetLength (FfsFile->Size)
                                                  );
      } else {
        FfsFile->IntegrityCheck.Checksum.File = FFS_FIXED_CHECKSUM;
      }

      FfsFile->State = SavedState;
    }
    //
    // Get this module function address from ModulePeMapFile and add them into FvMap file
    //
    WriteMapFile (
      FvMapFile, 
      FileName, 
      ImageContext.DestinationAddress, 
      TEImageHeader->AddressOfEntryPoint, 
      TEImageHeader->StrippedSize - sizeof (EFI_TE_IMAGE_HEADER)
      );  
  }
 
  return EFI_SUCCESS;
}

EFI_STATUS
FindApResetVectorPosition (
  IN  MEMORY_FILE  *FvImage,
  OUT UINT8        **Pointer
  )
/*++

Routine Description:

  Find the position in this FvImage to place Ap reset vector.

Arguments:

  FvImage       Memory file for the FV memory image.
  Pointer       Pointer to pointer to position.

Returns:

  EFI_NOT_FOUND   - No satisfied position is found.
  EFI_SUCCESS     - The suitable position is return.

--*/
{
  EFI_FFS_FILE_HEADER   *PadFile;
  UINT32                Index;
  EFI_STATUS            Status;
  UINT8                 *FixPoint;
  UINT32                FileLength;

  for (Index = 1; ;Index ++) {
    //
    // Find Pad File to add ApResetVector info
    //
    Status = GetFileByType (EFI_FV_FILETYPE_FFS_PAD, Index, &PadFile);
    if (EFI_ERROR (Status) || (PadFile == NULL)) {
      //
      // No Pad file to be found.
      //
      break;
    }
    //
    // Get Pad file size.
    //
    FileLength = (*(UINT32 *)(PadFile->Size)) & 0x00FFFFFF;
    FileLength = (FileLength + EFI_FFS_FILE_HEADER_ALIGNMENT - 1) & ~(EFI_FFS_FILE_HEADER_ALIGNMENT - 1); 
    //
    // FixPoint must be align on 0x1000 relative to FvImage Header
    //
    FixPoint = (UINT8*) PadFile + sizeof (EFI_FFS_FILE_HEADER);
    FixPoint = FixPoint + 0x1000 - (((UINTN) FixPoint - (UINTN) FvImage->FileImage) & 0xFFF);
    //
    // FixPoint be larger at the last place of one fv image.
    //
    while (((UINTN) FixPoint + SIZEOF_STARTUP_DATA_ARRAY - (UINTN) PadFile) <= FileLength) {
      FixPoint += 0x1000;
    }
    FixPoint -= 0x1000;
    
    if ((UINTN) FixPoint < ((UINTN) PadFile + sizeof (EFI_FFS_FILE_HEADER))) {
      //
      // No alignment FixPoint in this Pad File.
      //
      continue;
    }

    if ((UINTN) FvImage->Eof - (UINTN)FixPoint <= 0x20000) {    
      //
      // Find the position to place ApResetVector
      //
      *Pointer = FixPoint;
      return EFI_SUCCESS;
    }
  }
  
  return EFI_NOT_FOUND;
}

EFI_STATUS
WriteMapFile (
  IN OUT FILE                  *FvMapFile,
  IN     CHAR8                 *FileName, 
  IN     EFI_PHYSICAL_ADDRESS  ImageBaseAddress,
  IN     UINT32                AddressOfEntryPoint,
  IN     UINT32                Offset
  )
/*++

Routine Description:

  This function abstracts Pe Map file information and add them into FvMap file for Debug.

Arguments:

  FvMapFile             A pointer to FvMap File
  FileName              Ffs File PathName
  ImageBaseAddress      PeImage Base Address.
  AddressOfEntryPoint   EntryPoint address relative to PeBase Address
  Offset                Offset between TeImage address and original PeImage.

Returns:

  EFI_SUCCESS           Added required map information.

--*/
{
  CHAR8           PeMapFileName [_MAX_PATH];
  CHAR8           *Cptr;
  CHAR8           *FileGuidName;
  EFI_GUID        FileGuidValue;
  FILE            *PeMapFile;
  CHAR8           Line [MAX_LINE_LEN];
  CHAR8           KeyWord [MAX_LINE_LEN];
  CHAR8                 FunctionName [MAX_LINE_LEN];
  EFI_PHYSICAL_ADDRESS  FunctionAddress;
  UINT32                FunctionType;
  CHAR8                 FunctionTypeName [MAX_LINE_LEN];
  
  //
  // Init local variable
  //
  FunctionType = 0;
  
  //
  // Construct Map file Name 
  //
  strcpy (PeMapFileName, FileName);
  Cptr = PeMapFileName + strlen (PeMapFileName);
  while (*Cptr != '.') {
    Cptr --;
  }
  if (*Cptr != '.') {
    return EFI_NOT_FOUND;
  } else {
    *(Cptr + 1) = 'm';
    *(Cptr + 2) = 'a';
    *(Cptr + 3) = 'p';
    *(Cptr + 4) = '\0';
  }
  //
  // Open PeMapFile
  //
  PeMapFile = fopen (PeMapFileName, "r");
  if (PeMapFile == NULL) {
    // fprintf (stdout, "can't open %s file to reading\n", PeMapFileName);
    return EFI_ABORTED;
  }
  //
  // Get Module Guid from FileName
  //
  *Cptr = '\0';
  while ((*Cptr != FILE_SEP_CHAR) && (Cptr >= PeMapFileName)) {
    Cptr --;
  }
  if (*Cptr == FILE_SEP_CHAR) {
    FileGuidName = Cptr + 1;
    if (StringToGuid (FileGuidName, &FileGuidValue) != EFI_SUCCESS) {
      FileGuidName = NULL;
    }
  }
  //
  // Output Functions information into Fv Map file
  //
  fgets (Line, MAX_LINE_LEN, PeMapFile);
  sscanf (Line, "%s", KeyWord);
  //
  // module information output
  //
  if (FileGuidName != NULL) {
    fprintf (FvMapFile, "%s (", KeyWord);
    fprintf (FvMapFile, "BaseAddress=%08lx, ", ImageBaseAddress + Offset);
    fprintf (FvMapFile, "EntryPoint=%08lx, ", ImageBaseAddress + AddressOfEntryPoint);
    fprintf (FvMapFile, "GUID=%s)\n\n", FileGuidName);
  } else {
    fprintf (FvMapFile, "%s (", KeyWord);
    fprintf (FvMapFile, "BaseAddress=%08lx, ", ImageBaseAddress + Offset);
    fprintf (FvMapFile, "EntryPoint=%08lx)", ImageBaseAddress + AddressOfEntryPoint);
  }

  while (fgets (Line, MAX_LINE_LEN, PeMapFile) != NULL) {
    //
    // Skip blank line
    //
    if (Line[0] == 0x0a) {
      FunctionType = 0;
      continue;
    }
    //
    // By Address and Static keyword
    //  
    if (FunctionType == 0) {
      sscanf (Line, "%s", KeyWord);
      if (stricmp (KeyWord, "Address") == 0) {
        //
        // function list
        //
        FunctionType = 1;
        fgets (Line, MAX_LINE_LEN, PeMapFile);
      } else if (stricmp (KeyWord, "Static") == 0) {
        //
        // static function list
        //
        FunctionType = 2;
        fgets (Line, MAX_LINE_LEN, PeMapFile);
      }
      continue;
    }
    //
    // Printf Function Information
    //
    if (FunctionType == 1) {
      sscanf (Line, "%s %s %lx %s", KeyWord, FunctionName, &FunctionAddress, FunctionTypeName);
      if (FunctionTypeName [1] == '\0' && (FunctionTypeName [0] == 'f' || FunctionTypeName [0] == 'F')) {
        fprintf (FvMapFile, "  %016lx F  ", ImageBaseAddress + FunctionAddress);
        fprintf (FvMapFile, "%s\n", FunctionName);
    } else {
        fprintf (FvMapFile, "  %016lx    ", ImageBaseAddress + FunctionAddress);
        fprintf (FvMapFile, "%s\n", FunctionName);
      }
    } else if (FunctionType == 2) {
      sscanf (Line, "%s %s %lx %s", KeyWord, FunctionName, &FunctionAddress, FunctionTypeName);
      if (FunctionTypeName [1] == '\0' && (FunctionTypeName [0] == 'f' || FunctionTypeName [0] == 'F')) {
        fprintf (FvMapFile, "  %016lx FS ", ImageBaseAddress + FunctionAddress);
        fprintf (FvMapFile, "%s\n", FunctionName);
      } else {
        fprintf (FvMapFile, "  %016lx    ", ImageBaseAddress + FunctionAddress);
        fprintf (FvMapFile, "%s\n", FunctionName);
      }
    }
  }
  //
  // Close PeMap file
  //
  fprintf (FvMapFile, "\n\n");
  fclose (PeMapFile);
  
  return EFI_SUCCESS;
}

EFI_STATUS
ParseCapInf (
  IN  MEMORY_FILE  *InfFile,
  OUT CAP_INFO     *CapInfo
  )
/*++

Routine Description:

  This function parses a Cap.INF file and copies info into a CAP_INFO structure.

Arguments:

  InfFile        Memory file image.
  CapInfo        Information read from INF file.

Returns:

  EFI_SUCCESS       INF file information successfully retrieved.
  EFI_ABORTED       INF file has an invalid format.
  EFI_NOT_FOUND     A required string was not found in the INF file.
--*/
{
  CHAR8       Value[_MAX_PATH];
  UINT64      Value64;
  UINTN       Index;
  EFI_STATUS  Status;

  //
  // Initialize Cap info
  //
  memset (CapInfo, 0, sizeof (CAP_INFO));

  //
  // Read the Capsule Guid
  //
  Status = FindToken (InfFile, OPTIONS_SECTION_STRING, EFI_CAPSULE_GUID_STRING, 0, Value);
  if (Status == EFI_SUCCESS) {
    //
    // Get the Capsule Guid
    //
    Status = StringToGuid (Value, &CapInfo->CapGuid);
    if (EFI_ERROR (Status)) {
      Error (NULL, 0, 2000, "Invalid parameter", "%s = %s", EFI_CAPSULE_GUID_STRING, Value);
      return EFI_ABORTED;
    }
    DebugMsg (NULL, 0, 9, "Capsule Guid", "%s = %s", EFI_CAPSULE_GUID_STRING, Value);
  } else {
    Error (NULL, 0, 2001, "Missing required argument", EFI_CAPSULE_GUID_STRING);
    return EFI_ABORTED;
  }

  //
  // Read the Capsule Header Size
  //
  Status = FindToken (InfFile, OPTIONS_SECTION_STRING, EFI_CAPSULE_HEADER_SIZE_STRING, 0, Value);
  if (Status == EFI_SUCCESS) {
    Status = AsciiStringToUint64 (Value, FALSE, &Value64);
    if (EFI_ERROR (Status)) {
      Error (NULL, 0, 2000, "Invalid parameter", "%s = %s", EFI_CAPSULE_HEADER_SIZE_STRING, Value);
      return EFI_ABORTED;
    }
    CapInfo->HeaderSize = (UINT32) Value64;
    DebugMsg (NULL, 0, 9, "Capsule Header size", "%s = %s", EFI_CAPSULE_HEADER_SIZE_STRING, Value);
  }

  //
  // Read the Capsule Flag
  //
  Status = FindToken (InfFile, OPTIONS_SECTION_STRING, EFI_CAPSULE_FLAGS_STRING, 0, Value);
  if (Status == EFI_SUCCESS) {
    if (strstr (Value, "PopulateSystemTable") != NULL) {
      CapInfo->Flags |= CAPSULE_FLAGS_PERSIST_ACROSS_RESET | CAPSULE_FLAGS_POPULATE_SYSTEM_TABLE;
    } else if (strstr (Value, "PersistAcrossReset") != NULL) {
      CapInfo->Flags |= CAPSULE_FLAGS_PERSIST_ACROSS_RESET; 
    } else {
      Error (NULL, 0, 2000, "Invalid parameter", "invalid Flag setting for %s.", EFI_CAPSULE_FLAGS_STRING);
      return EFI_ABORTED;
    }
    DebugMsg (NULL, 0, 9, "Capsule Flag", Value);
  }

  //
  // Read Capsule File name
  //
  Status = FindToken (InfFile, OPTIONS_SECTION_STRING, EFI_FILE_NAME_STRING, 0, Value);
  if (Status == EFI_SUCCESS) {
    //
    // Get output file name
    //
    strcpy (CapInfo->CapName, Value);
  }

  //
  // Read the Capsule FileImage
  //
  for (Index = 0; Index < MAX_NUMBER_OF_FILES_IN_CAP; Index++) {
    //
    // Read the capsule file name
    //
    Status = FindToken (InfFile, FILES_SECTION_STRING, EFI_FILE_NAME_STRING, Index, Value);

    if (Status == EFI_SUCCESS) {
      //
      // Add the file
      //
      strcpy (CapInfo->CapFiles[Index], Value);
      DebugMsg (NULL, 0, 9, "Capsule component file", "the %dth file name is %s", Index, CapInfo->CapFiles[Index]); 
    } else {
      break;
    }
  }
  
  if (Index == 0) {
    Warning (NULL, 0, 0, "Capsule components are not specified.", NULL);
  }

  return EFI_SUCCESS;
}

EFI_STATUS
GenerateCapImage (
  IN CHAR8                *InfFileImage,
  IN UINTN                InfFileSize,
  IN CHAR8                *CapFileName
  )
/*++

Routine Description:

  This is the main function which will be called from application to create UEFI Capsule image.

Arguments:

  InfFileImage   Buffer containing the INF file contents.
  InfFileSize    Size of the contents of the InfFileImage buffer.
  CapFileName    Requested name for the Cap file.

Returns:

  EFI_SUCCESS             Function completed successfully.
  EFI_OUT_OF_RESOURCES    Could not allocate required resources.
  EFI_ABORTED             Error encountered.
  EFI_INVALID_PARAMETER   A required parameter was NULL.

--*/
{
  UINT32                CapSize;
  UINT8                 *CapBuffer;
  EFI_CAPSULE_HEADER    *CapsuleHeader;
  MEMORY_FILE           InfMemoryFile;
  UINT32                FileSize;
  UINT32                Index;
  FILE                  *fpin, *fpout;
  EFI_STATUS            Status;
  CAP_INFO              CapInfo;

  //
  // Initialize file structures
  //
  InfMemoryFile.FileImage           = InfFileImage;
  InfMemoryFile.CurrentFilePointer  = InfFileImage;
  InfMemoryFile.Eof                 = InfFileImage + InfFileSize;

  //
  // Parse the Cap inf file for header information
  //
  Status = ParseCapInf (&InfMemoryFile, &CapInfo);
  if (Status != EFI_SUCCESS) {
    return Status;
  }
  
  if (CapInfo.HeaderSize == 0) {
    CapInfo.HeaderSize = sizeof (EFI_CAPSULE_HEADER);
  }

  if (CapInfo.HeaderSize < sizeof (EFI_CAPSULE_HEADER)) {
    Error (NULL, 0, 2000, "Invalid parameter", "The specified HeaderSize cannot be less than the size of EFI_CAPSULE_HEADER.");
    return EFI_INVALID_PARAMETER;
  }
  
  if (CapFileName == NULL && CapInfo.CapName[0] != '\0') {
    CapFileName = CapInfo.CapName;
  }
  
  if (CapFileName == NULL) {
    Error (NULL, 0, 2001, "Missing required argument", "Output Capsule file name");
    return EFI_INVALID_PARAMETER;
  }

  //
  // Calculate the size of capsule image.
  //
  Index    = 0;
  FileSize = 0;
  CapSize  = CapInfo.HeaderSize;
  while (CapInfo.CapFiles [Index][0] != '\0') {
    fpin = fopen (CapInfo.CapFiles[Index], "rb");
    if (fpin == NULL) {
      Error (NULL, 0, 0001, "Error opening file", CapInfo.CapFiles[Index]);
      return EFI_ABORTED;
    }
    FileSize  = _filelength (fileno (fpin));
    CapSize  += FileSize;
    fclose (fpin);
    Index ++;
  }

  //
  // Allocate buffer for capsule image.
  //
  CapBuffer = (UINT8 *) malloc (CapSize);
  if (CapBuffer == NULL) {
    Error (NULL, 0, 4001, "Resource", "memory cannot be allocated for creating the capsule.");
    return EFI_OUT_OF_RESOURCES;
  }

  //
  // Initialize the capsule header to zero
  //
  memset (CapBuffer, 0, CapInfo.HeaderSize);
  
  //
  // create capsule header and get capsule body
  //
  CapsuleHeader = (EFI_CAPSULE_HEADER *) CapBuffer;
  memcpy (&CapsuleHeader->CapsuleGuid, &CapInfo.CapGuid, sizeof (EFI_GUID));
  CapsuleHeader->HeaderSize       = CapInfo.HeaderSize;
  CapsuleHeader->Flags            = CapInfo.Flags;
  CapsuleHeader->CapsuleImageSize = CapSize;

  Index    = 0;
  FileSize = 0;
  CapSize  = CapsuleHeader->HeaderSize;
  while (CapInfo.CapFiles [Index][0] != '\0') {
    fpin = fopen (CapInfo.CapFiles[Index], "rb");
    if (fpin == NULL) {
      Error (NULL, 0, 0001, "Error opening file", CapInfo.CapFiles[Index]);
      free (CapBuffer);
      return EFI_ABORTED;
    }
    FileSize = _filelength (fileno (fpin));
    fread (CapBuffer + CapSize, 1, FileSize, fpin);
    fclose (fpin);
    Index ++;
    CapSize += FileSize;
  }
  
  //
  // write capsule data into the output file
  //
  fpout = fopen (CapFileName, "wb");
  if (fpout == NULL) {
    Error (NULL, 0, 0001, "Error opening file", CapFileName);
    free (CapBuffer);
    return EFI_ABORTED;
  }

  fwrite (CapBuffer, 1, CapSize, fpout);
  fclose (fpout);
  
  VerboseMsg ("The size of the generated capsule image is %d bytes", CapSize);

  return EFI_SUCCESS;
}
