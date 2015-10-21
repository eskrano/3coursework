# -*- coding: latin-1 -*-
##
##	   Copyright (c) 2000-2013 Thomas Heller
##
## Permission is hereby granted, free of charge, to any person obtaining
## a copy of this software and associated documentation files (the
## "Software"), to deal in the Software without restriction, including
## without limitation the rights to use, copy, modify, merge, publish,
## distribute, sublicense, and/or sell copies of the Software, and to
## permit persons to whom the Software is furnished to do so, subject to
## the following conditions:
##
## The above copyright notice and this permission notice shall be
## included in all copies or substantial portions of the Software.
##
## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
## EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
## MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
## NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
## LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
## OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
## WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
##

import struct

VOS_NT_WINDOWS32 = 0x00040004
VFT_APP = 0x00000001

RT_VERSION = 16

class VersionError(Exception):
    pass

def w32_uc(text):
    """Encode a string into UTF-16 little endian, ready to use for
    win32 apis"""
    return text.encode("utf-16-le")

class VS_FIXEDFILEINFO:
    dwSignature = 0xFEEF04BD
    dwStrucVersion = 0x00010000
    dwFileVersionMS = 0x00010000
    dwFileVersionLS = 0x00000001
    dwProductVersionMS = 0x00010000
    dwProductVersionLS = 0x00000001
    dwFileFlagsMask = 0x3F
    dwFileFlags = 0
    dwFileOS = VOS_NT_WINDOWS32
    dwFileType = VFT_APP
    dwFileSubtype = 0
    dwFileDateMS = 0
    dwFileDateLS = 0

    fmt = "13L"

    def __init__(self, version):
        version = version.replace(",", ".")
        fields = (version + '.0.0.0.0').split(".")[:4]
        fields = [f.strip() for f in fields]
        try:
            self.dwFileVersionMS = int(fields[0]) * 65536 + int(fields[1])
            self.dwFileVersionLS = int(fields[2]) * 65536 + int(fields[3])
        except ValueError:
            raise VersionError("could not parse version number '%s'" % version)

    def tobytes(self):
        return struct.pack(self.fmt,
                           self.dwSignature,
                           self.dwStrucVersion,
                           self.dwFileVersionMS,
                           self.dwFileVersionLS,
                           self.dwProductVersionMS,
                           self.dwProductVersionLS,
                           self.dwFileFlagsMask,
                           self.dwFileFlags,
                           self.dwFileOS,
                           self.dwFileType,
                           self.dwFileSubtype,
                           self.dwFileDateMS,
                           self.dwFileDateLS)
                    
def align(data):
    pad = - len(data) % 4
    return data + b'\000' * pad

class VS_STRUCT:
    items = ()
    
    def tobytes(self):
        szKey = w32_uc(self.name)
        ulen = len(szKey)+2

        value = self.get_value()
        data = struct.pack("h%ss0i" % ulen, self.wType, szKey) + value

        data = align(data)

        for item in self.items:
            data = data + item.tobytes()

        wLength = len(data) + 4 # 4 bytes for wLength and wValueLength
        wValueLength = len(value)

        return self.pack("hh", wLength, wValueLength, data)

    def pack(self, fmt, len, vlen, data):
        return struct.pack(fmt, len, vlen) + data

    def get_value(self):
        return b""


class String(VS_STRUCT):
    wType = 1
    items = ()

    def __init__(self, name_value):
        (name, value) = name_value
        self.name = name
        if value:
            self.value = value + '\000' # strings must be zero terminated
        else:
            self.value = value

    def pack(self, fmt, len, vlen, data):
        # ValueLength is measured in WORDS, not in BYTES!
        return struct.pack(fmt, len, vlen//2) + data

    def get_value(self):
        return w32_uc(self.value)


class StringTable(VS_STRUCT):
    wType = 1

    def __init__(self, name, strings):
        self.name = name
        self.items = map(String, strings)


class StringFileInfo(VS_STRUCT):
    wType = 1
    name = "StringFileInfo"

    def __init__(self, name, strings):
        self.items = [StringTable(name, strings)]

class Var(VS_STRUCT):
    # MSDN says:
    # If you use the Var structure to list the languages your
    # application or DLL supports instead of using multiple version
    # resources, use the Value member to contain an array of DWORD
    # values indicating the language and code page combinations
    # supported by this file. The low-order word of each DWORD must
    # contain a Microsoft language identifier, and the high-order word
    # must contain the IBM� code page number. Either high-order or
    # low-order word can be zero, indicating that the file is language
    # or code page independent. If the Var structure is omitted, the
    # file will be interpreted as both language and code page
    # independent.
    wType = 0
    name = "Translation"

    def __init__(self, value):
        self.value = value

    def get_value(self):
        return struct.pack("l", self.value)

class VarFileInfo(VS_STRUCT):
    wType = 1
    name = "VarFileInfo"

    def __init__(self, *names):
        self.items = map(Var, names)
        
    def get_value(self):
        return b""

class VS_VERSIONINFO(VS_STRUCT):
    wType = 0 # 0: binary data, 1: text data
    name = "VS_VERSION_INFO"

    def __init__(self, version, items):
        self.value = VS_FIXEDFILEINFO(version)
        self.items = items

    def get_value(self):
        return self.value.tobytes()

class Version(object):
    def __init__(self,
                 version,
                 comments = None,
                 company_name = None,
                 file_description = None,
                 internal_name = None,
                 legal_copyright = None,
                 legal_trademarks = None,
                 original_filename = None,
                 private_build = None,
                 product_name = None,
                 product_version = None,
                 special_build = None):
        self.version = version
        strings = []
        if comments is not None:
            strings.append(("Comments", comments))
        if company_name is not None:
            strings.append(("CompanyName", company_name))
        if file_description is not None:
            strings.append(("FileDescription", file_description))
        strings.append(("FileVersion", version))
        if internal_name is not None:
            strings.append(("InternalName", internal_name))
        if legal_copyright is not None:
            strings.append(("LegalCopyright", legal_copyright))
        if legal_trademarks is not None:
            strings.append(("LegalTrademarks", legal_trademarks))
        if original_filename is not None:
            strings.append(("OriginalFilename", original_filename))
        if private_build is not None:
            strings.append(("PrivateBuild", private_build))
        if product_name is not None:
            strings.append(("ProductName", product_name))
        strings.append(("ProductVersion", product_version or version))
        if special_build is not None:
            strings.append(("SpecialBuild", special_build))
        from . import __version__
        strings.append(("Creator", "py2exe %s" % __version__))
        self.strings = strings
        
    def resource_bytes(self):
        vs = VS_VERSIONINFO(self.version,
                            [StringFileInfo("040904B0",
                                            self.strings),
                             VarFileInfo(0x04B00409)])
        return vs.tobytes()

def test():
    import sys
    sys.path.append("c:/tmp")
    version = Version("1, 0, 0, 1",
                      comments = "�ml�ut comments",
                      company_name = "No Company",
                      file_description = "silly application",
                      internal_name = "silly",
                      legal_copyright = u"Copyright � 2003",
##                      legal_trademark = "",
                      original_filename = "silly.exe",
                      private_build = "test build",
                      product_name = "silly product",
                      product_version = None,
##                      special_build = ""
                      )
    print(version.resource_bytes())

if __name__ == '__main__':
    test()
