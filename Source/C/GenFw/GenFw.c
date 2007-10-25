/*++

Copyright (c) 2004 - 2007, Intel Corporation                                                         
All rights reserved. This program and the accompanying materials                          
are licensed and made available under the terms and conditions of the BSD License         
which accompanies this distribution.  The full text of the license may be found at        
http://opensource.org/licenses/bsd-license.php                                            
                                                                                          
THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,                     
WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.             

Module Name:

    GenFw.c

Abstract:

    Converts a pe32+ image to an FW image type

--*/

#include "WinNtInclude.h"

//
// List of OS and CPU which support ELF to PE conversion
//
#if defined(linux)
#if defined (__i386__) || defined(__x86_64__)
#define HAVE_ELF
#endif
#endif

#ifndef __GNUC__
#include <windows.h>
#endif
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#ifdef HAVE_ELF
#include <elf.h>
#endif

#include <Common/UefiBaseTypes.h>
#include <IndustryStandard/PeImage.h>

//
// Acpi Table definition
//
#include <IndustryStandard/Acpi.h>
#include <IndustryStandard/Acpi1_0.h>
#include <IndustryStandard/Acpi2_0.h>
#include <IndustryStandard/Acpi3_0.h>
#include <IndustryStandard/MemoryMappedConfigurationSpaceAccessTable.h>

#include "CommonLib.h"
#include "EfiUtilityMsgs.h"

//
// Version of this utility
//
#define UTILITY_NAME "GenFw"
#define UTILITY_MAJOR_VERSION 0
#define UTILITY_MINOR_VERSION 2

//
// Action for this tool.
//
#define FW_DUMMY_IMAGE       0
#define FW_EFI_IMAGE         1
#define FW_TE_IMAGE          2
#define FW_ACPI_IMAGE        3
#define FW_BIN_IMAGE         4
#define FW_ZERO_DEBUG_IMAGE  5
#define FW_SET_STAMP_IMAGE   6
#define FW_MCI_IMAGE         7
#define FW_MERGE_IMAGE       8

#define DUMP_TE_HEADER       0x11

#define DEFAULT_MC_PAD_BYTE_VALUE  0xFF
#define DEFAULT_MC_ALIGNMENT       16

#ifndef _MAX_PATH
#define _MAX_PATH 500
#endif

#define STATUS_IGNORE        0xA
//
// Structure definition for a microcode header
//
typedef struct {
  UINTN  HeaderVersion;
  UINTN  PatchId;
  UINTN  Date;
  UINTN  CpuId;
  UINTN  Checksum;
  UINTN  LoaderVersion;
  UINTN  PlatformId;
  UINTN  DataSize;   // if 0, then TotalSize = 2048, and TotalSize field is invalid
  UINTN  TotalSize;  // number of bytes
  UINTN  Reserved[3];
} MICROCODE_IMAGE_HEADER;

STATIC UINT8 *mInImageName;

STATIC
EFI_STATUS
ZeroDebugData (
  IN OUT UINT8   *FileBuffer
  );

STATIC 
EFI_STATUS
SetStamp (
  IN OUT UINT8  *FileBuffer, 
  IN     CHAR8  *TimeStamp
  );

STATIC 
STATUS
MicrocodeReadData (
  FILE          *InFptr,
  UINTN         *Data
  );

STATIC
VOID
Version (
  VOID
  )
/*++

Routine Description:

  Print out version information for this utility.

Arguments:

  None
  
Returns:

  None
  
--*/ 
{
  fprintf (stdout, "%s Version %d.%d\n", UTILITY_NAME, UTILITY_MAJOR_VERSION, UTILITY_MINOR_VERSION);
}

STATIC
VOID
Usage (
  VOID
  )
/*++

Routine Description:

  Print Help message.

Arguments:

  VOID

Returns:

  None

--*/
{
  //
  // Summary usage
  //
  fprintf (stdout, "\nUsage: %s [options] <input_file>\n\n", UTILITY_NAME);
  
  //
  // Copyright declaration
  // 
  fprintf (stdout, "Copyright (c) 2007, Intel Corporation. All rights reserved.\n\n");

  //
  // Details Option
  //
  fprintf (stdout, "Options:\n");
  fprintf (stdout, "  -o FileName, --outputfile FileName\n\
                        File will be created to store the ouput content.\n");
  fprintf (stdout, "  -e EFI_FILETYPE, --efiImage EFI_FILETYPE\n\
                        Create Efi Image. EFI_FILETYPE is one of BASE, SEC,\n\
                        PEI_CORE, PEIM, DXE_CORE, DXE_RUNTIME_DRIVER,\n\
                        DXE_SAL_DRIVER, UEFI_DRIVER, UEFI_APPLICATION, \n\
                        DXE_SMM_DRIVER, SECURITY_CORE, COMBINED_PEIM_DRIVER, \n\
                        PIC_PEIM, RELOCATABLE_PEIM, BS_DRIVER, RT_DRIVER,\n\
                        APPLICATION, SAL_RT_DRIVER to support all module types\n");
  fprintf (stdout, "  -c, --acpi            Create Acpi table.\n");
  fprintf (stdout, "  -t, --terse           Create Te Image.\n");
  fprintf (stdout, "  -u, --dump            Dump TeImage Header.\n");
  fprintf (stdout, "  -z, --zero            Zero the Debug Data Fields in the PE input image file.\n");
  fprintf (stdout, "  -b, --exe2bin         Convert the input EXE to the output BIN file.\n");
  fprintf (stdout, "  -r, --replace         Overwrite the input file with the output content.\n");
  fprintf (stdout, "  -s timedate, --stamp timedate\n\
                        timedate format is \"yyyy-mm-dd 00:00:00\". if timedata \n\
                        is set to NOW, current system time is used.\n");
  fprintf (stdout, "  -m, --mcifile         Convert input microcode txt file to microcode bin file.\n");
  fprintf (stdout, "  -j, --join            Combine multi microcode bin files to one file.\n");
  fprintf (stdout, "  -a NUM, --align NUM   NUM is one HEX or DEC format alignment value.\n");
  fprintf (stdout, "  -p NUM, --pad NUM     NUM is one HEX or DEC format padding value.\n");
  fprintf (stdout, "  -v, --verbose         Turn on verbose output with informational messages.\n");
  fprintf (stdout, "  -q, --quiet           Disable all messages except key message and fatal error\n");
  fprintf (stdout, "  -d, --debug level     Enable debug messages, at input debug level.\n");
  fprintf (stdout, "  --version             Show program's version number and exit\n");
  fprintf (stdout, "  -h, --help            Show this help message and exit\n");
}

STATIC
STATUS
CheckAcpiTable (
  VOID      *AcpiTable,
  UINT32    Length
  )
/*++

Routine Description:
  
  Check Acpi Table 

Arguments:

  AcpiTable     Buffer for AcpiSection
  Length        AcpiSection Length

Returns:

  0             success
  non-zero      otherwise

--*/
{
  EFI_ACPI_DESCRIPTION_HEADER                   *AcpiHeader;
  EFI_ACPI_3_0_FIRMWARE_ACPI_CONTROL_STRUCTURE  *Facs;
  UINT32                                        ExpectedLength;

  AcpiHeader = (EFI_ACPI_DESCRIPTION_HEADER *)AcpiTable;

  //
  // Generic check for AcpiTable length.
  //
  if (AcpiHeader->Length > Length) {
    Error (NULL, 0, 3000, "Invalid", "failed to pass AcpiTable Length check", NULL);
    return STATUS_ERROR;
  }

  //
  // Currently, we only check must-have tables: FADT, FACS, DSDT,
  // and some important tables: MADT, MCFG.
  //
  switch (AcpiHeader->Signature) {

  //
  // "FACP" Fixed ACPI Description Table
  //
  case EFI_ACPI_3_0_FIXED_ACPI_DESCRIPTION_TABLE_SIGNATURE:
    switch (AcpiHeader->Revision) {
    case EFI_ACPI_1_0_FIXED_ACPI_DESCRIPTION_TABLE_REVISION:
      ExpectedLength = sizeof(EFI_ACPI_1_0_FIXED_ACPI_DESCRIPTION_TABLE);
      break;
    case EFI_ACPI_2_0_FIXED_ACPI_DESCRIPTION_TABLE_REVISION:
      ExpectedLength = sizeof(EFI_ACPI_2_0_FIXED_ACPI_DESCRIPTION_TABLE);
      break;
    case EFI_ACPI_3_0_FIXED_ACPI_DESCRIPTION_TABLE_REVISION:
      ExpectedLength = sizeof(EFI_ACPI_3_0_FIXED_ACPI_DESCRIPTION_TABLE);
      break;
    default:
      Error (NULL, 0, 3000, "Invalid", "failed to pass FACP revision check");
      return STATUS_ERROR;
    }
    if (ExpectedLength != AcpiHeader->Length) {
      Error (NULL, 0, 3000, "Invalid", "failed to pass FACP Length check");
      return STATUS_ERROR;
    }
    break;

  //
  // "FACS" Firmware ACPI Control Structure
  //
  case EFI_ACPI_3_0_FIRMWARE_ACPI_CONTROL_STRUCTURE_SIGNATURE:
    Facs = (EFI_ACPI_3_0_FIRMWARE_ACPI_CONTROL_STRUCTURE *)AcpiTable;
    if ((Facs->Version != 0) &&
        (Facs->Version != EFI_ACPI_2_0_FIRMWARE_ACPI_CONTROL_STRUCTURE_VERSION) &&
        (Facs->Version != EFI_ACPI_3_0_FIRMWARE_ACPI_CONTROL_STRUCTURE_VERSION)){
      Error (NULL, 0, 3000, "Invalid", "failed to pass FACS version check");
      return STATUS_ERROR;
    }
    if ((Facs->Length != sizeof(EFI_ACPI_1_0_FIRMWARE_ACPI_CONTROL_STRUCTURE)) &&
        (Facs->Length != sizeof(EFI_ACPI_2_0_FIRMWARE_ACPI_CONTROL_STRUCTURE)) &&
        (Facs->Length != sizeof(EFI_ACPI_3_0_FIRMWARE_ACPI_CONTROL_STRUCTURE))) {
      Error (NULL, 0, 3000, "Invalid", "failed to pass FACS Length check");
      return STATUS_ERROR;
    }
    break;

  //
  // "DSDT" Differentiated System Description Table
  //
  case EFI_ACPI_3_0_DIFFERENTIATED_SYSTEM_DESCRIPTION_TABLE_SIGNATURE:
    if (AcpiHeader->Revision > EFI_ACPI_3_0_DIFFERENTIATED_SYSTEM_DESCRIPTION_TABLE_REVISION) {
      Error (NULL, 0, 3000, "Invalid", "failed to pass DSDT revision check");
      return STATUS_ERROR;
    }
    if (AcpiHeader->Length <= sizeof(EFI_ACPI_DESCRIPTION_HEADER)) {
      Error (NULL, 0, 3000, "Invalid", "failed to pass DSDT Length check");
      return STATUS_ERROR;
    }
    break;

  //
  // "APIC" Multiple APIC Description Table
  //
  case EFI_ACPI_3_0_MULTIPLE_APIC_DESCRIPTION_TABLE_SIGNATURE:
    if ((AcpiHeader->Revision != EFI_ACPI_1_0_MULTIPLE_APIC_DESCRIPTION_TABLE_REVISION) &&
        (AcpiHeader->Revision != EFI_ACPI_2_0_MULTIPLE_APIC_DESCRIPTION_TABLE_REVISION) &&
        (AcpiHeader->Revision != EFI_ACPI_3_0_MULTIPLE_APIC_DESCRIPTION_TABLE_REVISION)) {
      Error (NULL, 0, 3000, "Invalid", "failed to pass APIC revision check");
      return STATUS_ERROR;
    }
    if (AcpiHeader->Length <= sizeof(EFI_ACPI_DESCRIPTION_HEADER) + sizeof(UINT32) + sizeof(UINT32)) {
      Error (NULL, 0, 3000, "Invalid", "failed to pass APIC Length check");
      return STATUS_ERROR;
    }
    break;

  //
  // "MCFG" PCI Express Memory Mapped Configuration Space Base Address Description Table
  //
  case EFI_ACPI_3_0_PCI_EXPRESS_MEMORY_MAPPED_CONFIGURATION_SPACE_BASE_ADDRESS_DESCRIPTION_TABLE_SIGNATURE:
    if (AcpiHeader->Revision != EFI_ACPI_MEMORY_MAPPED_CONFIGURATION_SPACE_ACCESS_TABLE_REVISION) {
      Error (NULL, 0, 3000, "Invalid", "failed to pass MCFG revision check");
      return STATUS_ERROR;
    }
    if (AcpiHeader->Length <= sizeof(EFI_ACPI_DESCRIPTION_HEADER) + sizeof(UINT64)) {
      Error (NULL, 0, 3000, "Invalid", "failed to pass MCFG Length check");
      return STATUS_ERROR;
    }
    break;

  //
  // Other table pass check
  //
  default:
    break;
  }

  return STATUS_SUCCESS;
}

STATIC
STATUS
FCopyFile (
  FILE    *in,
  FILE    *out
  )
{
  UINT32  filesize;
  UINT32  offset;
  UINT32  length;
  UINT8 Buffer[8 * 1024];

  fseek (in, 0, SEEK_END);
  filesize = ftell (in);

  fseek (in, 0, SEEK_SET);
  fseek (out, 0, SEEK_SET);

  offset = 0;
  while (offset < filesize) {
    length = sizeof (Buffer);
    if (filesize - offset < length) {
      length = filesize - offset;
    }

    fread (Buffer, length, 1, in);
    fwrite (Buffer, length, 1, out);
    offset += length;
  }

  if ((UINT32 ) ftell (out) != filesize) {
    Error (NULL, 0, 0002, "Error writing file", NULL);
    return STATUS_ERROR;
  }

  return STATUS_SUCCESS;
}

#ifdef HAVE_ELF
INTN
IsElfHeader(
  UINT8  *FileBuffer
)
{
  return (FileBuffer[EI_MAG0] == ELFMAG0
    && FileBuffer[EI_MAG1] == ELFMAG1
    && FileBuffer[EI_MAG2] == ELFMAG2
    && FileBuffer[EI_MAG3] == ELFMAG3);
}

typedef Elf32_Shdr Elf_Shdr;
typedef Elf32_Ehdr Elf_Ehdr;
typedef Elf32_Rel Elf_Rel;
typedef Elf32_Sym Elf_Sym;
#define ELFCLASS ELFCLASS32
#define ELF_R_TYPE(r) ELF32_R_TYPE(r)
#define ELF_R_SYM(r) ELF32_R_SYM(r)

//
// Well known ELF structures.
//
Elf_Ehdr *Ehdr;
Elf_Shdr *ShdrBase;

//
// PE section alignment.
//
const UINT32 CoffAlignment = 0x20;
const UINT32 CoffNbrSections = 4;

//
// Current offset in coff file.
//
UINT32 CoffOffset;

//
// Result Coff file in memory.
//
UINT8 *CoffFile = NULL;
//
// ELF sections to offset in Coff file.
//
UINT32 *CoffSectionsOffset = NULL;

//
// Offset in Coff file of headers and sections.
//
UINT32 NtHdrOffset;
UINT32 TableOffset;
UINT32 TextOffset;
UINT32 DataOffset;
UINT32 RelocOffset;

EFI_IMAGE_BASE_RELOCATION *CoffBaseRel;
UINT16 *CoffEntryRel;

UINT32
CoffAlign(
  UINT32 Offset
  )
{
  return (Offset + CoffAlignment - 1) & ~(CoffAlignment - 1);
}

Elf_Shdr *
GetShdrByIndex(
  UINT32 Num
  )
{
  if (Num >= Ehdr->e_shnum)
    return NULL;
  return (Elf_Shdr*)((UINT8*)ShdrBase + Num * Ehdr->e_shentsize);
}

INTN
CheckElfHeader(
  VOID
  )
{
  //
  // Note: Magic has already been tested.
  //
  if (Ehdr->e_ident[EI_CLASS] != ELFCLASS)
    return 0;
  if (Ehdr->e_ident[EI_DATA] != ELFDATA2LSB)
    return 0;
  if (Ehdr->e_type != ET_EXEC)
    return 0;
  if (Ehdr->e_machine != EM_386)
    return 0;
  if (Ehdr->e_version != EV_CURRENT)
    return 0;

  //
  // Find the section header table
  // 
  ShdrBase = (Elf_Shdr *)((UINT8 *)Ehdr + Ehdr->e_shoff);

  CoffSectionsOffset = (UINT32 *)malloc(Ehdr->e_shnum * sizeof (UINT32));

  memset(CoffSectionsOffset, 0, Ehdr->e_shnum * sizeof(UINT32));
  return 1;
}

int
IsTextShdr(
  Elf_Shdr *Shdr
  )
{
  return (Shdr->sh_flags & (SHF_WRITE | SHF_ALLOC)) == SHF_ALLOC;
}

int
IsDataShdr(
  Elf_Shdr *Shdr
  )
{
  return (Shdr->sh_flags & (SHF_WRITE | SHF_ALLOC)) == (SHF_ALLOC | SHF_WRITE);
}

VOID
CreateSectionHeader(
  const CHAR8 *Name,
  UINT32      Offset,
  UINT32      Size,
  UINT32      Flags
  )
{
  EFI_IMAGE_SECTION_HEADER *Hdr;
  Hdr = (EFI_IMAGE_SECTION_HEADER*)(CoffFile + TableOffset);

  strcpy(Hdr->Name, Name);
  Hdr->Misc.VirtualSize = Size;
  Hdr->VirtualAddress = Offset;
  Hdr->SizeOfRawData = Size;
  Hdr->PointerToRawData = Offset;
  Hdr->PointerToRelocations = 0;
  Hdr->PointerToLinenumbers = 0;
  Hdr->NumberOfRelocations = 0;
  Hdr->NumberOfLinenumbers = 0;
  Hdr->Characteristics = Flags;

  TableOffset += sizeof (EFI_IMAGE_SECTION_HEADER);
}

VOID
ScanSections(
  VOID
  )
{
  UINT32 i;
  EFI_IMAGE_DOS_HEADER *DosHdr;
  EFI_IMAGE_NT_HEADERS *NtHdr;
  UINT32 CoffEntry = 0;

  CoffOffset = 0;

  //
  // Coff file start with a DOS header.
  //
  CoffOffset = sizeof(EFI_IMAGE_DOS_HEADER) + 0x40;
  NtHdrOffset = CoffOffset;
  CoffOffset += sizeof(EFI_IMAGE_NT_HEADERS);
  TableOffset = CoffOffset;
  CoffOffset += CoffNbrSections * sizeof(EFI_IMAGE_SECTION_HEADER);

  //
  // First text sections.
  //
  CoffOffset = CoffAlign(CoffOffset);
  TextOffset = CoffOffset;
  for (i = 0; i < Ehdr->e_shnum; i++) {
    Elf_Shdr *shdr = GetShdrByIndex(i);
    if (IsTextShdr(shdr)) {
      //
      // Align the coff offset to meet with the alignment requirement of section
      // itself.
      // 
      if ((shdr->sh_addralign != 0) && (shdr->sh_addralign != 1)) {
        CoffOffset = (CoffOffset + shdr->sh_addralign - 1) & ~(shdr->sh_addralign - 1);
      }

      /* Relocate entry.  */
      if ((Ehdr->e_entry >= shdr->sh_addr) && 
          (Ehdr->e_entry < shdr->sh_addr + shdr->sh_size)) {
        CoffEntry = CoffOffset + Ehdr->e_entry - shdr->sh_addr;
      }
      CoffSectionsOffset[i] = CoffOffset;
      CoffOffset += shdr->sh_size;
    }
  }
  CoffOffset = CoffAlign(CoffOffset);

  //
  //  Then data sections.
  //
  DataOffset = CoffOffset;
  for (i = 0; i < Ehdr->e_shnum; i++) {
    Elf_Shdr *shdr = GetShdrByIndex(i);
    if (IsDataShdr(shdr)) {
      //
      // Align the coff offset to meet with the alignment requirement of section
      // itself.
      // 
      if ((shdr->sh_addralign != 0) && (shdr->sh_addralign != 1)) {
        CoffOffset = (CoffOffset + shdr->sh_addralign - 1) & ~(shdr->sh_addralign - 1);
      }
     
      CoffSectionsOffset[i] = CoffOffset;
      CoffOffset += shdr->sh_size;
    }
  }
  CoffOffset = CoffAlign(CoffOffset);

  RelocOffset = CoffOffset;  

  //
  // Allocate base Coff file.  Will be expanded later for relocations. 
  //
  CoffFile = (UINT8 *)malloc(CoffOffset);
  memset(CoffFile, 0, CoffOffset);

  //
  // Fill headers.
  //
  DosHdr = (EFI_IMAGE_DOS_HEADER *)CoffFile;
  DosHdr->e_magic = EFI_IMAGE_DOS_SIGNATURE;
  DosHdr->e_lfanew = NtHdrOffset;

  NtHdr = (EFI_IMAGE_NT_HEADERS*)(CoffFile + NtHdrOffset);

  NtHdr->Signature = EFI_IMAGE_NT_SIGNATURE;

  NtHdr->FileHeader.Machine = EFI_IMAGE_MACHINE_IA32;
  NtHdr->FileHeader.NumberOfSections = CoffNbrSections;
  NtHdr->FileHeader.TimeDateStamp = time(NULL);
  NtHdr->FileHeader.PointerToSymbolTable = 0;
  NtHdr->FileHeader.NumberOfSymbols = 0;
  NtHdr->FileHeader.SizeOfOptionalHeader = sizeof(NtHdr->OptionalHeader);
  NtHdr->FileHeader.Characteristics = EFI_IMAGE_FILE_EXECUTABLE_IMAGE
    | EFI_IMAGE_FILE_LINE_NUMS_STRIPPED
    | EFI_IMAGE_FILE_LOCAL_SYMS_STRIPPED
    | EFI_IMAGE_FILE_32BIT_MACHINE;
  
  NtHdr->OptionalHeader.Magic = EFI_IMAGE_NT_OPTIONAL_HDR32_MAGIC;
  NtHdr->OptionalHeader.SizeOfCode = DataOffset - TextOffset;
  NtHdr->OptionalHeader.SizeOfInitializedData = RelocOffset - DataOffset;
  NtHdr->OptionalHeader.SizeOfUninitializedData = 0;
  NtHdr->OptionalHeader.AddressOfEntryPoint = CoffEntry;
  NtHdr->OptionalHeader.BaseOfCode = TextOffset;

  NtHdr->OptionalHeader.BaseOfData = DataOffset;
  NtHdr->OptionalHeader.ImageBase = 0;
  NtHdr->OptionalHeader.SectionAlignment = CoffAlignment;
  NtHdr->OptionalHeader.FileAlignment = CoffAlignment;
  NtHdr->OptionalHeader.SizeOfImage = 0;

  NtHdr->OptionalHeader.SizeOfHeaders = TextOffset;
  NtHdr->OptionalHeader.NumberOfRvaAndSizes = EFI_IMAGE_NUMBER_OF_DIRECTORY_ENTRIES;

  //
  // Section headers.
  //
  CreateSectionHeader (".text", TextOffset, DataOffset - TextOffset,
           EFI_IMAGE_SCN_CNT_CODE
           | EFI_IMAGE_SCN_MEM_EXECUTE
           | EFI_IMAGE_SCN_MEM_READ);
  CreateSectionHeader (".data", DataOffset, RelocOffset - DataOffset,
           EFI_IMAGE_SCN_CNT_INITIALIZED_DATA
           | EFI_IMAGE_SCN_MEM_WRITE
           | EFI_IMAGE_SCN_MEM_READ);
}

VOID
WriteSections(
  int   (*Filter)(Elf_Shdr *)
  )
{
  UINT32 Idx;

  //
  // First: copy sections.
  //
  for (Idx = 0; Idx < Ehdr->e_shnum; Idx++) {
    Elf_Shdr *Shdr = GetShdrByIndex(Idx);
    if ((*Filter)(Shdr)) {
      switch (Shdr->sh_type) {
      case SHT_PROGBITS:
  /* Copy.  */
  memcpy(CoffFile + CoffSectionsOffset[Idx],
         (UINT8*)Ehdr + Shdr->sh_offset,
         Shdr->sh_size);
  break;
      case SHT_NOBITS:
  memset(CoffFile + CoffSectionsOffset[Idx], 0, Shdr->sh_size);
  break;
      default:
  Error (NULL, 0, 3000, "Invalid", "%s unhandle section type %x", mInImageName, (UINTN)Shdr->sh_type);
      }
    }
  }

  //
  // Second: apply relocations.
  //
  for (Idx = 0; Idx < Ehdr->e_shnum; Idx++) {
    Elf_Shdr *RelShdr = GetShdrByIndex(Idx);
    if (RelShdr->sh_type != SHT_REL)
      continue;
    Elf_Shdr *SecShdr = GetShdrByIndex(RelShdr->sh_info);
    UINT32 SecOffset = CoffSectionsOffset[RelShdr->sh_info];
    if (RelShdr->sh_type == SHT_REL && (*Filter)(SecShdr)) {
      UINT32 RelIdx;
      Elf_Shdr *SymtabShdr = GetShdrByIndex(RelShdr->sh_link);
      UINT8 *Symtab = (UINT8*)Ehdr + SymtabShdr->sh_offset;

      for (RelIdx = 0; RelIdx < RelShdr->sh_size; RelIdx += RelShdr->sh_entsize) {
  Elf_Rel *Rel = (Elf_Rel *)((UINT8*)Ehdr + RelShdr->sh_offset + RelIdx);
  Elf_Sym *Sym = (Elf_Sym *)
    (Symtab + ELF_R_SYM(Rel->r_info) * SymtabShdr->sh_entsize);
  Elf_Shdr *SymShdr;
  UINT8 *Targ;

  if (Sym->st_shndx == SHN_UNDEF
      || Sym->st_shndx == SHN_ABS
      || Sym->st_shndx > Ehdr->e_shnum) {
    Error (NULL, 0, 3000, "Invalid", "%s bad symbol definition", mInImageName);
  }
  SymShdr = GetShdrByIndex(Sym->st_shndx);

  //
  // Note: r_offset in a memory address.
  //  Convert it to a pointer in the coff file.
  //
  Targ = CoffFile + SecOffset + (Rel->r_offset - SecShdr->sh_addr);

  switch (ELF_R_TYPE(Rel->r_info)) {
  case R_386_NONE:
    break;
  case R_386_32:
    //
    // Absolute relocation.
    //
    *(UINT32 *)Targ = *(UINT32 *)Targ - SymShdr->sh_addr
      + CoffSectionsOffset[Sym->st_shndx];
    break;
  case R_386_PC32:
    //
    // Relative relocation: Symbol - Ip + Addend
    //
    *(UINT32 *)Targ = *(UINT32 *)Targ
      + (CoffSectionsOffset[Sym->st_shndx] - SymShdr->sh_addr)
      - (SecOffset - SecShdr->sh_addr);
    break;
  default:
    Error (NULL, 0, 3000, "Invalid", "%s unhandle section type %x", mInImageName, ELF_R_TYPE(Rel->r_info));
  }
      }
    }
  }
}

VOID
CoffAddFixupEntry(
  UINT16 Val
  )
{
  *CoffEntryRel = Val;
  CoffEntryRel++;
  CoffBaseRel->SizeOfBlock += 2;
  CoffOffset += 2;
}

VOID
CoffAddFixup(
  UINT32 Offset,
  UINT8  Type
  )
{
  if (CoffBaseRel == NULL
      || CoffBaseRel->VirtualAddress != (Offset & ~0xfff)) {
    if (CoffBaseRel != NULL) {
      //
      // Add a null entry (is it required ?)
      //
      CoffAddFixupEntry (0);
      //
      // Pad for alignment.
      //
      if (CoffOffset % 4 != 0)
  CoffAddFixupEntry (0);
    }
      
    CoffFile = realloc
      (CoffFile,
       CoffOffset + sizeof(EFI_IMAGE_BASE_RELOCATION) + 2*0x1000);
    memset(CoffFile + CoffOffset, 0,
     sizeof(EFI_IMAGE_BASE_RELOCATION) + 2*0x1000);

    CoffBaseRel = (EFI_IMAGE_BASE_RELOCATION*)(CoffFile + CoffOffset);
    CoffBaseRel->VirtualAddress = Offset & ~0xfff;
    CoffBaseRel->SizeOfBlock = sizeof(EFI_IMAGE_BASE_RELOCATION);

    CoffEntryRel = (UINT16 *)(CoffBaseRel + 1);
    CoffOffset += sizeof(EFI_IMAGE_BASE_RELOCATION);
  }

  //
  // Fill the entry.
  //
  CoffAddFixupEntry((Type << 12) | (Offset & 0xfff));
}

VOID
WriteRelocations(
  VOID
  )
{
  UINT32 Idx;
  EFI_IMAGE_NT_HEADERS *NtHdr;
  EFI_IMAGE_DATA_DIRECTORY *Dir;

  for (Idx = 0; Idx < Ehdr->e_shnum; Idx++) {
    Elf_Shdr *RelShdr = GetShdrByIndex(Idx);
    if (RelShdr->sh_type == SHT_REL) {
      Elf_Shdr *SecShdr = GetShdrByIndex(RelShdr->sh_info);
      if (IsTextShdr(SecShdr) || IsDataShdr(SecShdr)) {
  UINT32 RelIdx;
  for (RelIdx = 0; RelIdx < RelShdr->sh_size; RelIdx += RelShdr->sh_entsize) {
    Elf_Rel *Rel = (Elf_Rel *)
      ((UINT8*)Ehdr + RelShdr->sh_offset + RelIdx);
    switch (ELF_R_TYPE(Rel->r_info)) {
    case R_386_NONE:
    case R_386_PC32:
      break;
    case R_386_32:
      CoffAddFixup(CoffSectionsOffset[RelShdr->sh_info]
       + (Rel->r_offset - SecShdr->sh_addr),
       EFI_IMAGE_REL_BASED_HIGHLOW);
      break;
    default:
      Error (NULL, 0, 3000, "Invalid", "%s unhandle section type %x", mInImageName, ELF_R_TYPE(Rel->r_info));
    }
  }
      }
    }
  }

  //
  // Pad by adding empty entries. 
  //
  while (CoffOffset & (CoffAlignment - 1)) {
    CoffAddFixupEntry(0);
  }

  CreateSectionHeader (".reloc", RelocOffset, CoffOffset - RelocOffset,
           EFI_IMAGE_SCN_CNT_INITIALIZED_DATA
           | EFI_IMAGE_SCN_MEM_DISCARDABLE
           | EFI_IMAGE_SCN_MEM_READ);

  NtHdr = (EFI_IMAGE_NT_HEADERS *)(CoffFile + NtHdrOffset);
  Dir = &NtHdr->OptionalHeader.DataDirectory[EFI_IMAGE_DIRECTORY_ENTRY_BASERELOC];
  Dir->VirtualAddress = RelocOffset;
  Dir->Size = CoffOffset - RelocOffset;
}

VOID
WriteDebug(
  VOID
  )
{
  UINT32 Len = strlen(mInImageName) + 1;
  UINT32 DebugOffset = CoffOffset;
  EFI_IMAGE_NT_HEADERS *NtHdr;
  EFI_IMAGE_DATA_DIRECTORY *DataDir;
  EFI_IMAGE_DEBUG_DIRECTORY_ENTRY *Dir;
  EFI_IMAGE_DEBUG_CODEVIEW_NB10_ENTRY *Nb10;

  CoffOffset += sizeof(EFI_IMAGE_DEBUG_DIRECTORY_ENTRY)
    + sizeof(EFI_IMAGE_DEBUG_CODEVIEW_NB10_ENTRY)
    + Len;
  CoffOffset = CoffAlign(CoffOffset);

  CoffFile = realloc
    (CoffFile, CoffOffset);
  memset(CoffFile + DebugOffset, 0, CoffOffset - DebugOffset);
  
  Dir = (EFI_IMAGE_DEBUG_DIRECTORY_ENTRY*)(CoffFile + DebugOffset);
  Dir->Type = EFI_IMAGE_DEBUG_TYPE_CODEVIEW;
  Dir->SizeOfData = sizeof(EFI_IMAGE_DEBUG_DIRECTORY_ENTRY) + Len;
  Dir->RVA = DebugOffset + sizeof(EFI_IMAGE_DEBUG_DIRECTORY_ENTRY);
  Dir->FileOffset = DebugOffset + sizeof(EFI_IMAGE_DEBUG_DIRECTORY_ENTRY);
  
  Nb10 = (EFI_IMAGE_DEBUG_CODEVIEW_NB10_ENTRY*)(Dir + 1);
  Nb10->Signature = CODEVIEW_SIGNATURE_NB10;
  strcpy ((UINT8 *)(Nb10 + 1), mInImageName);

  CreateSectionHeader (".debug", DebugOffset, CoffOffset - DebugOffset,
           EFI_IMAGE_SCN_CNT_INITIALIZED_DATA
           | EFI_IMAGE_SCN_MEM_DISCARDABLE
           | EFI_IMAGE_SCN_MEM_READ);

  NtHdr = (EFI_IMAGE_NT_HEADERS *)(CoffFile + NtHdrOffset);
  DataDir = &NtHdr->OptionalHeader.DataDirectory[EFI_IMAGE_DIRECTORY_ENTRY_DEBUG];
  DataDir->VirtualAddress = DebugOffset;
  DataDir->Size = CoffOffset - DebugOffset;
}

VOID
ConvertElf (
  UINT8  **FileBuffer,
  UINTN *FileLength
  )
{
  EFI_IMAGE_NT_HEADERS *NtHdr;

  //
  // Check header, read section table.
  //
  Ehdr = (Elf32_Ehdr*)*FileBuffer;
  if (!CheckElfHeader())
    return;

  //
  // Compute sections new address.
  //
  ScanSections();

  //
  // Write and relocate sections.
  //
  WriteSections(IsTextShdr);
  WriteSections(IsDataShdr);

  //
  // Translate and write relocations.
  //
  WriteRelocations();

  //
  // Write debug info.
  //
  WriteDebug();

  NtHdr = (EFI_IMAGE_NT_HEADERS *)(CoffFile + NtHdrOffset);
  NtHdr->OptionalHeader.SizeOfImage = CoffOffset;

  //
  // Replace.
  //
  free(*FileBuffer);
  *FileBuffer = CoffFile;
  *FileLength = CoffOffset;
  
  //
  // Free memory space
  //
  if (CoffSectionsOffset != NULL) {
    free (CoffSectionsOffset);
  }
}
#endif // HAVE_ELF

int
main (
  int  argc,
  char *argv[]
  )
/*++

Routine Description:

  Main function.

Arguments:

  argc - Number of command line parameters.
  argv - Array of pointers to command line parameter strings.

Returns:
  STATUS_SUCCESS - Utility exits successfully.
  STATUS_ERROR   - Some error occurred during execution.

--*/
{
  UINT32            Type;
  UINT32            InputFileNum;
  CHAR8             **InputFileName;
  UINT8             *OutImageName;
  UINT8             *ModuleType;
  CHAR8             *TimeStamp;
  CHAR8             FileName[_MAX_PATH];
  UINT32            OutImageType;
  FILE              *fpIn;
  FILE              *fpOut;
  FILE              *fpInOut;
  UINTN             Data;
  UINTN             *DataPointer;
  UINTN             *OldDataPointer;
  UINTN             CheckSum;
  UINT32            Index;
  UINT32            Index1;
  UINT32            Index2;
  UINT64            Temp64;
  UINT32            MciAlignment;
  UINT8             MciPadValue;
  UINT32            AllignedRelocSize;
  UINT8             *FileBuffer;
  UINT32            FileLength;
  RUNTIME_FUNCTION  *RuntimeFunction;
  UNWIND_INFO       *UnwindInfo;
  STATUS            Status;
  BOOLEAN           ReplaceFlag;
  UINT64            LogLevel;
  EFI_TE_IMAGE_HEADER          TEImageHeader;
  EFI_IMAGE_SECTION_HEADER     *SectionHeader;
  EFI_IMAGE_DOS_HEADER         *DosHdr;
  EFI_IMAGE_NT_HEADERS         *PeHdr;
  EFI_IMAGE_OPTIONAL_HEADER32  *Optional32;
  EFI_IMAGE_OPTIONAL_HEADER64  *Optional64;
  EFI_IMAGE_DOS_HEADER         BackupDosHdr;
  MICROCODE_IMAGE_HEADER       *MciHeader; 

  SetUtilityName (UTILITY_NAME);

  //
  // Assign to fix compile warning
  //
  InputFileNum      = 0; 
  InputFileName     = NULL;
  mInImageName       = NULL;
  OutImageName      = NULL;
  ModuleType        = NULL;
  OutImageType      = FW_DUMMY_IMAGE;
  Type              = 0;
  Status            = STATUS_SUCCESS;
  FileBuffer        = NULL;
  fpIn              = NULL;
  fpOut             = NULL;
  fpInOut           = NULL;
  TimeStamp         = NULL;
  MciAlignment      = DEFAULT_MC_ALIGNMENT;
  MciPadValue       = DEFAULT_MC_PAD_BYTE_VALUE;
  FileLength        = 0;
  MciHeader         = NULL;
  CheckSum          = 0;
  ReplaceFlag       = FALSE;
  LogLevel          = 0;

  if (argc == 1) {
    Error (NULL, 0, 1001, "Missing options", "No input options");
    Usage ();
    return STATUS_ERROR;
  }
  
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
    if ((stricmp (argv[0], "-o") == 0) || (stricmp (argv[0], "--outputfile") == 0)) {
      OutImageName = argv[1];
      argc -= 2;
      argv += 2;
      continue; 
    }

    if ((stricmp (argv[0], "-e") == 0) || (stricmp (argv[0], "--efiImage") == 0)) {
      ModuleType   = argv[1];
      if (OutImageType != FW_TE_IMAGE) {
        OutImageType = FW_EFI_IMAGE;
      }
      argc -= 2;
      argv += 2;
      continue;
    }

    if ((stricmp (argv[0], "-c") == 0) || (stricmp (argv[0], "--acpi") == 0)) {
      OutImageType = FW_ACPI_IMAGE;
      argc --;
      argv ++;
      continue;
    }

    if ((stricmp (argv[0], "-t") == 0) || (stricmp (argv[0], "--terse") == 0)) {
      OutImageType = FW_TE_IMAGE;
      argc --;
      argv ++;
      continue;
    }

    if ((stricmp (argv[0], "-u") == 0) || (stricmp (argv[0], "--dump") == 0)) {
      OutImageType = DUMP_TE_HEADER;
      argc --;
      argv ++;
      continue;
    }

    if ((stricmp (argv[0], "-b") == 0) || (stricmp (argv[0], "--exe2bin") == 0)) {
      OutImageType = FW_BIN_IMAGE;
      argc --;
      argv ++;
      continue;
    }

    if ((stricmp (argv[0], "-z") == 0) || (stricmp (argv[0], "--zero") == 0)) {
      OutImageType = FW_ZERO_DEBUG_IMAGE;
      argc --;
      argv ++;
      continue;
    }

    if ((stricmp (argv[0], "-s") == 0) || (stricmp (argv[0], "--stamp") == 0)) {
      OutImageType = FW_SET_STAMP_IMAGE;
      TimeStamp    = argv[1];
      argc -= 2;
      argv += 2;
      continue;
    }

    if ((stricmp (argv[0], "-r") == 0) || (stricmp (argv[0], "--replace") == 0)) {
      ReplaceFlag = TRUE;
      argc --;
      argv ++;
      continue;
    }

    if ((stricmp (argv[0], "-m") == 0) || (stricmp (argv[0], "--mcifile") == 0)) {
      OutImageType = FW_MCI_IMAGE;
      argc --;
      argv ++;
      continue;
    }

    if ((stricmp (argv[0], "-j") == 0) || (stricmp (argv[0], "--join") == 0)) {
      OutImageType = FW_MERGE_IMAGE;
      argc --;
      argv ++;
      continue;
    }

    if ((stricmp (argv[0], "-a") == 0) || (stricmp (argv[0], "--align") == 0)) {
      if (AsciiStringToUint64 (argv[1], FALSE, &Temp64) != EFI_SUCCESS) {
        Error (NULL, 0, 1003, "Invalid option value", "%s = %s", argv[0], argv[1]);
        goto Finish;
      }
      MciAlignment = (UINT32) Temp64;
      argc -= 2;
      argv += 2;
      continue;
    }

    if ((stricmp (argv[0], "-p") == 0) || (stricmp (argv[0], "--pad") == 0)) {
      if (AsciiStringToUint64 (argv[1], FALSE, &Temp64) != EFI_SUCCESS) {
        Error (NULL, 0, 1003, "Invalid option value", "%s = %s", argv[0], argv[1]);
        goto Finish;
      }
      MciPadValue = (UINT8) Temp64;
      argc -= 2;
      argv += 2;
      continue;
    }

    if ((stricmp (argv[0], "-v") == 0) || (stricmp (argv[0], "--verbose") == 0)) {
      SetPrintLevel (VERBOSE_LOG_LEVEL);
      VerboseMsg ("Verbose output Mode Set!");
      argc --;
      argv ++;
      continue;
    }

    if ((stricmp (argv[0], "-q") == 0) || (stricmp (argv[0], "--quiet") == 0)) {
      SetPrintLevel (KEY_LOG_LEVEL);
      KeyMsg ("Quiet output Mode Set!");
      argc --;
      argv ++;
      continue;
    }

    if ((stricmp (argv[0], "-d") == 0) || (stricmp (argv[0], "--debug") == 0)) {
      Status = AsciiStringToUint64 (argv[1], FALSE, &LogLevel);
      if (EFI_ERROR (Status)) {
        Error (NULL, 0, 1003, "Invalid option value", "%s = %s", argv[0], argv[1]);
        goto Finish;
      }
      if (LogLevel > 9) {
        Error (NULL, 0, 1003, "Invalid option value", "Debug Level range is 0~9, currnt input level is %d", LogLevel);
        goto Finish;
      }
      SetPrintLevel (LogLevel);
      DebugMsg (NULL, 0, 9, "Debug Mode Set", "Debug Output Mode Level %s is set!", argv[1]);
      argc -= 2;
      argv += 2;
      continue;
    }

    //
    // Get Input file name
    //
    if ((InputFileNum == 0) && (InputFileName == NULL)) {
      InputFileName = (CHAR8 **) malloc (MAXIMUM_INPUT_FILE_NUM * sizeof (CHAR8 *));
      if (InputFileName == NULL) {
        Error (NULL, 0, 4001, "Resource", "memory cannot be allcoated");
        return EFI_OUT_OF_RESOURCES;
      }

      memset (InputFileName, 0, (MAXIMUM_INPUT_FILE_NUM * sizeof (CHAR8 *)));
    } else if (InputFileNum % MAXIMUM_INPUT_FILE_NUM == 0) {
      //
      // InputFileName buffer too small, need to realloc
      //
      InputFileName = (CHAR8 **) realloc (
                                  InputFileName,
                                  (InputFileNum + MAXIMUM_INPUT_FILE_NUM) * sizeof (CHAR8 *)
                                  );

      if (InputFileName == NULL) {
        Error (NULL, 0, 4001, "Resource", "memory cannot be allcoated");
        return EFI_OUT_OF_RESOURCES;
      }

      memset (&(InputFileName[InputFileNum]), 0, (MAXIMUM_INPUT_FILE_NUM * sizeof (CHAR8 *)));
    }

    InputFileName [InputFileNum ++] = argv[0];
    argc --;
    argv ++;
  }
  
  VerboseMsg ("%s tool start.", UTILITY_NAME);

  if (OutImageType == FW_DUMMY_IMAGE) {
    Error (NULL, 0, 1001, "Missing option", "No action specified, such as -e, -c or -t");
    goto Finish;
  }

  //
  // check input files
  //
  if (InputFileNum == 0) {
    Error (NULL, 0, 1001, "Missing option", "Input files");
    goto Finish;
  }

  //
  // Combine MciBinary files to one file
  //
  if ((OutImageType == FW_MERGE_IMAGE) && ReplaceFlag) {
    Error (NULL, 0, 1002, "Conflicting option", "-r replace parameter can't be input together with -j merge files");
    goto Finish;
  }
   
  //
  // Input image file
  //
  mInImageName = InputFileName [InputFileNum - 1];
  VerboseMsg ("the input file name is %s", mInImageName);
  
  //
  // Action will be taken for the input file.
  //
  switch (OutImageType) {
  case FW_EFI_IMAGE:
    VerboseMsg ("Create efi image on module type %s based on the input PE image.", ModuleType);
    break;
  case FW_TE_IMAGE:
    VerboseMsg ("Create Te Image based on the input PE image.");
    break;
  case FW_ACPI_IMAGE:
    VerboseMsg ("Get acpi table data from the input PE image.");
    break;
  case FW_BIN_IMAGE:
    VerboseMsg ("Convert the input EXE to the output BIN file.");
    break;
  case FW_ZERO_DEBUG_IMAGE:
    VerboseMsg ("Zero the Debug Data Fields in input PE image.");
    break;
  case FW_SET_STAMP_IMAGE:
    VerboseMsg ("Set new time stamp %s in the input PE image.", TimeStamp);
    break;
  case DUMP_TE_HEADER:
    VerboseMsg ("Dump the TE header information of the input TE image.");
    break;
  case FW_MCI_IMAGE:
    VerboseMsg ("Conver input MicroCode.txt file to MicroCode.bin file.");
    break;
  case FW_MERGE_IMAGE:
    VerboseMsg ("Combine the input multi microcode bin files to one bin file.");
    break;
  default:
    break;
  }
  
  if (ReplaceFlag) {
    VerboseMsg ("Overwrite the input file with the output content.");
  }

  //
  // Open output file and Write image into the output file.
  //
  if (OutImageName != NULL) {
    fpOut = fopen (OutImageName, "wb");
    if (!fpOut) {
      Error (NULL, 0, 0001, "Error opening file", OutImageName);
      goto Finish;
    }
    VerboseMsg ("Output file name is %s", OutImageName);
  } else if (!ReplaceFlag) {
    if (OutImageType == DUMP_TE_HEADER) {
      fpOut = stdout;
    } else {
      Error (NULL, 0, 1001, "Missing option", "output file");
      goto Finish;
    }
  }

  //
  // Combine MciBinary files to one file
  //
  if (OutImageType == FW_MERGE_IMAGE) {
    for (Index = 0; Index < InputFileNum; Index ++) {
      fpIn = fopen (InputFileName [Index], "rb");
      if (!fpIn) {
        Error (NULL, 0, 0001, "Error opening file", InputFileName [Index]);
        goto Finish;
      }
    
      FileLength = _filelength (fileno (fpIn));
      FileBuffer = malloc (FileLength);
      if (FileBuffer == NULL) {
        Error (NULL, 0, 4001, "Resource", "memory cannot be allcoated");
        fclose (fpIn);
        goto Finish;
      }
      
      fread (FileBuffer, 1, FileLength, fpIn);
      fclose (fpIn);
      //
      // write input file to out file
      //
      fwrite (FileBuffer, 1, FileLength, fpOut);
      //
      // write pad value to out file.
      //
      while (FileLength ++ % MciAlignment != 0) {
        fwrite (&MciPadValue, 1, 1, fpOut);
      }
      //
      // free allcoated memory space
      //
      free (FileBuffer);
      FileBuffer = NULL;
    }
    // 
    // Done successfully
    //
    goto Finish;
  }

  //
  // Convert MicroCode.txt file to MicroCode.bin file
  //
  if (OutImageType == FW_MCI_IMAGE) {
    fpIn = fopen (mInImageName, "r");
    if (!fpIn) {
      Error (NULL, 0, 0001, "Error opening file", mInImageName);
      goto Finish;
    }
    
    //
    // The first pass is to determine 
    // how much data is in the file so we can allocate a working buffer. 
    //
    FileLength = 0;
    do {
      Status = MicrocodeReadData (fpIn, &Data);
      if (Status == STATUS_SUCCESS) {
        FileLength += sizeof (Data);
      }
      if (Status == STATUS_IGNORE) {
        Status = STATUS_SUCCESS;
      }
    } while (Status == STATUS_SUCCESS);
    //
    // Error if no data.
    //
    if (FileLength == 0) {
      Error (NULL, 0, 3000, "Invalid", "no parse-able data found in file %s", mInImageName);
      goto Finish;
    }
    if (FileLength < sizeof (MICROCODE_IMAGE_HEADER)) {
      Error (NULL, 0, 3000, "Invalid", "amount of parse-able data in %s is insufficient to contain a microcode header", mInImageName);
      goto Finish;
    }

    //
    // Allocate a buffer for the data
    //
    FileBuffer = malloc (FileLength);
    if (FileBuffer == NULL) {
      Error (NULL, 0, 4001, "Resource", "memory cannot be allcoated");
      goto Finish;
    }
    //
    // Re-read the file, storing the data into our buffer
    //
    fseek (fpIn, 0, SEEK_SET);
    DataPointer = (UINTN *) FileBuffer;
    OldDataPointer = DataPointer;
    do {
      OldDataPointer = DataPointer;
      Status = MicrocodeReadData (fpIn, DataPointer++);
      if (Status == STATUS_IGNORE) {
        DataPointer = OldDataPointer;
        Status = STATUS_SUCCESS;
      }
    } while (Status == STATUS_SUCCESS);
    //
    // close input file after read data
    //
    fclose (fpIn);

    //
    // Can't do much checking on the header because, per the spec, the
    // DataSize field may be 0, which means DataSize = 2000 and TotalSize = 2K,
    // and the TotalSize field is invalid (actually missing). Thus we can't
    // even verify the Reserved fields are 0.
    //
    MciHeader = (MICROCODE_IMAGE_HEADER *) FileBuffer;
    if (MciHeader->DataSize == 0) {
      Index = 2048;
    } else {
      Index = MciHeader->TotalSize;
    }

    if (Index != FileLength) {
      Error (NULL, 0, 3000, "Invalid", "file contents of %s (0x%x) do not equal expected TotalSize: 0x%04X", mInImageName, FileLength, Index);
      goto Finish;
    }

    //
    // Checksum the contents
    //
    DataPointer = (UINTN *) FileBuffer;
    CheckSum  = 0;
    Index     = 0;
    while (Index < FileLength) {
      CheckSum    += *DataPointer;
      DataPointer ++;
      Index       += sizeof (UINTN);
    }
    if (CheckSum != 0) {
      Error (NULL, 0, 3000, "Invalid", "checksum (0x%x) failed on file contents of %s", CheckSum, mInImageName);
      goto Finish;
    }
    //
    // Open the output file and write the buffer contents
    //
    if (fpOut != NULL) {
      if (fwrite (FileBuffer, FileLength, 1, fpOut) != 1) {
        Error (NULL, 0, 0002, "Error writing file", OutImageName);
        goto Finish;
      }
    }
    
    if (ReplaceFlag) {
      fpInOut = fopen (mInImageName, "wb");
      if (fpInOut != NULL) {
        Error (NULL, 0, 0001, "Error opening file", mInImageName);
        goto Finish;
      }
      if (fwrite (FileBuffer, FileLength, 1, fpInOut) != 1) {
        Error (NULL, 0, 0002, "Error writing file", mInImageName);
        goto Finish;
      }
    }
    VerboseMsg ("the size of output file is %d bytes", FileLength);
    //
    //  Convert Mci.TXT to Mci.bin file successfully
    //
    goto Finish;
  }

  //
  // Open input file and read file data into file buffer.
  //
  fpIn = fopen (mInImageName, "rb");
  if (!fpIn) {
    Error (NULL, 0, 0001, "Error opening file", mInImageName);
    goto Finish;
  }

  FileLength = _filelength (fileno (fpIn));
  FileBuffer = malloc (FileLength);
  if (FileBuffer == NULL) {
    Error (NULL, 0, 4001, "Resource", "memory cannot be allcoated");
    fclose (fpIn);
    goto Finish;
  }
  
  fread (FileBuffer, 1, FileLength, fpIn);
  fclose (fpIn);
  
  DebugMsg (NULL, 0, 9, "input file info", "the input file size is %d bytes", FileLength);
  
  //
  // Replace file
  //
  if (ReplaceFlag) {
    fpInOut = fopen (mInImageName, "wb");
    if (!fpInOut) {
      Error (NULL, 0, 0001, "Error opening file", mInImageName);
      goto Finish;
    }
  }
  //
  // Dump TeImage Header into output file.
  //
  if (OutImageType == DUMP_TE_HEADER) {
    memcpy (&TEImageHeader, FileBuffer, sizeof (TEImageHeader));
    if (TEImageHeader.Signature != EFI_TE_IMAGE_HEADER_SIGNATURE) {
      Error (NULL, 0, 3000, "Invalid", "TE header signature of file %s is not correct", mInImageName);
      goto Finish;      
    }
    if (fpInOut != NULL) {
      fprintf (fpInOut, "Dump of file %s\n\n", mInImageName);
      fprintf (fpInOut, "TE IMAGE HEADER VALUES\n");
      fprintf (fpInOut, "%17X machine\n", TEImageHeader.Machine);
      fprintf (fpInOut, "%17X number of sections\n", TEImageHeader.NumberOfSections);
      fprintf (fpInOut, "%17X subsystems\n", TEImageHeader.Subsystem);
      fprintf (fpInOut, "%17X stripped size\n", TEImageHeader.StrippedSize);
      fprintf (fpInOut, "%17X entry point\n", TEImageHeader.AddressOfEntryPoint);
      fprintf (fpInOut, "%17X base of code\n", TEImageHeader.BaseOfCode);
      fprintf (fpInOut, "%17X image base\n", TEImageHeader.ImageBase);
      fprintf (fpInOut, "%17X [%8X] RVA [size] of Base Relocation Directory\n", TEImageHeader.DataDirectory[0].VirtualAddress, TEImageHeader.DataDirectory[0].Size);
      fprintf (fpInOut, "%17X [%8X] RVA [size] of Debug Directory\n", TEImageHeader.DataDirectory[1].VirtualAddress, TEImageHeader.DataDirectory[1].Size);
    }

    if (fpOut != NULL) {
      fprintf (fpOut, "Dump of file %s\n\n", mInImageName);
      fprintf (fpOut, "TE IMAGE HEADER VALUES\n");
      fprintf (fpOut, "%17X machine\n", TEImageHeader.Machine);
      fprintf (fpOut, "%17X number of sections\n", TEImageHeader.NumberOfSections);
      fprintf (fpOut, "%17X subsystems\n", TEImageHeader.Subsystem);
      fprintf (fpOut, "%17X stripped size\n", TEImageHeader.StrippedSize);
      fprintf (fpOut, "%17X entry point\n", TEImageHeader.AddressOfEntryPoint);
      fprintf (fpOut, "%17X base of code\n", TEImageHeader.BaseOfCode);
      fprintf (fpOut, "%17X image base\n", TEImageHeader.ImageBase);
      fprintf (fpOut, "%17X [%8X] RVA [size] of Base Relocation Directory\n", TEImageHeader.DataDirectory[0].VirtualAddress, TEImageHeader.DataDirectory[0].Size);
      fprintf (fpOut, "%17X [%8X] RVA [size] of Debug Directory\n", TEImageHeader.DataDirectory[1].VirtualAddress, TEImageHeader.DataDirectory[1].Size);
    }
    goto Finish;
  }

  //
  // Following code to convert dll to efi image or te image.
  // Get new image type
  //
  if ((OutImageType == FW_EFI_IMAGE) || (OutImageType == FW_TE_IMAGE)) {
    if (ModuleType == NULL) {
      if (OutImageType == FW_EFI_IMAGE) {
        Error (NULL, 0, 1001, "Missing option", "EFI_FILETYPE");
        goto Finish;
      } else if (OutImageType == FW_TE_IMAGE) {
        //
        // Default TE Image Type is Boot service driver
        //
        Type = EFI_IMAGE_SUBSYSTEM_EFI_BOOT_SERVICE_DRIVER;
        VerboseMsg ("Efi Image substytem type is efi boot service driver");
      }
    } else {
      if (stricmp (ModuleType, "BASE") == 0 ||
          stricmp (ModuleType, "SEC") == 0 ||
          stricmp (ModuleType, "SECURITY_CORE") == 0 ||
          stricmp (ModuleType, "PEI_CORE") == 0 ||
          stricmp (ModuleType, "PEIM") == 0 ||
          stricmp (ModuleType, "COMBINED_PEIM_DRIVER") == 0 ||
          stricmp (ModuleType, "PIC_PEIM") == 0 ||
          stricmp (ModuleType, "RELOCATABLE_PEIM") == 0 ||
          stricmp (ModuleType, "DXE_CORE") == 0 ||
          stricmp (ModuleType, "BS_DRIVER") == 0  ||
          stricmp (ModuleType, "DXE_DRIVER") == 0 ||
          stricmp (ModuleType, "DXE_SMM_DRIVER") == 0  ||
          stricmp (ModuleType, "UEFI_DRIVER") == 0) {
        Type = EFI_IMAGE_SUBSYSTEM_EFI_BOOT_SERVICE_DRIVER;
        VerboseMsg ("Efi Image substytem type is efi boot service driver");
    
      } else if (stricmp (ModuleType, "UEFI_APPLICATION") == 0 || 
                 stricmp (ModuleType, "APPLICATION") == 0) {
        Type = EFI_IMAGE_SUBSYSTEM_EFI_APPLICATION;
        VerboseMsg ("Efi Image substytem type is efi application");
    
      } else if (stricmp (ModuleType, "DXE_RUNTIME_DRIVER") == 0 || 
                 stricmp (ModuleType, "RT_DRIVER") == 0) {
        Type = EFI_IMAGE_SUBSYSTEM_EFI_RUNTIME_DRIVER;
        VerboseMsg ("Efi Image substytem type is efi runtime driver");
    
      } else if (stricmp (ModuleType, "DXE_SAL_DRIVER") == 0 || 
                 stricmp (ModuleType, "SAL_RT_DRIVER") == 0) {
        Type = EFI_IMAGE_SUBSYSTEM_SAL_RUNTIME_DRIVER;
        VerboseMsg ("Efi Image substytem type is efi sal runtime driver");
    
      } else {
        Error (NULL, 0, 1003, "Invalid option value", "EFI_FILETYPE = %s", ModuleType);
        goto Finish;
      }
    }
  }

  //
  // Convert EFL image to PeImage
  //
#ifdef HAVE_ELF
  if (IsElfHeader(FileBuffer)) {
    VerboseMsg ("Convert the input ELF Image to Pe Image");
    ConvertElf(&FileBuffer, &FileLength);
  }
#endif

  //
  // Read the dos & pe hdrs of the image
  //
  DosHdr = (EFI_IMAGE_DOS_HEADER *)FileBuffer;
  if (DosHdr->e_magic != EFI_IMAGE_DOS_SIGNATURE) {
    Error (NULL, 0, 3000, "Invalid", "DOS header signature not found in %s image", mInImageName);
    goto Finish;
  }

  PeHdr = (EFI_IMAGE_NT_HEADERS *)(FileBuffer + DosHdr->e_lfanew);
  if (PeHdr->Signature != EFI_IMAGE_NT_SIGNATURE) {
    Error (NULL, 0, 3000, "Invalid", "PE header signature not found in %s image", mInImageName);
    goto Finish;
  }
  
  //
  // Extract bin data from Pe image.
  //
  if (OutImageType == FW_BIN_IMAGE) {
    if (FileLength < PeHdr->OptionalHeader.SizeOfHeaders) {
      Error (NULL, 0, 3000, "Invalid", "FileSize of %s is not a legal size.", mInImageName);
      goto Finish;
    }
    //
    // Output bin data from exe file
    //
    if (fpOut != NULL) {
      fwrite (FileBuffer + PeHdr->OptionalHeader.SizeOfHeaders, 1, FileLength - PeHdr->OptionalHeader.SizeOfHeaders, fpOut);
    }
    if (fpInOut != NULL) {
      fwrite (FileBuffer + PeHdr->OptionalHeader.SizeOfHeaders, 1, FileLength - PeHdr->OptionalHeader.SizeOfHeaders, fpInOut);
    }
    VerboseMsg ("the size of output file is %d bytes", FileLength - PeHdr->OptionalHeader.SizeOfHeaders);
    goto Finish;
  }

  //
  // Zero Debug Information of Pe Image
  //
  if (OutImageType == FW_ZERO_DEBUG_IMAGE) {
    Status = ZeroDebugData (FileBuffer);
    if (EFI_ERROR (Status)) {
      goto Finish;
    }
    
    if (fpOut != NULL) {
      fwrite (FileBuffer, 1, FileLength, fpOut);
    }
    if (fpInOut != NULL) {
      fwrite (FileBuffer, 1, FileLength, fpInOut);
    }
    VerboseMsg ("the size of output file is %d bytes", FileLength);
    goto Finish; 
  }

  //
  // Set Time Stamp of Pe Image
  //
  if (OutImageType == FW_SET_STAMP_IMAGE) {
    Status = SetStamp (FileBuffer, TimeStamp);
    if (EFI_ERROR (Status)) {
      goto Finish;
    }
    
    if (fpOut != NULL) {
      fwrite (FileBuffer, 1, FileLength, fpOut);  
    }
    if (fpInOut != NULL) {
      fwrite (FileBuffer, 1, FileLength, fpInOut);
    }
    VerboseMsg ("the size of output file is %d bytes", FileLength);
    goto Finish;
  }

  //
  // Extract acpi data from pe image.
  //
  if (OutImageType == FW_ACPI_IMAGE) {
    SectionHeader = (EFI_IMAGE_SECTION_HEADER *) ((UINT8 *) &(PeHdr->OptionalHeader) + PeHdr->FileHeader.SizeOfOptionalHeader); 
    for (Index = 0; Index < PeHdr->FileHeader.NumberOfSections; Index ++, SectionHeader ++) {
      if (strcmp (SectionHeader->Name, ".data") == 0 || strcmp (SectionHeader->Name, ".sdata") == 0) {
        //
        // Check Acpi Table
        //
        if (SectionHeader->Misc.VirtualSize < SectionHeader->SizeOfRawData) {
          FileLength = SectionHeader->Misc.VirtualSize;
        } else {
          FileLength = SectionHeader->SizeOfRawData;
        }

        if (CheckAcpiTable (FileBuffer + SectionHeader->PointerToRawData, FileLength) != STATUS_SUCCESS) {
          Error (NULL, 0, 3000, "Invalid", "failed to check ACPI table in %s", mInImageName);
          goto Finish;
        }
        
        //
        // Output Apci data to file
        //
        if (fpOut != NULL) {
          fwrite (FileBuffer + SectionHeader->PointerToRawData, 1, FileLength, fpOut);
        }
        if (fpInOut != NULL) {
          fwrite (FileBuffer + SectionHeader->PointerToRawData, 1, FileLength, fpInOut);
        }
        VerboseMsg ("the size of output file is %d bytes", FileLength);
        goto Finish;
      }
    }
    Error (NULL, 0, 3000, "Invalid", "failed to get ACPI table from %s", mInImageName);
    goto Finish;
  }
  //
  // Zero all unused fields of the DOS header
  //
  memcpy (&BackupDosHdr, DosHdr, sizeof (EFI_IMAGE_DOS_HEADER));
  memset (DosHdr, 0, sizeof (EFI_IMAGE_DOS_HEADER));
  DosHdr->e_magic  = BackupDosHdr.e_magic;
  DosHdr->e_lfanew = BackupDosHdr.e_lfanew;

  for (Index = sizeof (EFI_IMAGE_DOS_HEADER); Index < (UINT32 ) DosHdr->e_lfanew; Index++) {
    FileBuffer[Index] = DosHdr->e_cp;
  }
  
  //
  // Initialize TeImage Header
  //
  memset (&TEImageHeader, 0, sizeof (EFI_TE_IMAGE_HEADER));
  TEImageHeader.Signature        = EFI_TE_IMAGE_HEADER_SIGNATURE;
  TEImageHeader.Machine          = PeHdr->FileHeader.Machine;
  TEImageHeader.NumberOfSections = (UINT8) PeHdr->FileHeader.NumberOfSections;
  TEImageHeader.StrippedSize     = (UINT16) ((UINTN) ((UINT8 *) &(PeHdr->OptionalHeader) + PeHdr->FileHeader.SizeOfOptionalHeader) - (UINTN) FileBuffer);
  TEImageHeader.Subsystem        = (UINT8) Type;

  //
  // Patch the PE header
  //
  PeHdr->OptionalHeader.Subsystem = (UINT16) Type;

  if (PeHdr->OptionalHeader.Magic == EFI_IMAGE_NT_OPTIONAL_HDR32_MAGIC) {
    Optional32 = (EFI_IMAGE_OPTIONAL_HEADER32 *)&PeHdr->OptionalHeader;
    Optional32->MajorLinkerVersion          = 0;
    Optional32->MinorLinkerVersion          = 0;
    Optional32->MajorOperatingSystemVersion = 0;
    Optional32->MinorOperatingSystemVersion = 0;
    Optional32->MajorImageVersion           = 0;
    Optional32->MinorImageVersion           = 0;
    Optional32->MajorSubsystemVersion       = 0;
    Optional32->MinorSubsystemVersion       = 0;
    Optional32->Win32VersionValue           = 0;
    Optional32->CheckSum                    = 0;
    Optional32->SizeOfStackReserve = 0;
    Optional32->SizeOfStackCommit  = 0;
    Optional32->SizeOfHeapReserve  = 0;
    Optional32->SizeOfHeapCommit   = 0;
    
    TEImageHeader.AddressOfEntryPoint = Optional32->AddressOfEntryPoint;
    TEImageHeader.BaseOfCode          = Optional32->BaseOfCode;
    TEImageHeader.ImageBase           = (UINT64) (Optional32->ImageBase);

    if (Optional32->NumberOfRvaAndSizes > EFI_IMAGE_DIRECTORY_ENTRY_BASERELOC) {
      TEImageHeader.DataDirectory[EFI_TE_IMAGE_DIRECTORY_ENTRY_BASERELOC].VirtualAddress = Optional32->DataDirectory[EFI_IMAGE_DIRECTORY_ENTRY_BASERELOC].VirtualAddress;
      TEImageHeader.DataDirectory[EFI_TE_IMAGE_DIRECTORY_ENTRY_BASERELOC].Size = Optional32->DataDirectory[EFI_IMAGE_DIRECTORY_ENTRY_BASERELOC].Size;
    }

    if (Optional32->NumberOfRvaAndSizes > EFI_IMAGE_DIRECTORY_ENTRY_DEBUG) {
      TEImageHeader.DataDirectory[EFI_TE_IMAGE_DIRECTORY_ENTRY_DEBUG].VirtualAddress = Optional32->DataDirectory[EFI_IMAGE_DIRECTORY_ENTRY_DEBUG].VirtualAddress;
      TEImageHeader.DataDirectory[EFI_TE_IMAGE_DIRECTORY_ENTRY_DEBUG].Size = Optional32->DataDirectory[EFI_IMAGE_DIRECTORY_ENTRY_DEBUG].Size;
    }

    //
    // Strip zero padding at the end of the .reloc section 
    //
    if (Optional32->NumberOfRvaAndSizes > EFI_IMAGE_DIRECTORY_ENTRY_BASERELOC) {
      if (Optional32->DataDirectory[EFI_IMAGE_DIRECTORY_ENTRY_BASERELOC].Size != 0) {
        SectionHeader = (EFI_IMAGE_SECTION_HEADER *)(FileBuffer + DosHdr->e_lfanew + sizeof(UINT32) + sizeof (EFI_IMAGE_FILE_HEADER) + PeHdr->FileHeader.SizeOfOptionalHeader);
        for (Index = 0; Index < PeHdr->FileHeader.NumberOfSections; Index++, SectionHeader++) {
          //
          // Look for the Section Header that starts as the same virtual address as the Base Relocation Data Directory
          //
          if (SectionHeader->VirtualAddress == Optional32->DataDirectory[EFI_IMAGE_DIRECTORY_ENTRY_BASERELOC].VirtualAddress) {
            SectionHeader->Misc.VirtualSize = Optional32->DataDirectory[EFI_IMAGE_DIRECTORY_ENTRY_BASERELOC].Size;
            AllignedRelocSize = (Optional32->DataDirectory[EFI_IMAGE_DIRECTORY_ENTRY_BASERELOC].Size + Optional32->FileAlignment - 1) & (~(Optional32->FileAlignment - 1));
            //
            // Check to see if there is zero padding at the end of the base relocations
            //
            if (AllignedRelocSize < SectionHeader->SizeOfRawData) {
              //
              // Check to see if the base relocations are at the end of the file
              //
              if (SectionHeader->PointerToRawData + SectionHeader->SizeOfRawData == Optional32->SizeOfImage) {
                //
                // All the required conditions are met to strip the zero padding of the end of the base relocations section
                //
                Optional32->SizeOfImage -= (SectionHeader->SizeOfRawData - AllignedRelocSize);
                Optional32->SizeOfInitializedData -= (SectionHeader->SizeOfRawData - AllignedRelocSize);
                SectionHeader->SizeOfRawData = AllignedRelocSize;
                FileLength = Optional32->SizeOfImage;
                DebugMsg (NULL, 0, 9, "Remove the zero padding bytes at the end of the base relocations", "The size of padding bytes is %d", SectionHeader->SizeOfRawData - AllignedRelocSize);
              }
            }
          }
        }
      }
    }
  } 

  if (PeHdr->OptionalHeader.Magic == EFI_IMAGE_NT_OPTIONAL_HDR64_MAGIC) {
    Optional64 = (EFI_IMAGE_OPTIONAL_HEADER64 *)&PeHdr->OptionalHeader;
    Optional64->MajorLinkerVersion          = 0;
    Optional64->MinorLinkerVersion          = 0;
    Optional64->MajorOperatingSystemVersion = 0;
    Optional64->MinorOperatingSystemVersion = 0;
    Optional64->MajorImageVersion           = 0;
    Optional64->MinorImageVersion           = 0;
    Optional64->MajorSubsystemVersion       = 0;
    Optional64->MinorSubsystemVersion       = 0;
    Optional64->Win32VersionValue           = 0;
    Optional64->CheckSum                    = 0;
    Optional64->SizeOfStackReserve = 0;
    Optional64->SizeOfStackCommit  = 0;
    Optional64->SizeOfHeapReserve  = 0;
    Optional64->SizeOfHeapCommit   = 0;

    TEImageHeader.AddressOfEntryPoint = Optional64->AddressOfEntryPoint;
    TEImageHeader.BaseOfCode          = Optional64->BaseOfCode;
    TEImageHeader.ImageBase           = (UINT64) (Optional64->ImageBase);

    if (Optional64->NumberOfRvaAndSizes > EFI_IMAGE_DIRECTORY_ENTRY_BASERELOC) {
      TEImageHeader.DataDirectory[EFI_TE_IMAGE_DIRECTORY_ENTRY_BASERELOC].VirtualAddress = Optional64->DataDirectory[EFI_IMAGE_DIRECTORY_ENTRY_BASERELOC].VirtualAddress;
      TEImageHeader.DataDirectory[EFI_TE_IMAGE_DIRECTORY_ENTRY_BASERELOC].Size = Optional64->DataDirectory[EFI_IMAGE_DIRECTORY_ENTRY_BASERELOC].Size;
    }

    if (Optional64->NumberOfRvaAndSizes > EFI_IMAGE_DIRECTORY_ENTRY_DEBUG) {
      TEImageHeader.DataDirectory[EFI_TE_IMAGE_DIRECTORY_ENTRY_DEBUG].VirtualAddress = Optional64->DataDirectory[EFI_IMAGE_DIRECTORY_ENTRY_DEBUG].VirtualAddress;
      TEImageHeader.DataDirectory[EFI_TE_IMAGE_DIRECTORY_ENTRY_DEBUG].Size = Optional64->DataDirectory[EFI_IMAGE_DIRECTORY_ENTRY_DEBUG].Size;
    }

    //
    // Zero the .pdata section if the machine type is X64 and the Debug Directory is empty
    //
    if (PeHdr->FileHeader.Machine == IMAGE_FILE_MACHINE_X64) { // X64
      if (Optional64->NumberOfRvaAndSizes > EFI_IMAGE_DIRECTORY_ENTRY_EXCEPTION) {
        if (Optional64->NumberOfRvaAndSizes <= EFI_IMAGE_DIRECTORY_ENTRY_DEBUG || (Optional64->NumberOfRvaAndSizes > EFI_IMAGE_DIRECTORY_ENTRY_DEBUG && Optional64->DataDirectory[EFI_IMAGE_DIRECTORY_ENTRY_DEBUG].Size == 0)) {
          SectionHeader = (EFI_IMAGE_SECTION_HEADER *)(FileBuffer + DosHdr->e_lfanew + sizeof(UINT32) + sizeof (EFI_IMAGE_FILE_HEADER) + PeHdr->FileHeader.SizeOfOptionalHeader);
          for (Index = 0; Index < PeHdr->FileHeader.NumberOfSections; Index++, SectionHeader++) {
            if (SectionHeader->VirtualAddress == Optional64->DataDirectory[EFI_IMAGE_DIRECTORY_ENTRY_EXCEPTION].VirtualAddress) {
              RuntimeFunction = (RUNTIME_FUNCTION *)(FileBuffer + SectionHeader->PointerToRawData);
              for (Index1 = 0; Index1 < Optional64->DataDirectory[EFI_IMAGE_DIRECTORY_ENTRY_EXCEPTION].Size / sizeof (RUNTIME_FUNCTION); Index1++, RuntimeFunction++) {
                SectionHeader = (EFI_IMAGE_SECTION_HEADER *)(FileBuffer + DosHdr->e_lfanew + sizeof(UINT32) + sizeof (EFI_IMAGE_FILE_HEADER) + PeHdr->FileHeader.SizeOfOptionalHeader);
                for (Index2 = 0; Index2 < PeHdr->FileHeader.NumberOfSections; Index2++, SectionHeader++) {
                  if (RuntimeFunction->UnwindInfoAddress > SectionHeader->VirtualAddress && RuntimeFunction->UnwindInfoAddress < (SectionHeader->VirtualAddress + SectionHeader->SizeOfRawData)) {
                    UnwindInfo = (UNWIND_INFO *)(FileBuffer + SectionHeader->PointerToRawData + (RuntimeFunction->UnwindInfoAddress - SectionHeader->VirtualAddress));
                    if (UnwindInfo->Version == 1) {
                      memset (UnwindInfo + 1, 0, UnwindInfo->CountOfUnwindCodes * sizeof (UINT16));
                      memset (UnwindInfo, 0, sizeof (UNWIND_INFO));
                    }
                  }
                }
                memset (RuntimeFunction, 0, sizeof (RUNTIME_FUNCTION));
              }
              DebugMsg (NULL, 0, 9, "Zero the .pdata section if the machine type is X64 and the Debug Directory is empty", NULL);

              break;
            }
          }
          Optional64->DataDirectory[EFI_IMAGE_DIRECTORY_ENTRY_EXCEPTION].Size = 0;
          Optional64->DataDirectory[EFI_IMAGE_DIRECTORY_ENTRY_EXCEPTION].VirtualAddress = 0;
        }
      }
    }

    //
    // Strip zero padding at the end of the .reloc section 
    //
    if (Optional64->NumberOfRvaAndSizes > EFI_IMAGE_DIRECTORY_ENTRY_DEBUG) {
      if (Optional64->DataDirectory[EFI_IMAGE_DIRECTORY_ENTRY_BASERELOC].Size != 0) {
        SectionHeader = (EFI_IMAGE_SECTION_HEADER *)(FileBuffer + DosHdr->e_lfanew + sizeof(UINT32) + sizeof (EFI_IMAGE_FILE_HEADER) + PeHdr->FileHeader.SizeOfOptionalHeader);
        for (Index = 0; Index < PeHdr->FileHeader.NumberOfSections; Index++, SectionHeader++) {
          //
          // Look for the Section Header that starts as the same virtual address as the Base Relocation Data Directory
          //
          if (SectionHeader->VirtualAddress == Optional64->DataDirectory[EFI_IMAGE_DIRECTORY_ENTRY_BASERELOC].VirtualAddress) {
            SectionHeader->Misc.VirtualSize = Optional64->DataDirectory[EFI_IMAGE_DIRECTORY_ENTRY_BASERELOC].Size;
            AllignedRelocSize = (Optional64->DataDirectory[EFI_IMAGE_DIRECTORY_ENTRY_BASERELOC].Size + Optional64->FileAlignment - 1) & (~(Optional64->FileAlignment - 1));
            //
            // Check to see if there is zero padding at the end of the base relocations
            //
            if (AllignedRelocSize < SectionHeader->SizeOfRawData) {
              //
              // Check to see if the base relocations are at the end of the file
              //
              if (SectionHeader->PointerToRawData + SectionHeader->SizeOfRawData == Optional64->SizeOfImage) {
                //
                // All the required conditions are met to strip the zero padding of the end of the base relocations section
                //
                Optional64->SizeOfImage -= (SectionHeader->SizeOfRawData - AllignedRelocSize);
                Optional64->SizeOfInitializedData -= (SectionHeader->SizeOfRawData - AllignedRelocSize);
                SectionHeader->SizeOfRawData = AllignedRelocSize;
                FileLength = Optional64->SizeOfImage;
                DebugMsg (NULL, 0, 9, "Remove the zero padding bytes at the end of the base relocations", "The size of padding bytes is %d", SectionHeader->SizeOfRawData - AllignedRelocSize);
              }
            }
          }
        }
      }
    }
  }

  if (OutImageType == FW_TE_IMAGE) {
    if ((PeHdr->FileHeader.NumberOfSections &~0xFF) || (Type &~0xFF)) {
      //
      // Pack the subsystem and NumberOfSections into 1 byte. Make sure they fit both.
      //
      Error (NULL, 0, 3000, "Invalid", "Image subsystem or NumberOfSections of PeImage %s cannot be packed into 1 byte", mInImageName);
      goto Finish;
    }

    if ((PeHdr->OptionalHeader.SectionAlignment != PeHdr->OptionalHeader.FileAlignment)) {
      //
      // TeImage has the same section alignment and file alignment.
      //
      Error (NULL, 0, 3000, "Invalid", "Section-Alignment and File-Alignment of PeImage %s does not match for TeImage", mInImageName);
      goto Finish;
    }
    
    DebugMsg (NULL, 0, 9, "TeImage Header Info", "Machine type is %X, Sections number is %X, Stripped size is %X, EntryPoint is %X, BaseOfCode is %X, ImageBase is %X", 
              TEImageHeader.Machine, TEImageHeader.NumberOfSections, TEImageHeader.StrippedSize, TEImageHeader.AddressOfEntryPoint, TEImageHeader.BaseOfCode, TEImageHeader.ImageBase);
    //
    // Update Image to TeImage
    //
    if (fpOut != NULL) {
      fwrite (&TEImageHeader, 1, sizeof (EFI_TE_IMAGE_HEADER), fpOut);
      fwrite (FileBuffer + TEImageHeader.StrippedSize, 1, FileLength - TEImageHeader.StrippedSize, fpOut);
    }
    if (fpInOut != NULL) {
      fwrite (&TEImageHeader, 1, sizeof (EFI_TE_IMAGE_HEADER), fpInOut);
      fwrite (FileBuffer + TEImageHeader.StrippedSize, 1, FileLength - TEImageHeader.StrippedSize, fpInOut);
    }
    VerboseMsg ("the size of output file is %d bytes", FileLength - TEImageHeader.StrippedSize);
    goto Finish;
  }
  
  //
  // Update Image to EfiImage
  //
  if (fpOut != NULL) {
    fwrite (FileBuffer, 1, FileLength, fpOut);
  }
  if (fpInOut != NULL) {
    fwrite (FileBuffer, 1, FileLength, fpInOut);
  }
  VerboseMsg ("the size of output file is %d bytes", FileLength);

Finish:
  if (FileBuffer != NULL) {
    free (FileBuffer);
  }
  
  if (InputFileName != NULL) {
    free (InputFileName);
  }

  if (fpOut != NULL) {
    //
    // Write converted data into fpOut file and close output file.
    //
    fclose (fpOut);
  }

  if (fpInOut != NULL) {
    //
    // Write converted data into fpInOut file and close input file.
    //
    fclose (fpInOut);
  }
  
  VerboseMsg ("%s tool done with return code is 0x%x.", UTILITY_NAME, GetUtilityStatus ());
  
  return GetUtilityStatus ();
}

STATIC
EFI_STATUS
ZeroDebugData (
  IN OUT UINT8   *FileBuffer
  )
/*++

Routine Description:

  Zero debug information in PeImage.

Arguments:

  FileBuffer    - Pointer to PeImage.

Returns:

  EFI_ABORTED   - PeImage is invalid.
  EFI_SUCCESS   - Zero debug data successfully.

--*/
{
  UINTN                           Index;
  UINTN                           DebugDirectoryEntryRva;
  UINTN                           DebugDirectoryEntryFileOffset;
  EFI_IMAGE_DOS_HEADER            *DosHdr;
  EFI_IMAGE_FILE_HEADER           *FileHdr;
  EFI_IMAGE_OPTIONAL_HEADER32     *Optional32Hdr;
  EFI_IMAGE_OPTIONAL_HEADER64     *Optional64Hdr;
  EFI_IMAGE_SECTION_HEADER        *SectionHeader;
  EFI_IMAGE_DEBUG_DIRECTORY_ENTRY *DebugEntry;
   
  DosHdr   = (EFI_IMAGE_DOS_HEADER *)  FileBuffer;
  FileHdr  = (EFI_IMAGE_FILE_HEADER *) (FileBuffer + DosHdr->e_lfanew + sizeof (UINT32));
  DebugDirectoryEntryRva = 0;

  //
  // Get DebugEntryTable RVA address.
  //
  if (FileHdr->Machine == EFI_IMAGE_MACHINE_IA32) {
    Optional32Hdr = (EFI_IMAGE_OPTIONAL_HEADER32 *) ((UINT8*) FileHdr + sizeof (EFI_IMAGE_FILE_HEADER));
    SectionHeader = (EFI_IMAGE_SECTION_HEADER *) ((UINT8 *) Optional32Hdr +  FileHdr->SizeOfOptionalHeader);
    if (Optional32Hdr->NumberOfRvaAndSizes > EFI_IMAGE_DIRECTORY_ENTRY_DEBUG && \
        Optional32Hdr->DataDirectory[EFI_IMAGE_DIRECTORY_ENTRY_DEBUG].Size != 0) {
      DebugDirectoryEntryRva = Optional32Hdr->DataDirectory[EFI_IMAGE_DIRECTORY_ENTRY_DEBUG].VirtualAddress;
    } else {
      //
      // No Debug Data, nothing to do.
      //
      return EFI_SUCCESS;
    }
  } else {
    Optional64Hdr = (EFI_IMAGE_OPTIONAL_HEADER64 *) ((UINT8*) FileHdr + sizeof (EFI_IMAGE_FILE_HEADER));
    SectionHeader = (EFI_IMAGE_SECTION_HEADER *) ((UINT8 *) Optional64Hdr +  FileHdr->SizeOfOptionalHeader);
    if (Optional64Hdr->NumberOfRvaAndSizes > EFI_IMAGE_DIRECTORY_ENTRY_DEBUG && \
        Optional64Hdr->DataDirectory[EFI_IMAGE_DIRECTORY_ENTRY_DEBUG].Size != 0) {
      DebugDirectoryEntryRva = Optional64Hdr->DataDirectory[EFI_IMAGE_DIRECTORY_ENTRY_DEBUG].VirtualAddress;
    } else {
      //
      // No Debug Data, nothing to do.
      //
      return EFI_SUCCESS;
    }
  }
  
  //
  // Get DebugEntryTable file offset.
  //
  for (Index = 0; Index < FileHdr->NumberOfSections; Index ++, SectionHeader ++) {
    if (DebugDirectoryEntryRva >= SectionHeader->VirtualAddress &&
        DebugDirectoryEntryRva < SectionHeader->VirtualAddress + SectionHeader->Misc.VirtualSize) {
        DebugDirectoryEntryFileOffset =
        DebugDirectoryEntryRva - SectionHeader->VirtualAddress + SectionHeader->PointerToRawData;
      break;
    }
  }
  
  if (Index >= FileHdr->NumberOfSections) {
    Error (NULL, 0, 3000, "Invalid", "PeImage");
    return EFI_ABORTED;
  }
  
  //
  // Zero Debug Data and TimeStamp
  //
  DebugEntry = (EFI_IMAGE_DEBUG_DIRECTORY_ENTRY *) (FileBuffer + DebugDirectoryEntryFileOffset);
  DebugEntry->TimeDateStamp = 0;
  memset (FileBuffer + DebugEntry->FileOffset, 0, DebugEntry->SizeOfData);
  
  return EFI_SUCCESS;
}

STATIC 
EFI_STATUS
SetStamp (
  IN OUT UINT8  *FileBuffer, 
  IN     CHAR8  *TimeStamp
  )
/*++

Routine Description:

  Set new time stamp into PeImage FileHdr and Directory table: 
  Debug, Export and Resource.

Arguments:

  FileBuffer    - Pointer to PeImage.
  TimeStamp     - Time stamp string.

Returns:

  EFI_INVALID_PARAMETER   - TimeStamp format is not recognized.
  EFI_SUCCESS             - Set new time stamp in this image successfully.

--*/
{
  struct tm                       stime;
  struct tm                       *ptime;
  time_t                          newtime;
  UINTN                           Index;
  UINTN                           DebugDirectoryEntryRva;
  UINTN                           DebugDirectoryEntryFileOffset;
  UINTN                           ExportDirectoryEntryRva;
  UINTN                           ExportDirectoryEntryFileOffset;
  UINTN                           ResourceDirectoryEntryRva;
  UINTN                           ResourceDirectoryEntryFileOffset;
  EFI_IMAGE_DOS_HEADER            *DosHdr;
  EFI_IMAGE_FILE_HEADER           *FileHdr;
  EFI_IMAGE_OPTIONAL_HEADER32     *Optional32Hdr;
  EFI_IMAGE_OPTIONAL_HEADER64     *Optional64Hdr;
  EFI_IMAGE_SECTION_HEADER        *SectionHeader;
  UINT32                          *NewTimeStamp;
  
  //
  // Init variable.
  //  
  DebugDirectoryEntryRva    = 0;
  ExportDirectoryEntryRva   = 0;
  ResourceDirectoryEntryRva = 0;

  //
  // Get time and date that will be set.
  //
  if (TimeStamp == NULL) {
    Error (NULL, 0, 3000, "Invalid", "TimeData can't be NULL");
    return EFI_INVALID_PARAMETER;
  }
  //
  // compare the value with "NOW", if yes, current system time is set.
  //
  if (stricmp (TimeStamp, "NOW") == 0) {
    //
    // get system current time and date
    //
    time (&newtime);
  } else {
    //
    // get the date and time from TimeStamp
    //
    if (sscanf (TimeStamp, "%d-%d-%d %d:%d:%d",
            &stime.tm_year,
            &stime.tm_mon,
            &stime.tm_mday,
            &stime.tm_hour,
            &stime.tm_min,
            &stime.tm_sec
            ) != 6) {
      Error (NULL, 0, 3000, "Invalid", "%s Invaild date or time!", TimeStamp);
      return EFI_INVALID_PARAMETER;
    }

    //
    // in struct, Month (0 - 11; Jan = 0). So decrease 1 from it
    //
    stime.tm_mon -= 1;
  
    //
    // in struct, Year (current year minus 1900)
    // and only the dates can be handled from Jan 1, 1970 to Jan 18, 2038
    //
    //
    // convert 0 -> 100 (2000), 1 -> 101 (2001), ..., 38 -> 138 (2038)
    //
    if (stime.tm_year <= 38) {
      stime.tm_year += 100;
    } else if (stime.tm_year >= 1970) {
      //
      // convert 1970 -> 70, 2000 -> 100, ...
      //
      stime.tm_year -= 1900;
    }

    //
    // convert the date and time to time_t format
    //
    newtime = mktime (&stime);
    if (newtime == (time_t) - 1) {
      Error (NULL, 0, 3000, "Invalid", "%s Invaild date or time!", TimeStamp);
      return EFI_INVALID_PARAMETER;
    }
  }
  
  ptime = localtime (&newtime);
  DebugMsg (NULL, 0, 9, "New Image Time Stamp", "%04d-%02d-%02d %02d:%02d:%02d",
            ptime->tm_year + 1900, ptime->tm_mon + 1, ptime->tm_mday, ptime->tm_hour, ptime->tm_min, ptime->tm_sec); 
  //
  // Set new time and data into PeImage.
  //
  DosHdr   = (EFI_IMAGE_DOS_HEADER *)  FileBuffer;
  FileHdr  = (EFI_IMAGE_FILE_HEADER *) (FileBuffer + DosHdr->e_lfanew + sizeof (UINT32));
  
  //
  // Get Debug, Export and Resource EntryTable RVA address.
  // Resource Directory entry need to review.
  //
  if (FileHdr->Machine == EFI_IMAGE_MACHINE_IA32) {
    Optional32Hdr = (EFI_IMAGE_OPTIONAL_HEADER32 *) ((UINT8*) FileHdr + sizeof (EFI_IMAGE_FILE_HEADER));
    SectionHeader = (EFI_IMAGE_SECTION_HEADER *) ((UINT8 *) Optional32Hdr +  FileHdr->SizeOfOptionalHeader);
    if (Optional32Hdr->NumberOfRvaAndSizes > EFI_IMAGE_DIRECTORY_ENTRY_EXPORT && \
        Optional32Hdr->DataDirectory[EFI_IMAGE_DIRECTORY_ENTRY_EXPORT].Size != 0) {
      ExportDirectoryEntryRva = Optional32Hdr->DataDirectory[EFI_IMAGE_DIRECTORY_ENTRY_EXPORT].VirtualAddress;
    }
    if (Optional32Hdr->NumberOfRvaAndSizes > EFI_IMAGE_DIRECTORY_ENTRY_RESOURCE && \
        Optional32Hdr->DataDirectory[EFI_IMAGE_DIRECTORY_ENTRY_RESOURCE].Size != 0) {
      ResourceDirectoryEntryRva = Optional32Hdr->DataDirectory[EFI_IMAGE_DIRECTORY_ENTRY_RESOURCE].VirtualAddress;
    }
    if (Optional32Hdr->NumberOfRvaAndSizes > EFI_IMAGE_DIRECTORY_ENTRY_DEBUG && \
        Optional32Hdr->DataDirectory[EFI_IMAGE_DIRECTORY_ENTRY_DEBUG].Size != 0) {
      DebugDirectoryEntryRva = Optional32Hdr->DataDirectory[EFI_IMAGE_DIRECTORY_ENTRY_DEBUG].VirtualAddress;
    }
  } else {
    Optional64Hdr = (EFI_IMAGE_OPTIONAL_HEADER64 *) ((UINT8*) FileHdr + sizeof (EFI_IMAGE_FILE_HEADER));
    SectionHeader = (EFI_IMAGE_SECTION_HEADER *) ((UINT8 *) Optional64Hdr +  FileHdr->SizeOfOptionalHeader);
    if (Optional64Hdr->NumberOfRvaAndSizes > EFI_IMAGE_DIRECTORY_ENTRY_EXPORT && \
        Optional64Hdr->DataDirectory[EFI_IMAGE_DIRECTORY_ENTRY_EXPORT].Size != 0) {
      ExportDirectoryEntryRva = Optional64Hdr->DataDirectory[EFI_IMAGE_DIRECTORY_ENTRY_EXPORT].VirtualAddress;
    }
    if (Optional64Hdr->NumberOfRvaAndSizes > EFI_IMAGE_DIRECTORY_ENTRY_RESOURCE && \
        Optional64Hdr->DataDirectory[EFI_IMAGE_DIRECTORY_ENTRY_RESOURCE].Size != 0) {
      ResourceDirectoryEntryRva = Optional64Hdr->DataDirectory[EFI_IMAGE_DIRECTORY_ENTRY_RESOURCE].VirtualAddress;
    }
    if (Optional64Hdr->NumberOfRvaAndSizes > EFI_IMAGE_DIRECTORY_ENTRY_DEBUG && \
        Optional64Hdr->DataDirectory[EFI_IMAGE_DIRECTORY_ENTRY_DEBUG].Size != 0) {
      DebugDirectoryEntryRva = Optional64Hdr->DataDirectory[EFI_IMAGE_DIRECTORY_ENTRY_DEBUG].VirtualAddress;
    }
  }

  //
  // Get DirectoryEntryTable file offset.
  //
  for (Index = 0; Index < FileHdr->NumberOfSections; Index ++, SectionHeader ++) {
    if (DebugDirectoryEntryRva >= SectionHeader->VirtualAddress &&
        DebugDirectoryEntryRva < SectionHeader->VirtualAddress + SectionHeader->Misc.VirtualSize) {
        DebugDirectoryEntryFileOffset =
        DebugDirectoryEntryRva - SectionHeader->VirtualAddress + SectionHeader->PointerToRawData;
    }
    if (ExportDirectoryEntryRva >= SectionHeader->VirtualAddress &&
        ExportDirectoryEntryRva < SectionHeader->VirtualAddress + SectionHeader->Misc.VirtualSize) {
        ExportDirectoryEntryFileOffset =
        ExportDirectoryEntryRva - SectionHeader->VirtualAddress + SectionHeader->PointerToRawData;
    }
    if (ResourceDirectoryEntryRva >= SectionHeader->VirtualAddress &&
        ResourceDirectoryEntryRva < SectionHeader->VirtualAddress + SectionHeader->Misc.VirtualSize) {
        ResourceDirectoryEntryFileOffset =
        ResourceDirectoryEntryRva - SectionHeader->VirtualAddress + SectionHeader->PointerToRawData;
    }
  }
  
  //
  // Set new stamp
  //
  FileHdr->TimeDateStamp = (UINT32) newtime;

  if (ExportDirectoryEntryRva != 0) {
    NewTimeStamp  = (UINT32 *) (FileBuffer + ExportDirectoryEntryFileOffset + sizeof (UINT32));
    *NewTimeStamp = (UINT32) newtime;
  }

  if (ResourceDirectoryEntryRva != 0) {
    NewTimeStamp  = (UINT32 *) (FileBuffer + ResourceDirectoryEntryFileOffset + sizeof (UINT32));
    *NewTimeStamp = (UINT32) newtime;
  }

  if (DebugDirectoryEntryRva != 0) {
    NewTimeStamp  = (UINT32 *) (FileBuffer + DebugDirectoryEntryFileOffset + sizeof (UINT32));
    *NewTimeStamp = (UINT32) newtime;
  }
  
  return EFI_SUCCESS;
}

STATIC
STATUS
MicrocodeReadData (
  FILE          *InFptr,
  UINTN         *Data
  )
/*++

Routine Description:
  Read a 32-bit microcode data value from a text file and convert to raw binary form.

Arguments:
  InFptr    - file pointer to input text file
  Data      - pointer to where to return the data parsed

Returns:
  STATUS_SUCCESS    - no errors or warnings, Data contains valid information
  STATUS_ERROR      - errors were encountered

--*/
{
  CHAR8  Line[MAX_LINE_LEN];
  CHAR8  *cptr;
  UINT8  ctr;

  Line[MAX_LINE_LEN - 1]  = 0;
  if (fgets (Line, MAX_LINE_LEN, InFptr) == NULL) {
    return STATUS_ERROR;
  }

  // Strip leading white-space characters (except carriage returns) from Line
  //
  if (isspace(Line[0]) && Line[0] != '\n') {
    // printf("Found a space character at Line[0] = 0x%x\n", Line[0]);
    while (isspace(Line[0])) {
       for (ctr = 0; ctr < strlen(Line); ctr++)
         if (Line[ctr] != '\n')
           Line[ctr] = Line[ctr + 1];
    }
  }

  //
  // If it was a binary file, then it may have overwritten our null terminator
  //
  if (Line[MAX_LINE_LEN - 1] != 0) {
    return STATUS_ERROR;
  }

  // Look for
  // dd 000000001h ; comment
  // dd XXXXXXXX
  // DD  XXXXXXXXX
  //  DD XXXXXXXXX
  //
  for (cptr = Line; *cptr && isspace(*cptr); cptr++) {
  }

  if ((tolower(cptr[0]) == 'd') && (tolower(cptr[1]) == 'd') && isspace (cptr[2])) {
    //
    // Skip blanks and look for a hex digit
    //
    cptr += 3;
    for (; *cptr && isspace(*cptr); cptr++) {
    }
    if (isxdigit (*cptr)) {
      if (sscanf (cptr, "%X", Data) != 1) {
        return STATUS_ERROR;
      }
    }
    return STATUS_SUCCESS;
  }
  // Skip Blank Lines 
  if (strlen(Line) == 1) {
    return STATUS_IGNORE;
  }
  // Skip Comment Lines
  if (tolower(cptr[0]) == ';') {
    return STATUS_IGNORE;
  }

  return STATUS_ERROR;
}
