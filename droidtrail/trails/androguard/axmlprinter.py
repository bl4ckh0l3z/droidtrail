# This file is part of DroidTrail.
#
# bl4ckh0l3 <bl4ckh0l3z at gmail.com>
#
# DroidTrail is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# DroidTrail is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with DroidTrail. If not, see <http://www.gnu.org/licenses/>.
#
# **********************************************************************
#   NOTE: This file is part of Androguard;
#         Copyright (C) 2012, Anthony Desnos <desnos at t0t0.fr>
#         All rights reserved.
#
#         It is a modified and sanitized version for DroidTrail,
#         created by bl4ckh0l3 <bl4ckh0l3z at gmail.com>.
# **********************************************************************
#

__author__ = 'desnos'
__license__ = 'GPL v2'
__maintainer__ = 'bl4ckh0l3'
__email__ = 'bl4ckh0l3z@gmail.com'

from xml.dom import minidom
from xml.sax.saxutils import escape
from struct import pack, unpack
from axmlparser import AXMLParser

import sys
sys.path.append('../../')
from utils.utils import Utils

class AXMLPrinter:

    START_DOCUMENT = 0
    END_DOCUMENT = 1
    START_TAG = 2
    END_TAG = 3
    TEXT = 4

    TYPE_ATTRIBUTE = 2
    TYPE_DIMENSION = 5
    TYPE_FIRST_COLOR_INT = 28
    TYPE_FIRST_INT = 16
    TYPE_FLOAT = 4
    TYPE_FRACTION = 6
    TYPE_INT_BOOLEAN = 18
    TYPE_INT_COLOR_ARGB4 = 30
    TYPE_INT_COLOR_ARGB8 = 28
    TYPE_INT_COLOR_RGB4 = 31
    TYPE_INT_COLOR_RGB8 = 29
    TYPE_INT_DEC = 16
    TYPE_INT_HEX = 17
    TYPE_LAST_COLOR_INT = 31
    TYPE_LAST_INT = 31
    TYPE_NULL = 0
    TYPE_REFERENCE = 1
    TYPE_STRING = 3

    DIMENSION_UNITS = ["px", "dip", "sp", "pt", "in", "mm"]
    FRACTION_UNITS = ["%", "%p"]
    COMPLEX_UNIT_MASK = 15

    def __init__(self, raw_buff):
        self.axml = AXMLParser(raw_buff)
        self.xmlns = False

        self.buff = u''

        while True and self.axml.is_valid():
            _type = self.axml.next()

            if _type == self.START_DOCUMENT:
                self.buff += u'<?xml version="1.0" encoding="utf-8"?>\n'
            elif _type == self.START_TAG:
                self.buff += u'<' + self.getPrefix(self.axml.getPrefix()) + self.axml.getName() + u'\n'
                self.buff += self.axml.getXMLNS()

                for i in range(0, self.axml.getAttributeCount()):
                    self.buff += "%s%s=\"%s\"\n" % (self.getPrefix(
                        self.axml.getAttributePrefix(i)), self.axml.getAttributeName(i), self._escape(self.getAttributeValue(i)))

                self.buff += u'>\n'

            elif _type == self.END_TAG:
                self.buff += "</%s%s>\n" % (self.getPrefix(self.axml.getPrefix()), self.axml.getName())

            elif _type == self.TEXT:
                self.buff += "%s\n" % self.axml.getText()

            elif _type == self.END_DOCUMENT:
                break

    def _escape(self, s):
        s = s.replace("&", "&amp;")
        s = s.replace('"', "&quot;")
        s = s.replace("'", "&apos;")
        s = s.replace("<", "&lt;")
        s = s.replace(">", "&gt;")
        return escape(s)

    def get_buff(self):
        return self.buff.encode('utf-8')

    def get_xml(self):
        return minidom.parseString(self.get_buff()).toprettyxml(encoding="utf-8")

    def get_xml_obj(self):
        return minidom.parseString(self.get_buff())

    def getPrefix(self, prefix):
        if prefix == None or len(prefix) == 0:
            return u''

        return prefix + u':'

    def getAttributeValue(self, index):
        _type = self.axml.getAttributeValueType(index)
        _data = self.axml.getAttributeValueData(index)

        if _type == self.TYPE_STRING:
            return self.axml.getAttributeValue(index)

        elif _type == self.TYPE_ATTRIBUTE:
            return "?%s%08X" % (self.getPackage(_data), _data)

        elif _type == self.TYPE_REFERENCE:
            return "@%s%08X" % (self.getPackage(_data), _data)

        elif _type == self.TYPE_FLOAT:
            return "%f" % unpack("=f", pack("=L", _data))[0]

        elif _type == self.TYPE_INT_HEX:
            return "0x%08X" % _data

        elif _type == self.TYPE_INT_BOOLEAN:
            if _data == 0:
                return "false"
            return "true"

        elif _type == self.TYPE_DIMENSION:
            return "%f%s" % (Utils.complexToFloat(_data), self.DIMENSION_UNITS[_data & self.COMPLEX_UNIT_MASK])

        elif _type == self.TYPE_FRACTION:
            return "%f%s" % (Utils.complexToFloat(_data) * 100, self.FRACTION_UNITS[_data & self.COMPLEX_UNIT_MASK])

        elif _type >= self.TYPE_FIRST_COLOR_INT and _type <= self.TYPE_LAST_COLOR_INT:
            return "#%08X" % _data

        elif _type >= self.TYPE_FIRST_INT and _type <= self.TYPE_LAST_INT:
            return "%d" % Utils.long_to_int(_data)

        return "<0x%X, type 0x%02X>" % (_data, _type)

    def getPackage(self, id):
        if id >> 24 == 1:
            return "android:"
        return ""
