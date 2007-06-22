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
        -i, --inputfile [FileName (FV.inf)]\n\
        -o, --outputfile [FileName (FileName.fv)]\n\
        -r, --baseaddress (0x##### or #####)\n\
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
  EFI_STATUS  Status;
  CHAR8       *InfFileName;
  CHAR8       *InfFileImage;
  UINTN       InfFileSize;
  CHAR8       *FvFileName;
  EFI_PHYSICAL_ADDRESS XipBase;

  InfFileName   = NULL;
  InfFileImage  = NULL;
  FvFileName    = NULL;
  XipBase       = -1;
  InfFileSize   = 0;

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
      FvFileName = argv[1];
      if (FvFileName == NULL) {
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
  // Call the GenFvImageFunction to generate Fv Image
  //
  Status = GenerateFvImage (
            InfFileImage,
            InfFileSize,
            FvFileName,
            XipBase
            );

  //
  // free InfFileImage memory
  //
  free (InfFileImage);

  if (EFI_ERROR (Status)) {
    switch (Status) {

    case EFI_INVALID_PARAMETER:
      Error (NULL, 0, 0, "invalid parameter passed to GenerateFvImage", NULL);
      return GetUtilityStatus ();
      break;

    case EFI_ABORTED:
      Error (NULL, 0, 0, "error detected while creating the file image", NULL);
      return GetUtilityStatus ();
      break;

    case EFI_OUT_OF_RESOURCES:
      Error (NULL, 0, 0, "GenFvImage Lib could not allocate required resources", NULL);
      return GetUtilityStatus ();
      break;

    case EFI_VOLUME_CORRUPTED:
      Error (NULL, 0, 0, "no base address was specified, but the FV.INF included a PEI or BSF file", NULL);
      return GetUtilityStatus ();
      break;

    case EFI_LOAD_ERROR:
      Error (NULL, 0, 0, "could not load FV image generation library", NULL);
      return GetUtilityStatus ();
      break;

    default:
      Error (NULL, 0, 0, "GenFvImage Lib returned unknown status", "status returned = 0x%X", Status);
      return GetUtilityStatus ();
      break;
    }
  }

  return GetUtilityStatus ();
}
