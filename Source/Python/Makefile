
FREEZE=$(PYTHON_FREEZER_PATH)\FreezePython.exe

MODULES=encodings.cp437,encodings.gbk,encodings.utf_16,encodings.utf_8

BIN_DIR=$(EDK_TOOLS_PATH)\Bin\Win32


APPLICATIONS=$(BIN_DIR)\build.exe $(BIN_DIR)\GenFds.exe $(BIN_DIR)\Trim.exe $(BIN_DIR)\MigrationMsa2Inf.exe $(BIN_DIR)\TargetTool.exe

all: $(APPLICATIONS)
  

$(BIN_DIR)\build.exe: $(BASE_TOOLS_PATH)\Source\Python\build\build.py
  @pushd . & @cd build & @$(FREEZE) --include-modules=$(MODULES) --install-dir=$(BIN_DIR) build.py & @popd

$(BIN_DIR)\GenFds.exe: $(BASE_TOOLS_PATH)\Source\Python\GenFds\GenFds.py
  @pushd . & @cd GenFds & @$(FREEZE) --include-modules=$(MODULES) --install-dir=$(BIN_DIR) GenFds.py & @popd

$(BIN_DIR)\Trim.exe: $(BASE_TOOLS_PATH)\Source\Python\Trim\Trim.py
  @pushd . & @cd Trim & @$(FREEZE) --include-modules=$(MODULES) --install-dir=$(BIN_DIR) Trim.py & @popd

$(BIN_DIR)\MigrationMsa2Inf.exe: $(BASE_TOOLS_PATH)\Source\Python\MigrationMsa2Inf\MigrationMsa2Inf.py
  @pushd . & @cd MigrationMsa2Inf & @$(FREEZE) --include-modules=$(MODULES) --install-dir=$(BIN_DIR) MigrationMsa2Inf.py & @popd 

$(BIN_DIR)\TargetTool.exe: $(BASE_TOOLS_PATH)\Source\Python\TargetTool\TargetTool.py
  @pushd . & @cd TargetTool & @$(FREEZE) --include-modules=$(MODULES) --install-dir=$(BIN_DIR) TargetTool.py & @popd


cleanall:  
  @del /f /q $(BIN_DIR)\*.pyd $(BIN_DIR)\*.dll
  @for %%i in ($(APPLICATIONS)) do @del /f /q %%i

