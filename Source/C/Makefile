ARCH = IA32

!INCLUDE MSmakefile.common

LIBRARIES = Common PeCoffLoader String
APPLICATIONS = GenFw GenSec GenFv GenFfs GenVtf EfiRom LzmaCompress TianoCompress

all: libs apps install

libs: $(LIBRARIES)
	@echo.
	@echo ######################
	@echo # Build libraries
	@echo ######################
	@if not exist $(LIB_PATH) mkdir $(LIB_PATH)
	@for %%i in ($**) do @pushd . & cd %%i & $(MAKE) & popd

apps: $(APPLICATIONS)
	@echo.
	@echo ######################
	@echo # Build executables
	@echo ######################
	@if not exist $(BIN_PATH) mkdir $(BIN_PATH)
	@for %%i in ($**) do @pushd . & cd %%i & $(MAKE) & popd

install: $(LIB_PATH) $(BIN_PATH)
	@echo.
	@echo ######################
	@echo # Install to $(SYS_LIB_PATH)
	@echo ######################
	@xcopy $(LIB_PATH)\*.lib $(SYS_LIB_PATH) /I /D /E /F /Y
	@xcopy $(BIN_PATH)\*.exe $(SYS_BIN_PATH) /I /D /E /F /Y

.PHONY: clean
clean:
	@for %%i in ($(LIBRARIES) $(APPLICATIONS)) do @pushd . & cd %%i & $(MAKE) clean & popd

.PHONY: cleanall
cleanall:
	@for %%i in ($(LIBRARIES) $(APPLICATIONS)) do @pushd . & cd %%i & $(MAKE) cleanall & popd
        @del /f /q $(BIN_PATH)\*.pdb $(BIN_PATH)\*.ilk

!INCLUDE MSmakefile.rule

