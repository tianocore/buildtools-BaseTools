/*++

Copyright (c)  1999 - 2002 Intel Corporation. 
All rights reserved. This program and the accompanying materials                      
are licensed and made available under the terms and conditions of the CPL License         
which accompanies this distribution.  The full text of the license may be found at        
http://opensource.org/licenses/cpl1.0.php                                          

THE PROGRAM IS DISTRIBUTED UNDER THE CPL LICENSE ON AN "AS IS" BASIS,                     
WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.

Module Name:
  
  BufferStream.cpp

Abstract:
  
--*/

#include "StdAfx.h"

#include "Windows.h"
#include "..\7Zip\Common\FileStreams.h"
#include "BufferStream.h"

CInBufferStream::CInBufferStream(Byte *Base, UInt32 Size)
{
  InBufferBase = Base;
  InBufferSize = Size; 
  CurrentPtr   = Base;  
}

COutBufferStream::COutBufferStream(Byte *Base, UInt32 Size)
{
  OutBufferBase = Base;
  OutBufferSize = Size; 
  CurrentPtr    = Base;
  RequiredSize  = 0;
}

STDMETHODIMP CInBufferStream::Read(void *data, UInt32 size, UInt32 *processedSize)
{  
  if (data == NULL) return S_FALSE;
  
  if   (CurrentPtr == InBufferBase + InBufferSize)  size = 0;    
  else if (CurrentPtr + size > InBufferBase + InBufferSize) {    
    size = (InBufferBase + InBufferSize) - CurrentPtr;    
  }  
 
  memcpy(data, CurrentPtr, size);
  CurrentPtr += size;
  
  if (processedSize != NULL)   *processedSize = size;
      
  return S_OK;  
}
  
STDMETHODIMP CInBufferStream::ReadPart(void *data, UInt32 size, UInt32 *processedSize)
{
  return Read(data, size, processedSize);
}


STDMETHODIMP COutBufferStream::Write(const void *data, UInt32 size, UInt32 *processedSize)
{
  
  if (data == NULL) {
    return RequiredSize;	  
  }
  
  UInt32 realProcessedSize;    
  BOOL res = TRUE;
  Byte  *pData;
  
  pData = (Byte *)data;
  RequiredSize += size;
  
  if(processedSize != NULL) *processedSize = size;
  
  while (size > 0)
  {
    // Seems that Windows doesn't like big amounts writing to stdout.
    // So we limit portions by 32KB.
    UInt32 sizeTemp = (1 << 15); 
    if (sizeTemp > size) sizeTemp = size;
    
    realProcessedSize = 0;
    
    while (CurrentPtr < OutBufferBase + OutBufferSize) {
      if (realProcessedSize < sizeTemp) {
      	*CurrentPtr++ = *pData++;      	
		realProcessedSize++;
      } else {
      	break;
      }     
    }    
    
    size -= sizeTemp;
    data = (const void *)((const Byte *)data + realProcessedSize);    
  }
      
  return S_OK;  
}
  
STDMETHODIMP COutBufferStream::WritePart(const void *data, UInt32 size, UInt32 *processedSize)
{
  return Write(data, size, processedSize);
}
