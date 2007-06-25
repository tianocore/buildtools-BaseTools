/*++

Copyright (c)  1999 - 2002 Intel Corporation. 
All rights reserved. This program and the accompanying materials                      
are licensed and made available under the terms and conditions of the CPL License         
which accompanies this distribution.  The full text of the license may be found at        
http://opensource.org/licenses/cpl1.0.php                                          

THE PROGRAM IS DISTRIBUTED UNDER THE CPL LICENSE ON AN "AS IS" BASIS,                     
WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.

Module Name:
  
  BufferStream.h

Abstract:
  
--*/

#ifndef __BUFFERSTREAM_H
#define __BUFFERSTREAM_H

#ifdef WIN32
#include "../Windows/FileIO.h"
#else
#include "../Common/C_FileIO.h"
#endif

#include "../7Zip/IStream.h"
#include "../Common/MyCom.h"

class CInBufferStream :
  public ISequentialInStream,
  public CMyUnknownImp
{
/* */
public:
  //
  // HANDLE File;
  // CStdInFileStream() File(INVALID_HANDLE_VALUE): {}
  // void Open() { File = GetStdHandle(STD_INPUT_HANDLE); };
  //
  MY_UNKNOWN_IMP

  STDMETHOD (Read) (void *data, UInt32 size, UInt32 *processedSize);
  STDMETHOD (ReadPart) (void *data, UInt32 size, UInt32 *processedSize);

  CInBufferStream (
    Byte   *Base,
    UInt32 Size
    )
/*++

Routine Description:

  GC_TODO: Add function description

Arguments:

  Base  - GC_TODO: add argument description
  Size  - GC_TODO: add argument description

Returns:

  GC_TODO: add return values

--*/
;

/* */
private:
  Byte    *InBufferBase;
  UInt32  InBufferSize;
  Byte    *CurrentPtr;
};

class COutBufferStream :
  public ISequentialOutStream,
  public CMyUnknownImp
{
/* */
public:
  MY_UNKNOWN_IMP

  STDMETHOD (Write) (const void *data, UInt32 size, UInt32 *processedSize);
  STDMETHOD (WritePart) (const void *data, UInt32 size, UInt32 *processedSize);

  COutBufferStream (
    Byte *Base,
    UInt32
    )
/*++

Routine Description:

  GC_TODO: Add function description

Arguments:

  Base    - GC_TODO: add argument description
  UInt32  - GC_TODO: add argument description

Returns:

  GC_TODO: add return values

--*/
;

/* */
private:
  Byte    *OutBufferBase;
  UInt32  OutBufferSize;
  Byte    *CurrentPtr;
  UInt32  RequiredSize;
};

#endif
