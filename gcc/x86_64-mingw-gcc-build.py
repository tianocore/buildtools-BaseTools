#!/usr/bin/env python

#
# Automation of instructions from:
#   http://mingw-w64.svn.sourceforge.net/viewvc/mingw-w64/trunk/mingw-w64-doc/
#     howto-build/mingw-w64-howto-build.txt?revision=216&view=markup
#

from optparse import OptionParser
import os
import shutil
import subprocess
import sys
import tarfile
import urllib
import urlparse
try:
    from hashlib import md5
except Exception:
    from md5 import md5

#
# Version and Copyright
#
VersionNumber = "0.01"
__version__ = "%prog Version " + VersionNumber
__copyright__ = "Copyright (c) 2008, Intel Corporation.  All rights reserved."

class Config:
    """class Config

    Stores the configuration options for the rest of the script.

    Handles the command line options, and allows the code within
    the script to easily interact with the 'config' requested by
    the user.
    """

    def __init__(self):
        self.base_dir = os.getcwd()
        (self.options, self.args) = self.CheckOptions()
        self.__init_dirs__()

    def CheckOptions(self):
        Parser = \
            OptionParser(
                description=__copyright__,
                version=__version__,
                prog="x86_64-mingw-gcc-build",
                usage="%prog [options] [target]"
                )
        Parser.add_option(
            "--arch",
            action = "append", type = "choice", choices = ['X64'],
            default = ['X64'],
            dest = "arch",
            help = "Processor architecture to build gcc for."
            )
        Parser.add_option(
            "--src-dir",
            action = "store", type = "string", dest = "src_dir",
            default = os.path.join(self.base_dir, 'src'),
            help = "Directory to download/extract binutils/gcc sources"
            )
        Parser.add_option(
            "--build-dir",
            action = "store", type = "string", dest = "build_dir",
            default = os.path.join(self.base_dir, 'build'),
            help = "Directory to download/extract binutils/gcc sources"
            )
        Parser.add_option(
            "--prefix",
            action = "store", type = "string", dest = "prefix",
            default = os.path.join(self.base_dir, 'install'),
            help = "Prefix to install binutils/gcc into"
            )
        Parser.add_option(
            "--symlinks",
            action = "store", type = "string", dest = "symlinks",
            default = os.path.join(self.base_dir, 'symlinks'),
            help = "Directory to create binutils/gcc symbolic links into."
            )
        Parser.add_option(
            "-v", "--verbose",
            action="store_true",
            type=None, help="Print verbose messages"
            )
    
        (Opt, Args) = Parser.parse_args()
        return (Opt, Args)

    def __init_dirs__(self):
        self.src_dir = os.path.realpath(os.path.expanduser(self.options.src_dir))
        self.build_dir = os.path.realpath(os.path.expanduser(self.options.build_dir))
        self.prefix = os.path.realpath(os.path.expanduser(self.options.prefix))
        self.symlinks = os.path.realpath(os.path.expanduser(self.options.symlinks))

    def IsConfigOk(self):
                
        print "Current directory:"
        print "   ", self.base_dir
        print "Sources download/extraction:", self.Relative(self.src_dir)
        print "Build directory            :", self.Relative(self.build_dir)
        print "Prefix (install) directory :", self.Relative(self.prefix)
        print "Create symlinks directory  :", self.Relative(self.symlinks)
        print
        answer = raw_input("Is this configuration ok? (default = no): ")
        if (answer.lower() not in ('y', 'yes')):
            print
            print "Please try using --help and then change the configuration."
            return False
        
        print
        return True

    def Relative(self, path):
        if path.startswith(self.base_dir):
            return '.' + path[len(self.base_dir):]
        return path

    def MakeDirs(self):
        for path in (self.src_dir, self.build_dir,self.prefix, self.symlinks):
            if not os.path.exists(path):
                os.makedirs(path)

class SourceFiles:
    """class SourceFiles

    Handles the downloading of source files used by the script.
    """

    def __init__(self, config):
        self.config = config

    source_files = {
        'gcc': {
            'url': 'http://gcc-ca.internet.bs/releases/' + \
                   'gcc-$version/gcc-$version.tar.bz2',
            'version': '4.3.0',
            'md5': '197ed8468b38db1d3481c3111691d85b'
            },
        'binutils': {
            'url': 'http://www.kernel.org/pub/linux/devel/binutils/' + \
                   'binutils-$version.tar.bz2',
            'version': '2.18.50.0.5',
            'md5': 'daee18dbbf0a6ccfc186141bee18bf62'
            },
        'mingw_hdr': { # http://superb-east.dl.sourceforge.net/sourceforge/
            'url': 'http://superb-west.dl.sourceforge.net/sourceforge/' + \
                   'mingw-w64/mingw-w64-snapshot-$version.tar.bz2',
            'version': '20080310',
            'md5': '235b2d15c2411f7d213c0c0977b2162f'
            },
        }
    for (fname, fdata) in source_files.items():
        fdata['url'] = fdata['url'].replace('$version', fdata['version'])
        fdata['filename'] = fdata['url'].split('/')[-1]

    def GetAll(self):

        def progress(received, blockSize, fileSize):
            if fileSize < 0: return
            wDots = (100 * received * blockSize) / fileSize / 10
            if wDots > self.dots:
                for i in range(wDots - self.dots):
                    print '.',
                    sys.stdout.flush()
                    self.dots += 1

        for (fname, fdata) in self.source_files.items():
            self.dots = 0
            local_file = os.path.join(self.config.src_dir, fdata['filename'])
            url = fdata['url']
            print 'Downloading %s:' % fname,
            sys.stdout.flush()

            completed = False
            if os.path.exists(local_file):
                md5_pass = self.checkHash(fdata)
                if md5_pass:
                    print '[md5 match]',
                else:
                    print '[md5 mismatch]',
                sys.stdout.flush()
                completed = md5_pass

            if not completed:
                urllib.urlretrieve(url, local_file, progress)

            #
            # BUGBUG: Suggest proxy to user if download fails.
            #
            # export http_proxy=http://proxyservername.mycompany.com:911
            # export ftp_proxy=http://proxyservername.mycompany.com:911

            if not completed and os.path.exists(local_file):
                md5_pass = self.checkHash(fdata)
                if md5_pass:
                    print '[md5 match]',
                else:
                    print '[md5 mismatch]',
                sys.stdout.flush()
                completed = md5_pass

            if completed:
                print '[done]'
            else:
                print '[failed]'
                return False

        return True

    def checkHash(self, fdata):
        local_file = os.path.join(self.config.src_dir, fdata['filename'])
        expect_md5 = fdata['md5']
        data = open(local_file).read()
        md5sum = md5()
        md5sum.update(data)
        return md5sum.hexdigest().lower() == expect_md5.lower()

    def GetModules(self):
        return self.source_files.keys()

    def GetFilenameOf(self, module):
        return self.source_files[module]['filename']

    def GetMd5Of(self, module):
        return self.source_files[module]['md5']

class Extracter:
    """class Extracter

    Handles the extraction of the source files from their downloaded
    archive files.
    """

    def __init__(self, source_files, config):
        self.source_files = source_files
        self.config = config

    def Extract(self, module):
        src = self.config.src_dir
        local_file = os.path.join(src, self.source_files.GetFilenameOf(module))
        moduleMd5 = self.source_files.GetMd5Of(module)
        extracted = os.path.join(src, local_file + '.extracted')
        if not os.path.exists(src):
            os.mkdir(src)

        extractedMd5 = None
        if os.path.exists(extracted):
            extractedMd5 = open(extracted).read()

        if extractedMd5 != moduleMd5:
            print 'Extracting %s:' % self.config.Relative(local_file)
            tar = tarfile.open(local_file)
            tar.extractall(src)
            open(extracted, 'w').write(moduleMd5)
        else:
            pass
            #print 'Previously extracted', self.config.Relative(local_file)

    def ExtractAll(self):
        for module in self.source_files.GetModules():
            self.Extract(module)

class Builder:
    """class Builder

    Builds and installs the GCC tool suite.
    """

    def __init__(self, source_files, config):
        self.source_files = source_files
        self.config = config

    def Build(self):
        self.BuildModule('binutils')
        self.CopyIncludeDirectory()
        self.BuildModule('gcc')
        self.MakeSymLinks()

    def IsBuildStepComplete(self, step):
        return \
            os.path.exists(
                os.path.join(
                    self.config.build_dir, step + '.completed'
                    )
                )

    def MarkBuildStepComplete(self, step):
        open(
            os.path.join(
                self.config.build_dir, step + '.completed'
                ),
            "w"
            ).close()

    def CopyIncludeDirectory(self):
        src = os.path.join(self.config.src_dir, 'trunk', 'mingw-w64-headers', 'include')
        dst_parent = os.path.join(self.config.prefix, 'x86_64-pc-mingw32')
        dst = os.path.join(dst_parent, 'include')
        linkdst = os.path.join(self.config.prefix, 'mingw')
        if not os.path.exists(dst):
            if not os.path.exists(dst_parent):
                os.makedirs(dst_parent)
            print 'Copying headers to', self.config.Relative(dst)
            shutil.copytree(src, dst, True)
        if not os.path.lexists(linkdst):
            print 'Making symlink at', self.config.Relative(linkdst)
            os.symlink('x86_64-pc-mingw32', linkdst)

    def BuildModule(self, module):
        base_dir = os.getcwd()
        build_dir = os.path.join(self.config.build_dir, 'x64', module)
        module_dir = self.source_files.GetFilenameOf(module)
        module_dir = module_dir[:-len('.tar.bz2')]
        module_dir = os.path.realpath(os.path.join('src', module_dir))
        configure = os.path.join(module_dir, 'configure')
        prefix = self.config.prefix
        if not os.path.exists(build_dir):
            os.makedirs(build_dir)
        os.chdir(build_dir)

        cmd = (
            configure,
            '--target=x86_64-pc-mingw32',
            '--prefix=' + prefix,
            '--with-sysroot=' + prefix,
            )
        if os.path.exists('/opt/local/include/gmp.h'):
            cmd += ('--with-gmp=/opt/local',)
        self.RunCommand(cmd, module, 'config', skipable=True)

        cmd = ('make',)
        if module == 'gcc':
            cmd += ('all-gcc',)
        self.RunCommand(cmd, module, 'build')

        cmd = ('make',)
        if module == 'gcc':
            cmd += ('install-gcc',)
        else:
            cmd += ('install',)
        self.RunCommand(cmd, module, 'install')

        os.chdir(base_dir)

        print '%s module is now built and installed' % module

    def RunCommand(self, cmd, module, stage, skipable=False):
        if skipable:
            if self.IsBuildStepComplete('%s.%s' % (module, stage)):
                return

        popen = lambda cmd: \
            subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
                )

        print '%s [%s] ...' % (module, stage),
        sys.stdout.flush()
        p = popen(cmd)
        output = p.stdout.read()
        p.wait()
        if p.returncode != 0:
            print '[failed!]'
            logFile = os.path.join(self.config.build_dir, 'log.txt')
            f = open(logFile, "w")
            f.write(output)
            f.close()
            raise Exception, 'Failed to %s %s\n' % (stage, module) + \
                'See output log at %s' % self.config.Relative(logFile)
        else:
            print '[done]'

        if skipable:
            self.MarkBuildStepComplete('%s.%s' % (module, stage))

    def MakeSymLinks(self):
        links_dir = os.path.join(self.config.symlinks, 'x64')
        if not os.path.exists(links_dir):
            os.makedirs(links_dir)
        startPrinted = False
        for link in ('ar', 'ld', 'gcc'):
            src = os.path.join(
                self.config.prefix, 'bin', 'x86_64-pc-mingw32-' + link
                )
            linkdst = os.path.join(links_dir, link)
            if not os.path.lexists(linkdst):
                if not startPrinted:
                    print 'Making symlinks in %s:' % self.config.Relative(links_dir),
                    startPrinted = True
                print link,
                os.symlink(src, linkdst)

        if startPrinted:
            print '[done]'

class App:
    """class App

    The main body of the application.
    """

    def __init__(self):
        config = Config()

        if not config.IsConfigOk():
            return

        config.MakeDirs()

        sources = SourceFiles(config)
        result = sources.GetAll()
        if result:
            print 'All files have been downloaded & verified'
        else:
            print 'An error occured while downloading a file'
            return

        Extracter(sources, config).ExtractAll()

        Builder(sources, config).Build()

App()

