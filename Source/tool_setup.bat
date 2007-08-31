@REM
@REM Copyright (c) 2007, Intel Corporation
@REM All rights reserved. This program and the accompanying materials
@REM are licensed and made available under the terms and conditions of the BSD License
@REM which accompanies this distribution.  The full text of the license may be found at
@REM http://opensource.org/licenses/bsd-license.php
@REM
@REM THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
@REM WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.
@REM

@echo off

REM ##############################################################
REM # You should not have to modify anything below this line
REM #
REM # This script executes from the Source Directory of the BaseTools project

if /I "%1"=="-h" goto Usage
if /I "%1"=="-help" goto Usage
if /I "%1"=="--help" goto Usage
if /I "%1"=="/h" goto Usage
if /I "%1"=="/?" goto Usage
if /I "%1"=="/help" goto Usage
if NOT "%1"=="" goto Usage


REM
REM check the EDK_TOOLS_PATH
REM
if not defined EDK_TOOLS_PATH goto no_tools_path
if not exist %EDK_TOOLS_PATH% goto no_tools_path

set BASE_TOOLS_PATH=%CD%\..
set PATH=%BASE_TOOLS_PATH%\Bin;%BASE_TOOLS_PATH%\Bin\Win32;%PATH%

if /I "%1"=="build" goto build
if /I "%1"=="rebuild" goto rebuild

IF NOT EXIST "%EDK_TOOLS_PATH%\Bin\Win32\antlr.exe" goto build
IF NOT EXIST "%EDK_TOOLS_PATH%\Bin\Win32\dlg.exe" goto build
IF NOT EXIST "%EDK_TOOLS_PATH%\Bin\Win32\BootSectImage.exe" goto build
IF NOT EXIST "%EDK_TOOLS_PATH%\Bin\Win32\EfiLdrImage.exe" goto build
IF NOT EXIST "%EDK_TOOLS_PATH%\Bin\Win32\EfiRom.exe" goto build
IF NOT EXIST "%EDK_TOOLS_PATH%\Bin\Win32\GenBootSector.exe" goto build
IF NOT EXIST "%EDK_TOOLS_PATH%\Bin\Win32\GenFfs.exe" goto build
IF NOT EXIST "%EDK_TOOLS_PATH%\Bin\Win32\GenFv.exe" goto build
IF NOT EXIST "%EDK_TOOLS_PATH%\Bin\Win32\GenFw.exe" goto build
IF NOT EXIST "%EDK_TOOLS_PATH%\Bin\Win32\GenPage.exe" goto build
IF NOT EXIST "%EDK_TOOLS_PATH%\Bin\Win32\GenSec.exe" goto build
IF NOT EXIST "%EDK_TOOLS_PATH%\Bin\Win32\GenVtf.exe" goto build
IF NOT EXIST "%EDK_TOOLS_PATH%\Bin\Win32\Split.exe" goto build
IF NOT EXIST "%EDK_TOOLS_PATH%\Bin\Win32\TianoCompress.exe" goto build
REM IF NOT EXIST "%EDK_TOOLS_PATH%\Bin\Win32\VfrCompile.exe" goto build

REM
REM Python Programs
REM

REM IF NOT EXIST "%EDK_TOOLS_PATH%\Bin\Win32\build.exe" goto build
REM IF NOT EXIST "%EDK_TOOLS_PATH%\Bin\Win32\GenFds.exe" goto build_python
REM IF NOT EXIST "%EDK_TOOLS_PATH%\Bin\Win32\PcdSyntaxUpdate.exe" goto build_python
REM IF NOT EXIST "%EDK_TOOLS_PATH%\Bin\Win32\TargetTool.exe" goto build_python
REM IF NOT EXIST "%EDK_TOOLS_PATH%\Bin\Win32\Trim.exe" goto build_python
goto end

:rebuild
pushd .
cd %BASE_TOOLS_PATH%\Source\C
call nmake cleanall
popd

:build
REM
REM Start to build the Framework Tools
REM

echo.
echo Building the Framework C-based Tools
echo.

pushd .
cd %BASE_TOOLS_PATH%\Source\C
call nmake
popd

REM :build_python
REM
REM pushd .
REM %BASE_TOOLS_PATH%\Source\Python
REM set PYTHONPATH=%BASE_TOOLS_PATH%\Source\Python
REM call FreezePython script here!
REM popd
REM

@REM
@REM Done!!!
@REM
goto end

:no_tools_path
echo.
echo !!! ERROR !!! No tools path found. Please set EDK_TOOLS_PATH.
echo.
goto end

:Usage
echo.
echo  Usage: %0 [build] [rebuild]
echo         build:    Incremental build, only build those updated tools; 
echo         rebuild:  Rebuild all tools neither updated or not; 
echo.

:end
@echo on
