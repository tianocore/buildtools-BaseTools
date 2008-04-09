
This file decribes how to build the BaseTools project.

=== Windows/Visual Studio Notes ===

To build the BaseTools, you should run the standard vsvars32.bat script.

In addition to this, you should set the following environment variables:

 * EDK_TOOLS_PATH - Path to the BaseTools sub directory under the edk2 tree
 * BASE_TOOLS_PATH - The directory where the BaseTools source is located.
   (It is the same directory where this README.txt is located.)
 * PYTHON_FREEZER_PATH - Path to where the python freezer tool is installed

After this, you can run the toolsetup.bat file, which is in the same
directory as this file.  It should setup the remainder of the environment,
and build the tools if necessary.

Please also refer to the 'BuildNotes.txt' file for more information on
building under Windows.

=== Unix-like operating systems ===

To build on Unix-like operating systems, you only need to type 'make' in
the base directory of the project.

=== Ubuntu Notes ===

On Ubuntu, the following command should install all the necessary build
packages to build all the C BaseTools:

  sudo apt-get install build-essentials uuid-dev

=== Python antlr3 module ===

Installation of the anltr3 python module is required to use the Python
BaseTools code.  This module can be installed from:
  http://www.antlr.org/download/Python/

You make use of the python easy_install command to install the antlr3 module.
To 'install' the easy_install python command:
  On Ubuntu, install the python-setuptools package:
    sudo apt-get install python-setuptools
  Or, refer to this web page:
    http://wiki.python.org/moin/EasyInstall

After you have easy_install available, you can use it to install the
antlr3 module (You may need to check http://www.antlr.org/download/Python
to see if there is a newer version):
  sudo easy_install \
    http://www.antlr.org/download/Python/antlr_python_runtime-3.0.1-py2.5.egg

