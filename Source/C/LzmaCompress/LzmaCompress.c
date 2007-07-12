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

#include "LzmaDecode.h"
#include <Common/UefiBaseTypes.h>
#include <Common/FirmwareVolumeImageFormat.h>

#pragma warning(disable : 4100)

#define UTILITY_NAME            "LzmaCompress"
#define UTILITY_MAJOR_VERSION  0
#define UTILITY_MINOR_VERSION  1

#define PARAMETER_NOT_SPECIFIED "Parameter not specified"
#define MAXIMUM_INPUT_FILE_NUM  10
#define ONE_TIANOCOMPRESS_ARGS  3
#define TWO_TIANOCOMPRESS_ARGS  5

typedef struct {
  UINT32  Lc;
  UINT32  Lp;
  UINT32  Pb;
  UINT32  DictionarySize;
  UINT32  InternalSize;
  UINT8   Properties[5];
} LZMAPARAMETER;

//
// global variable
//
STATIC UINT32 mSourceBufferSize = 0;
STATIC BOOLEAN ENCODE = FALSE;
STATIC BOOLEAN DECODE = FALSE;
UINT8                   *FileBuffer;
UINTN                   InputLength;
UINT8                   *OutputBuffer;
FILE                    *InFile;
UINT32                  FileSize = 0;

extern
EFI_STATUS
CustomizedCompress (
  IN      UINT8   *SrcBuffer,
  IN      UINT32  SrcSize,
  IN      UINT8   *DstBuffer,
  IN OUT  UINT32  *DstSize
  )
;

EFI_STATUS
CustomDecompress (
  IN CONST VOID  *Source,
  IN OUT VOID    *Destination,
  IN OUT VOID    *Scratch
  );
  

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
  // Copy the file contents to the output buffer.
  //
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
//  UINT8                   *FileBuffer;
//  UINTN                   InputLength;
  UINTN                   CompressedLength;      
//  UINT8                   *OutputBuffer;
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
//  printf("\n Start to compress!\n");
  assert(FileBuffer);
  assert(InputLength);
//  printf("\n%i InputLength",InputLength);
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
  printf ("Usage: "UTILITY_NAME "  -e|-d [-o OutputFile] input_file\n or \n");
  printf ("Usage: "UTILITY_NAME "  -e|-d input_file  [-o OutputFile]\n");
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
  UINT32                    DstSize, ScratchSize;
  VOID                      *Scratch;
//
// Initilize variables
//
//UINT8                   *FileBuffer;
//UINTN                   InputLength;
//UINT8                   *OutputBuffer;
//FILE                    *InFile;
//UINT32                  FileSize = 0;

  InputFileName         = NULL;
  OutputFileName        = NULL;

  InFile                = NULL;
  OutFile               = NULL;
  InputFileNum          = 0;
  Status                = EFI_SUCCESS;
  DstSize               = 0;
  ScratchSize           = 0;
  FileBuffer            = NULL;
  InputLength           = 0;
  OutputBuffer          = NULL;

  


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

  if (argc != ONE_TIANOCOMPRESS_ARGS && argc != TWO_TIANOCOMPRESS_ARGS) {
    Usage ();
    return 1;
  }
  
  Index = 1;
  if (strcmp(argv[Index],"-e") == 0) {
  //
  // encode the input file
  //
  Index++;
  ENCODE = TRUE;
  }
  else if (strcmp(argv[Index], "-d") == 0) {
  //
  // decode the input file
  //
  Index++;
  DECODE = TRUE;
  }
  else {
  //
  // Error command line
  //
  Usage();
  return 1;
  }
  
  while (Index < argc) {
    if ((argv[Index][0] != '-') && ((Index+1) == argc)) {
      //
      // Input file name and no output file name specified, So output to stdout
      //
      InputFileName = argv[Index];
//      printf("\n%s is input file name\n", InputFileName);
      Index+=1;      
      if (Index == argc)
      OutputFileName = NULL;
      OutFile = stdout;
      break;
    }
    else if ((argv[Index][0] != '-') && ((Index+1) < argc)) {
    //
    //
    //
      InputFileName = argv[Index];
      OutputFileName = argv[Index+2];
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
//      printf("\n%s is output file name\n", OutputFileName);
      
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

  if (ENCODE) {
  //
  // Compress the input file
  //

  if (OutputFileName == NULL) {
  printf("\n no output file name\n");
  Status = GenCompressionFile(InputFileName, 1, stdout);
  }
  else
  Status = GenCompressionFile(InputFileName, 1, OutFile);
  
  if (OutputFileName != NULL) {
  fclose(OutFile);
  }
  }
  else if (DECODE) {
  //
  // Decompress the input file
  //
//  printf("\n we come to decode!");
  InFile = fopen(InputFileName, "rb");
  if (InFile == NULL) {
    printf("\nError- Fail to open input file!");
    return 1;
  }
  Status = GetFileContents(
            InputFileName,
            1,
            FileBuffer,
            &InputLength);

  if (Status == EFI_BUFFER_TOO_SMALL) {
    FileBuffer = (UINT8 *) malloc (InputLength);
    if (FileBuffer == NULL) {
      printf ("application error", "failed to allocate memory\n");
      return EFI_OUT_OF_RESOURCES;
    }

    Status = GetFileContents (
              InputFileName,
              1,
              FileBuffer,
              &InputLength
              );
  }
  
  if (FileBuffer == NULL) {
    printf("\nError to allocate buffer for inputfile");
    if (InFile!=NULL)
      free(InFile);
    return 1;
  }
//  printf("\n input FileSize is %d", InputLength);
  Status = CustomDecompressGetInfo(FileBuffer, InputLength, &DstSize, &ScratchSize);
  if (Status != RETURN_SUCCESS) {
    printf("\nERROR in CustomDecompressGetInfo!\n");
  }
  Scratch = (VOID *)malloc(ScratchSize);
  if (Scratch == NULL) {
    printf("\nNo enough memory to allocate!\n");
    if (FileBuffer != NULL) {
      free(FileBuffer);
    }
    return 1;
  }
  
  OutputBuffer = (UINT8 *)malloc(DstSize);
  if (OutputBuffer == NULL) {
    printf("\nNo enough memory to allocate!");
    if (FileBuffer != NULL) {
      free(FileBuffer);
    }    
    if (Scratch != NULL) {
      free(Scratch);
    }
    return 1;
  }
  Status = CustomDecompress(FileBuffer, (VOID *)OutputBuffer, Scratch);
  if (Status != EFI_SUCCESS) {
    printf("\n ERROR in CustomDecompress");
    if (FileBuffer != NULL) {
      free(FileBuffer);
    }    
    if (Scratch != NULL) {
      free(Scratch);
    }
    if (OutputBuffer != NULL) {
      free(OutputBuffer);
    }
    return 1;
  }
//  printf("\nStart to write file!\n");
  fwrite(OutputBuffer, DstSize, 1, OutFile);
  free(FileBuffer);
  free(Scratch);
  free(OutputBuffer);      
  return 0;
  }
  return 0;
}

RETURN_STATUS
ParseLzma (
  IN CONST VOID         *Source,
  IN      UINT32        SrcSize,
  OUT     UINT32        *DstSize,
  OUT     UINT32        *ScratchSize,
  OUT     LZMAPARAMETER *Param
  )
/*++

Routine Description:

  The implementation of LZMA header parsing.

Arguments:

  Source      - The source buffer containing the compressed data.
  SrcSize     - The size of source buffer
  DstSize     - The size of destination buffer.
  ScratchSize - The size of scratch buffer.
  Param       - The parameter used by LZMA.

Returns:

  RETURN_SUCCESS           - The size of destination buffer and the size of scratch buffer are successull retrieved.
  RETURN_INVALID_PARAMETER - The source data is corrupted

--*/
{
  UINT8   Prop0;
  UINT32  Lc;
  UINT32  Lp;
  UINT32  Pb;
  UINT8   *SrcPtr;
  UINTN   Index;
  UINT32  OutSize;
  UINT32  InternalSize;
  UINT32  DictionarySize;
  
  if (Source == NULL || DstSize == NULL || ScratchSize == NULL) {
    return RETURN_INVALID_PARAMETER;
  }

  if (SrcSize < 13) {
    return RETURN_INVALID_PARAMETER;
  }
  
  SrcPtr          = (UINT8 *) Source;

  Prop0           = *SrcPtr;
  DictionarySize  = 0;

  if (Param != NULL) {
    for (Index = 0; Index < 5; Index++) {
      Param->Properties[Index] = *SrcPtr++;
    }
  } else {
    SrcPtr += 5;
  }

  OutSize = 0;
  for (Index = 0; Index < 4; Index++) {
    OutSize+= ((UINT32) (*SrcPtr++) << (Index * 8));
  }

  if (OutSize == 0xFFFFFFFF) {
    return RETURN_INVALID_PARAMETER;
  }
  
  for (Index = 0; Index < 4; Index++) {
    if ((*SrcPtr++) != 0) {
      return RETURN_INVALID_PARAMETER;
    }
  }

  if (Prop0 >= (9 * 5 * 5)) {
    return RETURN_INVALID_PARAMETER;
  }

  for (Pb = 0; Prop0 >= (9 * 5); Pb++, Prop0 -= (9 * 5))
    ;
  for (Lp = 0; Prop0 >= 9; Lp++, Prop0 -= 9)
    ;
  Lc            = Prop0;

  InternalSize  = (LZMA_BASE_SIZE + (LZMA_LIT_SIZE << (Lc + Lp))) * sizeof (CProb);

#ifdef _LZMA_OUT_READ
  InternalSize += 100;
#endif

  if (Param != NULL) {
    Param->Lc             = Lc;
    Param->Lp             = Lp;
    Param->Pb             = Pb;

    Param->DictionarySize = 0;
    Param->InternalSize   = InternalSize;

#ifdef _LZMA_OUT_READ
    for (Index = 0; Index < 4; Index++) {
      Param->DictionarySize = (UInt32) (Param.Properties[1 + Index]) << (Index * 8);
    }
  }

  DictionarySize = Param->DictionarySize;
#endif
}
*DstSize = OutSize;

//
// Request longer space to allow align
//
*ScratchSize = InternalSize + DictionarySize + 13;

return RETURN_SUCCESS;
}

RETURN_STATUS
EFIAPI
CustomDecompressGetInfo (
  IN  CONST VOID  *Source,
  IN  UINT32      SourceSize,
  OUT UINT32      *DestinationSize,
  OUT UINT32      *ScratchSize
  )
/*++

Routine Description:

  The implementation of LZMA GetInfo().

Arguments:

  Source      - The source buffer containing the compressed data.
  SrcSize     - The size of source buffer
  DstSize     - The size of destination buffer.
  ScratchSize - The size of scratch buffer.

Returns:

  RETURN_SUCCESS           - The size of destination buffer and the size of scratch buffer are successull retrieved.
  RETURN_INVALID_PARAMETER - The source data is corrupted

--*/
{
  mSourceBufferSize = SourceSize;

  return ParseLzma (
          Source,
          SourceSize,
          DestinationSize,
          ScratchSize,
          NULL
          );
}

#ifdef _LZMA_IN_CB
typedef struct _CBuffer {
  ILzmaInCallback InCallback;
  UINT8           *Buffer;
  UINT32          Size;
} CBuffer;

INT32
LzmaReadCompressed (
  VOID   *Object,
  UINT8  **Buffer,
  UINT32 *Size
  )
/*++

Routine Description:

  GC_TODO: Add function description

Arguments:

  Object  - GC_TODO: add argument description
  Buffer  - GC_TODO: add argument description
  Size    - GC_TODO: add argument description

Returns:

  GC_TODO: add return values

--*/

{
  CBUFFER *Bo;
  Bo      = (CBuffer *) Object;
  *Size   = Bo->Size; // You can specify any available size here
  *Buffer = Bo->Buffer;
  Bo->Buffer += *Size;
  Bo->Size -= *Size;
  return LZMA_RESULT_OK;
}
#endif

RETURN_STATUS
EFIAPI
CustomDecompress (
  IN CONST VOID  *Source,
  IN OUT VOID    *Destination,
  IN OUT VOID    *Scratch
  )
/*++

Routine Description:

  The implementation of LZMA Decompress().

Arguments:

  Source      - The source buffer containing the compressed data.
  Destination - The destination buffer to store the decompressed data
  Scratch     - The buffer used internally by the decompress routine. This  buffer is needed to store intermediate data.

Returns:

  RETURN_SUCCESS           - Decompression is successfull
  RETURN_INVALID_PARAMETER - The source data is corrupted

--*/
{
#ifdef _LZMA_IN_CB
  CBuffer       Bo;
#endif
  RETURN_STATUS Status;
  INT32         LzmaStatus;
  LZMAPARAMETER Param;
  UINT8         *SrcPtr;
  UINT32        CompressedSize;
  UINT32        OutSize;
  UINT32        RequiredScratchSize;
  UINT32        OutSizeProcessed;
  UINT32        SrcSize; 
  
  if (mSourceBufferSize == 0) {
    return RETURN_INVALID_PARAMETER;
  }
  
  SrcSize = mSourceBufferSize;
  mSourceBufferSize = 0;

  Status = ParseLzma (
            Source,
            SrcSize,
            &OutSize,
            &RequiredScratchSize,
            &Param
            );
  if (RETURN_ERROR (Status)) {
    return RETURN_INVALID_PARAMETER;
  }

  //
  // Skip the LZMA param field
  //
  CompressedSize  = SrcSize - 13;
  SrcPtr          = (UINT8 *) Source + 13;

#ifdef _LZMA_IN_CB
  Bo.InCallback.Read  = LzmaReadCompressed;
  Bo.Buffer           = (unsigned char *) SrcPtr;
  Bo.Size             = CompressedSize;
#endif

#ifdef _LZMA_OUT_READ
  {
    UINT32  NowPos;
    UINT8   *Dictionary;
    UINT32  DictionarySize;
    UINTN   Index;

    Dictionary = ((Param->InternalSize + (UINT8 *) Scratch) + 16) -
      ((Param->InternalSize + (UINT8 *) Scratch) & 0x0F)

      LzmaDecoderInit (
                                                        (UINT8 *) Scratch,
                                                        Param->InternalSize,
                                                        Param->Lc,
                                                        Param->Lp,
                                                        Param->Pb,
                                                        Dictionary,
                                                        Param->DictionarySize,
#ifdef _LZMA_IN_CB
                                                        & Bo.InCallback
#else
                                                        (UINT8 *) SrcPtr,
                                                        CompressedSize
#endif
                                                        );
    for (NowPos = 0; NowPos < OutSize;) {
      UINT32  BlockSize;
      UINT32  KBlockSize;

      KBlockSize  = 0x10000;
      BlockSize   = OutSize - NowPos;
      if (BlockSize > KBlockSize) {
        BlockSize = KBlockSize;
      }

      LzmaStatus = LzmaDecode (
                    (UINT8 *) Scratch,
                    ((UINT8 *) Destination) + NowPos,
                    BlockSize,
                    &OutSizeProcessed
                    );
      if (LzmaStatus != 0) {
        return RETURN_INVALID_PARAMETER;
      }

      if (OutSizeProcessed == 0) {
        OutSize = NowPos;
        break;
      }

      NowPos += OutSizeProcessed;
    }
  }

#else

  LzmaStatus = LzmaDecode (
                (UINT8 *) Scratch,
                RequiredScratchSize,
                Param.Lc,
                Param.Lp,
                Param.Pb,
#ifdef _LZMA_IN_CB
                & Bo.InCallback,
#else
                (UINT8 *) SrcPtr,
                CompressedSize,
#endif
                (UINT8 *) Destination,
                OutSize,
                &OutSizeProcessed
                );

  OutSize = OutSizeProcessed;
#endif

  if (LzmaStatus != 0) {
    return RETURN_INVALID_PARAMETER;
  }

  return RETURN_SUCCESS;
}
