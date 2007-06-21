ARCH ?= IA32
MAKEROOT = .

include header.makefile

LIBRARIES = 

all: subdirs $(MAKEROOT)/libs

SUBDIRS := Common CustomizedCompress String Pccts CreateMtFile EfiCompress EfiRom FlashMap FwImage GenAcpiTable GenBsfFixup GenBsfImage GenCRC32Section GenDepex GenFvImage GenFvMap GenSection GenTEImage MakeDeps ModifyInf SecApResetVectorFixup SecFixup SetStamp SplitFile StrGather Strip VfrCompile ZeroDebugData

.PHONY: subdirs $(SUBDIRS)
subdirs: $(SUBDIRS)
$(SUBDIRS):
	$(MAKE) -C $@

.PHONY: $(patsubst %,%-clean,$(sort $(SUBDIRS)))
$(patsubst %,%-clean,$(sort $(SUBDIRS))):
	-$(MAKE) -C $(@:-clean=) clean

clean:  $(patsubst %,%-clean,$(sort $(SUBDIRS)))

include footer.makefile
