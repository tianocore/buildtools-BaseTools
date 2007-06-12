class FD(object):
    def __init__(self):
        self.FdUiName = None
        self.CreateFileName = None
        self.BaseAddress = None
        self.BaseAddressPcd = None
        self.Size = None
        self.SizePcd = None
        self.ErasePolarity = False
        # 3-tuple list (blockSize, numBlocks, pcd)
        self.BlockSizeList = None
        # DefineVarDict[var] = value
        self.DefineVarDict = None
        # SetVarDict[var] = value
        self.SetVarDict = None
        self.RegionList = None