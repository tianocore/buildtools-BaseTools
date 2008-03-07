import AutoGen.UniClassObject
import AutoGen.StrGather as StrGather

# This acts like the main() function for the script, unless it is 'import'ed into another
# script.
if __name__ == '__main__':
    IncludeList = [
            r'C:\SVN\BuildTools\BaseTools\Source\Python\AutoGen',
            r'C:\SVN\BuildTools\BaseTools\Source\Python\build',
            r'C:\SVN\BuildTools\BaseTools\Source\Python\CalcDeps',
            r'C:\SVN\BuildTools\BaseTools\Source\Python\Common',
            r'C:\SVN\BuildTools\BaseTools\Source\Python\CommonDataClass',
            r'C:\SVN\BuildTools\BaseTools\Source\Python\Fdb',
            r'C:\SVN\BuildTools\BaseTools\Source\Python\FixFlash',
            r'C:\SVN\BuildTools\BaseTools\Source\Python\GenFds',
            r'C:\SVN\BuildTools\BaseTools\Source\Python\InstallFar',
            r'C:\SVN\BuildTools\BaseTools\Source\Python\MkBOM',
            r'C:\SVN\BuildTools\BaseTools\Source\Python\MkFar',
            r'C:\SVN\BuildTools\BaseTools\Source\Python\TargetTool',
            r'C:\SVN\BuildTools\BaseTools\Source\Python\Trim',
            r'C:\SVN\BuildTools\BaseTools\Source\Python\UpdateFv',
            r'C:\SVN\BuildTools\BaseTools\Source\Python\WkSpace'
        ]
    f = StrGather.GetFileList(IncludeList, '.pyc')
    tl = 0
    for item in f:
        l = 0
        fin = open(item, mode='rb')
        for line in fin:
            l = l + 1
        if l != 0:
            print l, ',  ', item
        tl = tl + l
    print 'total:', tl