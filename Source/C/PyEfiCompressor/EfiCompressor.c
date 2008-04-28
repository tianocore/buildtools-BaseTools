#include <Python.h>
#include <Decompress.h>

/*
 UefiDecompress(data_buffer, size, original_size)
*/
STATIC
PyObject*
UefiDecompress(
  PyObject    *Self,
  PyObject    *Args,
  PyObject    *Keywords
  ) 
{
  PyTypeObject  *SrcData;
  UINT32        SrcDataSize;
  UINT32        DstDataSize;
  UINT          Status;
  UINT8         *SrcBuf;
  UINT8         *DstBuf;
  UINT8         *TmpBuf;
  Py_ssize_t    SegNum;
  Py_ssize_t    Index;

  Status = PyArg_ParseTupleAndKeywords(
            Args,
            Keywords,
            "0ii",
            &SrcData,
            &SrcDataSize,
            &DstDataSize
            );
  if (Status == 0) {
    return NULL;
  }

  if (SrcData->tp_as_buffer == NULL
      || SrcData->tp_as_buffer->bf_getreadbuffer == NULL
      || SrcData->tp_as_buffer->bf_getsegcount == NULL) {
    return NULL;
  }

  // Because some Python objects which support "buffer" protocol have more than one
  // memory segment, we have to copy them into a contiguous memory.
  SrcBuf = malloc(SrcDataSize);
  DstBuf = malloc(DstDataSize);
  if (SrcBuf == NULL || DstBuf == NULL) {
    goto ERROR;
  }

  SegNum = SrcData->tp_as_buffer->bf_getsegcount(SrcData, NULL);
  TmpBuf = SrcBuf
  for (Index = 0; Index < SegNum; ++Index) {
    VOID *BufSeg;
    Py_ssize_t Len;

    Len = SrcData->tp_as_buffer->bf_getreadbuffer(SrcData, Index, &BufSeg);
    if (Len < 0) {
      goto ERROR;
    }
    memcpy(TmpBuf, BufSeg, Len);
    TmpBuf += Len;
  }

  Status = Extract((VOID *)SrcBuf, SrcDataSize, (VOID *)DstBuf, DstDataSize, 1);
  if (Status != EFI_SUCCESS) {
    goto ERROR;
  }

  return PyBuffer_FromMemory(DstBuf, (Py_ssize_t)DstDataSize);

ERROR:
  if (SrcBuf != NULL) {
    free(SrcBuf);
  }

  if (DstBuf != NULL) {
    free(DstBuf);
  }
  return NULL;
}


STATIC
PyObject*
FrameworkDecompress(
  PyObject    *Self,
  PyObject    *Args,
  PyObject    *Keywords
  )
{
  PyTypeObject  *SrcData;
  UINT32        SrcDataSize;
  UINT32        DstDataSize;
  UINT          Status;
  UINT8         *SrcBuf;
  UINT8         *DstBuf;
  UINT8         *TmpBuf;
  Py_ssize_t    SegNum;
  Py_ssize_t    Index;

  Status = PyArg_ParseTupleAndKeywords(
            Args,
            Keywords,
            "0ii",
            &SrcData,
            &SrcDataSize,
            &DstDataSize
            );
  if (Status == 0) {
    return NULL;
  }

  if (SrcData->tp_as_buffer == NULL
      || SrcData->tp_as_buffer->bf_getreadbuffer == NULL
      || SrcData->tp_as_buffer->bf_getsegcount == NULL) {
    return NULL;
  }

  // Because some Python objects which support "buffer" protocol have more than one
  // memory segment, we have to copy them into a contiguous memory.
  SrcBuf = malloc(SrcDataSize);
  DstBuf = malloc(DstDataSize);
  if (SrcBuf == NULL || DstBuf == NULL) {
    goto ERROR;
  }

  SegNum = SrcData->tp_as_buffer->bf_getsegcount(SrcData, NULL);
  TmpBuf = SrcBuf
  for (Index = 0; Index < SegNum; ++Index) {
    VOID *BufSeg;
    Py_ssize_t Len;

    Len = SrcData->tp_as_buffer->bf_getreadbuffer(SrcData, Index, &BufSeg);
    if (Len < 0) {
      goto ERROR;
    }
    memcpy(TmpBuf, BufSeg, Len);
    TmpBuf += Len;
  }

  Status = Extract((VOID *)SrcBuf, SrcDataSize, (VOID *)DstBuf, DstDataSize, 2);
  if (Status != EFI_SUCCESS) {
    goto ERROR;
  }

  return PyBuffer_FromMemory(DstBuf, (Py_ssize_t)DstDataSize);

ERROR:
  if (SrcBuf != NULL) {
    free(SrcBuf);
  }

  if (DstBuf != NULL) {
    free(DstBuf);
  }
  return NULL;
}

STATIC
PyObject*
UefiCompress(
  PyObject    *Self,
  PyObject    *Args,
  PyObject    *Keywords
  ) 
{
  return NULL;
}


STATIC
PyObject*
FrameworkCompress(
  PyObject    *Self,
  PyObject    *Args,
  PyObject    *Keywords
  )
{
  return NULL;
}

STATIC CHAR DecompressDocs[] = "Decompress(): Decompress data using UEFI standard algorithm\n";
STATIC CHAR CompressDocs[] = "Compress(): Compress data using UEFI standard algorithm\n";

STATIC PyMethodDef EfiCompressor_Funcs[] = {
  {"UefiDecompress", (PyCFunction)UefiDecompress, METH_KEYWORDS, DecompressDocs},
  {"UefiCompress", (PyCFunction)UefiCompress, METH_KEYWORDS, DecompressDocs},
  {"FrameworkDecompress", (PyCFunction)FrameworkDecompress, METH_KEYWORDS, DecompressDocs},
  {"FrameworkCompress", (PyCFunction)FrameworkCompress, METH_KEYWORDS, DecompressDocs},
  {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
InitEfiCompressor(VOID) {
  Py_InitModule3("EfiCompressor", EfiCompressor_Funcs, "EFI Compression Algorithm Extension Module");
}


