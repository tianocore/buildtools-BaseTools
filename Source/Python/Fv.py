import Ffs
import AprioriSection
from GenFdsGlobalVariable import GenFdsGlobalVariable
import os
class FV:
    def __init__(self):
        self.UiFvName = None
        self.CreateFileName = None
        # 3-tuple list (blockSize, numBlocks, pcd)
        self.BlockSizeList = []
        # DefineVarDict[var] = value
        self.DefineVarDict = {}
        # SetVarDict[var] = value
        self.SetVarDict = {}
        self.FvAlignment = None
        # FvAttributeDict[attribute] = TRUE/FALSE (1/0)
        self.FvAttributeDict = {}
##        self.FvAttributeset = None
##        self.FvAttributeClear = None
        self.AprioriSection = None
        self.FfsList = []
        
        self.FvInfFile = None
        
    #
    #  Generate Fv and add it to the Buffer
    #
    def AddToBuffer (self, Buffer) :
        #
        # First Process the Apriori section
        #
        if not (self.AprioriSection == None):
            FileNameList = self.AprioriSection.GenFfsFile ()
            #
            # Add Apriori section included Ffs file name to Inf file
            #
            for Ffs in FileNameList :
                self.FvInfFile.writelines("EFI_FILE_NAME = " + Ffs)
        #
        # Process Modules in FfsList
        #
        for FfsFile in self.FfsList :
            FileName = FfsFile.GenFfs()
            self.FvInfFile.writelines("EFI_FILE_NAME = " + FileName)
            
        self.FvInfFile.close()
        #
        # Call GenFv tool
        #
        
        cmd = 'GenFv -i ' + GenFdsGlobalVariable.FvDir + self.UiFvName + '.inf'\
               + ' -o ' + self.UiFvName
        os.popen(cmd, 'r')
        
        #
        # Write the Fv contents to Buffer
        #
        fv = open (self.UiFvName, mode='read')
        Buffer.write(fv.Read)
        fv.close
    
    def InitialInf (self, BlockSize, Offset, Size) :
        self.FvInfFile = open (GenFdsGlobalVariable.FvDir + self.UiFvName + '.inf', 'a+')
        #
        # Add [Options]
        #
        self.FvInfFile.writelines("[Options]" )
        self.FvInfFile.writelines("EFI_BASE_ADDRESS = " + Offset )
        self.FvInfFile.writelines("EFI_BLOCK_SIZE   = " + '%x' %BlockSize)
        #self.FvInfFile.writelines("EFI_NUM_BLOCKS   = " + '%x' %(Size/BlockSize))
        
        #
        # Add attribute
        #
        self.FvInfFile.writelines("[Attribute]")
        if not (self.FvAttributeDict == None):
            for FvAttribute in self.FvAttributeDict :
                self.FvInfFile.writelines(FvAttribute.Name + '=' + FvAttribute.Value)
            
        #
        # Add [Files]
        #
            
        self.FvInfFile.writelines("[files]")



    


