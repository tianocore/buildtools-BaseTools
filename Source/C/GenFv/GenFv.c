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
#include "GenFvInternalLib.h"

//
// Utility Name
//
#define UTILITY_NAME  "GenFv"

//
// Utility version information
//
#define UTILITY_MAJOR_VERSION 0
#define UTILITY_MINOR_VERSION 1

BOOLEAN VerboseMode = FALSE;

static
void 
Version (
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
  fprintf (stdout, "%s Version %d.%d\n", UTILITY_NAME, UTILITY_MAJOR_VERSION, UTILITY_MINOR_VERSION);
}

static
void 
Usage (
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
  //
  // Summary usage
  //
  fprintf (stdout, "Usage: %s [options]\n\n", UTILITY_NAME);
  
  //
  // Copyright declaration
  // 
  fprintf (stdout, "Copyright (c) 2007, Intel Corporation. All rights reserved.\n\n");

  //
  // Details Option
  //
  fprintf (stdout, "Options:\n");
  fprintf (stdout, "  -o FileName, --outputfile FileName\n\
                        File is the FvImage or CapImage to be created.\n");
  fprintf (stdout, "  -i FileName, --inputfile FileName\n\
                        File is the input FV.inf or Cap.inf to specify\n\
                        how to construct FvImage or CapImage.\n");
  fprintf (stdout, "  -r Address, --baseaddr Address\n\
                        Address is the rebase start address for drivers that\n\
                        run in Flash. It supports DEC or HEX digital format.\n");
  fprintf (stdout, "  -b Address, --bootbaseaddr Address\n\
                        Address is the boot time driver base address, which is\n\
                        used to define the prefered loaded address for all\n\
                        boot time drivers in this Fv image.\n\
                        It supports DEC or HEX digital format.\n");
  fprintf (stdout, "  -t Address, --runtimebaseaddr Address\n\
                        Address is the runtime driver base address, which is\n\
                        used to define the prefered loaded address for all\n\
                        runtime drivers in this Fv image.\n\
                        It supports DEC or HEX digital format.\n");
  fprintf (stdout, "  -c, --capsule         Create Capsule Image.\n");
  fprintf (stdout, "  -v, --verbose         Turn on verbose output with informational messages.\n");
  fprintf (stdout, "  --version             Show program's version number and exit.\n");
  fprintf (stdout, "  -h, --help            Show this help message and exit.\n");
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
  EFI_PHYSICAL_ADDRESS  BtBase;
  EFI_PHYSICAL_ADDRESS  RtBase;
  BOOLEAN               CapsuleFlag;

  InfFileName   = NULL;
  InfFileImage  = NULL;
  OutFileName   = NULL;
  XipBase       = -1;
  BtBase        = 0;
  RtBase        = 0;
  InfFileSize   = 0;
  CapsuleFlag   = FALSE;

  SetUtilityName (UTILITY_NAME);

  if (argc == 1) {
    Error (NULL, 0, 1001, "Missing options", "Input file");
    Usage ();
    return STATUS_ERROR;
  }

  //
  // Parse command line
  //
  argc --;
  argv ++;

  if ((stricmp (argv[0], "-h") == 0) || (stricmp (argv[0], "--help") == 0)) {
    Usage ();
    return STATUS_SUCCESS;    
  }

  if (stricmp (argv[0], "--version") == 0) {
    Version ();
    return STATUS_SUCCESS;    
  }

  while (argc > 0) {
    if ((stricmp (argv[0], "-i") == 0) || (stricmp (argv[0], "--inputfile") == 0)) {
      InfFileName = argv[1];
      argc -= 2;
      argv += 2;
      continue; 
    }

    if ((stricmp (argv[0], "-o") == 0) || (stricmp (argv[0], "--outputfile") == 0)) {
      OutFileName = argv[1];
      argc -= 2;
      argv += 2;
      continue; 
    }

    if ((stricmp (argv[0], "-r") == 0) || (stricmp (argv[0], "--baseaddr") == 0)) {
      Status = AsciiStringToUint64 (argv[1], FALSE, &XipBase);
      if (EFI_ERROR (Status)) {
        Error (NULL, 0, 1003, "Invalid option value", "%s = %s", argv[0], argv[1]);
        return STATUS_ERROR;        
      }
      argc -= 2;
      argv += 2;
      continue; 
    }

    if ((stricmp (argv[0], "-b") == 0) || (stricmp (argv[0], "--bootbaseaddr") == 0)) {
      Status = AsciiStringToUint64 (argv[1], FALSE, &BtBase);
      if (EFI_ERROR (Status)) {
        Error (NULL, 0, 1003, "Invalid option value", "%s = %s", argv[0], argv[1]);
        return STATUS_ERROR;        
      }
      argc -= 2;
      argv += 2;
      continue; 
    }

    if ((stricmp (argv[0], "-t") == 0) || (stricmp (argv[0], "--runtimebaseaddr") == 0)) {
      Status = AsciiStringToUint64 (argv[1], FALSE, &RtBase);
      if (EFI_ERROR (Status)) {
        Error (NULL, 0, 1003, "Invalid option value", "%s = %s", argv[0], argv[1]);
        return STATUS_ERROR;        
      }
      argc -= 2;
      argv += 2;
      continue; 
    }

    if ((stricmp (argv[0], "-c") == 0) || (stricmp (argv[0], "--capsule") == 0)) {
      CapsuleFlag = TRUE;
      argc --;
      argv ++;
      continue; 
    }

    if ((stricmp (argv[0], "-v") == 0) || (stricmp (argv[0], "--verbose") == 0)) {
      VerboseMode = TRUE;
      argc --;
      argv ++;
      continue;
    }
    //
    // Don't recognize the paramter.
    //
    Error (NULL, 0, 1000, "Unknown option", "%s", argv[0]);
    return STATUS_ERROR;
  }

  if (VerboseMode) {
    fprintf (stdout, "%s tool start.\n", UTILITY_NAME);
  }
  
  //
  // check input parameter
  //
  if (InfFileName == NULL) {
    Error (NULL, 0, 1001, "Missing Option", "Input File");
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
    // Call the GenerateCapImage to generate Capsule Image
    //
    GenerateCapImage (
      InfFileImage, 
      InfFileSize,
      OutFileName
      );
  } else {
    //
    // Call the GenerateFvImage to generate Fv Image
    //
    GenerateFvImage (
      InfFileImage,
      InfFileSize,
      OutFileName,
      XipBase,
      BtBase,
      RtBase
      );
  }

  //
  // free InfFileImage memory
  //
  if (InfFileImage == NULL) {
    free (InfFileImage);
  }

  if (VerboseMode) {
    fprintf (stdout, "%s tool done with return code is 0x%x.\n", UTILITY_NAME, GetUtilityStatus ());  
  }

  return GetUtilityStatus ();
}