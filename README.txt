
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

=== 

To build on Unix-like operating systems, you only need to type 'make' in
the base directory of the project.

=== Ubuntu Notes ===

On Ubuntu, the following command should install all the necessary build
packages to build all the C BaseTools:

  sudo apt-get install build-essentials uuid-dev


