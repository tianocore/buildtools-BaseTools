/** @file
  Converts an elf image to  pe32+ image

  Copyright (c) 2004 - 2009, Intel Corporation
  All rights reserved. This program and the accompanying materials
  are licensed and made available under the terms and conditions of the BSD License
  which accompanies this distribution.  The full text of the license may be found at
  http://opensource.org/licenses/bsd-license.php

  THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
  WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.

**/

//
// List of OS and CPU which support ELF to PE conversion
//

#if defined(unix) || defined(linux)
#if defined (__i386__) || defined(__x86_64__)
#define HAVE_ELF
#endif
#endif

#ifdef HAVE_ELF

#include <iostream>
#include <fstream>
#include <list>
#include <string>

using namespace std;

extern "C" {

#include <stdlib.h>
#include <string.h>
#include <time.h>

#include <elf.h>

#ifndef R_386_NONE
#define R_386_NONE      0
#endif

#ifndef R_386_32
#define R_386_32        1
#endif

#ifndef R_386_PC32
#define R_386_PC32      2
#endif

#include <Common/UefiBaseTypes.h>
#include <IndustryStandard/PeImage.h>

#include "CommonLib.h"
#include "EfiUtilityMsgs.h"

extern CHAR8 *mInImageName;

}

template <class Elf_Shdr>
int
IsTextShdr (
  Elf_Shdr *Shdr
  )
{
  return (Shdr->sh_flags & (SHF_WRITE | SHF_ALLOC)) == SHF_ALLOC;
}

template <class Elf_Shdr>
int
IsDataShdr (
  Elf_Shdr *Shdr
  )
{
  return (Shdr->sh_flags & (SHF_WRITE | SHF_ALLOC)) == (SHF_ALLOC | SHF_WRITE);
}


template
  <typename Elf_Shdr,
   typename Elf_Ehdr,
   typename Elf_Rel,
   typename Elf_Rela,
   typename Elf_Sym,
   typename Elf_GotAddr,
   typename IMAGE_NT_HEADER
  >
class ElfToPeCoffConverter
{

public:
  ElfToPeCoffConverter(
    int ELFCLASS,
    int EM_VALUE,
    UINT8  **FileBuffer,
    UINT32 *FileLength
    )
  {
    CoffAlignment = 0x20;
    CoffNbrSections = 4;
    CoffFile = NULL;
    CoffSectionsOffset = NULL;
    this->ELFCLASS = ELFCLASS;
    this->EM_VALUE = EM_VALUE;
    this->FileBuffer = FileBuffer;
    this->FileLength = FileLength;
    Ehdr = (Elf_Ehdr*)*FileBuffer;
  }

  UINT8  **FileBuffer;
  UINT32 *FileLength;

  //
  // Well known ELF structures.
  //
  Elf_Ehdr *Ehdr;
  Elf_Shdr *ShdrBase;
  char *NamesForSections;

  //
  // Sections
  //
  list<Elf_Shdr*> ElfSections;
  list<Elf_Shdr*> XferSections;
  bool DirectMappedSections;

  //
  // Relocations
  //
  list<UINT32> Relocations;

  //
  // PE section alignment.
  //
  UINT32 CoffAlignment;
  UINT32 CoffNbrSections;

  //
  // Current offset in coff file.
  //
  UINT32 CoffOffset;

  //
  // Result Coff file in memory.
  //
  UINT8 *CoffFile;

  //
  // ELF sections to offset in Coff file.
  //
  UINT32 *CoffSectionsOffset;

  //
  // Entry point address for image
  //
  UINT32 CoffEntry;

  //
  // Offset in Coff file of headers and sections.
  //
  UINT32 NtHdrOffset;
  UINT32 TableOffset;
  UINT32 RelocOffset;

  UINT32 BaseOfCode;
  UINT32 SizeOfCode;
  UINT32 BaseOfData;
  UINT32 SizeOfData;

  UINT32 SizeOfHeaders;

  UINT32 LastSectionFileOffset;

  int ELFCLASS;
  int EM_VALUE;

  virtual
  int
  ELF_R_TYPE(int r) = 0;

  virtual
  INT64
  ELF_R_SYM(INT64 r) = 0;

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

  char *
  GetSectionName (
    Elf_Shdr *section
    )
  {
    return NamesForSections + section->sh_name;
  }

  VOID *
  GetElfSectionData (
    Elf_Shdr *section
    )
  {
    return (VOID*)((UINT8 *)Ehdr + section->sh_offset);
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
    if ((Ehdr->e_type != ET_EXEC) && (Ehdr->e_type != ET_DYN))
      return 0;
    if (Ehdr->e_machine != EM_VALUE)
      return 0;
    if (Ehdr->e_version != EV_CURRENT)
      return 0;

    //
    // Find the section header table
    //
    ShdrBase = (Elf_Shdr *)((UINT8 *)Ehdr + Ehdr->e_shoff);

    Elf_Shdr *sectionNames = GetShdrByIndex(Ehdr->e_shstrndx);
    NamesForSections = (char*)GetElfSectionData(sectionNames);

    CoffSectionsOffset = (UINT32 *)malloc(Ehdr->e_shnum * sizeof (UINT32));

    CoffEntry = Ehdr->e_entry;

    memset(CoffSectionsOffset, 0, Ehdr->e_shnum * sizeof(UINT32));
    return 1;
  }

  VOID
  CreateSectionHeader(
    const CHAR8 *Name,
    UINT32      FileOffset,
    UINT32      VirtualOffset,
    UINT32      Size,
    UINT32      Flags
    )
  {
    EFI_IMAGE_SECTION_HEADER *Hdr;
    Hdr = (EFI_IMAGE_SECTION_HEADER*)(CoffFile + TableOffset);

    strcpy((char*)Hdr->Name, Name);
    Hdr->Misc.VirtualSize = Size;
    Hdr->VirtualAddress = VirtualOffset;
    Hdr->SizeOfRawData = Size;
    Hdr->PointerToRawData = FileOffset;
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

    CoffOffset = 0;
    DirectMappedSections = true;

    //
    // Coff file start with a DOS header.
    //
    SizeOfHeaders = sizeof(EFI_IMAGE_DOS_HEADER) + 0x40;
    NtHdrOffset = SizeOfHeaders;
    SizeOfHeaders += sizeof(IMAGE_NT_HEADER);
    TableOffset = SizeOfHeaders;
    //
    // Calculate header size based on the number of sections,
    // and add in the .reloc and .debug sections.
    //
    CoffNbrSections = XferSections.size () + 2;
    SizeOfHeaders +=
      CoffNbrSections * sizeof (EFI_IMAGE_SECTION_HEADER);
    SizeOfHeaders = CoffAlign (SizeOfHeaders);

    typename list<Elf_Shdr*>::iterator it;

    UINT32 TotalSizeOfSections = 0;
    UINT32 LastSectionVirtualOffset = 0;
    UINT32 SectionVirtualEndOffset;
    for (it = XferSections.begin(); it != XferSections.end(); it++) {
      Elf_Shdr *Shdr = *it;

      if (Shdr->sh_addr < SizeOfHeaders) {
        DirectMappedSections = false;
      }

      SectionVirtualEndOffset = CoffAlign (Shdr->sh_addr + Shdr->sh_size);
      LastSectionVirtualOffset =
        MAX (LastSectionVirtualOffset, SectionVirtualEndOffset);
      TotalSizeOfSections += Shdr->sh_size;
      TotalSizeOfSections = CoffAlign (TotalSizeOfSections);
    }

    if (LastSectionVirtualOffset > (1.5 * TotalSizeOfSections)) {
      DirectMappedSections = false;
    }

    if (DirectMappedSections) {
      LastSectionFileOffset = LastSectionVirtualOffset;
    } else {
      LastSectionFileOffset = TotalSizeOfSections + SizeOfHeaders;
    }

  }

  VOID
  AddFileHeaderAndSections(
    VOID
    )
  {
    CoffFile = (UINT8*)malloc (LastSectionFileOffset);
    memset (CoffFile, 0, LastSectionFileOffset);
    bool IsTextSection;

    typename list<Elf_Shdr*>::iterator it;

    BaseOfCode = 0;
    SizeOfCode = 0;
    BaseOfData = 0;
    SizeOfData = 0;
    CoffOffset = SizeOfHeaders;
    for (it = XferSections.begin(); it != XferSections.end(); it++) {
      Elf_Shdr *Shdr = *it;
      UINT32 SectionOffset;

      IsTextSection = IsTextShdr<Elf_Shdr>(Shdr);

      if (DirectMappedSections) {
        SectionOffset = Shdr->sh_addr;
      } else {
        SectionOffset = CoffOffset;
      }

      memcpy (
        CoffFile + SectionOffset,
        GetElfSectionData (Shdr),
        Shdr->sh_size);

      if (!DirectMappedSections) {
        CoffOffset += Shdr->sh_size;
        CoffOffset = CoffAlign (CoffOffset);
      }

      UINT32 SectionFlags;
      if (IsTextSection) {
        if (BaseOfCode == 0) {
          BaseOfCode = Shdr->sh_addr;
        } else {
          BaseOfCode = MIN (BaseOfCode, Shdr->sh_addr);
        }
        SizeOfCode += Shdr->sh_size;
        SectionFlags =
          EFI_IMAGE_SCN_CNT_CODE |
          EFI_IMAGE_SCN_MEM_EXECUTE |
          EFI_IMAGE_SCN_MEM_READ;
      } else {
        if (BaseOfData == 0) {
          BaseOfData = Shdr->sh_addr;
        } else {
          BaseOfData = MIN (BaseOfData, Shdr->sh_addr);
        }
        SizeOfData += Shdr->sh_size;
        SectionFlags =
          EFI_IMAGE_SCN_CNT_INITIALIZED_DATA |
          EFI_IMAGE_SCN_MEM_WRITE |
          EFI_IMAGE_SCN_MEM_READ;
      }

      //
      // Create section header
      //
      CreateSectionHeader (
        GetSectionName (Shdr),
        SectionOffset,
        Shdr->sh_addr,
        CoffAlign (Shdr->sh_size),
        SectionFlags
        );
    }

    if (DirectMappedSections) {
      CoffOffset = LastSectionFileOffset;
    }

    FillOsHeaders ();
  }

  virtual
  VOID
  FillOsHeaders (
    )
  {
    EFI_IMAGE_DOS_HEADER *DosHdr;
    IMAGE_NT_HEADER *NtHdr;

    //
    // Fill headers.
    //
    DosHdr = (EFI_IMAGE_DOS_HEADER *)CoffFile;
    DosHdr->e_magic = EFI_IMAGE_DOS_SIGNATURE;
    DosHdr->e_lfanew = NtHdrOffset;

    NtHdr = (IMAGE_NT_HEADER*)(CoffFile + NtHdrOffset);

    NtHdr->Signature = EFI_IMAGE_NT_SIGNATURE;

    NtHdr->FileHeader.NumberOfSections = CoffNbrSections;
    NtHdr->FileHeader.TimeDateStamp = time(NULL);
    NtHdr->FileHeader.PointerToSymbolTable = 0;
    NtHdr->FileHeader.NumberOfSymbols = 0;
    NtHdr->FileHeader.SizeOfOptionalHeader = sizeof(NtHdr->OptionalHeader);
    NtHdr->FileHeader.Characteristics = EFI_IMAGE_FILE_EXECUTABLE_IMAGE
      | EFI_IMAGE_FILE_LINE_NUMS_STRIPPED
      | EFI_IMAGE_FILE_LOCAL_SYMS_STRIPPED
      | EFI_IMAGE_FILE_32BIT_MACHINE;

    NtHdr->OptionalHeader.SizeOfCode = SizeOfCode;
    NtHdr->OptionalHeader.SizeOfInitializedData = SizeOfData;
    NtHdr->OptionalHeader.SizeOfUninitializedData = 0;
    NtHdr->OptionalHeader.AddressOfEntryPoint = CoffEntry;

    NtHdr->OptionalHeader.BaseOfCode = BaseOfCode;

    NtHdr->OptionalHeader.ImageBase = 0;
    NtHdr->OptionalHeader.SectionAlignment = CoffAlignment;
    NtHdr->OptionalHeader.FileAlignment = CoffAlignment;
    NtHdr->OptionalHeader.SizeOfImage = 0;

    NtHdr->OptionalHeader.SizeOfHeaders = SizeOfHeaders;
    NtHdr->OptionalHeader.NumberOfRvaAndSizes = EFI_IMAGE_NUMBER_OF_DIRECTORY_ENTRIES;
  }

  virtual
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
    //
    //  Ignore for unkown section type.
    //
    VerboseMsg ((CHAR8*)"%s unknown section type %x. We directly copy this section into Coff file", mInImageName, (UINTN)Shdr->sh_type);
    break;
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
      Error (NULL, 0, 3000, (CHAR8*)"Invalid", (CHAR8*)"%s bad symbol definition.", mInImageName);
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
      Error (NULL, 0, 3000, (CHAR8*)"Invalid", (CHAR8*)"%s unhandled section type %x.", mInImageName, ELF_R_TYPE(Rel->r_info));
    }
        }
      }
    }
  }

  EFI_IMAGE_BASE_RELOCATION *CoffBaseRel;
  UINT16 *CoffEntryRel;
  UINT32 RelocPageVa;
  UINT32 RelocDataSize;

  VOID
  CoffAddFixupEntry (
    UINT16 Val
    )
  {
    if (CoffBaseRel != NULL) {
      *CoffEntryRel = Val;
      CoffEntryRel++;
      CoffBaseRel->SizeOfBlock += 2;
      CoffOffset += 2;
    }
    RelocDataSize += 2;
  }

  VOID
  PadToAlignRelocSection (
    int alignment = 4
    )
  {
    //
    // Pad for alignment.
    //
    while ((RelocDataSize % alignment) != 0) {
      CoffAddFixupEntry (0);
    }
  }

  VOID
  CoffAddFixup (
    UINT32 Offset,
    UINT8  Type
    )
  {
    //VerboseMsg ((CHAR8*)"CoffAddFixup: 0x%x", Offset);
    if (
         RelocDataSize == 0 ||
         RelocPageVa != (Offset & ~0xfff)
       ) {
      if (RelocDataSize != 0) {
        //
        // Add a null entry (is it required ?)
        //
        CoffAddFixupEntry (0);
        //
        // Pad for alignment.
        //
        PadToAlignRelocSection ();
      }

      RelocPageVa = Offset & ~0xfff;

      if (CoffBaseRel != NULL) {
        CoffBaseRel = (EFI_IMAGE_BASE_RELOCATION*)(CoffFile + CoffOffset);
        CoffBaseRel->VirtualAddress = RelocPageVa;
        CoffBaseRel->SizeOfBlock = sizeof(EFI_IMAGE_BASE_RELOCATION);
  
        CoffEntryRel = (UINT16 *)(CoffBaseRel + 1);
        CoffOffset += sizeof(EFI_IMAGE_BASE_RELOCATION);
      }
      RelocDataSize += sizeof(EFI_IMAGE_BASE_RELOCATION);
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
    IMAGE_NT_HEADER *NtHdr;
    EFI_IMAGE_DATA_DIRECTORY *Dir;

    Relocations.sort ();

    list<UINT32>::iterator it;

    //
    // Determine the require size for the .reloc section
    //
    CoffBaseRel = NULL;
    RelocDataSize = 0;
    for (it = Relocations.begin (); it != Relocations.end (); it++) {
      CoffAddFixup(
        *it,
        EFI_IMAGE_REL_BASED_HIGHLOW
        );
    }
    PadToAlignRelocSection (CoffAlignment);
    VerboseMsg ((CHAR8*)".reloc section size: 0x%x", RelocDataSize);

    //
    // Re-allocate the CoffFile to add space for the .reloc section
    //
    CoffFile = (UINT8*)realloc (
      (VOID*)CoffFile,
      CoffOffset + RelocDataSize
      );
    memset(
      CoffFile + CoffOffset,
      0,
      RelocDataSize
      );

    //
    // Write the data for the .reloc section
    //
    RelocOffset = CoffOffset;
    CoffBaseRel = (EFI_IMAGE_BASE_RELOCATION*)(CoffFile + CoffOffset);
    RelocDataSize = 0;
    for (it = Relocations.begin (); it != Relocations.end (); it++) {
      CoffAddFixup(
        *it,
        EFI_IMAGE_REL_BASED_HIGHLOW
        );
    }
    PadToAlignRelocSection (CoffAlignment);

    CreateSectionHeader (
      ".reloc",
      RelocOffset,
      RelocOffset,
      CoffOffset - RelocOffset,
      EFI_IMAGE_SCN_CNT_INITIALIZED_DATA |
        EFI_IMAGE_SCN_MEM_DISCARDABLE |
        EFI_IMAGE_SCN_MEM_READ
      );

    NtHdr = (IMAGE_NT_HEADER *)(CoffFile + NtHdrOffset);
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
    IMAGE_NT_HEADER *NtHdr;
    EFI_IMAGE_DATA_DIRECTORY *DataDir;
    EFI_IMAGE_DEBUG_DIRECTORY_ENTRY *Dir;
    EFI_IMAGE_DEBUG_CODEVIEW_NB10_ENTRY *Nb10;

    DebugOffset = CoffOffset;
    CoffOffset += sizeof(EFI_IMAGE_DEBUG_DIRECTORY_ENTRY)
      + sizeof(EFI_IMAGE_DEBUG_CODEVIEW_NB10_ENTRY)
      + Len;
    CoffOffset = CoffAlign(CoffOffset);

    CoffFile = (UINT8*)realloc(
      (VOID*)CoffFile,
      CoffOffset
      );
    memset(CoffFile + DebugOffset, 0, CoffOffset - DebugOffset);

    Dir = (EFI_IMAGE_DEBUG_DIRECTORY_ENTRY*)(CoffFile + DebugOffset);
    Dir->Type = EFI_IMAGE_DEBUG_TYPE_CODEVIEW;
    Dir->SizeOfData = sizeof(EFI_IMAGE_DEBUG_DIRECTORY_ENTRY) + Len;
    Dir->RVA = DebugOffset + sizeof(EFI_IMAGE_DEBUG_DIRECTORY_ENTRY);
    Dir->FileOffset = DebugOffset + sizeof(EFI_IMAGE_DEBUG_DIRECTORY_ENTRY);

    Nb10 = (EFI_IMAGE_DEBUG_CODEVIEW_NB10_ENTRY*)(Dir + 1);
    Nb10->Signature = CODEVIEW_SIGNATURE_NB10;
    strcpy ((char*)(Nb10 + 1), mInImageName);

    CreateSectionHeader (
      ".debug",
      DebugOffset,
      DebugOffset,
      CoffOffset - DebugOffset,
      EFI_IMAGE_SCN_CNT_INITIALIZED_DATA |
        EFI_IMAGE_SCN_MEM_DISCARDABLE |
        EFI_IMAGE_SCN_MEM_READ
      );

    NtHdr = (IMAGE_NT_HEADER *)(CoffFile + NtHdrOffset);
    DataDir = &NtHdr->OptionalHeader.DataDirectory[EFI_IMAGE_DIRECTORY_ENTRY_DEBUG];
    DataDir->VirtualAddress = DebugOffset;
    DataDir->Size = CoffOffset - DebugOffset;
  }

  virtual
  VOID
  ConvertElf (
    )
  {
    IMAGE_NT_HEADER *NtHdr;

    //
    // Check header, read section table.
    //
    Ehdr = (Elf_Ehdr*)*FileBuffer;
    if (!CheckElfHeader())
      return;

    ScanElfSections ();

    DebugDumpElfMainHeader ();
    DebugDumpSectionHeaders ();

    FindAllRelocations ();

    VerboseMsg ((CHAR8*)"Check Elf Image Header");
    //
    // Compute sections new address.
    //
    ScanSections();

    //
    // Write sections.
    //
    VerboseMsg ((CHAR8*)"Writing sections.");
    AddFileHeaderAndSections ();

    //
    // Translate and write relocations.
    //
    VerboseMsg ((CHAR8*)"Writing relocations.");
    WriteRelocations();

    //
    // Write debug info.
    //
    VerboseMsg ((CHAR8*)"Writing debug info.");
    WriteDebug();

    NtHdr = (IMAGE_NT_HEADER *)(CoffFile + NtHdrOffset);
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

  bool
  ShouldSectionBeTransfered (
    Elf_Shdr *Shdr
    )
  {
    string name(GetSectionName(Shdr));
    return (
      Shdr->sh_type != SHT_REL &&
      name != ".shstrtab"
      );
  }

  VOID
  ScanElfSections (
    )
  {
    int sectionNum;
    for (sectionNum = 0; ; sectionNum++) {
      Elf_Shdr *Shdr = GetShdrByIndex(sectionNum);
      if (Shdr == NULL) {
        break;
      }

      if (Shdr->sh_type == SHT_NULL) {
        continue;
      }

      ElfSections.push_back (Shdr);

      if (ShouldSectionBeTransfered (Shdr)) {
        XferSections.push_back (Shdr);
      }
    }

    VerboseMsg (
      (CHAR8*)"#ELF sections: %d, #Xfer sections: %d",
      ElfSections.size (),
      XferSections.size ()
     );
  }

  VOID
  FindAllRelocations(
    VOID
    )
  {
    typename list<Elf_Shdr*>::iterator it;

    for (it = ElfSections.begin(); it != ElfSections.end(); it++) {
      Elf_Shdr *Shdr = *it;
      string name(GetSectionName(Shdr));
      if (Shdr->sh_type == SHT_REL) {
        AddElfRelSectionRelocations (Shdr);
      } else if (Shdr->sh_type == SHT_RELA) {
        AddElfRelaSectionRelocations (Shdr);
      }
    }
    VerboseMsg (
      (CHAR8*)"Number of relocation addresses found: %d",
      Relocations.size ()
      );
  }

  VOID
  AddElfRelSectionRelocations (
    Elf_Shdr *Shdr
    )
  {
    if (Shdr->sh_type != SHT_REL) {
      return;
    }

    VerboseMsg (
      (CHAR8*)"Finding relocation addresses in section %s",
      GetSectionName (Shdr)
      );

    Elf_Shdr *SecShdr = GetShdrByIndex(Shdr->sh_info);

    if (!IsTextShdr<Elf_Shdr>(SecShdr) &&
        !IsDataShdr<Elf_Shdr>(SecShdr)) {
      return;
    }

    UINT32 RelIdx;
    for (RelIdx = 0; RelIdx < Shdr->sh_size; RelIdx += Shdr->sh_entsize) {
      Elf_Rel *Rel = (Elf_Rel *)
        ((UINT8*)Ehdr + Shdr->sh_offset + RelIdx);
      switch (ELF_R_TYPE(Rel->r_info)) {
      case R_386_NONE:
      case R_386_PC32:
        break;
      case R_386_32:
        Relocations.push_back (
          CoffSectionsOffset[Shdr->sh_info] +
          (Rel->r_offset - SecShdr->sh_addr)
          );
        break;
      default:
        Error (NULL, 0, 3000, (CHAR8*)"Invalid", (CHAR8*)"%s unhandled section type %x.", mInImageName, ELF_R_TYPE(Rel->r_info));
      }
    }
  }

  VOID
  AddElfRelaSectionRelocations (
    Elf_Shdr *Shdr
    )
  {
    if (Shdr->sh_type != SHT_RELA) {
      return;
    }

    VerboseMsg (
      (CHAR8*)"Finding relocation addresses in section %s",
      GetSectionName (Shdr)
      );

    UINT32 RelIdx;
    for (RelIdx = 0; RelIdx < Shdr->sh_size; RelIdx += Shdr->sh_entsize) {
      Elf_Rela *Rel = (Elf_Rela *)
        ((UINT8*)Ehdr + Shdr->sh_offset + RelIdx);
      switch (ELF_R_TYPE(Rel->r_info)) {
      case R_386_NONE:
      case R_386_PC32:
        break;
      case R_386_32:
      case R_X86_64_RELATIVE:
        //VerboseMsg (
        //  (CHAR8*)"Relocation from %s: 0x%x",
        //  GetSectionName (Shdr),
        //  Rel->r_offset
        //  );
        Relocations.push_back (Rel->r_offset);
        break;
      default:
        Error (NULL, 0, 3000, (CHAR8*)"Invalid", (CHAR8*)"%s unhandled relocation type %x.", mInImageName, ELF_R_TYPE(Rel->r_info));
      }
    }
  }

  VOID
  AddElfGotSectionRelocations (
    Elf_Shdr *Shdr
    )
  {
    if (string(GetSectionName(Shdr)) != ".got") {
      return;
    }

    VerboseMsg (
      (CHAR8*)"Finding GOT relocation addresses in section %s",
      GetSectionName (Shdr)
      );

    if ((Shdr->sh_size % sizeof (Elf_GotAddr)) != 0) {
      Error (
        NULL,
        0,
        3000,
        (CHAR8*)"Invalid",
        (CHAR8*)"%s contains an invalid .got section.",
        mInImageName
        );
    }

    UINT32 RelOffset;
    int GotRemaining;

    RelOffset = Shdr->sh_addr;
    GotRemaining = Shdr->sh_size;
    while (GotRemaining > 0) {
      VerboseMsg (
        (CHAR8*)"Relocation from %s: 0x%x",
        GetSectionName (Shdr),
        RelOffset
        );
      Relocations.push_back (RelOffset);
      RelOffset += sizeof (Elf_GotAddr);
      GotRemaining -= sizeof (Elf_GotAddr);
    }
  }

  VOID
  DebugDumpElfMainHeader(
    )
  {
    VerboseMsg ((CHAR8*)"ELF HDR fields:");
    #define DUMP_EHDR_ITEM(i) \
      VerboseMsg ((CHAR8*)"  %s: 0x%x", #i, Ehdr->i);
    DUMP_EHDR_ITEM(e_type);
    DUMP_EHDR_ITEM(e_machine);
    DUMP_EHDR_ITEM(e_version);
    DUMP_EHDR_ITEM(e_entry);
    DUMP_EHDR_ITEM(e_phoff);
    DUMP_EHDR_ITEM(e_shoff);
    DUMP_EHDR_ITEM(e_flags);
    DUMP_EHDR_ITEM(e_ehsize);
    DUMP_EHDR_ITEM(e_phentsize);
    DUMP_EHDR_ITEM(e_phnum);
    DUMP_EHDR_ITEM(e_shentsize);
    DUMP_EHDR_ITEM(e_shnum);
    DUMP_EHDR_ITEM(e_shstrndx);
  }

  virtual
  VOID
  DebugDumpSectionHeaders(
    )
  {
    typename list<Elf_Shdr*>::iterator it;

    for (it = ElfSections.begin(); it != ElfSections.end(); it++) {
      Elf_Shdr *Shdr = *it;
      VerboseMsg (
        (CHAR8*)"ELF SECTION (%s) header fields",
        GetSectionName(Shdr)
        );
      #define DUMP_SHDR_ITEM(i) \
        VerboseMsg ((CHAR8*)"  %s: 0x%x", #i, Shdr->i);

      DUMP_SHDR_ITEM(sh_name);
      DUMP_SHDR_ITEM(sh_type);
      DUMP_SHDR_ITEM(sh_flags);
      DUMP_SHDR_ITEM(sh_addr);
      DUMP_SHDR_ITEM(sh_offset);
      DUMP_SHDR_ITEM(sh_size);
      DUMP_SHDR_ITEM(sh_link);
      DUMP_SHDR_ITEM(sh_info);
      DUMP_SHDR_ITEM(sh_addralign);
      DUMP_SHDR_ITEM(sh_entsize);
    }
  }

};

#define ELF32_T_PARMS \
  Elf32_Shdr,Elf32_Ehdr,Elf32_Rel,Elf32_Rela,Elf32_Sym,Elf32_Addr,EFI_IMAGE_NT_HEADERS32

class Elf32ToPeCoffConverter :
  public ElfToPeCoffConverter<ELF32_T_PARMS>
{
public:

  Elf32ToPeCoffConverter (
    UINT8  **FileBuffer,
    UINT32 *FileLength
    ) :
    ElfToPeCoffConverter<ELF32_T_PARMS>(
      ELFCLASS32,
      EM_386,
      FileBuffer,
      FileLength
      )
  {
  }

  virtual
  int
  ELF_R_TYPE(int r)
  {
    return ELF32_R_TYPE(r);
  }

  virtual
  INT64
  ELF_R_SYM(INT64 r)
  {
    return ELF32_R_SYM(r);
  }

  virtual
  VOID
  FillOsHeaders (
    )
  {
    EFI_IMAGE_NT_HEADERS32 *NtHdr;
    ElfToPeCoffConverter<ELF32_T_PARMS>::FillOsHeaders();
    NtHdr = (EFI_IMAGE_NT_HEADERS32*)(CoffFile + NtHdrOffset);
    NtHdr->OptionalHeader.BaseOfData = BaseOfData;
    NtHdr->OptionalHeader.Magic = EFI_IMAGE_NT_OPTIONAL_HDR32_MAGIC;
    NtHdr->FileHeader.Machine = EFI_IMAGE_MACHINE_IA32;
  }

};

#define ELF64_T_PARMS \
  Elf64_Shdr,Elf64_Ehdr,Elf64_Rel,Elf64_Rela,Elf64_Sym,Elf64_Addr,EFI_IMAGE_NT_HEADERS64

class Elf64ToPeCoffConverter :
  public ElfToPeCoffConverter<ELF64_T_PARMS>
{
public:

  Elf64ToPeCoffConverter (
    UINT8  **FileBuffer,
    UINT32 *FileLength
    ) :
    ElfToPeCoffConverter<ELF64_T_PARMS>(
      ELFCLASS64,
      EM_X86_64,
      FileBuffer,
      FileLength
      )
  {
  }

  virtual
  int
  ELF_R_TYPE(int r)
  {
    return ELF64_R_TYPE(r);
  }

  virtual
  INT64
  ELF_R_SYM(INT64 r)
  {
    return ELF64_R_SYM(r);
  }

  virtual
  VOID
  FillOsHeaders (
    )
  {
    EFI_IMAGE_NT_HEADERS64 *NtHdr;
    ElfToPeCoffConverter<ELF64_T_PARMS>::FillOsHeaders();
    NtHdr = (EFI_IMAGE_NT_HEADERS64*)(CoffFile + NtHdrOffset);
    NtHdr->OptionalHeader.Magic = EFI_IMAGE_NT_OPTIONAL_HDR64_MAGIC;
    NtHdr->FileHeader.Machine = EFI_IMAGE_MACHINE_X64;
  }

};

extern "C"
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

extern "C"
VOID
ConvertElf (
  UINT8  **FileBuffer,
  UINT32 *FileLength
  )
{
  Elf32ToPeCoffConverter conv32 (FileBuffer, FileLength);
  Elf64ToPeCoffConverter conv64 (FileBuffer, FileLength);

  if (conv32.CheckElfHeader ()) {
    VerboseMsg((CHAR8*)"Converting ELF32 to PE32");
    conv32.ConvertElf();
  } else if (conv64.CheckElfHeader ()) {
    VerboseMsg((CHAR8*)"Converting ELF64 to PE32+");
    conv64.ConvertElf();
  }
}

#endif // HAVE_ELF

