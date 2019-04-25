#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab

# Copyright (c) 2014 Kevin B. Hendricks, John Schember, and Doug Massay
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of
# conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list
# of conditions and the following disclaimer in the documentation and/or other materials
# provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY
# WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import unicode_literals, division, absolute_import, print_function

import sys
import codecs

iswindows = sys.platform.startswith('win')

try:
    from urllib.parse import unquote
except ImportError:
    from urllib import unquote

if sys.version_info[1] < 4:
    import html.parser
    _h = html.parser.HTMLParser()
else:
    import html as _h

text_type = str
binary_type = bytes
# if will be printing arbitraty binary data to stdout on python 3
# sys.stdin = sys.stdin.detach()
# sys.stdout = sys.stdout.detach()
# sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

# NOTE: Python 3 is completely broken when accessing single bytes in bytes strings
# (and they amazingly claim by design and no bug!)

# To illustrate: this works for unicode in Python 3 and for all Python 2.X for both bytestrings and unicode
# >>> o = '123456789'
# >>> o[-3]
# '7'
# >>> type(o[-3])
# <class 'str'>
# >>> type(o)
# <class 'str'>

# Unfortunately, this is what Python 3 does for no sane reason and only for bytestrings
# >>> o = b'123456789'
# >>> o[-3]
# 55
# >>> type(o[-3])
# <class 'int'>
# >>> type(o)
# <class 'bytes'>

# This mind boggling  behaviour also happens when indexing a bytestring and/or
# iteratoring over a bytestring.  In other words it will return an int but not
# the byte itself!!!!!!!

# The only way to access a single byte as a byte in bytestring and get the byte in both
# Python 2 and Python 3 is to use a slice

# This problem is so common there are horrible hacks floating around the net to **try**
# to work around it, so that code that works on both Python 2 and Python 3 is possible.

# So in order to write code that works on both Python 2 and Python 3
# if you index or access a single byte and want its ord() then use the bord() function.
# If instead you want it as a single character byte use the bchar() function
# both of which are defined below.

# Also Note: if decode a bytestring using 'latin-1' (or any other full range 0-255 encoding)
# in place of ascii you will get a byte value to half-word or integer value
# one-to-one mapping (in the 0 - 255 range)

def bchr(s):
    return bytes([s])

def bstr(s):
    if isinstance(s, str):
        return bytes(s, 'latin-1')
    else:
        return bytes(s)

def bord(s):
    return s

def bchar(s):
    return bytes([s])

def lrange(*args, **kwargs):
    return list(range(*args, **kwargs))

def lzip(*args, **kwargs):
    return list(zip(*args, **kwargs))

def lmap(*args, **kwargs):
    return list(map(*args, **kwargs))

def lfilter(*args, **kwargs):
    return list(filter(*args, **kwargs))

# In Python 3 you can no longer use .encode('hex') on a bytestring
# instead use the following on both platforms
import binascii
def hexlify(bdata):
    return (binascii.hexlify(bdata)).decode('ascii')

# If you: import struct
# Note:  struct pack, unpack, unpack_from all *require* bytestring format
# data all the way up to at least Python 2.7.5, Python 3 is okay with either

# If you: import re
# note: Python 3 "re" requires the pattern to be the exact same type as the data to be
# searched ... but u"" is not allowed for the pattern itself only b""
# Python 2.X allows the pattern to be any type and converts it to match the data
# and returns the same type as the data

# convert string to be utf-8 encoded
def utf8_str(p, enc='utf-8'):
    if p is None:
        return None
    if isinstance(p, text_type):
        return p.encode('utf-8')
    if enc != 'utf-8':
        return p.decode(enc).encode('utf-8')
    return p

# convert string to be unicode encoded
def unicode_str(p, enc='utf-8'):
    if p is None:
        return None
    if isinstance(p, text_type):
        return p
    return p.decode(enc)

ASCII_CHARS   = set(chr(x) for x in range(128))
URL_SAFE      = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                    'abcdefghijklmnopqrstuvwxyz'
                    '0123456789' '#' '_.-/~')
IRI_UNSAFE = ASCII_CHARS - URL_SAFE

# returns a quoted IRI (not a URI)
def quoteurl(href):
    if isinstance(href,binary_type):
        href = href.decode('utf-8')
    result = []
    for char in href:
        if char in IRI_UNSAFE:
            char = "%%%02x" % ord(char)
        result.append(char)
    return ''.join(result)

# unquotes url/iri
def unquoteurl(href):
    if isinstance(href,binary_type):
        href = href.decode('utf-8')
    href = unquote(href)
    return href

# unescape html
def unescapeit(sval):
    return _h.unescape(sval)

# Python 2.X commandline parsing under Windows has been horribly broken for years!
# Use the following code to emulate full unicode commandline parsing on Python 2
# ie. To get  sys.argv arguments and properly encode them as unicode

def unicode_argv():
    return sys.argv

# Python 2.X is broken in that it does not recognize CP65001 as UTF-8
def add_cp65001_codec():
    return
