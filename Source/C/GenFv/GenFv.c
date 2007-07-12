/*++

Copyright (c) 2007, Intel Corporation                                                         
All rights reserved. This program and the accompanying materials                          
are licensed and made available under the terms and conditions of the BSD License         
which accompanies this distribution.  The full text of the license may be found at        
http://opensource.org/licenses/bsd-license.php                                            
                                                                                          
THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,                     
WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.             

Module Name:

  GenFv.c

Abstract:

  This contains all code necessary to build the GenFvImage.exe utility.       
  This utility relies heavily on the GenFvImage Lib.  Definitions for both
  can be found in the Tiano Firmware Volume Generation Utility 
  Specification, review draft.

--*/

//
// File included in build
//
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "CommonLib.h"
#include "GenFvInternalLib.h"
#include "EfiUtilityMsgs.h"

//
// Utility Name
//
#define UTILITY_NAME  "GenFv"

//
// Utility version information
//
#define UTILITY_MAJOR_VERSION 0
#define UTILITY_MINOR_VERSION 1

EFI_STATUS
ParseCapInf (
  IN  MEMORY_FILE  *InfFile,
  OUT CAP_INFO     *CapInfo
  );

static
void 
Version(
  void
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
  printf ("%s v%d.%d - EDKII Firmware Volume Generation Utility.\n", UTILITY_NAME, UTILITY_MAJOR_VERSION, UTILITY_MINOR_VERSION);
  printf ("Copyright (c) 2007 Intel Corporation. All rights reserved.\n");
}
 

static
void 
Usage(
  void
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
  Version();

  printf ("\nUsage: " UTILITY_NAME "\n\
        -i, --inputfile [FileName (FV.inf or Cap.inf)]\n\
        -o, --outputfile [FileName (FileName.fv)]\n\
        -r, --baseaddress (0x##### or #####)\n\
        -c, --capsule\n\
        -h, --help\n\
        -V, --version\n");
}

int
main (
  IN INTN   argc,
  IN CHAR8  **argv
  )
/*++

Routine Description:

  This utility uses GenFvImage.Lib to build a firmware volume image.

Arguments:

  FvInfFileName      The name of an FV image description file.

  Arguments come in pair in any order.
    -I FvInfFileName 

Returns:

  EFI_SUCCESS            No error conditions detected.
  EFI_INVALID_PARAMETER  One or more of the input parameters is invalid.
  EFI_OUT_OF_RESOURCES   A resource required by the utility was unavailable.  
                         Most commonly this will be memory allocation 
                         or file creation.
  EFI_LOAD_ERROR         GenFvImage.lib could not be loaded.
  EFI_ABORTED            Error executing the GenFvImage lib.

--*/
{
  EFI_STATUS            Status;
  CHAR8                 *InfFileName;
  CHAR8                 *InfFileImage;
  UINTN                 InfFileSize;
  CHAR8                 *OutFileName;
  EFI_PHYSICAL_ADDRESS  XipBase;
  UINT8                 CapsuleFlag;
  CAP_INFO              CapInfo;
  MEMORY_FILE           InfMemoryFile;
  FILE                  *fpin, *fpout;
  UINT32                FileSize;
  UINT32                CapSize;
  UINT8                 *CapBuffer;
  EFI_CAPSULE_HEADER    *CapsuleHeader;
  UINT32                Index;

  InfFileName   = NULL;
  InfFileImage  = NULL;
  OutFileName   = NULL;
  XipBase       = -1;
  InfFileSize   = 0;
  CapsuleFlag   = 0;
  fpin          = NULL;
  fpout         = NULL;
  FileSize      = 0;
  CapSize       = 0;
  Index         = 0;
  CapBuffer     = NULL;
  CapsuleHeader = NULL;

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
    if ((stricmp (argv[0], "-i") == 0) || (stricmp (argv[0], "--inputfile") == 0)) {
      InfFileName = argv[1];
      if (InfFileName == NULL) {
        Warning (NULL, 0, 0, NULL, "No input file specified.");
      }
      argc -= 2;
      argv += 2;
      continue; 
    }

    if ((stricmp (argv[0], "-o") == 0) || (stricmp (argv[0], "--outputfile") == 0)) {
      OutFileName = argv[1];
      if (OutFileName == NULL) {
        Warning (NULL, 0, 0, NULL, "No output file specified.");
      }
      argc -= 2;
      argv += 2;
      continue; 
    }

    if ((stricmp (argv[0], "-r") == 0) || (stricmp (argv[0], "--baseaddr") == 0)) {
      Status = AsciiStringToUint64 (argv[1], FALSE, &XipBase);
      if (EFI_ERROR (Status)) {
        Error (NULL, 0, 0, "Input paramter is not one valid integrator.", NULL);
        return STATUS_ERROR;        
      }
      argc -= 2;
      argv += 2;
      continue; 
    }

    if ((stricmp (argv[0], "-c") == 0) || (stricmp (argv[0], "--capsule") == 0)) {
      CapsuleFlag = 1;
      argc --;
      argv ++;
      continue; 
    }
    //
    // Don't recognize the paramter.
    //
    Error (NULL, 0, 0, NULL, "%s is invaild paramter!", argv[0]);
    return STATUS_ERROR;
  }

  //
  // Read the INF file image
  //
  Status = GetFileImage (InfFileName, &InfFileImage, &InfFileSize);
  if (EFI_ERROR (Status)) {
    return STATUS_ERROR;
  }

  //
  // Create Capsule Header
  //
  if (CapsuleFlag) {
    //
    // Initialize file structures
    //
    InfMemoryFile.FileImage           = InfFileImage;
    InfMemoryFile.CurrentFilePointer  = InfFileImage;
    InfMemoryFile.Eof                 = InfFileImage + InfFileSize;

    //
    // Parse the Cap inf file for header information
    //
    Status = ParseCapInf (&InfMemoryFile, &CapInfo);
    if (Status != EFI_SUCCESS) {
      goto Finish;
    }
    
    if (CapInfo.HeaderSize == 0) {
      CapInfo.HeaderSize = sizeof (EFI_CAPSULE_HEADER);
    }

    if (CapInfo.HeaderSize < sizeof (EFI_CAPSULE_HEADER)) {
      Error (NULL, 0, 0, NULL, "The specified HeaderSize can't be less than the size of EFI_CAPSULE_HEADER.");
      goto Finish;
    }
    
    //
    // Calculate the size of capsule image.
    //
    Index    = 0;
    FileSize = 0;
    CapSize  = sizeof (EFI_CAPSULE_HEADER);
    while (CapInfo.CapFiles [Index][0] != '\0') {
      fpin = fopen (CapInfo.CapFiles[Index], "rb");
      if (fpin == NULL) {
        Error (NULL, 0, 0, NULL, "%s could not open for reading", CapInfo.CapFiles[Index]);
        goto Finish;
      }
      FileSize  = _filelength (fileno (fpin));
      CapSize  += FileSize;
      fclose (fpin);
      Index ++;
    }

    //
    // Allocate buffer for capsule image.
    //
    CapBuffer = (UINT8 *) malloc (CapSize);
    if (CapBuffer == NULL) {
      Error (NULL, 0, 0, NULL, "could not allocate enough memory space for capsule");
      goto Finish;
    }

    //
    // Initialize the capsule header to zero
    //
    memset (CapBuffer, 0, sizeof (EFI_CAPSULE_HEADER));
    
    //
    // create capsule header and get capsule body
    //
    CapsuleHeader = (EFI_CAPSULE_HEADER *) CapBuffer;
    memcpy (&CapsuleHeader->CapsuleGuid, &CapInfo.CapGuid, sizeof (EFI_GUID));
    CapsuleHeader->HeaderSize       = CapInfo.HeaderSize;
    CapsuleHeader->Flags            = CapInfo.Flags;
    CapsuleHeader->CapsuleImageSize = CapSize;

    Index    = 0;
    FileSize = 0;
    CapSize  = CapsuleHeader->HeaderSize;
    while (CapInfo.CapFiles [Index][0] != '\0') {
      fpin = fopen (CapInfo.CapFiles[Index], "rb");
      if (fpin == NULL) {
        Error (NULL, 0, 0, NULL, "%s could not open for reading", CapInfo.CapFiles[Index]);
        goto Finish;
      }
      FileSize = _filelength (fileno (fpin));
      fread (CapBuffer + CapSize, 1, FileSize, fpin);
      fclose (fpin);
      Index ++;
      CapSize += FileSize;
    }
    
    //
    // write capsule data into the output file
    //
    if (OutFileName == NULL) {
      fpout = stdout;
    } else {
      fpout = fopen (OutFileName, "wb");
      if (fpout == NULL) {
        Error (NULL, 0, 0, NULL, "could not open %s file for writing", OutFileName);
        free (CapBuffer);
        goto Finish;
      }
    }
    fwrite (CapBuffer, 1, CapSize, fpout);
    fclose (fpout);

  } else {
    //
    // Call the GenFvImageFunction to generate Fv Image
    //
    GenerateFvImage (
      InfFileImage,
      InfFileSize,
      OutFileName,
      XipBase
      );
  }

Finish:
  //
  // free InfFileImage memory
  //
  free (InfFileImage);

  return GetUtilityStatus ();
}

EFI_STATUS
ParseCapInf (
  IN  MEMORY_FILE  *InfFile,
  OUT CAP_INFO     *CapInfo
  )
/*++

Routine Description:

  This function parses a Cap.INF file and copies info into a CAP_INFO structure.

Arguments:

  InfFile        Memory file image.
  CapInfo        Information read from INF file.

Returns:

  EFI_SUCCESS       INF file information successfully retrieved.
  EFI_ABORTED       INF file has an invalid format.
  EFI_NOT_FOUND     A required string was not found in the INF file.
--*/
{
  CHAR8       Value[_MAX_PATH];
  UINT64      Value64;
  UINTN       Index;
  EFI_STATUS  Status;

  //
  // Initialize Cap info
  //
  memset (CapInfo, 0, sizeof (CAP_INFO));

  //
  // Read the Capsule Guid
  //
  Status = FindToken (InfFile, OPTIONS_SECTION_STRING, EFI_CAPSULE_GUID_STRING, 0, Value);
  if (Status == EFI_SUCCESS) {
    //
    // Get the Capsule Guid
    //
    Status = StringToGuid (Value, &CapInfo->CapGuid);
    if (EFI_ERROR (Status)) {
      Error (NULL, 0, 0, EFI_CAPSULE_GUID_STRING, "not valid guid value");
      return EFI_ABORTED;
    }
  } else {
    Error (NULL, 0, 0, EFI_CAPSULE_GUID_STRING, "is not specified.");
    return EFI_ABORTED;
  }

  //
  // Read the Capsule Header Size
  //
  Status = FindToken (InfFile, OPTIONS_SECTION_STRING, EFI_CAPSULE_HEADER_SIZE_STRING, 0, Value);
  if (Status == EFI_SUCCESS) {
    Status = AsciiStringToUint64 (Value, FALSE, &Value64);
    if (EFI_ERROR (Status)) {
      Error (NULL, 0, 0, Value, "invalid value for %s", EFI_CAPSULE_HEADER_SIZE_STRING);
      return EFI_ABORTED;
    }
    CapInfo->HeaderSize = (UINT32) Value64;
  }

  //
  // Read the Capsule Flag
  //
  Status = FindToken (InfFile, OPTIONS_SECTION_STRING, EFI_CAPSULE_FLAGS_STRING, 0, Value);
  if (Status == EFI_SUCCESS) {
    if (stricmp (Value, "PersistAcrossReset") == 0) {
      CapInfo->Flags = CAPSULE_FLAGS_PERSIST_ACROSS_RESET; 
    } else if (stricmp (Value, "PopulateSystemTable") == 0) {
      CapInfo->Flags = CAPSULE_FLAGS_PERSIST_ACROSS_RESET | CAPSULE_FLAGS_POPULATE_SYSTEM_TABLE;
    } else {
      Error (NULL, 0, 0, Value, "invalid Flag setting for %s", EFI_CAPSULE_FLAGS_STRING);
      return EFI_ABORTED;
    }
  }
  
  //
  // Read the Capsule Version
  //
  Status = FindToken (InfFile, OPTIONS_SECTION_STRING, EFI_CAPSULE_VERSION_STRING, 0, Value);
  if (Status == EFI_SUCCESS) {
    if (stricmp (Value, "UEFI") == 0) {
      CapInfo->Version = 0x20000;  
    } else if (stricmp (Value, "FRAMEWORK") == 0) {
      CapInfo->Version = 0x10010;
      Error (NULL, 0, 0, Value, "is not supported Version for %s", EFI_CAPSULE_VERSION_STRING);
      return EFI_ABORTED;
    } else {
      Error (NULL, 0, 0, Value, "invalid Version setting for %s", EFI_CAPSULE_VERSION_STRING);
      return EFI_ABORTED;
    }
  }

  //
  // Read the Capsule FileImage
  //
  for (Index = 0; Index < MAX_NUMBER_OF_FILES_IN_CAP; Index++) {
    //
    // Read the capsule file name
    //
    Status = FindToken (InfFile, FILES_SECTION_STRING, EFI_FILE_NAME_STRING, Index, Value);

    if (Status == EFI_SUCCESS) {
      //
      // Add the file
      //
      strcpy (CapInfo->CapFiles[Index], Value);
    } else {
      break;
    }
  }
  
  if (Index == 0) {
    printf("Cap Files are not specified.\n");
  }

  return EFI_SUCCESS;
}