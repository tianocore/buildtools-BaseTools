/*++

Copyright (c)  1999 - 2002 Intel Corporation. 
All rights reserved. This program and the accompanying materials                      
are licensed and made available under the terms and conditions of the CPL License         
which accompanies this distribution.  The full text of the license may be found at        
http://opensource.org/licenses/cpl1.0.php                                          

THE PROGRAM IS DISTRIBUTED UNDER THE CPL LICENSE ON AN "AS IS" BASIS,                     
WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.

Module Name:
  
  LzmaConfig.h

Abstract:
  
--*/

#ifndef __LZMACONFIG_H
#define __LZMACONFIG_H

#if !defined (CONFIG_DICTIONARY_SIZE)
#define CONFIG_DICTIONARY_SIZE            (1<<23)
#endif

#if !defined (CONFIG_MATCHFINDER)
#define CONFIG_MATCHFINDER                L"BT4"
#endif 

#if !defined (CONFIG_FASTBYTES)
#define CONFIG_FASTBYTES                  128
#endif 

#if !defined (CONFIG_LITERAL_CONTEXT_BITS)
#define CONFIG_LITERAL_CONTEXT_BITS       3
#endif 

#if !defined (CONFIG_LITERAL_POSITION_BITS)
#define CONFIG_LITERAL_POSITION_BITS      0
#endif 

#if !defined (CONFIG_POSITION_BITS)
#define CONFIG_POSITION_BITS              2
#endif 

#endif
