ARCH ?= IA32
MAKEROOT ?= ..

all: $(MAKEROOT)/bin
	$(MAKE) BIN_DIR=../../bin -C antlr -f makefile
	$(MAKE) BIN_DIR=../../bin -C dlg -f makefile

$(MAKEROOT)/bin:
	mkdir $(MAKEROOT)/bin
