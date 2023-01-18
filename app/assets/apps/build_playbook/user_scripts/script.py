"""
1. Take an executable file as input for a Jupyter Notebook, store the file.
2. Print out the header of the file, the file signature, and any interesting strings from it, from a malware analysts perspective.
"""
#!/usr/env python3

import sys
import os
import pefile
import urllib
import peutils
import binascii
import string
import re

# Get the file name from the command line
file_name = sys.argv[1]
print(file_name)

# Check if the file exists
if not os.path.isfile(file_name):
    print("[-] " + file_name + " does not exist.")
    exit(0)

# Check if we have read access to the file
if not os.access(file_name, os.R_OK):
    print("[-] " + file_name + " access denied.")
    exit(0)

# Open the file
fd = open(file_name, "rb")

# Read in the file
contents = fd.read()

# Close the file
fd.close()

# Get the file size
file_size = len(contents)

# Get the file type
file_type = sys.argv[2]

# Get the file signature
file_signature = binascii.hexlify(contents[:2])

# Print out the file name, size, and type
print("[+] File Name: " + file_name)
print("[+] File Size: " + str(file_size))
print("[+] File Type: " + str(file_type))
print("[+] File Signature: " + str(file_signature))

# Check if the file is a PE file
if file_type == "PE":
    # Parse the PE file
    pe = pefile.PE(file_name)

    # Print out the PE header
    print("[+] PE Header:")
    print("\t[+] Machine: " + str(pe.FILE_HEADER.Machine))
    print("\t[+] Number of Sections: " + str(pe.FILE_HEADER.NumberOfSections))
    print("\t[+] Time Date Stamp: " + str(pe.FILE_HEADER.TimeDateStamp))
    print("\t[+] Pointer to Symbol Table: " + str(pe.FILE_HEADER.PointerToSymbolTable))
    print("\t[+] Number of Symbols: " + str(pe.FILE_HEADER.NumberOfSymbols))
    print("\t[+] Size of Optional Header: " + str(pe.FILE_HEADER.SizeOfOptionalHeader))
    print("\t[+] Characteristics: " + str(pe.FILE_HEADER.Characteristics))

    # Print out the PE optional header
    print("[+] PE Optional Header:")
    print("\t[+] Magic: " + str(pe.OPTIONAL_HEADER.Magic))
    print("\t[+] Major Linker Version: " + str(pe.OPTIONAL_HEADER.MajorLinkerVersion))
    print("\t[+] Minor Linker Version: " + str(pe.OPTIONAL_HEADER.MinorLinkerVersion))
    print("\t[+] Size of Code: " + str(pe.OPTIONAL_HEADER.SizeOfCode))
    print("\t[+] Size of Initialized Data: " + str(pe.OPTIONAL_HEADER.SizeOfInitializedData))
    print("\t[+] Size of Uninitialized Data: " + str(pe.OPTIONAL_HEADER.SizeOfUninitializedData))
    print("\t[+] Address of Entry Point: " + str(pe.OPTIONAL_HEADER.AddressOfEntryPoint))
    print("\t[+] Base of Code: " + str(pe.OPTIONAL_HEADER.BaseOfCode))
    print("\t[+] Base of Data: " + str(pe.OPTIONAL_HEADER.BaseOfData))
    print("\t[+] Image Base: " + str(pe.OPTIONAL_HEADER.ImageBase))
    print("\t[+] Section Alignment: " + str(pe.OPTIONAL_HEADER.SectionAlignment))
    print("\t[+] File Alignment: " + str(pe.OPTIONAL_HEADER.FileAlignment))
    print("\t[+] Major Operating System Version: " + str(pe.OPTIONAL_HEADER.MajorOperatingSystemVersion))
    print("\t[+] Major Image Version: " + str(pe.OPTIONAL_HEADER.MajorImageVersion))
    print("\t[+] Minor Image Version: " + str(pe.OPTIONAL_HEADER.MinorImageVersion))
    print("\t[+] Major Subsystem Version: " + str(pe.OPTIONAL_HEADER.MajorSubsystemVersion))
    print("\t[+] Minor Subsystem Version: " + str(pe.OPTIONAL_HEADER.MinorSubsystemVersion))
    print("\t[+] Size of Image: " + str(pe.OPTIONAL_HEADER.SizeOfImage))
    print("\t[+] Size of Headers: " + str(pe.OPTIONAL_HEADER.SizeOfHeaders))
    print("\t[+] CheckSum: " + str(pe.OPTIONAL_HEADER.CheckSum))
    print("\t[+] Subsystem: " + str(pe.OPTIONAL_HEADER.Subsystem))
    print("\t[+] Dll Characteristics: " + str(pe.OPTIONAL_HEADER.DllCharacteristics))
    print("\t[+] Size of Stack Reserve: " + str(pe.OPTIONAL_HEADER.SizeOfStackReserve))
    print("\t[+] Size of Stack Commit: " + str(pe.OPTIONAL_HEADER.SizeOfStackCommit))
    print("\t[+] Size of Heap Reserve: " + str(pe.OPTIONAL_HEADER.SizeOfHeapReserve))
    print("\t[+] Size of Heap Commit: " + str(pe.OPTIONAL_HEADER.SizeOfHeapCommit))
    print("\t[+] Loader Flags: " + str(pe.OPTIONAL_HEADER.LoaderFlags))
    print("\t[+] Number of RVA and Sizes: " + str(pe.OPTIONAL_HEADER.NumberOfRvaAndSizes))

    # Print out the PE sections
    print("[+] PE Sections:")
    for section in pe.sections:
        print("\t[+] Name: " + str(section.Name))
        print("\t[+] Virtual Address: " + str(section.VirtualAddress))
        print("\t[+] Virtual Size: " + str(section.Misc_VirtualSize))
        print("\t[+] Size of Raw Data: " + str(section.SizeOfRawData))
        print("\t[+] Pointer to Raw Data: " + str(section.PointerToRawData))
        print("\t[+] Pointer to Relocations: " + str(section.PointerToRelocations))
        print("\t[+] Pointer to Linenumbers: " + str(section.PointerToLinenumbers))
        print("\t[+] Number of Relocations: " + str(section.NumberOfRelocations))
        print("\t[+] Number of Linenumbers: " + str(section.NumberOfLinenumbers))
        print("\t[+] Characteristics: " + str(section.Characteristics))

    # Print out the PE imports
    print("[+] PE Imports:")
    for entry in pe.DIRECTORY_ENTRY_IMPORT:
        print("\t[+] Library: " + str(entry.dll))
        for imp in entry.imports:
            print("\t\t[+] Import: " + str(imp.name))


    # Print out the PE resources
    print("[+] PE Resources:")
    for resource_type in pe.DIRECTORY_ENTRY_RESOURCE.entries:
        print("\t[+] Resource Type: " + str(resource_type.name))
        if resource_type.name is not None:
            name = str(resource_type.name)
        else:
            name = str(pefile.RESOURCE_TYPE.get(resource_type.struct.Id))
        if name == None:
            name = str(resource_type.struct.Id)
        if hasattr(resource_type, 'directory'):
            for resource_id in resource_type.directory.entries:
                if hasattr(resource_id, 'directory'):
                    for resource_lang in resource_id.directory.entries:
                        data = pe.get_data(resource_lang.data.struct.OffsetToData, resource_lang.data.struct.Size)
                        filetype = sys.argv[2]
                        print("\t\t[+] Resource Name: " + name)
                        print("\t\t[+] Resource Language: " + str(pefile.LANG.get(resource_lang.data.lang, '*unknown*')))
                        print("\t\t[+] Resource Sublanguage: " + str(pefile.get_sublang_name_for_lang(resource_lang.data.lang, resource_lang.data.sublang)))
                        print("\t\t[+] Resource Identifier: " + str(resource_id.name))
                        print("\t\t[+] Resource Data: " + str(data))
                        print("\t\t[+] Resource File Type: " + str(filetype))

    # Print out the PE version information
    print("[+] PE Version Information:")
    if hasattr(pe, 'VS_VERSIONINFO'):
        if hasattr(pe, 'FileInfo'):
            for entry in pe.FileInfo:
                if hasattr(entry, 'StringTable'):
                    for st_entry in entry.StringTable:
                        for str_entry in st_entry.entries.items():
                            print("\t[+] Entry: " + str(str_entry))
                elif hasattr(entry, 'Var'):
                    for var_entry in entry.Var:
                        if hasattr(var_entry, 'entry'):
                            print("\t[+] Entry: " + str(var_entry.entry.items()))

    # Print out the PE overlay
    print("[+] PE Overlay:")
    print("\t[+] Size: " + str(len(pe.get_overlay())))
