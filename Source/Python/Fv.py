import Ffs
import AprioriSection
class FV:
    def __init__(self):
        self.UiFvName = None
        self.CreateFileName = None
        # DefineVarDict[var] = value
        self.DefineVarDict = None
        # SetVarDict[var] = value
        self.SetVarDict = None
        self.FvAttributeList = None
        self.FvAttributeset = None
        self.FvAttributeClear = None
        self.AprioriSection = None
        self.FfsList = None
        
        self.FvInfFile = None
        
    #
    #  Generate Fv and add it to the Buffer
    #
    def AddToBuffer (Buffer) :
        #
        # First Process the Apriori section
        #
        FileNameList = self.AprioriSection.GenFfsFile ()
        #
        # Add Apriori section included Ffs file name to Inf file
        #
        for Ffs in FileNameList :
            self.FvInfFile.writelines("EFI_FILE_NAME = " + Ffs)
        #
        # Process Modules in FfsList
        #
        for Ffs in self.FFsList :
            FileName = Ffs.GenFfsFile ()
            self.FvInfFile.writelines("EFI_FILE_NAME = " + FileName)
            
        self.FvInfFile.close()
        #
        # Call GenFv tool
        #
        cmd = 'GenFv -i ' + self.FvInfFile.filename() + ' -o ' + self.UiFvName
        popen(cmd, mod ='r')
        
        #
        # Write the Fv contents to Buffer
        #
        fv = open (self.UiFvName, mode='read')
        Buffer.write(fv.Read)
        fv.close
    
    def InitialInf (BlockSize, Offset, Size) :
        self.FvInfFile = open (GenFdsGlobalVariable.FvDir + self.UiFvname + '.inf', mode='a+')
        #
        # Add [Options]
        #
        self.FvInfFile.writelines("[Options]")
        self.FvInfFile.writelines("EFI_BASE_ADDRESS = " + Offset )
        self.FvInfFile.writelines("EFI_BLOCK_SIZE   = " + BlockSize)
        self.FvInfFile.writelines("EFI_NUM_BLOCKS   = " + Size/BlockSize)
        
        #
        # Add attribute
        #
        self.FvInfFile.writelines("[Attribute]")
        for FvAttribute in self.FvAttributeList :
            self.FvInfFile.writelines(FvAttribute.Name + '=' + FvAttribute.Value)
            
        #
        # Add [Files]
        #
            
        self.FvInfFile.writelines("[files]")



    


