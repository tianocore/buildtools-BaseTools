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

#include <Common/UefiBaseTypes.h>
#include "GenFvInternalLib.h"
#include "CommonLib.h"
#include "EfiUtilityMsgs.h"
#include "WinNtInclude.h"

EFI_STATUS
CalculateFvSize (
  FV_INFO *FvInfoPtr
  );
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

EFI_STATUS
FfsRebase ( 
  IN OUT  FV_INFO               *FvInfo, 
  IN      CHAR8                 *FileName,           
  IN OUT  EFI_FFS_FILE_HEADER   *FfsFile,
  IN      UINTN                 XipOffset
  );
/*++

Routine Description:

  This function determines if a file is XIP and should be rebased.  It will
  rebase any PE32 sections found in the file using the base address.

Arguments:
  
  FvInfo            A pointer to FV_INFO struture.
  FileName          Ffs file Name
  FfsFile           A pointer to Ffs file image.
  XipOffset         The offset address to use for rebasing the XIP file image.

Returns:

  EFI_SUCCESS             The image was properly rebased.
  EFI_INVALID_PARAMETER   An input parameter is invalid.
  EFI_ABORTED             An error occurred while rebasing the input file image.
  EFI_OUT_OF_RESOURCES    Could not allocate a required resource.
  EFI_NOT_FOUND           No compressed sections could be found.

--*/

static UINT32 MaxFfsAlignment = 0;

EFI_GUID  gEfiFirmwareFileSystem2Guid = EFI_FIRMWARE_FILE_SYSTEM2_GUID;
EFI_GUID  gEfiFirmwareVolumeTopFileGuid = EFI_FFS_VOLUME_TOP_FILE_GUID;

CHAR8      *FvbAttributeName[] = {
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

CHAR8      *FvbAlignmentName[] = {
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
  FvInfo->BaseAddress = -1;

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
      Error (NULL, 0, 0, EFI_FV_BASE_ADDRESS_STRING, "invalid value");
      return EFI_ABORTED;
    }

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
      memcpy (&FvInfo->FvGuid, &gEfiFirmwareFileSystem2Guid, sizeof (EFI_GUID));
    }
  } else {
    memcpy (&FvInfo->FvGuid, &gEfiFirmwareFileSystem2Guid, sizeof (EFI_GUID));
  }

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
  for (Index = 0; Index < sizeof (FvbAttributeName)/sizeof (char *); Index ++) {
    if ((FvbAttributeName [Index] != NULL) && \
        (FindToken (InfFile, ATTRIBUTES_SECTION_STRING, FvbAttributeName [Index], 0, Value) == EFI_SUCCESS)) {
      if ((strcmp (Value, TRUE_STRING) == 0) || (strcmp (Value, ONE_STRING) == 0)) {
        FvInfo->FvAttributes |= 1 << Index;
      } else if ((strcmp (Value, FALSE_STRING) != 0) && (strcmp (Value, ZERO_STRING) != 0)) {
        Error (NULL, 0, 0, FvbAttributeName [Index], "expected %s | %s", TRUE_STRING, FALSE_STRING);
        return EFI_ABORTED;
      }
    }
  }

  //
  // Read Fv Alignment
  //
  for (Index = 0; Index < sizeof (FvbAlignmentName)/sizeof (char *); Index ++) {
    if (FindToken (InfFile, ATTRIBUTES_SECTION_STRING, FvbAlignmentName [Index], 0, Value) == EFI_SUCCESS) {
      if (strcmp (Value, TRUE_STRING) == 0) {
        FvInfo->FvAttributes |= Index << 16;
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
        Error (NULL, 0, 0, Value, "invalid value for %s", EFI_BLOCK_SIZE_STRING);
        return EFI_ABORTED;
      }

      FvInfo->FvBlocks[Index].Length = (UINT32) Value64;
    } else {
      //
      // If there is no blocks size, but there is the number of block, then we have a mismatched pair
      // and should return an error.
      //
      Status = FindToken (InfFile, OPTIONS_SECTION_STRING, EFI_NUM_BLOCKS_STRING, Index, Value);
      if (!EFI_ERROR (Status)) {
        Error (NULL, 0, 0, "must specify both", "%s and %s", EFI_NUM_BLOCKS_STRING, EFI_BLOCK_SIZE_STRING);
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
        Error (NULL, 0, 0, Value, "invalid value specified for %s", EFI_NUM_BLOCKS_STRING);
        return EFI_ABORTED;
      }

      FvInfo->FvBlocks[Index].NumBlocks = (UINT32) Value64;
    }
  }

  if (Index == 0) {
    Error (NULL, 0, 0, NULL, "at lease one block size must be specified.");
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
    } else {
      break;
    }
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
    Error (NULL, 0, 0, "nvalid file attribute calculated, this is most likely a utility error", NULL);
    return EFI_ABORTED;
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
  EFI_GUID            PadFileGuid;
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

#ifdef __GNUC__
  {
    uuid_t tmp_id;
    uuid_generate (tmp_id);
    memcpy (&PadFileGuid, tmp_id, sizeof (EFI_GUID));
  }
#else
  UuidCreate (&PadFileGuid);
#endif
  memset (PadFile, 0, sizeof (EFI_FFS_FILE_HEADER));
  memcpy (&PadFile->Name, &PadFileGuid, sizeof (EFI_GUID));
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
  if (!memcmp (&FileBuffer->Name, &gEfiFirmwareVolumeTopFileGuid, sizeof (EFI_GUID))) {
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
  IN OUT EFI_FFS_FILE_HEADER  **VtfFileImage  
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
    Error (NULL, 0, 0, FvInfo->FvFiles[Index], "failed to open file for reading");
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
    Error (NULL, 0, 0, "memory allocation failure", NULL);
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
    free (FileBuffer);
    Error (NULL, 0, 0, FvInfo->FvFiles[Index], "failed to read input file contents");
    return EFI_ABORTED;
  }
  
  //
  // Verify Ffs file
  //
  Status = VerifyFfsFile (FileBuffer);
  if (EFI_ERROR (Status)) {
    Error (NULL, 0, 0, FvInfo->FvFiles[Index], "the invalid FFS file");
    free (FileBuffer);
    return EFI_INVALID_PARAMETER;
  }

  //
  // Verify space exists to add the file
  //
  if (FileSize > (UINTN) ((UINTN) *VtfFileImage - (UINTN) FvImage->CurrentFilePointer)) {
    Error (NULL, 0, 0, FvInfo->FvFiles[Index], "insufficient space remains to add the file");
    free (FileBuffer);
    return EFI_OUT_OF_RESOURCES;
  }

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
        Error (NULL, 0, 0, NULL, "VTF file does not align on %d-byte boundary", 1 << CurrentFileAlignment);
        free (FileBuffer);
        return EFI_ABORTED;
      }
      //
      // Rebase the PE or TE image in FileBuffer of FFS file for XIP 
      // Rebase for the debug genfvmap tool
      //
      FfsRebase (FvInfo, FvInfo->FvFiles[Index], (EFI_FFS_FILE_HEADER *) FileBuffer, (UINTN) *VtfFileImage - (UINTN) FvImage->FileImage);
      //
      // copy VTF File
      //
      memcpy (*VtfFileImage, FileBuffer, FileSize);
      free (FileBuffer);
      return EFI_SUCCESS;
    } else {
      //
      // Already found a VTF file.
      //
      Error (NULL, 0, 0, "multiple VTF files are illegal in a single FV", NULL);
      free (FileBuffer);
      return EFI_ABORTED;
    }
  }

  //
  // Add pad file if necessary
  //
  Status = AddPadFile (FvImage, 1 << CurrentFileAlignment);
  if (EFI_ERROR (Status)) {
    Error (NULL, 0, 0, NULL, "ERROR: Could not align the file data properly.");
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
    FfsRebase (FvInfo, FvInfo->FvFiles[Index], (EFI_FFS_FILE_HEADER *) FileBuffer, (UINTN) FvImage->CurrentFilePointer - (UINTN) FvImage->FileImage);
    //
    // Copy the file
    //
    memcpy (FvImage->CurrentFilePointer, FileBuffer, FileSize);
    FvImage->CurrentFilePointer += FileSize;
  } else {
    Error (NULL, 0, 0, NULL, "ERROR: The firmware volume is out of space, could not add file %s.\n", FvInfo->FvFiles[Index]);
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
  EFI_GUID            PadFileGuid;

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
  // write header
  //
  memset (PadFile, 0, sizeof (EFI_FFS_FILE_HEADER));
#ifdef __GNUC__
  {
    uuid_t tmp_id;
    uuid_generate (tmp_id);
    memcpy (&PadFileGuid, tmp_id, sizeof (EFI_GUID));
  }
#else
  UuidCreate (&PadFileGuid);
#endif
  memcpy (&PadFile->Name, &PadFileGuid, sizeof (EFI_GUID));
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
  UINT32                    *Ia32ResetAddressPtr;
  UINT8                     *BytePointer;
  UINT8                     *BytePointer2;
  UINT16                    *WordPointer;
  UINT16                    CheckSum;
  UINTN                     Index;
  EFI_FFS_FILE_STATE        SavedState;
  UINT64                    FitAddress;
  FIT_TABLE                 *FitTablePtr;

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
  // Find the PEI Core
  //
  Status = GetFileByType (EFI_FV_FILETYPE_PEI_CORE, 1, &PeiCoreFile);
  if (EFI_ERROR (Status) || PeiCoreFile == NULL) {
    Error (NULL, 0, 0, "could not find the PEI core in the FV", NULL);
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
    Error (NULL, 0, 0, "could not find PE32 or TE section in PEI core file", NULL);
    return EFI_ABORTED;
  }

  Status = GetPe32Info (
            (VOID *) ((UINTN) Pe32Section.Pe32Section + sizeof (EFI_SECTION_PE32)),
            &EntryPoint,
            &BaseOfCode,
            &MachineType
            );

  if (EFI_ERROR (Status)) {
    Error (NULL, 0, 0, "could not get PE32 entry point for PEI core", NULL);
    return EFI_ABORTED;
  }
  //
  // Physical address is FV base + offset of PE32 + offset of the entry point
  //
  PeiCorePhysicalAddress = FvInfo->BaseAddress;
  PeiCorePhysicalAddress += (UINTN) Pe32Section.Pe32Section + sizeof (EFI_SECTION_PE32) - (UINTN) FvImage->FileImage;
  PeiCorePhysicalAddress += EntryPoint;

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
      Error (NULL, 0, 0, NULL,
        "ERROR: PEI_CORE entry point is not aligned on a 16 byte boundary, address specified is %Xh.",
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
    // Find the Sec Core
    //
    Status = GetFileByType (EFI_FV_FILETYPE_SECURITY_CORE, 1, &SecCoreFile);
    if (EFI_ERROR (Status) || SecCoreFile == NULL) {
      Error (NULL, 0, 0, "could not find the Sec core in the FV", NULL);
      return EFI_ABORTED;
    }
    //
    // Sec Core found, now find PE32 section
    //
    Status = GetSectionByType (SecCoreFile, EFI_SECTION_PE32, 1, &Pe32Section);
    if (EFI_ERROR (Status)) {
      Error (NULL, 0, 0, "could not find PE32 section in SEC core file", NULL);
      return EFI_ABORTED;
    }

    Status = GetPe32Info (
              (VOID *) ((UINTN) Pe32Section.Pe32Section + sizeof (EFI_SECTION_PE32)),
              &EntryPoint,
              &BaseOfCode,
              &MachineType
              );
    if (EFI_ERROR (Status)) {
      Error (NULL, 0, 0, "could not get PE32 entry point for SEC core", NULL);
      return EFI_ABORTED;
    }
    //
    // Physical address is FV base + offset of PE32 + offset of the entry point
    //
    SecCorePhysicalAddress = FvInfo->BaseAddress;
    SecCorePhysicalAddress += (UINTN) Pe32Section.Pe32Section + sizeof (EFI_SECTION_PE32) - (UINTN) FvImage->FileImage;
    SecCorePhysicalAddress += EntryPoint;

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
      Error (NULL, 0, 0, NULL, 
        "ERROR: SALE_ENTRY entry point is not aligned on a 16 byte boundary, address specified is %Xh.",
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
    Ia32ResetAddressPtr = (UINT32 *) ((UINTN) FvImage->Eof - IA32_PEI_CORE_ENTRY_OFFSET);

    //
    // Write lower 32 bits of physical address
    //
    *Ia32ResetAddressPtr = (UINT32) PeiCorePhysicalAddress;

    //
    // Update the BFV base address
    //
    Ia32ResetAddressPtr   = (UINT32 *) ((UINTN) FvImage->Eof - 4);
    *Ia32ResetAddressPtr  = (UINT32) (FvInfo->BaseAddress);

    CheckSum              = 0x0000;

    //
    // Update the Startup AP in the FVH header block ZeroVector region.
    //
    BytePointer   = (UINT8 *) ((UINTN) FvImage->FileImage);
    BytePointer2  = (FvInfo->Size == 0x10000) ? m64kRecoveryStartupApDataArray : m128kRecoveryStartupApDataArray;
    for (Index = 0; Index < SIZEOF_STARTUP_DATA_ARRAY; Index++) {
      *BytePointer++ = *BytePointer2++;
    }
    //
    // Calculate the checksum
    //
    WordPointer = (UINT16 *) ((UINTN) FvImage->FileImage);
    for (Index = 0; Index < SIZEOF_STARTUP_DATA_ARRAY / 2; Index++) {
      CheckSum = (UINT16) (CheckSum + ((UINT16) *WordPointer));
      WordPointer++;
    }
    //
    // Update the checksum field
    //
    BytePointer = (UINT8 *) ((UINTN) FvImage->FileImage);
    BytePointer += (SIZEOF_STARTUP_DATA_ARRAY - 2);
    WordPointer   = (UINT16 *) BytePointer;
    *WordPointer  = (UINT16) (0x10000 - (UINT32) CheckSum);
  } else {
    Error (NULL, 0, 0, "invalid machine type in PEI core", "machine type=0x%X", (UINT32) MachineType);
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
      Error (NULL, 0, 0, NULL, "ERROR: Unknown magic number in the DOS header, 0x%04X.", DosHeader->e_magic);
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
      Error (NULL, 0, 0, NULL, "ERROR: Unrecognized image signature 0x%08X.", NtHeader->Signature);
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
    Error (NULL, 0, 0, NULL, "ERROR: Unrecognized machine type in the PE32 file.");
    return EFI_UNSUPPORTED;
  }

  return EFI_SUCCESS;
}
//
// Exposed function implementations (prototypes are defined in GenFvImageLib.h)
//
EFI_STATUS
GenerateFvImage (
  IN CHAR8                *InfFileImage,
  IN UINTN                InfFileSize,
  IN CHAR8                *FvFileName,
  IN EFI_PHYSICAL_ADDRESS XipBaseAddress
  )
/*++

Routine Description:

  This is the main function which will be called from application.

Arguments:

  InfFileImage   Buffer containing the INF file contents.
  InfFileSize    Size of the contents of the InfFileImage buffer.
  FvFileName     Requested name for the FV file.
  XipBaseAddress BaseAddress is to be rebased.

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

  FvBufferHeader = NULL;
  FvFile         = NULL;
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
    Error (NULL, 0, 0, NULL, "ERROR: Could not parse the input INF file.");
    return Status;
  }

  //
  // Update the file name return values
  //
  if (FvFileName == NULL && FvInfo.FvName[0] != '\0') {
    FvFileName = FvInfo.FvName;
  }
  
  //
  // Update FvImage Base Address, XipBase not same to BtBase, RtBase address.
  //
  if (XipBaseAddress != -1) {
    FvInfo.BaseAddress = XipBaseAddress;
  }

  //
  // Calculate the FV size and Update Fv Size based on the actual FFS files.
  // And Update FvInfo data.
  //
  Status = CalculateFvSize (&FvInfo);
  if (EFI_ERROR (Status)) {
    return Status;    
  }
  
  //
  // support fv image and empty fv image
  //
  FvImageSize = FvInfo.Size;

  //
  // Allocate the FV, assure FvImage Header 8 byte alignment
  //
  FvBufferHeader = malloc (FvImageSize + 8);
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
  FvHeader->Revision        = EFI_FVH_PI_REVISION;
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
    Status = AddFile (&FvImageMemoryFile, &FvInfo, Index, &VtfFileImage);

    //
    // Exit if error detected while adding the file
    //
    if (EFI_ERROR (Status)) {
      Error (NULL, 0, 0, NULL, "ERROR: Could not add file %s.", FvInfo.FvFiles[Index]);
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
      Error (NULL, 0, 0, NULL, "ERROR: Could not create the pad file between the last file and the VTF file.");
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
        Error (NULL, 0, 0, NULL, "ERROR: Could not update the reset vector.");
        goto Finish;                                              
      }
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
  if (FvFileName == NULL) {
    FvFile = stdout;
  } else {
    FvFile = fopen (FvFileName, "wb");
  }

  if (FvFile == NULL) {
    Error (NULL, 0, 0, FvFileName, "could not open output file");
    Status = EFI_ABORTED;
    goto Finish;
  }

  if (fwrite (FvImage, 1, FvImageSize, FvFile) != FvImageSize) {
    Error (NULL, 0, 0, FvFileName, "failed to write to output file");
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
      Error (NULL, 0, 0, NULL, "%s could not open for reading", FvInfoPtr->FvFiles[Index]);
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
  IN      UINTN                 XipOffset
  )
/*++

Routine Description:

  This function determines if a file is XIP and should be rebased.  It will
  rebase any PE32 sections found in the file using the base address.

Arguments:
  
  FvInfo            A pointer to FV_INFO struture.
  FfsFile           A pointer to Ffs file image.
  XipOffset         The offset address to use for rebasing the XIP file image.

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

  Index              = 0;  
  MemoryImagePointer = NULL;
  BaseToUpdate       = NULL;
  TEImageHeader      = NULL;
  PeHdr              = NULL;
  Optional32         = NULL;
  Optional64         = NULL;
  MemoryImagePointer = NULL;
  SectionHeader      = NULL;
  //
  // Check XipAddress, BootAddress and RuntimeAddress
  //
  Flags = 0;

  if (FvInfo->BaseAddress != -1) {
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
      Error (NULL, 0, 0, "GetImageInfo() call failed on rebase", FileName);
      return Status;
    }

    //
    // Don't Load PeImage, only to relocate current image.
    //
    ImageContext.ImageAddress = (UINTN) CurrentPe32Section.Pe32Section + sizeof (EFI_PE32_SECTION);

    //
    // Get PeHeader pointer
    //
    PeHdr = (EFI_IMAGE_NT_HEADERS *)((UINTN)ImageContext.ImageAddress + ImageContext.PeCoffHeaderOffset);

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
          Warning (NULL, 0, 0, "Section-Alignment and File-Alignment does not match", FileName);
          return EFI_ABORTED;
        }

        NewPe32BaseAddress =
          XipBase + (UINTN)ImageContext.ImageAddress - (UINTN)FfsFile;
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
      Error (NULL, 0, 0, "Can't allocate enough memory on rebase", FileName);
      return EFI_OUT_OF_RESOURCES;
    }
    memset ((VOID *) MemoryImagePointer, 0, (UINTN) ImageContext.ImageSize + ImageContext.SectionAlignment);
    ImageContext.ImageAddress = ((UINTN) MemoryImagePointer + ImageContext.SectionAlignment - 1) & (~(ImageContext.SectionAlignment - 1));
    
    Status =  PeCoffLoaderLoadImage (&ImageContext);
    if (EFI_ERROR (Status)) {
      Error (NULL, 0, 0, "LocateImage() call failed on rebase", FileName);
      free ((VOID *) MemoryImagePointer);
      return Status;
    }
         
    ImageContext.DestinationAddress = NewPe32BaseAddress;
    Status                          = PeCoffLoaderRelocateImage (&ImageContext);
    if (EFI_ERROR (Status)) {
      Error (NULL, 0, 0, "RelocateImage() call failed on rebase", FileName);
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
      Error (
        NULL,
        0,
        0,
        "unknown machine type in PE32 image",
        "machine type=0x%X, file=%s",
        (UINT32) PeHdr->FileHeader.Machine,
        FileName
        );
      free ((VOID *) MemoryImagePointer);
      return EFI_ABORTED;
    }

    SectionHeader = (EFI_IMAGE_SECTION_HEADER *) (
                       (UINTN) ImageContext.ImageAddress +
                       ImageContext.PeCoffHeaderOffset +
                       sizeof (UINT32) + 
                       sizeof (EFI_IMAGE_FILE_HEADER) +  
                       PeHdr->FileHeader.SizeOfOptionalHeader
                       );
    
    for (Index = 0; Index < PeHdr->FileHeader.NumberOfSections; Index ++, SectionHeader ++) {
      CopyMem (
        (UINT8 *) ImageContext.Handle + SectionHeader->PointerToRawData, 
        (VOID*) (UINTN) (ImageContext.ImageAddress + SectionHeader->VirtualAddress), 
        SectionHeader->SizeOfRawData
        );
    }

    free ((VOID *) MemoryImagePointer);

    //
    // Update BASE address
    //
    *BaseToUpdate += EFI_SIZE_TO_PAGES (ImageContext.ImageSize) * EFI_PAGE_SIZE;

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
      Error (NULL, 0, 0, "GetImageInfo() call failed on rebase of TE image", FileName);
      return Status;
    }
    //
    // Don't reload TeImage
    //
    ImageContext.ImageAddress = (UINTN) TEImageHeader;

    //
    // Reloacate TeImage
    // 
    ImageContext.DestinationAddress = XipBase + (UINTN) TEImageHeader + sizeof (EFI_TE_IMAGE_HEADER) \
                                      - TEImageHeader->StrippedSize - (UINTN) FfsFile;
    Status                          = PeCoffLoaderRelocateImage (&ImageContext);
    if (EFI_ERROR (Status)) {
      Error (NULL, 0, 0, "RelocateImage() call failed on rebase of TE image", FileName);
      return Status;
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
  }
 
  return EFI_SUCCESS;
}