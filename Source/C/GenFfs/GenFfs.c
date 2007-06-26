/*++

Copyright (c) 2004-2007, Intel Corporation                                                         
All rights reserved. This program and the accompanying materials                          
are licensed and made available under the terms and conditions of the BSD License         
which accompanies this distribution.  The full text of the license may be found at        
http://opensource.org/licenses/bsd-license.php                                            
                                                                                          
THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,                     
WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.             

Module Name:

  GenFfs.c

Abstract:

  This file contains functions required to generate a Firmware File System
  file.

--*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <Common/UefiBaseTypes.h>
#include <Common/FirmwareVolumeImageFormat.h>
#include <Common/PiFirmwareFileSystem.h>

#include "CommonLib.h"
#include "EfiUtilityMsgs.h"

#define UTILITY_NAME            "GenFfs"
#define UTILITY_MAJOR_VERSION   1
#define UTILITY_MINOR_VERSION   0

#define MAXIMUM_INPUT_FILE_NUM 10

static CHAR8 *mFfsFileType[] = {
  NULL,                                   // 0x00
  "EFI_FV_FILETYPE_RAW",                  // 0x01
  "EFI_FV_FILETYPE_FREEFORM",             // 0x02
  "EFI_FV_FILETYPE_SECURITY_CORE",        // 0x03
  "EFI_FV_FILETYPE_PEI_CORE",             // 0x04
  "EFI_FV_FILETYPE_DXE_CORE",             // 0x05
  "EFI_FV_FILETYPE_PEIM",                 // 0x06
  "EFI_FV_FILETYPE_DRIVER",               // 0x07
  "EFI_FV_FILETYPE_COMBINED_PEIM_DRIVER", // 0x08
  "EFI_FV_FILETYPE_APPLICATION",          // 0x09
  NULL,                                   // 0x0A - reserved
  "EFI_FV_FILETYPE_FIRMWARE_VOLUME_IMAGE" // 0x0B
 };

static CHAR8 *mAlignName[] = {
  "1", "2", "4", "8", "16", "32", "64", "128", "256", "512",
  "1K", "2K", "4K", "8K", "16K", "32K", "64K"
 };

static CHAR8 *mFfsValidAlignName[] = {
  "8", "16", "128", "512", "1K", "4K", "32K", "64K"
 };

static UINT32 mFfsValidAlign[] = {0, 8, 16, 128, 512, 1024, 4096, 32768, 65536};

static EFI_GUID mZeroGuid = {0};

static
void 
Version(
  void
  )
/*++

Routine Description:

  Print out version information for this utility.

Arguments:

  None
  
Returns:

  None
  
--*/ 
{
  printf ("%s v%d.%d - EDKII utility to generate a Firmware File System files.\n", UTILITY_NAME, UTILITY_MAJOR_VERSION, UTILITY_MINOR_VERSION);
  printf ("Copyright (c) 2007 Intel Corporation. All rights reserved.\n");
}

static
void
Usage (
  void
  )
/*++

Routine Description:

  Print Error / Help message.

Arguments:

  void

Returns:

  None

--*/
{
  Version();
  
  printf ("\nUsage: " UTILITY_NAME "\n\
        -o, --outputfile [FileName]\n\
        -t, --filetype <EFI_FV_FILETYPE_RAW|\n\
                        EFI_FV_FILETYPE_FREEFORM|\n\
                        EFI_FV_FILETYPE_SECURITY_CORE|\n\
                        EFI_FV_FILETYPE_PEI_CORE|\n\
                        EFI_FV_FILETYPE_DXE_CORE|\n\
                        EFI_FV_FILETYPE_PEIM|\n\
                        EFI_FV_FILETYPE_DRIVER|\n\
                        EFI_FV_FILETYPE_COMBINED_PEIM_DRIVER|\n\
                        EFI_FV_FILETYPE_APPLICATION|\n\
                        EFI_FV_FILETYPE_FIRMWARE_VOLUME_IMAGE>|\n\
        -g, --fileguid [GuidValue (########-####-####-####-############)]\n\
        -x, --fixed\n\
        -s, --checksum\n\
        -a, --align <8,16,128,512,1K,4K,32K,64K>\n\
        -i, --sectionfile [FileName] [-n, --sectionalign <1~64K>]\n\
        -h, --help\n\
        -V, --version\n");
}

static
EFI_STATUS
StringtoAlignment (
  IN  CHAR8  *AlignBuffer,
  OUT UINT32 *AlignNumber
  )
{
  UINT32 Index = 0;
  for (Index = 0; Index < sizeof (mAlignName) / sizeof (CHAR8 *); Index ++) {
    if (stricmp (AlignBuffer, mAlignName [Index]) == 0) {
      *AlignNumber = Index;
      return EFI_SUCCESS;
    }
  }
  return EFI_INVALID_PARAMETER;
}

static
UINT8
StringToType (
  IN CHAR8 *String
  )
/*++

Routine Description:

  Converts File Type String to value.  EFI_FV_FILETYPE_ALL indicates that an
  unrecognized file type was specified.

Arguments:

  String    - File type string

Returns:

  File Type Value

--*/
{
  UINT8 Index = 0;
  
  if (String == NULL) {
    return EFI_FV_FILETYPE_ALL;
  }

  for (Index = 0; Index < sizeof (mFfsFileType) / sizeof (CHAR8 *); Index ++) {
    if (mFfsFileType [Index] != NULL && (stricmp (String, mFfsFileType [Index]) == 0)) {
      return Index;
    }
  }
  return EFI_FV_FILETYPE_ALL;
}

static
EFI_STATUS
GetSectionContents (
  IN  CHAR8   **InputFileName,
  IN  UINT32  *InputFileAlign,
  IN  UINT32  InputFileNum,
  OUT UINT8   *FileBuffer,
  OUT UINT32  *BufferLength,
  OUT UINT32  *MaxAlignment
  )
/*++
        
Routine Description:
           
  Get the contents of all section files specified in InputFileName
  into FileBuffer.
            
Arguments:
               
  InputFileName  - Name of the input file.
                
  InputFileAlign - Alignment required by the input file data.

  InputFileNum   - Number of input files. Should be at least 1.

  FileBuffer     - Output buffer to contain data

  BufferLength   - On input, this is size of the FileBuffer. 
                   On output, this is the actual length of the data.

  MaxAlignment   - The max alignment required by all the input file datas.

Returns:
                       
  EFI_SUCCESS on successful return
  EFI_INVALID_PARAMETER if InputFileNum is less than 1 or BufferLength point is NULL.
  EFI_ABORTED if unable to open input file.
  EFI_BUFFER_TOO_SMALL FileBuffer is not enough to contain all file data.
--*/
{
  UINT32                     Size;
  UINT32                     Offset;
  UINT32                     FileSize;
  UINT32                     Index;
  FILE                       *InFile;
  EFI_COMMON_SECTION_HEADER  *SectHeader;

  Size          = 0;
  Offset        = 0;
  *MaxAlignment = 0;
  //
  // Go through our array of file names and copy their contents
  // to the output buffer.
  //
  for (Index = 0; Index < InputFileNum; Index++) {
    //
    // make sure section ends on a DWORD boundary
    //
    while ((Size & 0x03) != 0) {
      Size++;
    }
    
    //
    // Get the Max alignment of all input file datas
    //
    if (*MaxAlignment < (1 << InputFileAlign [Index])) {
      *MaxAlignment = 1 << InputFileAlign [Index];
    }
    
    //
    // make sure section data meet its alignment requirement by adding one raw pad section.
    // But the different sections have the different section header. Necessary or not?
    // Based on section type to adjust offset? Todo
    //
    if (((Size + sizeof (EFI_COMMON_SECTION_HEADER)) % (1 << InputFileAlign [Index])) != 0) {
      Offset = ((Size + 2 * sizeof (EFI_COMMON_SECTION_HEADER) + (1 << InputFileAlign [Index]) - 1) & ~((1 << InputFileAlign [Index]) - 1)) - Size;
      Offset = Offset - sizeof (EFI_COMMON_SECTION_HEADER);
       
      if (FileBuffer != NULL && ((Size + Offset) < *BufferLength)) {
        SectHeader          = (EFI_COMMON_SECTION_HEADER *) FileBuffer;
        SectHeader->Type    = EFI_SECTION_RAW;
        SectHeader->Size[0] = (UINT8) (Offset & 0xff);
        SectHeader->Size[1] = (UINT8) ((Offset & 0xff00) >> 8);
        SectHeader->Size[2] = (UINT8) ((Offset & 0xff0000) >> 16);
      }

      Size = Size + Offset;
    }
    
    // 
    // Open file and read contents
    //
    InFile = fopen (InputFileName[Index], "rb");
    if (InFile == NULL) {
      Error (NULL, 0, 0, InputFileName[Index], "failed to open input file");
      return EFI_ABORTED;
    }

    fseek (InFile, 0, SEEK_END);
    FileSize = ftell (InFile);
    fseek (InFile, 0, SEEK_SET);
    //
    // Now read the contents of the file into the buffer
    // Buffer must be enough to contain the file content.
    //
    if (FileSize > 0 && FileBuffer != NULL && (Size + FileSize) <= *BufferLength) {
      if (fread (FileBuffer + Size, (size_t) FileSize, 1, InFile) != 1) {
        Error (NULL, 0, 0, InputFileName[Index], "failed to read contents of input file");
        fclose (InFile);
        return EFI_ABORTED;
      }
    }

    fclose (InFile);
    Size += FileSize;
  }
  
  if (Size > *BufferLength) {
    *BufferLength = Size;
    return EFI_BUFFER_TOO_SMALL;
  } else {
    *BufferLength = Size;
    return EFI_SUCCESS;
  }
}

int
main (
  INT32 argc,
  CHAR8 *argv[]
  )
/*++

Routine Description:

  Main function.

Arguments:

  argc - Number of command line parameters.
  argv - Array of pointers to parameter strings.

Returns:
  STATUS_SUCCESS - Utility exits successfully.
  STATUS_ERROR   - Some error occurred during execution.

--*/
{
  EFI_STATUS              Status;
  EFI_FFS_FILE_ATTRIBUTES FfsAttrib;
  UINT32                  FfsAlign;
  EFI_FV_FILETYPE         FfsFiletype;
  CHAR8                   *OutputFileName;
  EFI_GUID                FileGuid = {0};
  UINT32                  InputFileNum;
  UINT32                  *InputFileAlign;
  CHAR8                   **InputFileName;
  UINT8                   *FileBuffer;
  UINT32                  FileSize;
  UINT32                  MaxAlignment;
  EFI_FFS_FILE_HEADER     FfsFileHeader;
  FILE                    *FfsFile;
  UINT32                  Index;

  Index          = 0;
  FfsAttrib      = 0;  
  FfsAlign       = 0;
  FfsFiletype    = EFI_FV_FILETYPE_ALL;
  OutputFileName = NULL;
  InputFileNum   = 0;
  InputFileName  = NULL;
  InputFileAlign = NULL;
  FileBuffer     = NULL;
  FileSize       = 0;
  MaxAlignment   = 1;
  FfsFile        = NULL;
  Status         = EFI_SUCCESS;
  
  SetUtilityName (UTILITY_NAME);

  if (argc == 1) {
    Usage ();
    return STATUS_ERROR;
  }

  //
  // Parse command line
  //
  argc --;
  argv ++;

  if ((stricmp (argv[0], "-h") == 0) || (stricmp (argv[0], "--help") == 0)) {
    Usage();
    return STATUS_SUCCESS;    
  }

  if ((stricmp (argv[0], "-v") == 0) || (stricmp (argv[0], "--version") == 0)) {
    Version();
    return STATUS_SUCCESS;    
  }

  while (argc > 0) {
    if ((stricmp (argv[0], "-t") == 0) || (stricmp (argv[0], "--filetype") == 0)) {
      FfsFiletype = StringToType (argv[1]);
      argc -= 2;
      argv += 2;
      continue; 
    }

    if ((stricmp (argv[0], "-o") == 0) || (stricmp (argv[0], "--outputfile") == 0)) {
      OutputFileName = argv[1];
      argc -= 2;
      argv += 2;
      continue; 
    }

    if ((stricmp (argv[0], "-g") == 0) || (stricmp (argv[0], "--fileguid") == 0)) {
      Status = StringToGuid (argv[1], &FileGuid);
      if (EFI_ERROR (Status)) {
        Error (NULL, 0, 0, NULL, "ERROR: %s is not correct guid format", argv[1]);
        goto Finish;
      }
      argc -= 2;
      argv += 2;
      continue;
    }

    if ((stricmp (argv[0], "-x") == 0) || (stricmp (argv[0], "--fixed") == 0)) {
      FfsAttrib |= FFS_ATTRIB_FIXED;
      argc -= 1;
      argv += 1;
      continue;
    }

    if ((stricmp (argv[0], "-s") == 0) || (stricmp (argv[0], "--checksum") == 0)) {
      FfsAttrib |= FFS_ATTRIB_CHECKSUM;
      argc -= 1;
      argv += 1;
      continue;
    }

    if ((stricmp (argv[0], "-a") == 0) || (stricmp (argv[0], "--align") == 0)) {
      for (Index = 0; Index < sizeof (mFfsValidAlignName) / sizeof (CHAR8 *); Index ++) {
        if (stricmp (argv[1], mFfsValidAlignName[Index]) == 0) {
          break;
        }
      }
      if (Index == sizeof (mFfsValidAlignName) / sizeof (CHAR8 *)) {
        Error (NULL, 0, 0, NULL, "ERROR: %s is one invalid ffs file alignment", argv[1]);
        goto Finish;
      }
      FfsAlign = Index;
      argc -= 2;
      argv += 2;
      continue;
    }

    if ((stricmp (argv[0], "-i") == 0) || (stricmp (argv[0], "--sectionfile") == 0)) {
      //
      // Get Input file name and its alignment
      //
      
      //
      // Allocate Input file name buffer and its alignment buffer.
      //
      if ((InputFileNum == 0) && (InputFileName == NULL)) {
        InputFileName = (CHAR8 **) malloc (MAXIMUM_INPUT_FILE_NUM * sizeof (CHAR8 *));
        if (InputFileName == NULL) {
          Error (__FILE__, __LINE__, 0, "application error", "failed to allocate memory");
          return EFI_OUT_OF_RESOURCES;
        }
        memset (InputFileName, 0, (MAXIMUM_INPUT_FILE_NUM * sizeof (CHAR8 *)));
        
        InputFileAlign = (UINT32 *) malloc (MAXIMUM_INPUT_FILE_NUM * sizeof (UINT32));
        if (InputFileAlign == NULL) {
          Error (__FILE__, __LINE__, 0, "application error", "failed to allocate memory");
          free (InputFileName);
          return EFI_OUT_OF_RESOURCES;
        }
        memset (InputFileAlign, 0, MAXIMUM_INPUT_FILE_NUM * sizeof (UINT32));
      } else if (InputFileNum % MAXIMUM_INPUT_FILE_NUM == 0) {
        //
        // InputFileName and alignment buffer too small, need to realloc
        //
        InputFileName = (CHAR8 **) realloc (
                                    InputFileName,
                                    (InputFileNum + MAXIMUM_INPUT_FILE_NUM) * sizeof (CHAR8 *)
                                    );
  
        if (InputFileName == NULL) {
          Error (__FILE__, __LINE__, 0, "application error", "failed to allocate memory");
          free (InputFileAlign);
          return EFI_OUT_OF_RESOURCES;
        }
        memset (&(InputFileName[InputFileNum]), 0, (MAXIMUM_INPUT_FILE_NUM * sizeof (CHAR8 *)));

        InputFileAlign = (UINT32 *) realloc (
                                    InputFileAlign,
                                    (InputFileNum + MAXIMUM_INPUT_FILE_NUM) * sizeof (UINT32)
                                    );
  
        if (InputFileAlign == NULL) {
          Error (__FILE__, __LINE__, 0, "application error", "failed to allocate memory");
          free (InputFileName);
          return EFI_OUT_OF_RESOURCES;
        }
        memset (&(InputFileAlign[InputFileNum]), 0, (MAXIMUM_INPUT_FILE_NUM * sizeof (UINT32)));
      }
  
      InputFileName[InputFileNum] = argv[1];
      argc -= 2;
      argv += 2;

      if (argc <= 0) {
	    InputFileNum ++;
        break;
      }

      if ((stricmp (argv[0], "-n") == 0) || (stricmp (argv[0], "--sectionalign") == 0)) {
        Status = StringtoAlignment (argv[1], &(InputFileAlign[InputFileNum]));
        if (EFI_ERROR (Status)) {
          Error (NULL, 0, 0, NULL, "ERROR: %s is invalid alignment", argv[1]);
          goto Finish;
        }
        argc -= 2;
        argv += 2;
      }
      InputFileNum ++;
      continue; 
    }

    if ((stricmp (argv[0], "-n") == 0) || (stricmp (argv[0], "--sectionalign") == 0)) {
      Error (NULL, 0, 0, NULL, "ERROR: SectionAlign much be specified with section file");
      goto Finish;
    }
    
    Error (NULL, 0, 0, NULL, "%s is invaild paramter!", argv[0]);
    goto Finish;
  }
  
  //
  // Check the complete input paramters.
  //
  if (FfsFiletype == EFI_FV_FILETYPE_ALL) {
    Error (NULL, 0, 0, NULL, "ERROR: File Type is not specified or File Type is not one valid type");
    goto Finish;      
  }

  if (CompareGuid (&FileGuid, &mZeroGuid) == 0) {
    Error (NULL, 0, 0, NULL, "File Guid value is not specified");
    goto Finish;    
  }

  if (InputFileNum == 0) {
    Error (NULL, 0, 0, NULL, "ERROR: No input section files");
    goto Finish;
  }

  //
  // Calculate the size of all input section files.
  //  
  Status = GetSectionContents (
             InputFileName,
             InputFileAlign,
             InputFileNum,
             FileBuffer,
             &FileSize,
             &MaxAlignment
             );

  if (Status == EFI_BUFFER_TOO_SMALL) {
    FileBuffer = (UINT8 *) malloc (FileSize);
    if (FileBuffer == NULL) {
      Error (__FILE__, __LINE__, 0, "application error", "failed to allocate memory");
      goto Finish;
    }
    memset (FileBuffer, 0, FileSize);
    
    //
    // read all input file contents into a buffer
    //
    Status = GetSectionContents (
               InputFileName,
               InputFileAlign,
               InputFileNum,
               FileBuffer,
               &FileSize,
               &MaxAlignment
               );
  }

  if (EFI_ERROR (Status)) {
    goto Finish;
  }
  
  //
  // Create Ffs file header.
  //
  memset (&FfsFileHeader, 0, sizeof (EFI_FFS_FILE_HEADER));
  memcpy (&FfsFileHeader.Name, &FileGuid, sizeof (EFI_GUID));
  FfsFileHeader.Type       = FfsFiletype;
  //
  // Update FFS Alignment based on the max alignment required by input section files 
  //
  for (Index = 0; Index < sizeof (mFfsValidAlign) / sizeof (UINT32) - 1; Index ++) {
    if ((MaxAlignment > mFfsValidAlign [Index]) && (MaxAlignment <= mFfsValidAlign [Index + 1])) {
      break;
    }
  }
  if (FfsAlign < Index) {
    FfsAlign = Index;
  }
  
  FfsFileHeader.Attributes = FfsAttrib | (FfsAlign << 3);
  
  //
  // Now FileSize includes the EFI_FFS_FILE_HEADER
  //
  FileSize += sizeof (EFI_FFS_FILE_HEADER);
  FfsFileHeader.Size[0]  = (UINT8) (FileSize & 0xFF);
  FfsFileHeader.Size[1]  = (UINT8) ((FileSize & 0xFF00) >> 8);
  FfsFileHeader.Size[2]  = (UINT8) ((FileSize & 0xFF0000) >> 16);
  //
  // Fill in checksums and state, these must be zero for checksumming
  //
  // FileHeader.IntegrityCheck.Checksum.Header = 0;
  // FileHeader.IntegrityCheck.Checksum.File = 0;
  // FileHeader.State = 0;
  //
  FfsFileHeader.IntegrityCheck.Checksum.Header = CalculateChecksum8 (
                                                   (UINT8 *) &FfsFileHeader,
                                                   sizeof (EFI_FFS_FILE_HEADER)
                                                   );
  if (FfsFileHeader.Attributes & FFS_ATTRIB_CHECKSUM) {
    //
    // Ffs header checksum = zero, so only need to calculate ffs body.
    //
    FfsFileHeader.IntegrityCheck.Checksum.File = CalculateChecksum8 (
                                                   FileBuffer, 
                                                   FileSize - sizeof (EFI_FFS_FILE_HEADER)
                                                   );    
  } else {
    FfsFileHeader.IntegrityCheck.Checksum.File = FFS_FIXED_CHECKSUM;
  }

  FfsFileHeader.State = EFI_FILE_HEADER_CONSTRUCTION | EFI_FILE_HEADER_VALID | EFI_FILE_DATA_VALID;
  
  //
  // Open output file to write ffs data.
  //
  if (OutputFileName == NULL) {
    FfsFile = stdout;
  } else {
    FfsFile = fopen (OutputFileName, "wb");
  }
  if (FfsFile == NULL) {
    Error (NULL, 0, 0, NULL, "Can't open %s file to write!", OutputFileName);
    goto Finish;
  }
  //
  // write header
  //
  fwrite (&FfsFileHeader, 1, sizeof (FfsFileHeader), FfsFile);
  //
  // write data
  //
  fwrite (FileBuffer, 1, FileSize - sizeof (EFI_FFS_FILE_HEADER), FfsFile);

  fclose (FfsFile);

Finish:
  if (InputFileName != NULL) {
    free (InputFileName);
  }
  if (InputFileAlign != NULL) {
    free (InputFileAlign);
  }
  if (FileBuffer != NULL) {
    free (FileBuffer);
  }
  //
  // If any errors were reported via the standard error reporting
  // routines, then the status has been saved. Get the value and
  // return it to the caller.
  //
  return GetUtilityStatus ();
}
