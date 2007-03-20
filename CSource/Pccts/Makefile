!INCLUDE ..\MSmakefile.common
ARCH = IA32

all:
	@pushd . & cd antlr & $(MAKE) BIN_DIR=$(BIN_PATH) SOURCE_DIR=$(SOURCE_PATH) -f AntlrMs.mak & popd
	@pushd . & cd dlg   & $(MAKE) BIN_DIR=$(BIN_PATH) SOURCE_DIR=$(SOURCE_PATH) -f DlgMs.mak   & popd

clean:
	@pushd . & cd antlr & $(MAKE) BIN_DIR=$(BIN_PATH) SOURCE_DIR=$(SOURCE_PATH) -f AntlrMs.mak clean & popd
	@pushd . & cd dlg   & $(MAKE) BIN_DIR=$(BIN_PATH) SOURCE_DIR=$(SOURCE_PATH) -f DlgMs.mak clean   & popd

cleanall:
	@pushd . & cd antlr & $(MAKE) BIN_DIR=$(BIN_PATH) SOURCE_DIR=$(SOURCE_PATH) -f AntlrMs.mak distclean & popd
	@pushd . & cd dlg   & $(MAKE) BIN_DIR=$(BIN_PATH) SOURCE_DIR=$(SOURCE_PATH) -f DlgMs.mak distclean   & popd

