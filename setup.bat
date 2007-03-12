@REM
@REM Copyright (c) 2006, Intel Corporation
@REM All rights reserved. This program and the accompanying materials
@REM are licensed and made available under the terms and conditions of the BSD License
@REM which accompanies this distribution.  The full text of the license may be found at
@REM http://opensource.org/licenses/bsd-license.php
@REM
@REM THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
@REM WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.
@REM

@REM set following environment in this file or in command shell
@REM set JAVA_HOME=C:\Java\jdk1.5.0_06
@REM set ANT_HOME=C:\ANT
@REM set XMLBEANS_HOME=C:\xmlbeans
@REM set CYGWIN_HOME=C:\cygwin

@REM usage: edksetup.bat [Rebuild] [ForceRebuild] [Reconfig]
@REM if the argument, skip is present, only the paths and the
@REM test and set of environment settings are performed. 

@REM ##############################################################
@REM # You should not have to modify anything below this line
@REM #

@echo off

@REM
@REM Check the required system environment variables
@REM

:check_vc
if defined VCINSTALLDIR goto check_cygwin
if defined VS71COMNTOOLS (
  call "%VS71COMNTOOLS%\vsvars32.bat"
) else (
  echo.
  echo !!! WARNING !!!! Cannot find Visual Studio !!!
  echo.
)

:check_cygwin
if defined CYGWIN_HOME goto check_java
if exist c:\cygwin (
  set CYGWIN_HOME=c:\cygwin
) else (
  echo.
  echo !!! WARNING !!!! Not set CYGWIN_HOME, gcc build may not be used !!!
  echo.
)

:check_java
if "%JAVA_HOME%"=="" goto no_jdk

:check_ant
if "%ANT_HOME%"=="" goto no_ant
if not exist %ANT_HOME%\lib\ant-contrib.jar goto no_antcontrib

:check_xmlbeans
if "%XMLBEANS_HOME%"=="" goto no_xmlbeans
if not exist %XMLBEANS_HOME%\lib\saxon8.jar goto no_saxon8

@REM
@REM Set the WORKSPACE to the current working directory
@REM
set WORKSPACE=%CD%

@REM
@REM check the EDK_TOOLS_PATH
@REM
if not defined EDK_TOOLS_PATH goto no_tools_path
if not exist %EDK_TOOLS_PATH% (
  echo.
  echo !!! WARNING !!!! %EDK_TOOLS_PATH% doesn't exist. Please check EDK_TOOLS_PATH !!!
  echo.
  goto end
)

:no_tools_path
if exist %WORKSPACE%\Tools (
  set EDK_TOOLS_PATH=%WORKSPACE%\Tools
) else (
  echo.
  echo !!! WARNING !!!! No tools path found. Please set EDK_TOOLS_PATH !!!
  echo.
  goto end
)

if defined WORKSPACE_TOOLS_PATH goto check_path
set PATH=%EDK_TOOLS_PATH%\Bin;%JAVA_HOME%\bin;%ANT_HOME%\bin;%XMLBEANS_HOME%\bin;%PATH%
echo Setting the PATH variable to include the EDK_TOOLS_PATH for this WORKSPACE
goto path_ok

:check_path
if "%EDK_TOOLS_PATH%"=="%WORKSPACE_TOOLS_PATH%" goto path_ok
set PATH=%EDK_TOOLS_PATH%;%PATH%
set WORKSPACE_TOOLS_PATH=%EDK_TOOLS_PATH%
echo Resetting the PATH variable to include the EDK_TOOLS_PATH for this WORKSPACE

:path_ok

if not defined ORIGINAL_CLASSPATH set ORIGINAL_CLASSPATH=%CLASSPATH%
set CLASSPATH=%ORIGINAL_CLASSPATH%

@if /I "%1"=="-h" goto Usage
@if /I "%1"=="-help" goto Usage
@if /I "%1"=="--help" goto Usage
@if /I "%1"=="/h" goto Usage
@if /I "%1"=="/?" goto Usage
@if /I "%1"=="/help" goto Usage
@if /I "%1"=="ForceRebuild" goto ForceBuild
@if /I "%1"=="Reconfig" goto Reconfig

@IF NOT EXIST "%EDK_TOOLS_PATH%\Jars\Common.jar" goto NormalBuild
@IF NOT EXIST "%EDK_TOOLS_PATH%\Jars\PcdTools.jar" goto NormalBuild
@IF NOT EXIST "%EDK_TOOLS_PATH%\Jars\GenBuild.jar" goto NormalBuild
@IF NOT EXIST "%EDK_TOOLS_PATH%\Jars\SurfaceArea.jar" goto NormalBuild
@IF NOT EXIST "%EDK_TOOLS_PATH%\Jars\cpptasks.jar" goto NormalBuild
@IF NOT EXIST "%EDK_TOOLS_PATH%\Jars\frameworktasks.jar" goto NormalBuild
@IF NOT EXIST "%EDK_TOOLS_PATH%\bin\FrameworkWizard.jar" goto NormalBuild
@IF NOT EXIST "%EDK_TOOLS_PATH%\bin\CompressDll.dll" goto NormalBuild
@IF NOT EXIST "%EDK_TOOLS_PATH%\bin\CompressDll.lib" goto NormalBuild
@IF NOT EXIST "%EDK_TOOLS_PATH%\bin\CreateMtFile.exe" goto NormalBuild
@IF NOT EXIST "%EDK_TOOLS_PATH%\bin\EfiCompress.exe" goto NormalBuild
@IF NOT EXIST "%EDK_TOOLS_PATH%\bin\EfiRom.exe" goto NormalBuild
@IF NOT EXIST "%EDK_TOOLS_PATH%\bin\FlashMap.exe" goto NormalBuild
@IF NOT EXIST "%EDK_TOOLS_PATH%\bin\FwImage.exe" goto NormalBuild
@IF NOT EXIST "%EDK_TOOLS_PATH%\bin\GenAcpiTable.exe" goto NormalBuild
@IF NOT EXIST "%EDK_TOOLS_PATH%\bin\GenCRC32Section.exe" goto NormalBuild
@IF NOT EXIST "%EDK_TOOLS_PATH%\bin\GenCapsuleHdr.exe" goto NormalBuild
@IF NOT EXIST "%EDK_TOOLS_PATH%\bin\GenDepex.exe" goto NormalBuild
@IF NOT EXIST "%EDK_TOOLS_PATH%\bin\GenFfsFile.exe" goto NormalBuild
@IF NOT EXIST "%EDK_TOOLS_PATH%\bin\GenFvImage.exe" goto NormalBuild
@IF NOT EXIST "%EDK_TOOLS_PATH%\bin\GenSection.exe" goto NormalBuild
@IF NOT EXIST "%EDK_TOOLS_PATH%\bin\GenTEImage.exe" goto NormalBuild
@IF NOT EXIST "%EDK_TOOLS_PATH%\bin\GuidChk.exe" goto NormalBuild
@IF NOT EXIST "%EDK_TOOLS_PATH%\bin\MakeDeps.exe" goto NormalBuild
@IF NOT EXIST "%EDK_TOOLS_PATH%\bin\ModifyInf.exe" goto NormalBuild
@IF NOT EXIST "%EDK_TOOLS_PATH%\bin\PeiRebase_Ia32.exe" goto NormalBuild
@IF NOT EXIST "%EDK_TOOLS_PATH%\bin\PeiRebase_Ipf.exe" goto NormalBuild
@IF NOT EXIST "%EDK_TOOLS_PATH%\bin\PeiRebase_X64.exe" goto NormalBuild
@IF NOT EXIST "%EDK_TOOLS_PATH%\bin\SecApResetVectorFixup.exe" goto NormalBuild
@IF NOT EXIST "%EDK_TOOLS_PATH%\bin\SecFixup.exe" goto NormalBuild
@IF NOT EXIST "%EDK_TOOLS_PATH%\bin\SetStamp.exe" goto NormalBuild
@IF NOT EXIST "%EDK_TOOLS_PATH%\bin\SplitFile.exe" goto NormalBuild
@IF NOT EXIST "%EDK_TOOLS_PATH%\bin\StrGather.exe" goto NormalBuild
@IF NOT EXIST "%EDK_TOOLS_PATH%\bin\Strip.exe" goto NormalBuild
@IF NOT EXIST "%EDK_TOOLS_PATH%\bin\VfrCompile.exe" goto NormalBuild
@IF NOT EXIST "%EDK_TOOLS_PATH%\bin\ZeroDebugData.exe" goto NormalBuild
@IF NOT EXIST "%EDK_TOOLS_PATH%\bin\antlr.exe" goto NormalBuild
@IF NOT EXIST "%EDK_TOOLS_PATH%\bin\dlg.exe" goto NormalBuild

@if /I "%1"=="Rebuild" goto NormalBuild
@if NOT "%1"=="" goto Usage

goto skipbuild

:ForceBuild 
call ant -f %EDK_TOOLS_PATH%\build.xml -noclasspath cleanall

:NormalBuild
@REM
@REM Start to build the Framework Tools
@REM

echo.
echo Building the Framework Tools
echo.

@REM
@REM We are going to create the SurfaceArea.jar file first so that the other
@REM Java Programs can use it.
@REM It needs the XMLBEANS libraries in order to compile.
@REM
set CLASSPATH=%XMLBEANS_HOME%\lib;%CLASSPATH%
set CLASSPATH=%XMLBEANS_HOME%\lib\jsr173_1.0_api.jar;%CLASSPATH%
set CLASSPATH=%XMLBEANS_HOME%\lib\xbean.jar;%CLASSPATH%
set CLASSPATH=%XMLBEANS_HOME%\lib\xbean_xpath.jar;%CLASSPATH%
set CLASSPATH=%XMLBEANS_HOME%\lib\xmlpublic.jar;%CLASSPATH%
set CLASSPATH=%XMLBEANS_HOME%\lib\saxon8.jar;%CLASSPATH%
set CLASSPATH=%XMLBEANS_HOME%\lib\resolver.jar;%CLASSPATH%

call ant -f %EDK_TOOLS_PATH%\build.xml SurfaceArea

@REM
@REM Now we can make the other Java Programs
@REM All of the remaining Java Programs require the SurfaceArea library to compile
@REM
set CLASSPATH=%EDK_TOOLS_PATH%\Jars\SurfaceArea.jar;%CLASSPATH%

call ant -f %EDK_TOOLS_PATH%\build.xml JavaCode

@REM
@REM We have all of the Java Programs and add-in classes created, so we can start
@REM using the cpp-tasks to create our tools
@REM
set CLASSPATH=%EDK_TOOLS_PATH%\Jars\Common.jar;%CLASSPATH%
set CLASSPATH=%EDK_TOOLS_PATH%\Jars\PcdTools.jar;%CLASSPATH%
set CLASSPATH=%EDK_TOOLS_PATH%\Jars\GenBuild.jar;%CLASSPATH%
set CLASSPATH=%EDK_TOOLS_PATH%\Jars\cpptasks.jar;%CLASSPATH%
set CLASSPATH=%EDK_TOOLS_PATH%\Jars\frameworktasks.jar;%CLASSPATH%
set CLASSPATH=%EDK_TOOLS_PATH%\Bin\FrameworkWizard.jar;%CLASSPATH%
set CLASSPATH=%EDK_TOOLS_PATH%\Bin\MigrationTools.jar;%CLASSPATH%

call ant -f %EDK_TOOLS_PATH%\build.xml C_Code

@REM
@REM Done!!!
@REM
goto end

:no_jdk
echo.
echo !!! Please install Java, and set JAVA_HOME !!!
echo.
goto end

:no_ant
echo.
echo !!! Please install Apache Ant, and set ANT_HOME !!!
echo.
goto end

:no_antcontrib
echo.
echo !!! Please install Ant-contrib to ANT_HOME !!!
echo.
goto end

:no_xmlbeans
echo.
echo !!! Please install XML Beans, and set XMLBEANS_HOME !!!
echo.
goto end

:no_saxon8
echo.
echo !!! Please copy saxon8.jar file to XMLBEANS_HOME\lib !!!
echo.
goto end

:skipbuild
@REM
@REM This just sets up the CLASSPATH, the rest of the environment should have been set already.
@REM
echo.
echo WORKSPACE:     %WORKSPACE%
echo JAVA_HOME:     %JAVA_HOME%
echo ANT_HOME:      %ANT_HOME%
echo XMLBEANS_HOME: %XMLBEANS_HOME%
echo CYGWIN_HOME:   %CYGWIN_HOME%
echo PATH:          %PATH%
echo.
set CLASSPATH=%XMLBEANS_HOME%\lib;%CLASSPATH%
set CLASSPATH=%XMLBEANS_HOME%\lib\jsr173_1.0_api.jar;%CLASSPATH%
set CLASSPATH=%XMLBEANS_HOME%\lib\xbean.jar;%CLASSPATH%
set CLASSPATH=%XMLBEANS_HOME%\lib\xbean_xpath.jar;%CLASSPATH%
set CLASSPATH=%XMLBEANS_HOME%\lib\xmlpublic.jar;%CLASSPATH%
set CLASSPATH=%XMLBEANS_HOME%\lib\saxon8.jar;%CLASSPATH%
set CLASSPATH=%XMLBEANS_HOME%\lib\saxon8-dom.jar;%CLASSPATH%
set CLASSPATH=%XMLBEANS_HOME%\lib\saxon8-xpath.jar;%CLASSPATH%
set CLASSPATH=%XMLBEANS_HOME%\lib\resolver.jar;%CLASSPATH%
set CLASSPATH=%EDK_TOOLS_PATH%\Jars\SurfaceArea.jar;%CLASSPATH%
set CLASSPATH=%EDK_TOOLS_PATH%\Jars\Common.jar;%CLASSPATH%
set CLASSPATH=%EDK_TOOLS_PATH%\Jars\PcdTools.jar;%CLASSPATH%
set CLASSPATH=%EDK_TOOLS_PATH%\Jars\GenBuild.jar;%CLASSPATH%
set CLASSPATH=%EDK_TOOLS_PATH%\Jars\cpptasks.jar;%CLASSPATH%
set CLASSPATH=%EDK_TOOLS_PATH%\Jars\frameworktasks.jar;%CLASSPATH%
set CLASSPATH=%EDK_TOOLS_PATH%\Bin\FrameworkWizard.jar;%CLASSPATH%
set CLASSPATH=%EDK_TOOLS_PATH%\Bin\MigrationTools.jar;%CLASSPATH%
echo CLASSPATH:     %CLASSPATH%
goto end

:Reconfig
@REM
@REM Reinstall all config files
@REM
call ant -f %EDK_TOOLS_PATH%\build.xml reconfig
goto end

:Usage
echo.
echo  Usage: %0 [Rebuild] [ForceRebuild] [Reconfig]
echo         Rebuild:       Incremental build, only build those updated tools; 
echo         ForceRebuild:  Rebuild all tools neither updated or not; 
echo         Reconfig:      Reinstall target.txt, tools_def.txt, FrameworkDatabase.db. 
echo.
echo  Note that target.template, tools_def.template, FrameworkDatabase.template will be
echo  only copied to target.txt, tools_def.txt, FrameworkDatabase.db respectively if they
echo  are not existed. Using option [Reconfig] to do the force copy. 
echo.

:end
@echo on

