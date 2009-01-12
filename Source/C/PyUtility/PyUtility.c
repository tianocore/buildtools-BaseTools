#include <Python.h>
#include <Windows.h>
#include <Common/UefiBaseTypes.h>

/*
 SaveFileToDisk(FilePath, Content)
*/
STATIC
PyObject*
SaveFileToDisk (
  PyObject    *Self,
  PyObject    *Args
  )
{
  CHAR8         *File;
  UINT8         *Data;
  UINTN         DataLength;
  UINTN         WriteBytes;
  UINTN         Status;
  HANDLE        FileHandle;
  PyObject      *ReturnValue = Py_False;

  Status = PyArg_ParseTuple(
            Args,
            "ss#",
            &File,
            &Data,
            &DataLength
            );
  if (Status == 0) {
    return NULL;
  }

  FileHandle = CreateFile(
                File,
                GENERIC_WRITE,
                0,
                NULL,
                CREATE_ALWAYS,
                FILE_ATTRIBUTE_NORMAL,
                NULL
                );
  if (FileHandle == INVALID_HANDLE_VALUE) {
    PyErr_SetString(PyExc_Exception, "File creation failure");
    return NULL;
  }

  while (WriteFile(FileHandle, Data, DataLength, &WriteBytes, NULL)) {
    if (DataLength <= WriteBytes) {
      DataLength = 0;
      break;
    }

    Data += WriteBytes;
    DataLength -= WriteBytes;
  }

  if (DataLength != 0) {
    // file saved unsuccessfully
    PyErr_SetString(PyExc_Exception, "File write failure");
    goto Done;
  }

  if (!FlushFileBuffers(FileHandle)) {
    PyErr_SetString(PyExc_Exception, "File flush failure");
    goto Done;
  }

  // success!
  ReturnValue = Py_True;

Done:
  CloseHandle(FileHandle);
  return ReturnValue;
}

STATIC INT8 SaveFileToDiskDocs[] = "SaveFileToDisk(): Make sure the file is saved to disk\n";

STATIC PyMethodDef PyUtility_Funcs[] = {
  {"SaveFileToDisk", (PyCFunction)SaveFileToDisk, METH_VARARGS, SaveFileToDiskDocs},
  {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
initPyUtility(VOID) {
  Py_InitModule3("PyUtility", PyUtility_Funcs, "Utilties Module Implemented C Language");
}


