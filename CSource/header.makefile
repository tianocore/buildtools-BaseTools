# The makefile can be invoked with
# ARCH = x86_64 or x64 for EM64T build
# ARCH = ia32 or IA32 for IA32 build
# ARCH = ia64 or IA64 for IA64 build
#
ARCH ?= IA32

# Root directory where uefi lib and header files will be installed
INSTALLROOT = /usr/local
# Relative to INSTALL_ROOT
UEFI_HDR = include/uefi

ifeq ($(ARCH), IA32)
CC = gcc
AS = gcc
AR = ar
LD = ld
ARCH_INCLUDE = -I $(MAKEROOT)/Include/Ia32/
ASFLAGS = 
endif

ifeq ($(ARCH), X64)
CC = gcc
AS = gcc
AR = ar
LD = ld
ARCH_INCLUDE = -I $(MAKEROOT)/Include/x64/
endif

INCLUDE =  -I $(MAKEROOT) -I $(MAKEROOT)/Include/Common -I $(MAKEROOT)/Include/ -I $(MAKEROOT)/Include/IndustryStandard -I $(MAKEROOT)/Common/ -I .. -I . $(ARCH_INCLUDE) 
CPPFLAGS = $(INCLUDE)
CFLAGS = -MD -fshort-wchar -fno-strict-aliasing -fno-merge-constants -nostdlib -Wall -c -shared

.PHONY: all
.PHONY: install
.PHONY: clean

all:

$(MAKEROOT)/libs:
	mkdir $(MAKEROOT)/libs 

$(MAKEROOT)/bin:
	mkdir $(MAKEROOT)/bin
