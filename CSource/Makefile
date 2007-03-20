ARCH = IA32

!INCLUDE MSmakefile.common

LIBRARIES = Common CustomizedCompress String PeCoffLoader
APPLICATIONS = CreateMtFile EfiCompress EfiRom FlashMap FwImage GenAcpiTable \
               GenBsfFixup GenBsfImage GenCapsuleHdr GenCRC32Section GenDepex \
               GenFfsFile GenFvImage GenFvMap GenSection GenTEImage GuidChk \
               MakeDeps ModifyInf PeiRebase SecApResetVectorFixup SecFixup \
               SetStamp SplitFile StrGather Strip Pccts VfrCompile ZeroDebugData

all: libs apps install

libs: $(LIBRARIES)
	@echo.
	@echo ######################
	@echo # Build libraries
	@echo ######################
	@if not exist $(LIB_PATH) mkdir $(LIB_PATH)
	@for %%i in ($**) do @pushd . & cd %%i & $(MAKE) -f MSmakefile & popd

apps: $(APPLICATIONS)
	@echo.
	@echo ######################
	@echo # Build executables
	@echo ######################
	@if not exist $(BIN_PATH) mkdir $(BIN_PATH)
	@for %%i in ($**) do @pushd . & cd %%i & $(MAKE) -f MSmakefile & popd

install: $(LIB_PATH) $(BIN_PATH)
	@echo.
	@echo ######################
	@echo # Install to $(SYS_LIB_PATH)
	@echo ######################
	@xcopy $(LIB_PATH) $(SYS_LIB_PATH) /I /D /E /F /Y
	@xcopy $(BIN_PATH) $(SYS_BIN_PATH) /I /D /E /F /Y

.PHONY: clean
clean:
	@for %%i in ($(LIBRARIES) $(APPLICATIONS)) do @pushd . & cd %%i & $(MAKE) -f MSmakefile clean & popd

.PHONY: cleanall
cleanall:
	@for %%i in ($(LIBRARIES) $(APPLICATIONS)) do @pushd . & cd %%i & $(MAKE) -f MSmakefile cleanall & popd
        @del /f /q $(BIN_PATH)\*.pdb $(BIN_PATH)\*.ilk

!INCLUDE MSmakefile.rule

