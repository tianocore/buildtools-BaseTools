#include "stdio.h"
#include "stdlib.h"
#include "string.h"
//#include "process.h"
#include "VfrCompiler.h"
#include "EfiUtilityMsgs.h"

VOID
CVfrCompiler::SET_RUN_STATUS (
  IN COMPILER_RUN_STATUS Status
  )
{
  mRunStatus = Status;
}

BOOLEAN
CVfrCompiler::IS_RUN_STATUS (
  IN COMPILER_RUN_STATUS Status
  )
{
  return mRunStatus == Status;
}

VOID
CVfrCompiler::OptionInitialization (
  IN INT32      Argc, 
  IN CHAR8      **Argv
  )
{
  INT32         Index;
  
  SetUtilityName (PROGRAM_NAME);

  mOptions.VfrFileName[0]                = '\0';
  mOptions.RecordListFile[0]             = '\0';
  mOptions.CreateRecordListFile          = FALSE;
  mOptions.CreateIfrPkgFile              = FALSE;
  mOptions.PkgOutputFileName[0]          = '\0';
  mOptions.COutputFileName[0]            = '\0';
  mOptions.OutputDirectory[0]            = '\0';
  mOptions.PreprocessorOutputFileName[0] = '\0';
  mOptions.VfrBaseFileName[0]            = '\0';
  mOptions.IncludePaths                  = NULL;
  mOptions.SkipCPreprocessor             = FALSE;
  mOptions.CPreprocessorOptions          = NULL;

  for (Index = 1; (Index < Argc) && (Argv[Index][0] == '-'); Index++) {
    if ((strcmp(Argv[Index], "-h") == 0) || (strcmp(Argv[Index], "--help") == 0)) {
      Usage ();
      SET_RUN_STATUS (STATUS_DEAD);
      return;
    } else if (strcmp(Argv[Index], "-l") == 0) {
      mOptions.CreateRecordListFile = TRUE;
      gCIfrRecordInfoDB.TurnOn ();
    } else if (strcmp(Argv[Index], "-i") == 0) {
      Index++;
      if ((Index >= Argc) || (Argv[Index][0] == '-')) {
        Error (NULL, 0, 1001, "Missing option", "-i missing path argument"); 
        goto Fail;
      }

      AppendIncludePath(Argv[Index]);
    } else if (strcmp(Argv[Index], "-o") == 0 || strcmp(Argv[Index], "--output-directory") == 0) {
      Index++;
      if ((Index >= Argc) || (Argv[Index][0] == '-')) {
        Error (NULL, 0, 1001, "Missing option", "-od missing output directory name");
        goto Fail;
      }
      strcpy (mOptions.OutputDirectory, Argv[Index]);
      
      CHAR8 lastChar = mOptions.OutputDirectory[strlen(mOptions.OutputDirectory) - 1];
      if ((lastChar != '/') && (lastChar != '\\')) {
        if (strchr(mOptions.OutputDirectory, '/') != NULL) {
          strcat (mOptions.OutputDirectory, "/");
        } else {
          strcat (mOptions.OutputDirectory, "\\");
        }
      }
      printf("Debug! %s\n", mOptions.OutputDirectory);
    } else if (strcmp(Argv[Index], "-b") == 0 || strcmp(Argv[Index], "--create-ifr-package") == 0) {
      mOptions.CreateIfrPkgFile = TRUE;
    } else if (strcmp(Argv[Index], "--no-strings") == 0) {
    } else if (strcmp(Argv[Index], "-n") == 0 || strcmp(Argv[Index], "--no-pre-processing") == 0) {
      mOptions.SkipCPreprocessor = TRUE;
    } else if (strcmp(Argv[Index], "-f") == 0 || strcmp(Argv[Index], "--pre-processing-flag") == 0) {
      Index++;
      if ((Index >= Argc) || (Argv[Index][0] == '-')) {
        Error (NULL, 0, 1001, "Missing option", "-od - missing C-preprocessor argument");
        goto Fail;
      }

      AppendCPreprocessorOptions (Argv[Index]);
    } else {
      Error (NULL, 0, 1000, "Unknown option", "unrecognized option %s", Argv[Index]);
      Usage ();
      goto Fail;
    }
  }

  if (Index != Argc - 1) {
    Error (NULL, 0, 1001, "Missing option", "VFR file name is not specified.");
    Usage ();
    goto Fail;
  } else {
    strcpy (mOptions.VfrFileName, Argv[Index]);
  }

  if (SetBaseFileName() != 0) {
    goto Fail;
  }
  if (SetPkgOutputFileName () != 0) {
    goto Fail;
  }
  if (SetCOutputFileName() != 0) {
    goto Fail;
  }
  if (SetPreprocessorOutputFileName () != 0) {
    goto Fail;
  }
  if (SetRecordListFileName () != 0) {
    goto Fail;
  }
  return;

Fail:
  SET_RUN_STATUS (STATUS_DEAD);

  mOptions.VfrFileName[0]                = '\0';
  mOptions.RecordListFile[0]             = '\0';
  mOptions.CreateRecordListFile          = FALSE;
  mOptions.CreateIfrPkgFile              = FALSE;
  mOptions.PkgOutputFileName[0]          = '\0';
  mOptions.COutputFileName[0]            = '\0';
  mOptions.OutputDirectory[0]            = '\0';
  mOptions.PreprocessorOutputFileName[0] = '\0';
  mOptions.VfrBaseFileName[0]            = '\0';
  if (mOptions.IncludePaths != NULL) {
    delete mOptions.IncludePaths;
    mOptions.IncludePaths                = NULL;
  } 
  if (mOptions.CPreprocessorOptions != NULL) {
    delete mOptions.CPreprocessorOptions;
    mOptions.CPreprocessorOptions        = NULL;
  }
}

VOID
CVfrCompiler::AppendIncludePath (
  IN CHAR8      *PathStr
  )
{
  UINT32  Len           = 0;
  CHAR8   *IncludePaths = NULL;

  Len = strlen (" -I ") + strlen (PathStr) + 1;
  if (mOptions.IncludePaths != NULL) {
    Len += strlen (mOptions.IncludePaths);
  }
  IncludePaths = new CHAR8[Len];
  if (IncludePaths == NULL) {
    Error (NULL, 0, 4001, "Resource: memory can't be allocated", NULL);
    return;
  }
  IncludePaths[0] = '\0';
  if (mOptions.IncludePaths != NULL) {
    strcat (IncludePaths, mOptions.IncludePaths);
  }
  strcat (IncludePaths, " -I ");
  strcat (IncludePaths, PathStr);
  if (mOptions.IncludePaths != NULL) {
    delete mOptions.IncludePaths;
  }
  mOptions.IncludePaths = IncludePaths;
}

VOID
CVfrCompiler::AppendCPreprocessorOptions (
  IN CHAR8      *Options
  )
{
  UINT32  Len           = 0;
  CHAR8   *Opt          = NULL;

  Len = strlen (Options) + strlen (" ") + 1;
  if (mOptions.CPreprocessorOptions != NULL) {
    Len += strlen (mOptions.CPreprocessorOptions);
  }
  Opt = new CHAR8[Len];
  if (Opt == NULL) {
    Error (NULL, 0, 4001, "Resource: memory can't be allocated", NULL);
    return;
  }
  Opt[0] = 0;
  if (mOptions.CPreprocessorOptions != NULL) {
    strcat (Opt, mOptions.CPreprocessorOptions);
  }
  strcat (Opt, " ");
  strcat (Opt, Options);
  if (mOptions.CPreprocessorOptions != NULL) {
    delete mOptions.CPreprocessorOptions;
  }
  mOptions.CPreprocessorOptions = Opt;
}

INT8
CVfrCompiler::SetBaseFileName (
  VOID
  )
{
  CHAR8         *pFileName, *pPath, *pExt;

  if (mOptions.VfrFileName[0] == '\0') {
    return -1;
  }

  pFileName = mOptions.VfrFileName;
  while (
    ((pPath = strchr (pFileName, '\\')) != NULL) ||
    ((pPath = strchr (pFileName, '/')) != NULL)
    )
  {
    pFileName = pPath + 1;
  }

  if (pFileName == NULL) {
    return -1;
  }

  if ((pExt = strchr (pFileName, '.')) == NULL) {
    return -1;
  }

  strncpy (mOptions.VfrBaseFileName, pFileName, pExt - pFileName);
  mOptions.VfrBaseFileName[pExt - pFileName] = '\0';

  return 0;
}

INT8
CVfrCompiler::SetPkgOutputFileName (
  VOID
  )
{
  if (mOptions.VfrBaseFileName[0] == '\0') {
    return -1;
  }

  strcpy (mOptions.PkgOutputFileName, mOptions.OutputDirectory);
  strcat (mOptions.PkgOutputFileName, mOptions.VfrBaseFileName);
  strcat (mOptions.PkgOutputFileName, VFR_PACKAGE_FILENAME_EXTENSION);

  return 0;
}

INT8
CVfrCompiler::SetCOutputFileName (
  VOID
  )
{
  if (mOptions.VfrBaseFileName[0] == '\0') {
    return -1;
  }

  strcpy (mOptions.COutputFileName, mOptions.OutputDirectory);
  strcat (mOptions.COutputFileName, mOptions.VfrBaseFileName);
  strcat (mOptions.COutputFileName, ".c");

  return 0;
}

INT8
CVfrCompiler::SetPreprocessorOutputFileName (
  VOID
  )
{
  if (mOptions.VfrBaseFileName[0] == '\0') {
    return -1;
  }

  strcpy (mOptions.PreprocessorOutputFileName, mOptions.OutputDirectory);
  strcat (mOptions.PreprocessorOutputFileName, mOptions.VfrBaseFileName);
  strcat (mOptions.PreprocessorOutputFileName, VFR_PREPROCESS_FILENAME_EXTENSION);

  return 0;
}

INT8
CVfrCompiler::SetRecordListFileName (
  VOID
  )
{
  if (mOptions.VfrBaseFileName[0] == '\0') {
    return -1;
  }

  strcpy (mOptions.RecordListFile, mOptions.OutputDirectory);
  strcat (mOptions.RecordListFile, mOptions.VfrBaseFileName);
  strcat (mOptions.RecordListFile, VFR_RECORDLIST_FILENAME_EXTENSION);

  return 0;
}

CVfrCompiler::CVfrCompiler (
  IN INT32      Argc, 
  IN CHAR8      **Argv
  )
{
  mPreProcessCmd = PREPROCESSOR_COMMAND;
  mPreProcessOpt = PREPROCESSOR_OPTIONS;

  OptionInitialization(Argc, Argv);

  if ((IS_RUN_STATUS(STATUS_FAILED)) || (IS_RUN_STATUS(STATUS_DEAD))) {
    return;
  }

  SET_RUN_STATUS(STATUS_INITIALIZED);
}

CVfrCompiler::~CVfrCompiler (
  VOID
  )
{
  if (mOptions.IncludePaths != NULL) {
    delete mOptions.IncludePaths;
    mOptions.IncludePaths = NULL;
  }

  if (mOptions.CPreprocessorOptions != NULL) {
    delete mOptions.CPreprocessorOptions;
    mOptions.CPreprocessorOptions = NULL;
  }

  SET_RUN_STATUS(STATUS_DEAD);
}

VOID 
CVfrCompiler::Usage (
  VOID
  )
{
  UINT32 Index;
  CONST  CHAR8 *Help[] = {
    " ", 
    "VfrCompile version " VFR_COMPILER_VERSION,
    " ",
    "Usage: VfrCompile [options] VfrFile",
    " ",
    "Options:",
    "  -h, --help     prints this help",
    "  -l             create an output IFR listing file",
    "  -i IncPath     add IncPath to the search path for VFR included files",
    "  -o DIR, --output-directory DIR",
    "                 deposit all output files to directory OutputDir (default=cwd)",
    "  -b, --create-ifr-package",
    "                 create an IFR HII pack file",
    "  -n, --no-pre-processing",
    "                 do not preprocessing input file",
    "  -f, --pre-processing-flag",
    "                 Preprocessing flags",
    NULL
    };
  for (Index = 0; Help[Index] != NULL; Index++) {
    fprintf (stdout, "%s\n", Help[Index]);
  }
}

VOID
CVfrCompiler::PreProcess (
  VOID
  )
{
  FILE    *pVfrFile      = NULL;
  UINT32  CmdLen         = 0;
  CHAR8   *PreProcessCmd = NULL;

  if (!IS_RUN_STATUS(STATUS_INITIALIZED)) {
    goto Fail;
  }

  if (mOptions.SkipCPreprocessor == TRUE) {
    goto Out;
  }

  if ((pVfrFile = fopen (mOptions.VfrFileName, "r")) == NULL) {
    Error (NULL, 0, 0001, "Error opening the input VFR file", mOptions.VfrFileName);
    goto Fail;
  }
  fclose (pVfrFile);

  CmdLen = strlen (mPreProcessCmd) + strlen (mPreProcessOpt) + 
  	       strlen (mOptions.VfrFileName) + strlen (mOptions.PreprocessorOutputFileName);
  if (mOptions.CPreprocessorOptions != NULL) {
    CmdLen += strlen (mOptions.CPreprocessorOptions);
  }
  if (mOptions.IncludePaths != NULL) {
    CmdLen += strlen (mOptions.IncludePaths);
  }

  PreProcessCmd = new CHAR8[CmdLen + 10];
  if (PreProcessCmd == NULL) {
    Error (NULL, 0, 4001, "Resource: memory can't be allocated", NULL);
    goto Fail;
  }
  strcpy (PreProcessCmd, mPreProcessCmd), strcat (PreProcessCmd, " ");
  strcat (PreProcessCmd, mPreProcessOpt), strcat (PreProcessCmd, " ");
  if (mOptions.IncludePaths != NULL) {
    strcat (PreProcessCmd, mOptions.IncludePaths), strcat (PreProcessCmd, " ");
  }
  if (mOptions.CPreprocessorOptions != NULL) {
    strcat (PreProcessCmd, mOptions.CPreprocessorOptions), strcat (PreProcessCmd, " ");
  }
  strcat (PreProcessCmd, mOptions.VfrFileName), strcat (PreProcessCmd, " > ");
  strcat (PreProcessCmd, mOptions.PreprocessorOutputFileName);

  if (system (PreProcessCmd) != 0) {
    Error (NULL, 0, 0003, "Error parsing file", "failed to spawn C preprocessor on VFR file %s\n", PreProcessCmd);
    goto Fail;
  }

  delete PreProcessCmd;

Out:
  SET_RUN_STATUS (STATUS_PREPROCESSED);
  return;

Fail:
  if (!IS_RUN_STATUS(STATUS_DEAD)) {
    SET_RUN_STATUS (STATUS_FAILED);
  }
  delete PreProcessCmd;
}

extern UINT8 VfrParserStart (IN FILE *);

VOID
CVfrCompiler::Compile (
  VOID
  )
{
  FILE  *pInFile    = NULL;
  CHAR8 *InFileName = NULL;

  if (!IS_RUN_STATUS(STATUS_PREPROCESSED)) {
    goto Fail;
  }

  InFileName = (mOptions.SkipCPreprocessor == TRUE) ? mOptions.VfrFileName : mOptions.PreprocessorOutputFileName;

  gCVfrErrorHandle.SetInputFile (InFileName);

  if ((pInFile = fopen (InFileName, "r")) == NULL) {
    Error (NULL, 0, 0001, "Error opening the input file", InFileName);
    goto Fail;
  }

  if (VfrParserStart (pInFile) != 0) {
    goto Fail;
  }

  fclose (pInFile);

  if (gCFormPkg.HavePendingUnassigned () == TRUE) {
    gCFormPkg.PendingAssignPrintAll ();
    goto Fail;
  }

  SET_RUN_STATUS (STATUS_COMPILEED);
  return;

Fail:
  if (!IS_RUN_STATUS(STATUS_DEAD)) {
    Error (NULL, 0, 0003, "Error parsing", "compile error in file %s", InFileName);
    SET_RUN_STATUS (STATUS_FAILED);
  }
  if (pInFile != NULL) {
    fclose (pInFile);
  }
}

VOID
CVfrCompiler::GenBinary (
  VOID
  )
{
  FILE                    *pFile = NULL;

  if (!IS_RUN_STATUS(STATUS_COMPILEED)) {
    goto Fail;
  }

  if (mOptions.CreateIfrPkgFile == TRUE) {
    if ((pFile = fopen (mOptions.PkgOutputFileName, "wb")) == NULL) {
      Error (NULL, 0, 0001, "Error opening file", mOptions.PkgOutputFileName);
      goto Fail;
    }
    if (gCFormPkg.BuildPkg (pFile) != VFR_RETURN_SUCCESS) {
      fclose (pFile);
      goto Fail;
    }
    fclose (pFile);
  }

  SET_RUN_STATUS (STATUS_GENBINARY);
  return;

Fail:
  if (!IS_RUN_STATUS(STATUS_DEAD)) {
    SET_RUN_STATUS (STATUS_FAILED);
  }
}

static const char *gSourceFileHeader[] = {
  "//",
  "//  DO NOT EDIT -- auto-generated file",
  "//",
  "//  This file is generated by the vfrcompiler utility",
  "//",
  NULL
};

VOID
CVfrCompiler::GenCFile (
  VOID
  )
{
  FILE                    *pFile;
  UINT32                  Index;

  if (!IS_RUN_STATUS(STATUS_GENBINARY)) {
    goto Fail;
  }

  if ((pFile = fopen (mOptions.COutputFileName, "w")) == NULL) {
    Error (NULL, 0, 0001, "Error opening output C file", mOptions.COutputFileName);
    goto Fail;
  }

  for (Index = 0; gSourceFileHeader[Index] != NULL; Index++) {
    fprintf (pFile, "%s\n", gSourceFileHeader[Index]);
  }

  gCVfrBufferConfig.OutputCFile (pFile, mOptions.VfrBaseFileName);

  if (gCFormPkg.GenCFile (mOptions.VfrBaseFileName, pFile) != VFR_RETURN_SUCCESS) {
    fclose (pFile);
    goto Fail;
  }
  fclose (pFile);

  SET_RUN_STATUS (STATUS_FINISHED);
  return;

Fail:
  if (!IS_RUN_STATUS(STATUS_DEAD)) {
    SET_RUN_STATUS (STATUS_FAILED);
  }
}

VOID
CVfrCompiler::GenRecordListFile (
  VOID
  )
{
  CHAR8  *InFileName = NULL;
  FILE   *pInFile    = NULL;
  FILE   *pOutFile   = NULL;
  CHAR8  LineBuf[MAX_VFR_LINE_LEN];
  UINT32 LineNo;

  InFileName = (mOptions.SkipCPreprocessor == TRUE) ? mOptions.VfrFileName : mOptions.PreprocessorOutputFileName;

  if (mOptions.CreateRecordListFile == TRUE) {
    if ((InFileName[0] == '\0') || (mOptions.RecordListFile[0] == '\0')) {
      return;
    }

    if ((pInFile = fopen (InFileName, "r")) == NULL) {
      Error (NULL, 0, 0001, "Error opening the input VFR preprocessor output file", InFileName);
      return;
    }

    if ((pOutFile = fopen (mOptions.RecordListFile, "w")) == NULL) {
      Error (NULL, 0, 0001, "Error opening the record list file", mOptions.RecordListFile);
      goto Err1;
    }

    fprintf (pOutFile, "//\n//  VFR compiler version " VFR_COMPILER_VERSION "\n//\n");
    LineNo = 0;
    while (!feof (pInFile)) {
      if (fgets (LineBuf, MAX_VFR_LINE_LEN, pInFile) != NULL) {
        fprintf (pOutFile, "%s", LineBuf);
        LineNo++;
        gCIfrRecordInfoDB.IfrRecordOutput (pOutFile, LineNo);
      }
    }

    fclose (pOutFile);
    fclose (pInFile);
  }

  return;

Err1:
  fclose (pInFile);
}

INT32
main (
  IN INT32             Argc, 
  IN CHAR8             **Argv
  )
{
  COMPILER_RUN_STATUS  Status;
  CVfrCompiler         Compiler(Argc, Argv);
  
  Compiler.PreProcess();
  Compiler.Compile();
  Compiler.GenBinary();
  Compiler.GenCFile();
  Compiler.GenRecordListFile ();

  Status = Compiler.RunStatus ();
  if ((Status == STATUS_DEAD) || (Status == STATUS_FAILED)) {
    return 2;
  }

  return 0;
}

