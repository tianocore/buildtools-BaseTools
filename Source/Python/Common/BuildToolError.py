## @file
# Standardized Error Hanlding infrastructures.
#
# Copyright (c) 2007, Intel Corporation
# All rights reserved. This program and the accompanying materials
# are licensed and made available under the terms and conditions of the BSD License
# which accompanies this distribution.  The full text of the license may be found at
# http://opensource.org/licenses/bsd-license.php
#
# THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
# WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.
#

#
# name
# type
# lineno
# msg
# arg
# arg1
# arg2
# directory
# resource
# structure
# attribute
# port
#

FILE_NOT_FOUND = 0
FILE_OPEN_FAILURE = 1
FILE_WRITE_FAILURE = 2
FILE_PARSE_FAILURE = 3
FILE_READ_FAILURE = 4
FILE_CREATE_FAILURE = 5
FILE_CHECKSUM_FAILURE = 6
FILE_COMPRESS_FAILURE = 7
FILE_DECOMPRESS_FAILURE = 8
FILE_MOVE_FAILURE = 9
FILE_DELETE_FAILURE = 10
FILE_COPY_FAILURE = 11
FILE_POSITIONING_FAILURE = 12
FILE_ALREADY_EXIST = 13
FILE_UNKNOWN_ERROR = 0x0FFF

OPTION_UNKNOWN = 0x1000
OPTION_MISSING = 0x1001
OPTION_CONFLICT = 0x1002
OPTION_VALUE_INVALID = 0x1003
OPTION_DEPRECATED = 0x1004
OPTION_NOT_SUPPORTED = 0x1005
OPTION_UNKNOWN_ERROR = 0x1FFF

PARAMETER_INVALID = 0x2000
PARAMETER_MISSING = 0x2001
PARAMETER_UNKNOWN_ERROR =0x2FFF

FORMAT_INVALID = 0x3000
FORMAT_NOT_SUPPORTED = 0x3001
FORMAT_UNKNOWN = 0x3002
FORMAT_UNKNOWN_ERROR = 0x3FFF

RESOURCE_NOT_AVAILABLE = 0x4000
RESOURCE_ALLOCATE_FAILURE = 0x4001
RESOURCE_FULL = 0x4002
RESOURCE_OVERFLOW = 0x4003
RESOURCE_UNDERRUN = 0x4004
RESOURCE_UNKNOWN_ERROR = 0x4FFF

ATTRIBUTE_NOT_AVAILABLE = 0x5000
ATTRIBUTE_GET_FAILURE = 0x5001
ATTRIBUTE_SET_FAILURE = 0x5002
ATTRIBUTE_UPDATE_FAILURE = 0x5003
ATTRIBUTE_ACCESS_DENIED = 0x5004
ATTRIBUTE_UNKNOWN_ERROR = 0x5FFF

IO_NOT_READY = 0x6000
IO_BUSY = 0x6001
IO_TIMEOUT = 0x6002
IO_UNKNOWN_ERROR = 0x6FFF

AUTOGEN_ERROR = 0xF000
PARSER_ERROR = 0xF001
GENFDS_ERROR = 0xF002
MIGRATION_ERROR = 0xF010
UNKNOWN_ERROR = 0xFFFF

gKeyWord = ["name", "type", "lineno", "msg", "arg", "arg1", "arg2", "directory",
            "resource", "structure", "attribute", "port", "usage"]

gErrorMessage = {
    FILE_NOT_FOUND          :   "File not found: %(name)s",
    FILE_OPEN_FAILURE       :   "Opening file: %(name)s",
    FILE_WRITE_FAILURE      :   "Writing file: %(name)s",
    FILE_PARSE_FAILURE      :   "Parsing file: %(name)s",
    FILE_READ_FAILURE       :   "Reading file: %(name)s",
    FILE_CREATE_FAILURE     :   "Creating file: %(name)s",
    FILE_CHECKSUM_FAILURE   :   "Invalid checksum of file: %(name)s",
    FILE_COMPRESS_FAILURE   :   "Compressing file: %(name)s",
    FILE_DECOMPRESS_FAILURE :   "Decompressing file: %(name)s",
    FILE_MOVE_FAILURE       :   "Moving file: %(name)s",
    FILE_DELETE_FAILURE     :   "Deleting file: %(name)s",
    FILE_COPY_FAILURE       :   "Copying file: %(name)s",
    FILE_POSITIONING_FAILURE:   "Seeking position of ile: %(name)s",
    FILE_ALREADY_EXIST      :   "File or directory already exists: %(name)s",
    FILE_UNKNOWN_ERROR      :   "Unknown error encountered on file: %(name)s",

    OPTION_UNKNOWN          :   "Unknown option: %(name)s\n%(usage)s",
    OPTION_MISSING          :   "Missing option: %(name)s\n%(usage)s",
    OPTION_CONFLICT         :   "Conflict options: %(arg1) <-> %(arg2)\n%(usage)s",
    OPTION_VALUE_INVALID    :   "Invalid value of option: %(name)s\n%(usage)s",
    OPTION_DEPRECATED       :   "Deprecated option: %(name)s\n%(usage)s",
    OPTION_NOT_SUPPORTED    :   "Unsupported option: %(name)s\n%(usage)s",
    OPTION_UNKNOWN_ERROR    :   "Unknown error when processing options",

    PARAMETER_INVALID       :   "Invalid parameter: %(name)s",
    PARAMETER_MISSING       :   "Missing parameter: %(name)s",
    PARAMETER_UNKNOWN_ERROR :   "Unknown error in parameters",

    FORMAT_INVALID          :   "Invalid sytax/format at line %(lineno)s in file %(name)s",
    FORMAT_NOT_SUPPORTED    :   "Not supported: %(name)s",
    FORMAT_UNKNOWN          :   "Unknown format: %(name)s",
    FORMAT_UNKNOWN_ERROR    :   "Unknown error in %(name)s",

    RESOURCE_NOT_AVAILABLE  :   "%(name)s is not available",
    RESOURCE_ALLOCATE_FAILURE :   "Failed to allocate %(name)s",
    RESOURCE_FULL           :   "%(name)s is full",
    RESOURCE_OVERFLOW       :   "%(name)s is overflow",
    RESOURCE_UNDERRUN       :   "%(name)s is underrun",
    RESOURCE_UNKNOWN_ERROR  :   "Unkown error in %(name)s",

    ATTRIBUTE_NOT_AVAILABLE :   "%(name)s is not available",
    ATTRIBUTE_GET_FAILURE   :   "Failed to get %(name)s",
    ATTRIBUTE_SET_FAILURE   :   "Failed to set %(name)s",
    ATTRIBUTE_UPDATE_FAILURE:   "Failed to update %(name)s",
    ATTRIBUTE_ACCESS_DENIED :   "Access denied: %(name)s",
    ATTRIBUTE_UNKNOWN_ERROR :   "Unknown error when accessing %(name)s",

    IO_NOT_READY            :   "%(name)s is not ready",
    IO_BUSY                 :   "%(name)s is busy",
    IO_TIMEOUT              :   "%(name)s timeout",
    IO_UNKNOWN_ERROR        :   "Unknown error in %(name)s",

    AUTOGEN_ERROR           :   "%(msg)s",
    PARSER_ERROR            :   "%(msg)s",
    GENFDS_ERROR            :   "%(msg)s",
    MIGRATION_ERROR         :   "%(msg)s",
    
    UNKNOWN_ERROR           :   "Unknown error: %(msg)s",
}

class BuildToolError(Exception):
    def __init__(self, code=0xffff, **kwargs):
        if code not in gErrorMessage:
            code = 0xffff

        for key in gKeyWord:
            if key not in kwargs:
                kwargs[key] = "<Unknown>"

        self.ErrorMessage = gErrorMessage[code] % kwargs
        self.ErrorCode = 0xEEEE0000 + code

    def __str__(self):
        return "ERROR: %04X: %s" % (self.ErrorCode & 0xffff, self.ErrorMessage)

class AutoGenError(BuildToolError):
    def __init__(self, code=AUTOGEN_ERROR, **kwargs):
        BuildToolError.__init__(self, code, **kwargs)

    def __str__(self):
        return "\nAutoGen: %s" % BuildToolError.__str__(self)

class ParserError(BuildToolError):
    def __init__(self, code=PARSER_ERROR, **kwargs):
        BuildToolError.__init__(self, code, **kwargs)

    def __str__(self):
        return "\nParser: %s" % BuildToolError.__str__(self)

class GenFdsError(BuildToolError):
    def __init__(self, code=GENFDS_ERROR, **kwargs):
        BuildToolError.__init__(self, code, **kwargs)

    def __str__(self):
        return "\nGenFds: %s" % BuildToolError.__str__(self)

class MigrationError(BuildToolError):
    def __init__(self, code=MIGRATION_ERROR, **kwargs):
        BuildToolError.__init__(self, code, **kwargs)

    def __str__(self):
        return "\nMigration: %s" % BuildToolError.__str__(self)
    
if __name__ == "__main__":
    try:
        raise AutoGenError(FILE_ALREADY_EXIST, name="my_fault.file")
    except BuildToolError, e:
        print e
    except Exception, e:
        print "Python:", e

    try:
        raise GenFdsError(msg="my fault")
    except BuildToolError, e:
        print e
    except Exception, e:
        print "Python:", e

    try:
        xyz = abc[1]
    except BuildToolError, e:
        print e
    except Exception, e:
        print "\nPython:", e
