
all: subdirs

LANGUAGES = C Python

SUBDIRS := $(patsubst %,Source/%,$(sort $(LANGUAGES)))
CLEAN_SUBDIRS := $(patsubst %,%-clean,$(sort $(SUBDIRS)))

.PHONY: subdirs $(SUBDIRS)
subdirs: $(SUBDIRS)
$(SUBDIRS):
	$(MAKE) -C $@

.PHONY: $(CLEAN_SUBDIRS)
$(CLEAN_SUBDIRS):
	-$(MAKE) -C $(@:-clean=) clean

clean:  $(CLEAN_SUBDIRS)

test:
	@$(MAKE) -C Tests

