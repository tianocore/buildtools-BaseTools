/** @file
  Stub routines without ELF support

  Copyright (c) 2009, Intel Corporation
  All rights reserved. This program and the accompanying materials
  are licensed and made available under the terms and conditions of the BSD License
  which accompanies this distribution.  The full text of the license may be found at
  http://opensource.org/licenses/bsd-license.php

  THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
  WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.

**/

#include <Common/UefiBaseTypes.h>

#if defined(unix) || defined(linux)
#if defined (__i386__) || defined(__x86_64__)
#define HAVE_ELF
#endif
#endif

#ifndef HAVE_ELF

INTN
IsElfHeader (
  UINT8  *FileBuffer
  )
{
  return 0 == 1;
}

VOID
ConvertElf (
  UINT8  **FileBuffer,
  UINT32 *FileLength
  )
{
}

#endif // HAVE_ELF

