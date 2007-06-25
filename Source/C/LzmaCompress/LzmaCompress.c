/*++
  This file contains a 'Sample Driver' and is licensed as such  
  under the terms of your license agreement with Intel or your  
  vendor.  This file may be modified by the user, subject to    
  the additional terms of the license agreement                 
--*/
/*++

Copyright (c) 2006, Intel Corporation. All rights reserved. <BR>
This software and associated documentation (if any) is furnished
under a license and may only be used or copied in accordance
with the terms of the license. Except as permitted by such
license, no part of this software or documentation may be
reproduced, stored in a retrieval system, or transmitted in any
form or by any means without the express written consent of
Intel Corporation.          

Module Name:

  LzmaCompress.c

Abstract:

  Creates output file that is a properly formed section per the FV spec.

--*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

#include <Common/UefiBaseTypes.h>
#include <Common/FirmwareVolumeImageFormat.h>

extern
EFI_STATUS
CustomizedCompress (
  IN      UINT8   *SrcBuffer,
  IN      UINT32  SrcSize,
  IN      UINT8   *DstBuffer,
  IN OUT  UINT32  *DstSize
  )
;

#define UTILITY_NAME            "LzmaCompress"
#define UTILITY_MAJOR_VERSION  0
#define UTILITY_MINOR_VERSION  1

#define PARAMETER_NOT_SPECIFIED "Parameter not specified"
#define MAXIMUM_INPUT_FILE_NUM  10

EFI_STATUS
GetFileContents (
  char    *InputFileName,
  int     InputFileNum,
  UINT8   *FileBuffer,
  UINTN   *BufferLength
  );
  
EFI_STATUS
GenCompressionFile (
  IN char *InputFileName,
  IN int  InputFileNum,
  IN FILE *OutFile
  );

EFI_STATUS
GetFileContents (
  char    *InputFileName,
  int     InputFileNum,
  UINT8   *FileBuffer,
  UINTN   *BufferLength
  )
/*++
        
Routine Description:
           
  Get the contents of all section files specified in InputFileName
  into FileBuffer.
            
Arguments:
               
  InputFileName  - Name of the input file.
                
  InputFileNum   - Number of input files. Should be at least 1.

  FileBuffer     - Output buffer to contain data

  BufferLength   - Actual length of the data 

Returns:
                       
  EFI_SUCCESS on successful return
  EFI_INVALID_PARAMETER if InputFileNum is less than 1
  EFI_ABORTED if unable to open input file.

--*/
{
  UINTN   Size;
  UINTN   FileSize;
  INTN    Index;
  FILE    *InFile;

  if (InputFileNum < 1) {
    printf ("must specify one input file");
    return EFI_INVALID_PARAMETER;
  }

  Size = 0;
  //
  // Go through our array of file names and copy their contents
  // to the output buffer.
  //
  // Copy the file contents to the output buffer.
  //
//  for (Index = 0; Index < InputFileNum; Index++) {
//    InFile = fopen (InputFileName[Index], "rb");
    InFile = fopen (InputFileName, "rb");
    if (InFile == NULL) {
      printf ("%s failed to open input file\n", InputFileName);
      return EFI_ABORTED;
    }

    fseek (InFile, 0, SEEK_END);
    FileSize = ftell (InFile);
    fseek (InFile, 0, SEEK_SET);
    //
    // Now read the contents of the file into the buffer
    // 
    if (FileSize > 0 && FileBuffer != NULL) {
      if (fread (FileBuffer + Size, (size_t) FileSize, 1, InFile) != 1) {
        printf ("%s failed to read contents of input file\n", InputFileName);
        fclose (InFile);
        return EFI_ABORTED;
      }
    }

    fclose (InFile);
    Size += (UINTN) FileSize;
    //
    // make sure section ends on a DWORD boundary
    //
//    while ((Size & 0x03) != 0) {
//      if (FileBuffer != NULL) {
//        FileBuffer[Size] = 0;
//      }
//      Size++;
//    }
//  }
  
  *BufferLength = Size;
  
  if (FileBuffer != NULL) {
    return EFI_SUCCESS;
  } else {
    return EFI_BUFFER_TOO_SMALL;
  }
}


EFI_STATUS
GenCompressionFile (
  IN char *InputFileName,
  IN int  InputFileNum,
  IN FILE *OutFile
  )
{
  UINT8                   *FileBuffer;
  UINTN                   InputLength;
  UINTN                   CompressedLength;      
  UINT8                   *OutputBuffer;
  EFI_STATUS              Status;  
  
  InputLength       = 0;
  FileBuffer        = NULL;
  OutputBuffer      = NULL;
  CompressedLength  = 0;
  //
  // read input file contents into a buffer
  // first get the size of file contents
  //
  Status = GetFileContents (
            InputFileName,
            InputFileNum,
            FileBuffer,
            &InputLength
            );

  if (Status == EFI_BUFFER_TOO_SMALL) {
    FileBuffer = (UINT8 *) malloc (InputLength);
    if (FileBuffer == NULL) {
      printf ("application error", "failed to allocate memory\n");
      return EFI_OUT_OF_RESOURCES;
    }

    Status = GetFileContents (
              InputFileName,
              InputFileNum,
              FileBuffer,
              &InputLength
              );
  }

  if (EFI_ERROR (Status)) {
    free (FileBuffer);
    return Status;
  }
  //
  // Start to compress
  //
  printf("\n Start to compress!\n");
  assert(FileBuffer);
  assert(InputLength);
  printf("\n%i InputLength",InputLength);
//  assert(OutputBuffer);
  Status = CustomizedCompress (FileBuffer, InputLength, OutputBuffer, &CompressedLength);
  if (Status == EFI_BUFFER_TOO_SMALL) {
    OutputBuffer = malloc (CompressedLength);
    if (!OutputBuffer) {
      free (FileBuffer);
      return EFI_OUT_OF_RESOURCES;
    }

    Status = CustomizedCompress (FileBuffer, InputLength, OutputBuffer, &CompressedLength);
  }

  free (FileBuffer);
  FileBuffer = OutputBuffer;

  if (EFI_ERROR (Status)) {
    if (FileBuffer != NULL) {
      free (FileBuffer);
    }

    return Status;
  }
  
  fwrite (FileBuffer, CompressedLength, 1, OutFile);
  free (FileBuffer);
  
  return EFI_SUCCESS;
}

VOID
Version (
  VOID
  )
/*++

Routine Description:

  Displays the standard utility information to SDTOUT

Arguments:

  None

Returns:

  None

--*/
{
  printf (
    "%s, LZMA Compress Utility. Version %i.%i.\n",
    UTILITY_NAME,
    UTILITY_MAJOR_VERSION,
    UTILITY_MINOR_VERSION
    );
}

VOID
Usage (
  VOID
  )
/*++

Routine Description:

  Displays the utility usage syntax to STDOUT

Arguments:

  None

Returns:

  None

--*/
{
//  printf ("Usage: "UTILITY_NAME "  [-o OutputFile --version -v Verbose -q Quiet -d DebugLevel -h Help] CompressedFileName\n\n");
  printf ("Usage: "UTILITY_NAME "  [-o OutputFile -h Help] CompressedFileName\n\n");
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
  INTN                      Index;
  FILE                      *InFile;
  FILE                      *OutFile;
  INTN                      InputFileNum;
  char                      *InputFileName;
  char                      *OutputFileName;
  EFI_STATUS                Status;

  InputFileName         = NULL;
  OutputFileName        = NULL;

  InFile                = NULL;
  OutFile               = NULL;
  InputFileNum          = 0;
  Status                = EFI_SUCCESS;

  if (argc == 1) {
    Usage();
    return EFI_INVALID_PARAMETER;
  }
  //
  // Parse command line
  //
  if ((strcmp(argv[1], "-h") == 0) || (strcmp(argv[1], "--help") == 0) || 
      (strcmp(argv[1], "-?") == 0) || (strcmp(argv[1], "/?") == 0)) {
    Usage();
    return 1;
  }
  
  if ((strcmp(argv[1], "-V") == 0) || (strcmp(argv[1], "--version") == 0)) {
    Version();
    return 1;
  }

  Index = 1;
  while (Index < argc) {
    if ((argv[Index][0] != '-')) {
      //
      // Input file name and no output file name specified, So output to stdout
      //
      InputFileName = argv[Index];
      printf("\n%s is input file name\n", InputFileName);
      Index+=1;      
      if (Index == argc)
      OutputFileName = NULL;
      OutFile = stdout;
      break;
    }
    else if (strcmpi (argv[Index], "-o") == 0) {
      Index++;
      if (Index == argc) {
        printf("\nERROR Parameters!\n");
        Usage();
        return 1;
      }
      //
      // Output File specified
      //
      OutputFileName = argv[Index];
      printf("\n%s is output file name\n", OutputFileName);
      
      Index++;
      if (Index == argc) {
        printf("\nERROR Parameters!\n");
        Usage();
        return 1;
      }      
      //
      // Parse subsequent parameters until another switch is encountered
      //
      if ((Index < argc) && (argv[Index][0] != '-')) {
      //
      // Input file name
      //
      InputFileName = argv[Index];
      //
      // We are done here to parse the parameter
      //
      break;
      }
    }
    else {
      printf("\nERROR, Please input correct parameter!\n");
      Usage();
    }
    }

  //
  // We are done here to parse the input parameters
  //


  //
  // Open output file
  //
  if (OutputFileName != NULL) {
  OutFile = fopen (OutputFileName, "wb");
  if (OutFile == NULL) {
    printf ("%s failed to open output file for writing\n", OutputFileName);
    if (InFile != NULL) {
      fclose (InFile);
    }

    return EFI_ABORTED;
  }
  }
  //
  // At this point, we've fully validated the command line, and opened appropriate
  // files, so let's go and do what we've been asked to do...
  //

  //
  // Compress the input file
  //
//  printf("\nwe go here!\n");
  if (OutputFileName == NULL) {
  printf("\n no output file name\n");
  Status = GenCompressionFile(InputFileName, 1, stdout);
  }
  else
  Status = GenCompressionFile(InputFileName, 1, OutFile);
//  Status = GenCompressionFile(InputFileName, OutFile);
  
  if (InputFileName != NULL) {
    free(InputFileName);
  }
  if (OutputFileName != NULL) {
  fclose(OutFile);
  }

  return 0;
}
