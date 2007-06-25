/*++

Copyright (c) 2006 Intel Corporation. 
All rights reserved. This program and the accompanying materials                      
are licensed and made available under the terms and conditions of the CPL License         
which accompanies this distribution.  The full text of the license may be found at        
http://opensource.org/licenses/cpl1.0.php                                          

THE PROGRAM IS DISTRIBUTED UNDER THE CPL LICENSE ON AN "AS IS" BASIS,                     
WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.

Module Name:
  
  LzmaDecompress.c

Abstract:

  Implementation file for decompression routine
  
--*/

#include <stdio.h>
#include "LzmaDecode.h"

#include <Common/UefiBaseTypes.h>

#define UTILITY_NAME "LzmaDecompress"
#define UTILITY_MAJOR_VERSION 0
#define UTILITY_MINOR_VERSION 1

#pragma warning(disable : 4100)

typedef struct {
  UINT32  Lc;
  UINT32  Lp;
  UINT32  Pb;
  UINT32  DictionarySize;
  UINT32  InternalSize;
  UINT8   Properties[5];
} LZMAPARAMETER;

STATIC UINT32 mSourceBufferSize = 0;

EFI_STATUS
GetFileContents (
  IN char    *InputFileName,
  OUT UINT8   *FileBuffer,
  OUT UINT32  *BufferLength
  );
  
EFI_STATUS
CustomDecompress (
  IN CONST VOID  *Source,
  IN OUT VOID    *Destination,
  IN OUT VOID    *Scratch
  );

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
  *Size   = Bo->Size; /* You can specify any available size here */
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
    "%s, LZMA Decompress Utility. Version %i.%i.\n",
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
//  printf ("Usage: "UTILITY_NAME "  -o OutputFile --version -v Verbose -q Quiet -d DebugLevel -h Help\n\n");
  printf ("Usage: "UTILITY_NAME "  [-o OutputFile] DecompressedFileName\n");
}

int
main (
  int  argc,
  char *argv[]
  )
{
  INTN                      Index;
  char                      *InputFileName;
  char                      *OutputFileName;
  FILE                      *OutFile, *InFile;
  VOID                      *Scratch;
  VOID                      *OutBuffer, *InputBuffer;
  EFI_STATUS                Status;
  UINT32                    InputFileSize;
  UINT32                    DstSize, ScratchSize;
  
  Scratch = NULL;
  OutBuffer = NULL;
  InputBuffer = NULL;
  InputFileSize = 0;
  DstSize = 0;
  ScratchSize = 0;
  //
  // Verify the correct number of arguments
  //
  if (argc == 1) {
    Usage();
    return 1;
  }
  
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
      Index++;
      if (Index == argc) {
      Index--;
      InputFileName = argv[Index];
      printf("\n%s is input file name\n", InputFileName);
      Index+=1;      
      if (Index == argc)
      OutputFileName = NULL;
      OutFile = stdout;
      break;      
      }
      else {
        printf("\nERROR Parameters!\n");
        Usage();
        return 1;  
      }
    }
    else if (strcmpi (argv[Index], "-o") == 0) {
      Index++;
      //
      // Output File specified
      //
      OutputFileName = argv[Index];
      printf("\n%s is output file name\n", OutputFileName);
      
      Index++;
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
      else {
        printf("\nERROR Parameters!\n");
        Usage();
        return 1;
      }
    }
    else {
      printf("\nERROR, Please input correct parameter!\n");
      Usage();
      return 1;
    }
    }

  //
  // We are done here to parse the input parameters
  //
  InFile = fopen(InputFileName,"rb");
  if (InFile == NULL) {
    printf("\nERROR to open input file!\n");
    return 1;
  }
  printf("\nSuccess to open input file!\n");
  if (OutputFileName != NULL) {
  OutFile = fopen (OutputFileName, "wb");
  if (OutFile == NULL) {
    printf ("%s failed to open output file for writing\n", OutputFileName);
    if (InFile != NULL) {
      fclose (InFile);
    }
    return 1;
  }
  printf("\nSuccess to open output file!\n");  
  }
  
  //
  // Copy input file contents to InputBuffer
  //
  Status = GetFileContents(
            InputFileName,
            InputBuffer,
            &InputFileSize);

  if (Status == EFI_BUFFER_TOO_SMALL) {
    InputBuffer = (VOID *) malloc (InputFileSize);
    if (InputBuffer == NULL) {
      printf ("application error", "failed to allocate memory\n");
      return EFI_OUT_OF_RESOURCES;
    }
    
    Status = GetFileContents (
              InputFileName,
              InputBuffer,
              &InputFileSize
              );
  }
              
  Status = CustomDecompressGetInfo(InputBuffer, InputFileSize, &DstSize, &ScratchSize);
  if (Status != RETURN_SUCCESS) {
    printf("\nERROR!\n");
  }
  
//  printf("\nDstSize is %i", DstSize);
//  printf("\nScratchSize is %i", ScratchSize);
  
  Scratch = (VOID *)malloc(ScratchSize);
  if (Scratch == NULL) {
    printf("\nNo enough memory to allocate!\n");
    if (InputBuffer != NULL) {
      free(InputBuffer);
    }
    return 1;
  }
  
  OutBuffer = (VOID *)malloc(DstSize);
  if (OutBuffer == NULL) {
    printf("\nNo enough memory to allocate!");
    if (InputBuffer != NULL) {
      free(InputBuffer);
    }    
    if (Scratch != NULL) {
      free(OutBuffer);
    }
    return 1;
  }
  Status = CustomDecompress(InputBuffer, OutBuffer, Scratch);
  if (Status != EFI_SUCCESS) {
    printf("\n ERROR in CustomDecompress");
    if (InputBuffer != NULL) {
      free(InputBuffer);
    }    
    if (Scratch != NULL) {
      free(Scratch);
    }
    if (OutBuffer != NULL) {
      free(OutBuffer);
    }
    return 1;
  }
  printf("\nStart to write file!\n");
  fwrite(OutBuffer, DstSize, 1, OutFile);
  free(InputBuffer);
  free(Scratch);
  free(OutBuffer);
  return 0;    
}

EFI_STATUS
GetFileContents (
  IN char    *InputFileName,
  OUT UINT8   *FileBuffer,
  OUT UINT32  *BufferLength
  )
/*++
        
Routine Description:
           
  Get the contents of file specified in InputFileName
  into FileBuffer.
            
Arguments:
               
  InputFileName  - Name of the input file.
                
  FileBuffer     - Output buffer to contain data

  BufferLength   - Actual length of the data 

Returns:
                       
  EFI_SUCCESS on successful return
  EFI_ABORTED if unable to open input file.

--*/
{
  UINTN   Size;
  UINTN   FileSize;
  INTN    Index;
  FILE    *InputFile;

  Size = 0;
  //
  // Copy the file contents to the output buffer.
  //
  InputFile = fopen (InputFileName, "rb");
    if (InputFile == NULL) {
      printf ("%s failed to open input file\n", InputFileName);
      return EFI_ABORTED;
    }
  
    fseek (InputFile, 0, SEEK_END);
    FileSize = ftell (InputFile);
    fseek (InputFile, 0, SEEK_SET);
    //
    // Now read the contents of the file into the buffer
    // 
    if (FileSize > 0 && FileBuffer != NULL) {
      if (fread (FileBuffer + Size, (size_t) FileSize, 1, InputFile) != 1) {
        printf ("%s failed to read contents of input file\n", InputFileName);
        fclose (InputFile);
        return EFI_ABORTED;
      }
    }

  fclose (InputFile);
  Size += (UINTN) FileSize;
  *BufferLength = Size;
  
  if (FileBuffer != NULL) {
    return EFI_SUCCESS;
  } else {
    return EFI_BUFFER_TOO_SMALL;
  }
}

