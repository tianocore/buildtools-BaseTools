ARCH ?= IA32
MAKEROOT = .

include Makefiles/header.makefile

all: makerootdir subdirs $(MAKEROOT)/libs

LIBRARIES = Common
NON_BUILDABLE_APPLICATIONS = GenBootSector BootSectImage
APPLICATIONS = \
  EfiLdrImage \
  EfiRom \
  GenFfs \
  GenFv \
  GenFw \
  GenPage \
  GenSec \
  GenVtf \
  Split \
  TianoCompress \
  VolInfo \
  VfrCompile

SUBDIRS := $(LIBRARIES) $(APPLICATIONS)

.PHONY: outputdirs
makerootdir:
	-mkdir $(MAKEROOT)

.PHONY: subdirs $(SUBDIRS)
subdirs: $(SUBDIRS)
$(SUBDIRS):
	$(MAKE) -C $@

.PHONY: $(patsubst %,%-clean,$(sort $(SUBDIRS)))
$(patsubst %,%-clean,$(sort $(SUBDIRS))):
	-$(MAKE) -C $(@:-clean=) clean

clean:  $(patsubst %,%-clean,$(sort $(SUBDIRS)))

clean: localClean

localClean:
	rm -f $(MAKEROOT)/bin/*
	-rmdir $(MAKEROOT)/libs $(MAKEROOT)/bin

include Makefiles/footer.makefile
