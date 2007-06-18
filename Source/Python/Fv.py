import Ffs
import AprioriSection
from GenFdsGlobalVariable import GenFdsGlobalVariable
import os
import subprocess

T_CHAR_LF = '\n'

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
                self.FvInfFile.writelines("EFI_FILE_NAME = " + \
                                           Ffs               + \
                                           T_CHAR_LF)
        #
        # Process Modules in FfsList
        #
        for FfsFile in self.FfsList :
            FileName = FfsFile.GenFfs()
            self.FvInfFile.writelines("EFI_FILE_NAME = " + \
                                       FileName          + \
                                       T_CHAR_LF)
            
        self.FvInfFile.close()
        #
        # Call GenFv tool
        #
        
        cmd = 'GenFvImage -i '            + \
               GenFdsGlobalVariable.FvDir + \
               self.UiFvName              + \
               '.inf'                     + \
               ' -o '                     + \
               self.UiFvName

        # For Test
        cmd = "GenFvImage -i FvMain.inf"
        #
        # Call GenFv Tools
        #
        print cmd
        subprocess.Popen(cmd).communicate()
        
        #
        # Write the Fv contents to Buffer
        #
        fv = open (GenFdsGlobalVariable.OuputDir + \
                   self.UiFvName                 + \
                   '.fv',                          \
                   'r+b')
                   
        print GenFdsGlobalVariable.OuputDir + \
              self.UiFvName                 + \
              '.fv'
              
        Buffer.write(fv.read())
        fv.close
    
    def InitialInf (self, BlockSize, Offset, Size) :
        self.FvInfFile = open (GenFdsGlobalVariable.FvDir + \
                               self.UiFvName              + \
                               '.inf',                      \
                               'w+')
        #
        # Add [Options]
        #
        self.FvInfFile.writelines("[Options]" + T_CHAR_LF)
        
        self.FvInfFile.writelines("EFI_BASE_ADDRESS = " + \
                                   Offset               + \
                                   T_CHAR_LF)
                                   
        self.FvInfFile.writelines("EFI_BLOCK_SIZE   = " + \
                                  '%x' %BlockSize       + \
                                  T_CHAR_LF)
                                  
        #self.FvInfFile.writelines("EFI_NUM_BLOCKS   = " + '%x' %(Size/BlockSize) \
        #                          + ReturnSign)
        
        #
        # Add attribute
        #
        self.FvInfFile.writelines("[Attribute]" + T_CHAR_LF)
        
        if not (self.FvAttributeDict == None):
            for FvAttribute in self.FvAttributeDict :
                self.FvInfFile.writelines(FvAttribute.Name  + \
                                          '='               + \
                                          FvAttribute.Value + \
                                          T_CHAR_LF )
            
        #
        # Add [Files]
        #
            
        self.FvInfFile.writelines("[files]" + T_CHAR_LF)



    


