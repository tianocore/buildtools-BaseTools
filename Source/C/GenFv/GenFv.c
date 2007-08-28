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
  fprintf (stdout, "  -a AddressFile, --addrfile AddressFile\n\
                        AddressFile is one file used to record boot driver base\n\
                        address and runtime driver base address. And this tool\n\
                        will update these two addresses after it relocates all\n\
                        boot drivers and runtime drivers in this fv iamge to\n\
                        the preferred loaded memory address.\n");
  fprintf (stdout, "  -m logfile, --map logfile\n\
                        Logfile is the output fv map file name. if it is not\n\
                        given, the FvName.map will be the default map file name\n"); 
  fprintf (stdout, "  -c, --capsule         Create Capsule Image.\n");
  fprintf (stdout, "  -p, --dump            Dump Capsule Image header.\n");
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

  FvInfFileName      The name of an FV image description file or Capsule Image.

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
  CHAR8                 *AddrFileName;
  CHAR8                 *MapFileName;
  CHAR8                 *InfFileImage;
  UINTN                 InfFileSize;
  CHAR8                 *OutFileName;
  CHAR8                 ValueString[_MAX_PATH];
  EFI_PHYSICAL_ADDRESS  XipBase;
  EFI_PHYSICAL_ADDRESS  BtBase;
  EFI_PHYSICAL_ADDRESS  RtBase;
  BOOLEAN               CapsuleFlag;
  BOOLEAN               DumpCapsule;
  MEMORY_FILE           AddrMemoryFile;
  FILE                  *FpFile;
  EFI_CAPSULE_HEADER    *CapsuleHeader;

  InfFileName   = NULL;
  AddrFileName  = NULL;
  InfFileImage  = NULL;
  OutFileName   = NULL;
  MapFileName   = NULL;
  XipBase       = -1;
  BtBase        = 0;
  RtBase        = 0;
  InfFileSize   = 0;
  CapsuleFlag   = FALSE;
  DumpCapsule   = FALSE;
  FpFile        = NULL;
  CapsuleHeader = NULL;

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
    Version ();
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

    if ((stricmp (argv[0], "-a") == 0) || (stricmp (argv[0], "--addrfile") == 0)) {
      AddrFileName = argv[1];
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

    if ((stricmp (argv[0], "-c") == 0) || (stricmp (argv[0], "--capsule") == 0)) {
      CapsuleFlag = TRUE;
      argc --;
      argv ++;
      continue; 
    }

    if ((stricmp (argv[0], "-p") == 0) || (stricmp (argv[0], "--dump") == 0)) {
      DumpCapsule = TRUE;
      argc --;
      argv ++;
      continue; 
    }

    if ((stricmp (argv[0], "-m") == 0) || (stricmp (argv[0], "--map") == 0)) {
      MapFileName = argv[1];
      argc -= 2;
      argv += 2;
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

  if (!DumpCapsule && OutFileName == NULL) {
    Error (NULL, 0, 1001, "Missing option", "Output file name");
    return STATUS_ERROR;
  }
  
  //
  // Read boot and runtime address from address file
  //
  if (AddrFileName != NULL) {
    Status = GetFileImage (AddrFileName, &InfFileImage, &InfFileSize);
    if (EFI_ERROR (Status)) {
      return STATUS_ERROR;
    }

    AddrMemoryFile.FileImage           = InfFileImage;
    AddrMemoryFile.CurrentFilePointer  = InfFileImage;
    AddrMemoryFile.Eof                 = InfFileImage + InfFileSize;

    //
    // Read the boot driver base address for this FV image
    //
    Status = FindToken (&AddrMemoryFile, OPTIONS_SECTION_STRING, EFI_FV_BOOT_DRIVER_BASE_ADDRESS_STRING, 0, ValueString);
    if (Status == EFI_SUCCESS) {
      //
      // Get the base address
      //
      Status = AsciiStringToUint64 (ValueString, FALSE, &BtBase);
      if (EFI_ERROR (Status)) {
        Error (NULL, 0, 2000, "Invalid paramter", "%s = %s", EFI_FV_BOOT_DRIVER_BASE_ADDRESS_STRING, ValueString);
        return STATUS_ERROR;
      }
    }
  
    //
    // Read the FV runtime driver base address
    //
    Status = FindToken (&AddrMemoryFile, OPTIONS_SECTION_STRING, EFI_FV_RUNTIME_DRIVER_BASE_ADDRESS_STRING, 0, ValueString);
    if (Status == EFI_SUCCESS) {
      //
      // Get the base address
      //
      Status = AsciiStringToUint64 (ValueString, FALSE, &RtBase);
      if (EFI_ERROR (Status)) {
        Error (NULL, 0, 2000, "Invalid paramter", "%s = %s", EFI_FV_RUNTIME_DRIVER_BASE_ADDRESS_STRING, ValueString);
        return STATUS_ERROR;
      }
    }
    
    //
    // free the allocated memory space for addr file.
    //
    free (InfFileImage);
  }

  //
  // Read the INF file image
  //
  Status = GetFileImage (InfFileName, &InfFileImage, &InfFileSize);
  if (EFI_ERROR (Status)) {
    return STATUS_ERROR;
  }
  
  if (DumpCapsule) {
    //
    // Dump Capsule Image Header Information
    //
    CapsuleHeader = (EFI_CAPSULE_HEADER *) InfFileImage;
    if (OutFileName == NULL) {
      FpFile = stdout;
    } else {
      FpFile = fopen (OutFileName, "w");
      if (FpFile == NULL) {
        Error (NULL, 0, 0001, "Error opening file", OutFileName);
        return STATUS_ERROR;
      }
    }
    fprintf (FpFile, "Capsule %s Image Header Information\n", InfFileName);
    fprintf (FpFile, "  GUID                  %08X-%04X-%04X-%02X%02X-%02X%02X%02X%02X%02X%02X\n", 
                    CapsuleHeader->CapsuleGuid.Data1,
                    (UINT32) CapsuleHeader->CapsuleGuid.Data2,
                    (UINT32) CapsuleHeader->CapsuleGuid.Data3,
                    (UINT32) CapsuleHeader->CapsuleGuid.Data4[0],
                    (UINT32) CapsuleHeader->CapsuleGuid.Data4[1],
                    (UINT32) CapsuleHeader->CapsuleGuid.Data4[2],
                    (UINT32) CapsuleHeader->CapsuleGuid.Data4[3],
                    (UINT32) CapsuleHeader->CapsuleGuid.Data4[4],
                    (UINT32) CapsuleHeader->CapsuleGuid.Data4[5],
                    (UINT32) CapsuleHeader->CapsuleGuid.Data4[6],
                    (UINT32) CapsuleHeader->CapsuleGuid.Data4[7]);
    fprintf (FpFile, "  Header size           0x%08X\n", CapsuleHeader->HeaderSize);
    fprintf (FpFile, "  Flags                 0x%08X\n", CapsuleHeader->Flags);
    fprintf (FpFile, "  Capsule image size    0x%08X\n", CapsuleHeader->CapsuleImageSize);
    fclose (FpFile);
  } else if (CapsuleFlag) {
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
      MapFileName,
      XipBase,
      &BtBase,
      &RtBase
      );
  }

  //
  // free InfFileImage memory
  //
  if (InfFileImage != NULL) {
    free (InfFileImage);
  }
  
  //
  //  update boot driver address and runtime driver address in address file
  //
  if (AddrFileName != NULL) {
    FpFile = fopen (AddrFileName, "w");
    if (FpFile == NULL) {
      Error (NULL, 0, 0001, "Error opening file", AddrFileName);
      return STATUS_ERROR;
    }
    fprintf (FpFile, OPTIONS_SECTION_STRING);
    fprintf (FpFile, "\n");
    if (BtBase != 0) {
      fprintf (FpFile, EFI_FV_BOOT_DRIVER_BASE_ADDRESS_STRING);
      fprintf (FpFile, " = 0x%x\n", BtBase);
    }
    if (RtBase != 0) {
      fprintf (FpFile, EFI_FV_RUNTIME_DRIVER_BASE_ADDRESS_STRING);
      fprintf (FpFile, " = 0x%x\n", RtBase);
    }
    fclose (FpFile);
  }

  if (VerboseMode) {
    fprintf (stdout, "%s tool done with return code is 0x%x.\n", UTILITY_NAME, GetUtilityStatus ());  
  }

  return GetUtilityStatus ();
}