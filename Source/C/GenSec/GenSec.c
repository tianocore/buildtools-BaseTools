/*++

Copyright (c) 2004, Intel Corporation                                                         
All rights reserved. This program and the accompanying materials                          
are licensed and made available under the terms and conditions of the BSD License         
which accompanies this distribution.  The full text of the license may be found at        
http://opensource.org/licenses/bsd-license.php                                            
                                                                                          
THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,                     
WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.             

Module Name:

  GenSection.c

Abstract:

  Creates output file that is a properly formed section per the FV spec.

--*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <Common/UefiBaseTypes.h>
#include <Common/FirmwareVolumeImageFormat.h>
#include <Protocol/GuidedSectionExtraction.h>

#include "CommonLib.h"
#include "Compress.h"
#include "Crc32.h"
#include "EfiUtilityMsgs.h"

//
// GenSec Tool Information
//
#define UTILITY_NAME            "GenSec"
#define UTILITY_MAJOR_VERSION   1
#define UTILITY_MINOR_VERSION   0

#define MAXIMUM_INPUT_FILE_NUM  10
#define MAX_SECTION_SIZE        0x1000000

CHAR8      *SectionTypeName[] = {
  NULL,                                 // 0x00 - reserved
  "EFI_SECTION_COMPRESSION",            // 0x01
  "EFI_SECTION_GUID_DEFINED",           // 0x02
  NULL,                                 // 0x03 - reserved
  NULL,                                 // 0x04 - reserved
  NULL,                                 // 0x05 - reserved
  NULL,                                 // 0x06 - reserved
  NULL,                                 // 0x07 - reserved
  NULL,                                 // 0x08 - reserved
  NULL,                                 // 0x09 - reserved
  NULL,                                 // 0x0A - reserved
  NULL,                                 // 0x0B - reserved
  NULL,                                 // 0x0C - reserved
  NULL,                                 // 0x0D - reserved
  NULL,                                 // 0x0E - reserved
  NULL,                                 // 0x0F - reserved
  "EFI_SECTION_PE32",                   // 0x10
  "EFI_SECTION_PIC",                    // 0x11
  "EFI_SECTION_TE",                     // 0x12
  "EFI_SECTION_DXE_DEPEX",              // 0x13
  "EFI_SECTION_VERSION",                // 0x14
  "EFI_SECTION_USER_INTERFACE",         // 0x15
  "EFI_SECTION_COMPATIBILITY16",        // 0x16
  "EFI_SECTION_FIRMWARE_VOLUME_IMAGE",  // 0x17
  "EFI_SECTION_FREEFORM_SUBTYPE_GUID",  // 0x18
  "EFI_SECTION_RAW",                    // 0x19
  NULL,                                 // 0x1A
  "EFI_SECTION_PEI_DEPEX"               // 0x1B
};

CHAR8      *CompressionTypeName[]    = { "PI_NONE", "PI_STD" };
CHAR8      *GUIDedSectionAttribue[]  = { NULL, "PROCESSING_REQUIRED", "AUTH_STATUS_VALID"};

//
// Crc32 GUID section related definitions.
//
typedef struct {
  EFI_GUID_DEFINED_SECTION  GuidSectionHeader;
  UINT32                    CRC32Checksum;
} CRC32_SECTION_HEADER;

EFI_GUID  gZeroGuid                 = {0x0, 0x0, 0x0, {0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0}};
EFI_GUID  gEfiCrc32SectionGuid      = EFI_CRC32_GUIDED_SECTION_EXTRACTION_PROTOCOL_GUID;

STATIC
VOID 
Version(
  VOID
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
  printf ("%s v%d.%d - EDKII Utility to create output file with formed section per the PI spec.\n", UTILITY_NAME, UTILITY_MAJOR_VERSION, UTILITY_MINOR_VERSION);
  printf ("Copyright (c) 2007 Intel Corporation. All rights reserved.\n");
}

STATIC
VOID
Usage (
  VOID
  )
{
  Version();

  printf ("\nUsage: " UTILITY_NAME " [inputfilename]\n\
        -o, --outputfile [FileName]\n\
        -s, --SectionType <EFI_SECTION_COMPRESSION|\n\
                          EFI_SECTION_GUID_DEFINED|\n\
                          EFI_SECTION_PE32|\n\
                          EFI_SECTION_PIC|\n\
                          EFI_SECTION_TE|\n\
                          EFI_SECTION_DXE_DEPEX|\n\
                          EFI_SECTION_VERSION|\n\
                          EFI_SECTION_USER_INTERFACE|\n\
                          EFI_SECTION_COMPATIBILITY16|\n\
                          EFI_SECTION_FIRMWARE_VOLUME_IMAGE|\n\
                          EFI_SECTION_FREEFORM_SUBTYPE_GUID|\n\
                          EFI_SECTION_RAW|\n\
                          EFI_SECTION_PEI_DEPEX>\n\
        -c, --compress <PI_NONE|PI_STD>\n\
        -g, --vendorguid [GuidValue (########-####-####-####-############)]\n\
        -r, --attributes <PROCESSING_REQUIRED|AUTH_STATUS_VALID>\n\
        -n, --name \"string\"\n\
        -j, --buildnumber #### (0000~9999)\n\
        -h, --help\n\
        -V, --version\n");
}

VOID
Ascii2UnicodeWriteString (
  CHAR8    *String,
  FILE     *OutFile
  )
{
  UINT32 Index;
  UINT8  AsciiNull;

  AsciiNull = 0;

  //
  // Next, write out the string... Convert ASCII to Unicode in the process.
  //
  Index = 0;
  do {
    fwrite (&String[Index], 1, 1, OutFile);
    fwrite (&AsciiNull, 1, 1, OutFile);
  } while (String[Index++] != 0);
}

STATUS
GenSectionCommonLeafSection (
  CHAR8   **InputFileName,
  UINT32  InputFileNum,
  UINT8   SectionType,
  FILE    *OutFile
  )
/*++
        
Routine Description:
           
  Generate a leaf section of type other than EFI_SECTION_VERSION
  and EFI_SECTION_USER_INTERFACE. Input file must be well formed.
  The function won't validate the input file's contents. For
  common leaf sections, the input file may be a binary file.
  The utility will add section header to the file.
            
Arguments:
               
  InputFileName  - Name of the input file.
                
  InputFileNum   - Number of input files. Should be 1 for leaf section.

  SectionType    - A valid section type string

  OutFile        - Output file handle

Returns:
                       
  STATUS_ERROR            - can't continue
  STATUS_SUCCESS          - successful return

--*/
{
  UINT32                    InputFileLength;
  FILE                      *InFile;
  UINT8                     *Buffer;
  UINT32                    TotalLength;
  EFI_COMMON_SECTION_HEADER CommonSect;
  STATUS                    Status;

  if (InputFileNum > 1) {
    Error (NULL, 0, 0, "invalid parameter", "more than one input file specified");
    return STATUS_ERROR;
  } else if (InputFileNum < 1) {
    Error (NULL, 0, 0, "no input file specified", NULL);
    return STATUS_ERROR;
  }
  //
  // Open the input file
  //
  InFile = fopen (InputFileName[0], "rb");
  if (InFile == NULL) {
    Error (NULL, 0, 0, InputFileName[0], "failed to open input file");
    return STATUS_ERROR;
  }

  Status  = STATUS_ERROR;
  Buffer  = NULL;
  //
  // Seek to the end of the input file so we can determine its size
  //
  fseek (InFile, 0, SEEK_END);
  InputFileLength = ftell (InFile);
  fseek (InFile, 0, SEEK_SET);
  //
  // Fill in the fields in the local section header structure
  //
  CommonSect.Type = (EFI_SECTION_TYPE) SectionType;
  TotalLength     = sizeof (CommonSect) + InputFileLength;
  //
  // Size must fit in 3 bytes
  //
  if (TotalLength >= MAX_SECTION_SIZE) {
    Error (NULL, 0, 0, InputFileName[0], "file size (0x%X) exceeds section size limit(%dM).", TotalLength, MAX_SECTION_SIZE>>20);
    goto Done;
  }
  //
  // Now copy the size into the section header and write out the section header
  //
  memcpy (&CommonSect.Size, &TotalLength, 3);
  fwrite (&CommonSect, sizeof (CommonSect), 1, OutFile);
  //
  // Allocate a buffer to read in the contents of the input file. Then
  // read it in as one block and write it to the output file.
  //
  if (InputFileLength != 0) {
    Buffer = (UINT8 *) malloc ((size_t) InputFileLength);
    if (Buffer == NULL) {
      Error (__FILE__, __LINE__, 0, "memory allocation failure", NULL);
      goto Done;
    }

    if (fread (Buffer, (size_t) InputFileLength, 1, InFile) != 1) {
      Error (NULL, 0, 0, InputFileName[0], "failed to read contents of file");
      goto Done;
    }

    if (fwrite (Buffer, (size_t) InputFileLength, 1, OutFile) != 1) {
      Error (NULL, 0, 0, "failed to write to output file", NULL);
      goto Done;
    }
  }

  Status = STATUS_SUCCESS;

Done:
  fclose (InFile);
  if (Buffer != NULL) {
    free (Buffer);
  }

  return Status;
}

EFI_STATUS
GetSectionContents (
  CHAR8   **InputFileName,
  UINT32  InputFileNum,
  UINT8   *FileBuffer,
  UINT32  *BufferLength
  )
/*++
        
Routine Description:
           
  Get the contents of all section files specified in InputFileName
  into FileBuffer.
            
Arguments:
               
  InputFileName  - Name of the input file.
                
  InputFileNum   - Number of input files. Should be at least 1.

  FileBuffer     - Output buffer to contain data

  BufferLength   - On input, this is size of the FileBuffer. 
                   On output, this is the actual length of the data.

Returns:
                       
  EFI_SUCCESS on successful return
  EFI_INVALID_PARAMETER if InputFileNum is less than 1 or BufferLength point is NULL.
  EFI_ABORTED if unable to open input file.
  EFI_BUFFER_TOO_SMALL FileBuffer is not enough to contain all file data.
--*/
{
  UINT32   Size;
  UINT32   FileSize;
  UINT32   Index;
  FILE    *InFile;

  if (InputFileNum < 1) {
    Error (NULL, 0, 0, "must specify at least one input file", NULL);
    return EFI_INVALID_PARAMETER;
  }

  if (BufferLength == NULL) {
    Error (NULL, 0, 0, "BufferLength can't be NULL", NULL);
    return EFI_INVALID_PARAMETER;
  }

  Size = 0;
  //
  // Go through our array of file names and copy their contents
  // to the output buffer.
  //
  for (Index = 0; Index < InputFileNum; Index++) {
    //
    // make sure section ends on a DWORD boundary
    //
    while ((Size & 0x03) != 0) {
      if (FileBuffer != NULL && Size < *BufferLength) {
        FileBuffer[Size] = 0;
      }
      Size++;
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

EFI_STATUS
GenSectionCompressionSection (
  CHAR8    **InputFileName,
  UINT32  InputFileNum,
  UINT8   SectCompSubType,
  FILE    *OutFile
  )
/*++
        
Routine Description:
           
  Generate an encapsulating section of type EFI_SECTION_COMPRESSION
  Input file must be already sectioned. The function won't validate
  the input files' contents. Caller should hand in files already 
  with section header.
            
Arguments:
               
  InputFileName  - Name of the input file.
                
  InputFileNum   - Number of input files. Should be at least 1.

  SectCompSubType - Specify the compression algorithm requested. 
  
  OutFile        - Output file handle

Returns:
                       
  EFI_SUCCESS           on successful return
  EFI_INVALID_PARAMETER if InputFileNum is less than 1
  EFI_ABORTED           if unable to open input file.
  EFI_OUT_OF_RESOURCES  No resource to complete the operation.
--*/
{
  UINT32                  TotalLength;
  UINT32                  InputLength;
  UINT32                  CompressedLength;
  UINT8                   *FileBuffer;
  UINT8                   *OutputBuffer;
  EFI_STATUS              Status;
  EFI_COMPRESSION_SECTION CompressionSect;
  COMPRESS_FUNCTION       CompressFunction;

  InputLength       = 0;
  FileBuffer        = NULL;
  OutputBuffer      = NULL;
  CompressedLength  = 0;
  //
  // read all input file contents into a buffer
  // first get the size of all file contents
  //
  Status = GetSectionContents (
            InputFileName,
            InputFileNum,
            FileBuffer,
            &InputLength
            );

  if (Status == EFI_BUFFER_TOO_SMALL) {
    FileBuffer = (UINT8 *) malloc (InputLength);
    if (FileBuffer == NULL) {
      Error (__FILE__, __LINE__, 0, "application error", "failed to allocate memory");
      return EFI_OUT_OF_RESOURCES;
    }
    //
    // read all input file contents into a buffer
    //
    Status = GetSectionContents (
              InputFileName,
              InputFileNum,
              FileBuffer,
              &InputLength
              );
  }

  if (EFI_ERROR (Status)) {
    if (FileBuffer != NULL) {
      free (FileBuffer);
    }
    return Status;
  }

  CompressFunction = NULL;

  //
  // Now data is in FileBuffer, compress the data
  //
  switch (SectCompSubType) {
  case EFI_NOT_COMPRESSED:
    CompressedLength = InputLength;
    break;

  case EFI_STANDARD_COMPRESSION:
    CompressFunction = (COMPRESS_FUNCTION) EfiCompress;
    break;

  default:
    Error (NULL, 0, 0, "unknown compression type", NULL);
    free (FileBuffer);
    return EFI_ABORTED;
  }

  if (CompressFunction != NULL) {

    Status = CompressFunction (FileBuffer, InputLength, OutputBuffer, &CompressedLength);
    if (Status == EFI_BUFFER_TOO_SMALL) {
      OutputBuffer = malloc (CompressedLength);
      if (!OutputBuffer) {
        free (FileBuffer);
        return EFI_OUT_OF_RESOURCES;
      }

      Status = CompressFunction (FileBuffer, InputLength, OutputBuffer, &CompressedLength);
    }

    free (FileBuffer);
    FileBuffer = OutputBuffer;

    if (EFI_ERROR (Status)) {
      if (FileBuffer != NULL) {
        free (FileBuffer);
      }

      return Status;
    }
  }

  TotalLength = CompressedLength + sizeof (EFI_COMPRESSION_SECTION);
  if (TotalLength >= MAX_SECTION_SIZE) {
    Error (__FILE__, __LINE__, 0, "input error", "The size of all files exceeds section size limit(%dM).", MAX_SECTION_SIZE>>20);
    if (FileBuffer != NULL) {
      free (FileBuffer);
    }
    if (OutputBuffer != NULL) {
      free (OutputBuffer);
    }
    return STATUS_ERROR;
  }

  //
  // Add the section header for the compressed data
  //
  CompressionSect.CommonHeader.Type     = EFI_SECTION_COMPRESSION;
  CompressionSect.CommonHeader.Size[0]  = (UINT8) (TotalLength & 0xff);
  CompressionSect.CommonHeader.Size[1]  = (UINT8) ((TotalLength & 0xff00) >> 8);
  CompressionSect.CommonHeader.Size[2]  = (UINT8) ((TotalLength & 0xff0000) >> 16);
  CompressionSect.CompressionType       = SectCompSubType;
  CompressionSect.UncompressedLength    = InputLength;

  fwrite (&CompressionSect, sizeof (CompressionSect), 1, OutFile);
  fwrite (FileBuffer, CompressedLength, 1, OutFile);
  free (FileBuffer);
  return EFI_SUCCESS;
}

EFI_STATUS
GenSectionGuidDefinedSection (
  CHAR8    **InputFileName,
  UINT32   InputFileNum,
  EFI_GUID *VendorGuid,
  UINT16   DataAttribute,
  FILE     *OutFile
  )
/*++
        
Routine Description:
           
  Generate an encapsulating section of type EFI_SECTION_GUID_DEFINED
  Input file must be already sectioned. The function won't validate
  the input files' contents. Caller should hand in files already 
  with section header.
            
Arguments:
               
  InputFileName - Name of the input file.
                
  InputFileNum  - Number of input files. Should be at least 1.

  VendorGuid    - Specify vendor guid value.

  DataAttribute - Specify attribute for the vendor guid data. 
  
  OutFile       - Output file handle

Returns:
                       
  EFI_SUCCESS on successful return
  EFI_INVALID_PARAMETER if InputFileNum is less than 1
  EFI_ABORTED if unable to open input file.
  EFI_OUT_OF_RESOURCES  No resource to complete the operation.

--*/
{
  UINT32                TotalLength;
  UINT32                InputLength;
  UINT8                 *FileBuffer;
  UINT32                Crc32Checksum;
  EFI_STATUS            Status;
  CRC32_SECTION_HEADER  Crc32GuidSect;
  EFI_GUID_DEFINED_SECTION  VendorGuidSect;

  InputLength = 0;
  FileBuffer  = NULL;
  //
  // read all input file contents into a buffer
  // first get the size of all file contents
  //
  Status = GetSectionContents (
            InputFileName,
            InputFileNum,
            FileBuffer,
            &InputLength
            );

  if (Status == EFI_BUFFER_TOO_SMALL) {
    FileBuffer = (UINT8 *) malloc (InputLength);
    if (FileBuffer == NULL) {
      Error (__FILE__, __LINE__, 0, "application error", "failed to allocate memory");
      return EFI_OUT_OF_RESOURCES;
    }
    //
    // read all input file contents into a buffer
    //
    Status = GetSectionContents (
              InputFileName,
              InputFileNum,
              FileBuffer,
              &InputLength
              );
  }

  if (EFI_ERROR (Status)) {
    if (FileBuffer != NULL) {
      free (FileBuffer);
    }
    return Status;
  }

  //
  // Now data is in FileBuffer
  //
  if (CompareGuid (VendorGuid, &gEfiCrc32SectionGuid) == 0) {
    //
    // Default Guid section is CRC32.
    //
    Crc32Checksum = 0;
    CalculateCrc32 (FileBuffer, InputLength, &Crc32Checksum);

    TotalLength = InputLength + sizeof (CRC32_SECTION_HEADER);
    if (TotalLength >= MAX_SECTION_SIZE) {
      Error (__FILE__, __LINE__, 0, "input error", "The size of all files exceeds section size limit(%dM).", MAX_SECTION_SIZE>>20);
      free (FileBuffer);
      return STATUS_ERROR;
    }

    Crc32GuidSect.GuidSectionHeader.CommonHeader.Type     = EFI_SECTION_GUID_DEFINED;
    Crc32GuidSect.GuidSectionHeader.CommonHeader.Size[0]  = (UINT8) (TotalLength & 0xff);
    Crc32GuidSect.GuidSectionHeader.CommonHeader.Size[1]  = (UINT8) ((TotalLength & 0xff00) >> 8);
    Crc32GuidSect.GuidSectionHeader.CommonHeader.Size[2]  = (UINT8) ((TotalLength & 0xff0000) >> 16);
    memcpy (&(Crc32GuidSect.GuidSectionHeader.SectionDefinitionGuid), &gEfiCrc32SectionGuid, sizeof (EFI_GUID));
    Crc32GuidSect.GuidSectionHeader.Attributes  = EFI_GUIDED_SECTION_AUTH_STATUS_VALID;
    Crc32GuidSect.GuidSectionHeader.DataOffset  = sizeof (CRC32_SECTION_HEADER);
    Crc32GuidSect.CRC32Checksum                 = Crc32Checksum;
    fwrite (&Crc32GuidSect, sizeof (Crc32GuidSect), 1, OutFile);  

  } else {
    TotalLength = InputLength + sizeof (EFI_GUID_DEFINED_SECTION);
    if (TotalLength >= MAX_SECTION_SIZE) {
      Error (__FILE__, __LINE__, 0, "input error", "The size of all files exceeds section size limit(%dM).", MAX_SECTION_SIZE>>20);
      free (FileBuffer);
      return STATUS_ERROR;
    }

    VendorGuidSect.CommonHeader.Type     = EFI_SECTION_GUID_DEFINED;
    VendorGuidSect.CommonHeader.Size[0]  = (UINT8) (TotalLength & 0xff);
    VendorGuidSect.CommonHeader.Size[1]  = (UINT8) ((TotalLength & 0xff00) >> 8);
    VendorGuidSect.CommonHeader.Size[2]  = (UINT8) ((TotalLength & 0xff0000) >> 16);
    memcpy (&(VendorGuidSect.SectionDefinitionGuid), VendorGuid, sizeof (EFI_GUID));
    VendorGuidSect.Attributes  = DataAttribute;
    VendorGuidSect.DataOffset  = sizeof (EFI_GUID_DEFINED_SECTION);
    fwrite (&VendorGuidSect, sizeof (EFI_GUID_DEFINED_SECTION), 1, OutFile);  
  }

  fwrite (FileBuffer, InputLength, 1, OutFile);
  free (FileBuffer);

  return EFI_SUCCESS;
}

int
main (
  int  argc,
  char *argv[]
  )
/*++

Routine Description:

  Main

Arguments:

  command line parameters

Returns:

  EFI_SUCCESS    Section header successfully generated and section concatenated.
  EFI_ABORTED    Could not generate the section
  EFI_OUT_OF_RESOURCES  No resource to complete the operation.

--*/
{
  UINT32                    Index;
  UINT32                    InputFileNum;
  FILE                      *InFile;
  FILE                      *OutFile;
  CHAR8                     **InputFileName;
  CHAR8                     *OutputFileName;
  CHAR8                     *SectionName;
  CHAR8                     *CompressionName;
  CHAR8                     *StringBuffer;
  EFI_GUID                  VendorGuid = gZeroGuid;
  INT32                     VersionNumber;
  UINT8                     SectType;
  UINT8                     SectCompSubType;
  UINT16                    SectGuidAttribute; 
  EFI_COMMON_SECTION_HEADER CommonSect;
  UINT32                    InputLength;
  UINT8                     *FileBuffer;
  BOOLEAN                   AllocatedFlag;
  EFI_STATUS                Status;
 
  fprintf (stdout, "GenSec tool start.\n");  
  
  InputFileName         = NULL;
  OutputFileName        = NULL;
  SectionName           = NULL;
  CompressionName       = NULL;
  StringBuffer          = "";

  InFile                = NULL;
  OutFile               = NULL;
  VersionNumber         = 0;
  InputFileNum          = 0;
  SectType              = EFI_SECTION_ALL;
  SectCompSubType       = 0;
  SectGuidAttribute     = 0;
  FileBuffer            = NULL;
  InputLength           = 0;
  AllocatedFlag         = FALSE;
  Status                = STATUS_SUCCESS;
  

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
    return STATUS_ERROR;    
  }

  if ((stricmp (argv[0], "-v") == 0) || (stricmp (argv[0], "--version") == 0)) {
    Version();
    return STATUS_ERROR;    
  }

  while (argc > 0) {
    if ((stricmp (argv[0], "-s") == 0) || (stricmp (argv[0], "--SectionType") == 0)) {
      SectionName = argv[1];
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

    if ((stricmp (argv[0], "-c") == 0) || (stricmp (argv[0], "--compress") == 0)) {
      CompressionName = argv[1];
      argc -= 2;
      argv += 2;
      continue;
    }

    if ((stricmp (argv[0], "-g") == 0) || (stricmp (argv[0], "--vendorguid") == 0)) {
      Status = StringToGuid (argv[1], &VendorGuid);
      if (EFI_ERROR (Status)) {
        Error (NULL, 0, 0, NULL, "ERROR: %s is not a formal GUID value.", argv[1]);
        goto Finish;
      }
      argc -= 2;
      argv += 2;
      continue;
    }

    if ((stricmp (argv[0], "-r") == 0) || (stricmp (argv[0], "--attributes") == 0)) {
      if (stricmp (argv[1], GUIDedSectionAttribue[EFI_GUIDED_SECTION_PROCESSING_REQUIRED]) == 0) {
        SectGuidAttribute |= EFI_GUIDED_SECTION_PROCESSING_REQUIRED;
      } else if (stricmp (argv[1], GUIDedSectionAttribue[EFI_GUIDED_SECTION_AUTH_STATUS_VALID]) == 0) {
        SectGuidAttribute |= EFI_GUIDED_SECTION_AUTH_STATUS_VALID;
      } else {
        Error (NULL, 0, 0, argv[1], "unknown Guid Section Attribute");
        goto Finish;
      }
      argc -= 2;
      argv += 2;
      continue;
    }

    if ((stricmp (argv[0], "-n") == 0) || (stricmp (argv[0], "--name") == 0)) {
      StringBuffer = argv[1];
      argc -= 2;
      argv += 2;
      continue;
    }

    if ((stricmp (argv[0], "-j") == 0) || (stricmp (argv[0], "--buildnumber") == 0)) {
      //
      // Verify string is a integrator number
      //
      for (Index = 0; Index < strlen (argv[1]); Index++) {
        if ((argv[1][Index] != '-') && (isdigit (argv[1][Index]) == 0)) {
          Error (NULL, 0, 0, NULL, "ERROR: %s is not a valid integer.", argv[1]);
          goto Finish;
        }
      }

      sscanf (argv[1], "%d", &VersionNumber);
      argc -= 2;
      argv += 2;
      continue;
    }

    //
    // Get Input file name
    //
    if ((InputFileNum == 0) && (InputFileName == NULL)) {
      InputFileName = (CHAR8 **) malloc (MAXIMUM_INPUT_FILE_NUM * sizeof (CHAR8 *));
      if (InputFileName == NULL) {
        Error (__FILE__, __LINE__, 0, "application error", "failed to allocate memory");
        return EFI_OUT_OF_RESOURCES;
      }

      memset (InputFileName, 0, (MAXIMUM_INPUT_FILE_NUM * sizeof (CHAR8 *)));
    } else if (InputFileNum % MAXIMUM_INPUT_FILE_NUM == 0) {
      //
      // InputFileName buffer too small, need to realloc
      //
      InputFileName = (CHAR8 **) realloc (
                                  InputFileName,
                                  (InputFileNum + MAXIMUM_INPUT_FILE_NUM) * sizeof (CHAR8 *)
                                  );

      if (InputFileName == NULL) {
        Error (__FILE__, __LINE__, 0, "application error", "failed to allocate memory");
        return EFI_OUT_OF_RESOURCES;
      }

      memset (&(InputFileName[InputFileNum]), 0, (MAXIMUM_INPUT_FILE_NUM * sizeof (CHAR8 *)));
    }

    InputFileName[InputFileNum++] = argv[0];
    argc --;
    argv ++;
  }

  //
  // Parse all command line parameters to get the corresponding section type.
  //
  if (SectionName == NULL) {
    //
    // No specified Section type, default is SECTION_ALL.
    //
    SectType = EFI_SECTION_ALL;
  } else if (stricmp (SectionName, SectionTypeName[EFI_SECTION_COMPRESSION]) == 0) {
    SectType     = EFI_SECTION_COMPRESSION;
    if (CompressionName == NULL) {
      //
      // Default is PI_STD compression algorithm.
      //
      SectCompSubType = EFI_STANDARD_COMPRESSION;
    } else if (stricmp (CompressionName, CompressionTypeName[EFI_NOT_COMPRESSED]) == 0) {
      SectCompSubType = EFI_NOT_COMPRESSED;
    } else if (stricmp (CompressionName, CompressionTypeName[EFI_STANDARD_COMPRESSION]) == 0) {
      SectCompSubType = EFI_STANDARD_COMPRESSION;
    } else {
      Error (NULL, 0, 0, CompressionName, "unknown compression type");
      goto Finish;
    }
  } else if (stricmp (SectionName, SectionTypeName[EFI_SECTION_GUID_DEFINED]) == 0) {
    SectType     = EFI_SECTION_GUID_DEFINED;

    if (CompareGuid (&VendorGuid, &gZeroGuid) == 0) {
      memcpy (&VendorGuid, &gEfiCrc32SectionGuid, sizeof (EFI_GUID));
    }
    
    if (SectGuidAttribute == 0) {
      SectGuidAttribute = EFI_GUIDED_SECTION_PROCESSING_REQUIRED;
    }
  } else if (stricmp (SectionName, SectionTypeName[EFI_SECTION_PE32]) == 0) {
    SectType = EFI_SECTION_PE32;
  } else if (stricmp (SectionName, SectionTypeName[EFI_SECTION_PIC]) == 0) {
    SectType = EFI_SECTION_PIC;
  } else if (stricmp (SectionName, SectionTypeName[EFI_SECTION_TE]) == 0) {
    SectType = EFI_SECTION_TE;
  } else if (stricmp (SectionName, SectionTypeName[EFI_SECTION_DXE_DEPEX]) == 0) {
    SectType = EFI_SECTION_DXE_DEPEX;
  } else if (stricmp (SectionName, SectionTypeName[EFI_SECTION_VERSION]) == 0) {
    SectType = EFI_SECTION_VERSION;
    if (VersionNumber < 0 || VersionNumber > 9999) {
      Error (NULL, 0, 0, NULL, "%d is illegal version number\n", VersionNumber);
      goto Finish;
    }
  } else if (stricmp (SectionName, SectionTypeName[EFI_SECTION_USER_INTERFACE]) == 0) {
    SectType = EFI_SECTION_USER_INTERFACE;
    if (StringBuffer[0] == '\0') {
      Error (NULL, 0, 0, "user interface string not specified", NULL);
      goto Finish;
    }
  } else if (stricmp (SectionName, SectionTypeName[EFI_SECTION_COMPATIBILITY16]) == 0) {
    SectType = EFI_SECTION_COMPATIBILITY16;
  } else if (stricmp (SectionName, SectionTypeName[EFI_SECTION_FIRMWARE_VOLUME_IMAGE]) == 0) {
    SectType = EFI_SECTION_FIRMWARE_VOLUME_IMAGE;
  } else if (stricmp (SectionName, SectionTypeName[EFI_SECTION_FREEFORM_SUBTYPE_GUID]) == 0) {
    SectType = EFI_SECTION_FREEFORM_SUBTYPE_GUID;
  } else if (stricmp (SectionName, SectionTypeName[EFI_SECTION_RAW]) == 0) {
    SectType = EFI_SECTION_RAW;
  } else if (stricmp (SectionName, SectionTypeName[EFI_SECTION_PEI_DEPEX]) == 0) {
    SectType = EFI_SECTION_PEI_DEPEX;
  } else {
    Error (NULL, 0, 0, SectionName, "unknown section type");
    goto Finish;
  }
  
  if ((SectType != EFI_SECTION_VERSION) && (SectType != EFI_SECTION_USER_INTERFACE)) {
    //
    // The input file are required for those section type.
    // The file are from stdin.
    //
    if (InputFileNum == 0) {
      Error (NULL, 0, 0, NULL, "No input files is specified.");
      goto Finish;
    }
  }
  
  //
  // Open output file
  //
  if (OutputFileName == NULL) {
    Error (NULL, 0, 0, NULL, "No output file name is specified.");
    goto Finish;
    // OutFile = stdout;
  } else {
    OutFile = fopen (OutputFileName, "wb");
  }

  if (OutFile == NULL) {
    Error (NULL, 0, 0, OutputFileName, "failed to open output file for writing");
    goto Finish;
  }
  
  //
  // At this point, we've fully validated the command line, and opened appropriate
  // files, so let's go and do what we've been asked to do...
  //
  //
  // Within this switch, build and write out the section header including any
  // section type specific pieces.  If there's an input file, it's tacked on later
  //
  switch (SectType) {
  case EFI_SECTION_COMPRESSION:
    Status = GenSectionCompressionSection (
              InputFileName,
              InputFileNum,
              SectCompSubType,
              OutFile
              );
    break;

  case EFI_SECTION_GUID_DEFINED:
    Status = GenSectionGuidDefinedSection (
              InputFileName,
              InputFileNum,
              &VendorGuid,
              SectGuidAttribute,
              OutFile
              );
    break;

  case EFI_SECTION_VERSION:
    CommonSect.Type = (EFI_SECTION_TYPE) SectType;

    Index           = sizeof (CommonSect);
    //
    // 2 bytes for the build number UINT16
    //
    Index += 2;
    //
    // StringBuffer is ascii.. unicode is 2X + 2 bytes for terminating unicode null.
    //
    Index += (strlen (StringBuffer) * 2) + 2;
    memcpy (&CommonSect.Size, &Index, 3);
    fwrite (&CommonSect, sizeof (CommonSect), 1, OutFile);
    fwrite (&VersionNumber, sizeof (UINT16), 1, OutFile);
    Ascii2UnicodeWriteString (StringBuffer, OutFile);
    break;

  case EFI_SECTION_USER_INTERFACE:
    CommonSect.Type = (EFI_SECTION_TYPE) SectType;
    Index           = sizeof (CommonSect);
    //
    // StringBuffer is ascii.. unicode is 2X + 2 bytes for terminating unicode null.
    //
    Index += (strlen (StringBuffer) * 2) + 2;
    memcpy (&CommonSect.Size, &Index, 3);
    fwrite (&CommonSect, sizeof (CommonSect), 1, OutFile);
    Ascii2UnicodeWriteString (StringBuffer, OutFile);
    break;

  case EFI_SECTION_ALL:
    //
    // read all input file contents into a buffer
    // first get the size of all file contents
    //
    Status = GetSectionContents (
              InputFileName,
              InputFileNum,
              FileBuffer,
              &InputLength
              );
  
    if (Status == EFI_BUFFER_TOO_SMALL) {
      FileBuffer = (UINT8 *) malloc (InputLength);
      if (FileBuffer == NULL) {
        Error (__FILE__, __LINE__, 0, "application error", "failed to allocate memory");
        goto Finish;
      }
      //
      // read all input file contents into a buffer
      //
      Status = GetSectionContents (
                InputFileName,
                InputFileNum,
                FileBuffer,
                &InputLength
                );
    }
  
    if (Status == EFI_SUCCESS) {
      fwrite (FileBuffer, InputLength, 1, OutFile);
    }

    if (FileBuffer != NULL) {
      free (FileBuffer);
    }
    
    break;
  default:
    //
    // All other section types are caught by default (they're all the same)
    //
    Status = GenSectionCommonLeafSection (
              InputFileName,
              InputFileNum,
              SectType,
              OutFile
              );
    break;
  }

Finish:
  if (AllocatedFlag == TRUE) {
    for (Index = 0; Index < InputFileNum; Index ++) {
      free (InputFileName[Index]);
    }
  }

  if (InputFileName != NULL) {
    free (InputFileName);
  }

  if (OutFile != NULL) {
    fclose (OutFile);
  }

  fprintf (stdout, "GenSec tool done with return code is 0x%x.\n", GetUtilityStatus ()); 

  return GetUtilityStatus ();
}
