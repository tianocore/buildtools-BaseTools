/*++

Copyright (c)  1999 - 2002 Intel Corporation. 
All rights reserved. This program and the accompanying materials                      
are licensed and made available under the terms and conditions of the CPL License         
which accompanies this distribution.  The full text of the license may be found at        
http://opensource.org/licenses/cpl1.0.php                                          

THE PROGRAM IS DISTRIBUTED UNDER THE CPL LICENSE ON AN "AS IS" BASIS,                     
WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.

Module Name:
  
  LzmaMain.cpp

Abstract:
  
--*/

#include "StdAfx.h"

#define EFI_MAX_BIT       0x80000000
#define EFIERR(a)       (EFI_MAX_BIT | (a)) 

#define EFI_SUCCESS                             0
#define EFI_INVALID_PARAMETER           EFIERR(2)
#define EFI_UNSUPPORTED                 EFIERR(3)
#define EFI_BUFFER_TOO_SMALL            EFIERR(5)
#define EFI_OUT_OF_RESOURCES            EFIERR(9)

#define INITGUID

typedef enum {
  NONE_TYPE,
  LZMA_TYPE
} COMPRESSTYPE;

#include "../Common/MyWindows.h"
#include "BufferStream.h"
#include "LzmaConfig.h"

// #include <limits.h>
#include <stdio.h>

#if defined(WIN32) || defined(OS2) || defined(MSDOS)
#include <fcntl.h>
#include <io.h>
#define MY_SET_BINARY_MODE(file) setmode(fileno(file),O_BINARY)
#else
#define MY_SET_BINARY_MODE(file)
#endif

#include "../Common/CommandLineParser.h"
#include "../Common/StringConvert.h"
#include "../Common/StringToInt.h"

#include "../7Zip/Common/FileStreams.h"
#include "../7Zip/Compress/LZMA/LZMADecoder.h"
#include "../7Zip/Compress/LZMA/LZMAEncoder.h"
#include "../7Zip/Compress/LZMA_ALONE/LzmaBench.h"

CMyComPtr<ISequentialInStream>  inStream;  
CMyComPtr<ISequentialOutStream> outStream;

COMPRESSTYPE  mCompressType = NONE_TYPE;

extern "C" 
int 
SetCustomizedCompressionType(
  CHAR            *Type
)
{
  if (strcmp(Type, "LZMA") == 0) {
    mCompressType = LZMA_TYPE;
    return EFI_SUCCESS;
  }
  return EFI_UNSUPPORTED;
}

extern "C" 
int 
CustomizedCompress(
  Byte            *SrcBuffer,
  UInt32          SrcSize,
  Byte            *DstBuffer,
  UInt32          *pDstSize  
)
{        
  UInt32   Status;
  UInt32   RequiredSize;
  UInt32   DstSize;
  UInt64   fileSize;
  
  inStream  = new CInBufferStream ((Byte*)SrcBuffer, SrcSize);    
  outStream = new COutBufferStream((Byte*)DstBuffer, *pDstSize);  

  DstSize  = *pDstSize;
  fileSize = SrcSize;
  
  NCompress::NLZMA::CEncoder *encoderSpec = new NCompress::NLZMA::CEncoder;
  CMyComPtr<ICompressCoder> encoder = encoderSpec;

  UInt32 dictionary       = CONFIG_DICTIONARY_SIZE;
  UInt32 posStateBits     = CONFIG_POSITION_BITS;
  UInt32 litContextBits   = CONFIG_LITERAL_CONTEXT_BITS; // for normal files
  UInt32 litPosBits       = CONFIG_LITERAL_POSITION_BITS;
  UInt32 algorithm        = 2;
  UInt32 numFastBytes     = CONFIG_FASTBYTES;
  UString mf              = CONFIG_MATCHFINDER;
           
  PROPID propIDs[] = 
  {
    NCoderPropID::kDictionarySize,
    NCoderPropID::kPosStateBits,
    NCoderPropID::kLitContextBits,
    NCoderPropID::kLitPosBits,
    NCoderPropID::kAlgorithm,
    NCoderPropID::kNumFastBytes,
    NCoderPropID::kMatchFinder,
    NCoderPropID::kEndMarker
  };
  const int kNumProps = sizeof(propIDs) / sizeof(propIDs[0]);
  /*
  NWindows::NCOM::CPropVariant properties[kNumProps];
  properties[0] = UInt32(dictionary);
  properties[1] = UInt32(posStateBits);
  properties[2] = UInt32(litContextBits);
  
  properties[3] = UInt32(litPosBits);
  properties[4] = UInt32(algorithm);
  properties[5] = UInt32(numFastBytes);
  properties[6] = mf;
  properties[7] = eos;
  */
  PROPVARIANT properties[kNumProps];
  for (int p = 0; p < 6; p++)
    properties[p].vt = VT_UI4;
  properties[0].ulVal = UInt32(dictionary);
  properties[1].ulVal = UInt32(posStateBits);
  properties[2].ulVal = UInt32(litContextBits);
  properties[3].ulVal = UInt32(litPosBits);
  properties[4].ulVal = UInt32(algorithm);
  properties[5].ulVal = UInt32(numFastBytes);
  
  properties[6].vt = VT_BSTR;
  properties[6].bstrVal = (BSTR)(const wchar_t *)mf;

  properties[7].vt = VT_BOOL;
  properties[7].boolVal = VARIANT_TRUE;

  encoderSpec->SetCoderProperties(propIDs, properties, kNumProps);
    
  encoderSpec->WriteCoderProperties(outStream);
  
  fileSize = (UInt64)SrcSize;
  
  for (int i = 0; i < 8; i++)
  {
    Byte b = Byte(fileSize >> (8 * i));
    outStream->Write(&b, sizeof(b), 0);    
  }
  
  HRESULT result = encoder->Code(inStream, outStream, 0, 0, 0);
  if (result == E_OUTOFMEMORY)
  {               
    Status = EFI_OUT_OF_RESOURCES;    // Out of memory
  } else if (result != S_OK) {   

    Status = EFI_INVALID_PARAMETER;   // Other failures
  } else {
    // Get actual required size	
    RequiredSize = outStream->Write(NULL, 0, NULL);
      *pDstSize = RequiredSize;

    if (RequiredSize > DstSize) { 
      Status = EFI_BUFFER_TOO_SMALL;  // Buffer too small
    } else {   
      Status = EFI_SUCCESS;           // OK    
    }
  }
    
  return Status;
}


extern "C" 
int 
CustomizedGetInfo (
  void   *Source,
  UInt32 SrcSize,
  UInt32 *DstSize,
  UInt32 *ScratchSize
  )
{
  UInt64 fileSize;

  inStream  = new CInBufferStream((Byte*)Source, SrcSize);    
   
  NCompress::NLZMA::CDecoder *decoderSpec = new NCompress::NLZMA::CDecoder;
    
  CMyComPtr<ICompressCoder> decoder = decoderSpec;
  if (decoderSpec->SetDecoderProperties(inStream) != S_OK)
  {
    return EFI_INVALID_PARAMETER;
  }

  fileSize = 0;
  for (int i = 0; i < 8; i++)
  {
    Byte b;
    UInt32 processedSize;
    inStream->Read(&b, sizeof(b), &processedSize);    
    fileSize |= ((UInt64)b) << (8 * i);
  }
  
  if (fileSize > 0xFFFFFFFF) {
    return EFI_INVALID_PARAMETER;
  }

  *DstSize     = (UInt32)fileSize;
  *ScratchSize = 0x10;
  return EFI_SUCCESS;
}


extern "C" 
int 
CustomizedDecompress(
  void   *Source,
  UInt32 SrcSize,
  void   *Destination,
  UInt32 DstSize,
  void   *Scratch,
  UInt32 ScratchSize
)
{        
  UInt64  fileSize;
  
  inStream  = new CInBufferStream ((Byte*)Source,      SrcSize);    
  outStream = new COutBufferStream((Byte*)Destination, DstSize);  
  
  NCompress::NLZMA::CDecoder *decoderSpec = new NCompress::NLZMA::CDecoder;
  CMyComPtr<ICompressCoder> decoder = decoderSpec;
  if (decoderSpec->SetDecoderProperties(inStream) != S_OK)
  {
    return EFI_INVALID_PARAMETER;
  }

  fileSize = 0;
  for (int i = 0; i < 8; i++)
  {
    Byte b;
    UInt32 processedSize;
    inStream->Read(&b, sizeof(b), &processedSize);    
    fileSize |= ((UInt64)b) << (8 * i);
  }
  
  if (decoder->Code(inStream, outStream, 0, &fileSize, 0) != S_OK)
  {  
    return EFI_INVALID_PARAMETER;
  }           
  return EFI_SUCCESS;
}
