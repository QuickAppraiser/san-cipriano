#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Compile .po files to .mo files using proper GNU gettext format.
Based on Python's Tools/i18n/msgfmt.py
"""

import struct
import os
import sys
import re

MESSAGES = {}

def add(msgid, msgstr, fuzzy):
    """Add a non-fuzzy translation to the dictionary."""
    # Always add header (empty msgid with content) for charset info
    # For regular messages, only add non-fuzzy ones
    if msgid == '' and msgstr:  # Header must have content
        MESSAGES[msgid] = msgstr
    elif msgid and not fuzzy and msgstr:  # Regular entries need both msgid and msgstr
        MESSAGES[msgid] = msgstr

def generate():
    """Return the generated output as bytes."""
    keys = sorted(MESSAGES.keys())
    offsets = []
    ids = b''
    strs = b''
    for id in keys:
        # For each string, first the id then the translation
        offsets.append((len(ids), len(id.encode('utf-8')), len(strs), len(MESSAGES[id].encode('utf-8'))))
        ids += id.encode('utf-8') + b'\x00'
        strs += MESSAGES[id].encode('utf-8') + b'\x00'

    # The header is 7 32-bit unsigned integers
    keystart = 7 * 4 + 16 * len(keys)
    valuestart = keystart + len(ids)

    koffsets = []
    voffsets = []
    for o1, l1, o2, l2 in offsets:
        koffsets += [l1, o1 + keystart]
        voffsets += [l2, o2 + valuestart]

    offsets = koffsets + voffsets
    output = struct.pack("Iiiiiii",
                         0x950412de,       # Magic
                         0,                 # Version
                         len(keys),         # # of entries
                         7*4,               # start of key index
                         7*4+len(keys)*8,   # start of value index
                         0, 0)              # size and offset of hash table

    output += struct.pack(str(len(offsets))+"i", *offsets)
    output += ids
    output += strs
    return output

def make(filename, outfile):
    """Main function to process a PO file."""
    global MESSAGES
    MESSAGES = {}

    # Read the PO file
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    msgid = []
    msgstr = []
    in_msgid = False
    in_msgstr = False
    fuzzy = False

    for line in lines:
        line = line.strip()

        # Handle comments
        if line.startswith('#'):
            if line.startswith('#,') and 'fuzzy' in line:
                fuzzy = True
            continue

        # Empty line = end of entry
        if not line:
            if msgid is not None:
                msgid_str = ''.join(msgid)
                msgstr_str = ''.join(msgstr)
                # Include header (empty msgid) for charset info
                add(msgid_str, msgstr_str, fuzzy)
            msgid = []
            msgstr = []
            in_msgid = False
            in_msgstr = False
            fuzzy = False
            continue

        # msgid
        if line.startswith('msgid '):
            in_msgid = True
            in_msgstr = False
            content = line[6:].strip()
            if content.startswith('"') and content.endswith('"'):
                content = content[1:-1]
            # Unescape
            content = content.replace('\\n', '\n').replace('\\"', '"').replace('\\\\', '\\')
            msgid = [content]
            continue

        # msgstr
        if line.startswith('msgstr '):
            in_msgid = False
            in_msgstr = True
            content = line[7:].strip()
            if content.startswith('"') and content.endswith('"'):
                content = content[1:-1]
            # Unescape
            content = content.replace('\\n', '\n').replace('\\"', '"').replace('\\\\', '\\')
            msgstr = [content]
            continue

        # Continuation line
        if line.startswith('"') and line.endswith('"'):
            content = line[1:-1]
            # Unescape
            content = content.replace('\\n', '\n').replace('\\"', '"').replace('\\\\', '\\')
            if in_msgid:
                msgid.append(content)
            elif in_msgstr:
                msgstr.append(content)

    # Don't forget the last entry
    if msgid is not None:
        msgid_str = ''.join(msgid)
        msgstr_str = ''.join(msgstr)
        add(msgid_str, msgstr_str, fuzzy)

    # Generate the MO file
    output = generate()

    # Write the output
    with open(outfile, 'wb') as f:
        f.write(output)

    print(f"Compiled {filename} -> {outfile} ({len(MESSAGES)} messages)")


if __name__ == '__main__':
    base_path = os.path.dirname(os.path.abspath(__file__))
    locale_path = os.path.join(base_path, 'locale')

    languages = ['en', 'fr', 'de', 'it', 'pt']

    for lang in languages:
        po_file = os.path.join(locale_path, lang, 'LC_MESSAGES', 'django.po')
        mo_file = os.path.join(locale_path, lang, 'LC_MESSAGES', 'django.mo')

        if os.path.exists(po_file):
            try:
                make(po_file, mo_file)
            except Exception as e:
                print(f"Error compiling {po_file}: {e}")
        else:
            print(f"Warning: {po_file} not found")

    print("\nDone! All .mo files compiled.")
