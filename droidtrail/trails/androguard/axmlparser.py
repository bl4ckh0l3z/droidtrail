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
# NOTE: This file is part of Androguard;
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

import logging
from struct import pack, unpack
from buffhandle import BuffHandle
from stringblock import StringBlock

class AXMLParser:

    CHUNK_AXML_FILE = 0x00080003
    CHUNK_RESOURCEIDS = 0x00080180
    CHUNK_XML_FIRST = 0x00100100
    CHUNK_XML_START_NAMESPACE = 0x00100100
    CHUNK_XML_END_NAMESPACE = 0x00100101
    CHUNK_XML_START_TAG = 0x00100102
    CHUNK_XML_END_TAG = 0x00100103
    CHUNK_XML_TEXT = 0x00100104
    CHUNK_XML_LAST = 0x00100104

    START_DOCUMENT = 0
    END_DOCUMENT = 1
    START_TAG = 2
    END_TAG = 3
    TEXT = 4

    ATTRIBUTE_IX_NAMESPACE_URI = 0
    ATTRIBUTE_IX_NAME = 1
    ATTRIBUTE_IX_VALUE_STRING = 2
    ATTRIBUTE_IX_VALUE_TYPE = 3
    ATTRIBUTE_IX_VALUE_DATA = 4
    ATTRIBUTE_LENGHT = 5

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

    def __init__(self, utils, raw_buff):
        self._utils = utils

        self.reset()

        self.valid_axml = True
        self.buff = BuffHandle(raw_buff)

        axml_file = unpack('<L', self.buff.read(4))[0]

        if axml_file == self.CHUNK_AXML_FILE:
            self.buff.read(4)

            self.sb = StringBlock(self.buff)

            self.m_resourceIDs = []
            self.m_prefixuri = {}
            self.m_uriprefix = {}
            self.m_prefixuriL = []

            self.visited_ns = []
        else:
            self.valid_axml = False
            logging.warning("Not a valid xml file")

    def is_valid(self):
        return self.valid_axml

    def reset(self):
        self.m_event = -1
        self.m_lineNumber = -1
        self.m_name = -1
        self.m_namespaceUri = -1
        self.m_attributes = []
        self.m_idAttribute = -1
        self.m_classAttribute = -1
        self.m_styleAttribute = -1

    def next(self):
        self.doNext()
        return self.m_event

    def doNext(self):
        if self.m_event == self.END_DOCUMENT:
            return

        event = self.m_event

        self.reset()
        while True:
            chunkType = -1

            # Fake END_DOCUMENT event.
            if event == self.END_TAG:
                pass

            # START_DOCUMENT
            if event == self.START_DOCUMENT:
                chunkType = self.CHUNK_XML_START_TAG
            else:
                if self.buff.end():
                    self.m_event = self.END_DOCUMENT
                    break
                chunkType = unpack('<L', self.buff.read(4))[0]

            if chunkType == self.CHUNK_RESOURCEIDS:
                chunkSize = unpack('<L', self.buff.read(4))[0]
                # FIXME
                if chunkSize < 8 or chunkSize % 4 != 0:
                    logging.warning("Invalid chunk size")

                for i in range(0, chunkSize / 4 - 2):
                    self.m_resourceIDs.append(unpack('<L', self.buff.read(4))[0])

                continue

            # FIXME
            if chunkType < self.CHUNK_XML_FIRST or chunkType > self.CHUNK_XML_LAST:
                logging.warning("invalid chunk type")

            # Fake START_DOCUMENT event.
            if chunkType == self.CHUNK_XML_START_TAG and event == -1:
                self.m_event = self.START_DOCUMENT
                break

            self.buff.read(4)  # /*chunkSize*/
            lineNumber = unpack('<L', self.buff.read(4))[0]
            self.buff.read(4)  # 0xFFFFFFFF

            if chunkType == self.CHUNK_XML_START_NAMESPACE or chunkType == self.CHUNK_XML_END_NAMESPACE:
                if chunkType == self.CHUNK_XML_START_NAMESPACE:
                    prefix = unpack('<L', self.buff.read(4))[0]
                    uri = unpack('<L', self.buff.read(4))[0]

                    self.m_prefixuri[prefix] = uri
                    self.m_uriprefix[uri] = prefix
                    self.m_prefixuriL.append((prefix, uri))
                    self.ns = uri
                else:
                    self.ns = -1
                    self.buff.read(4)
                    self.buff.read(4)
                    (prefix, uri) = self.m_prefixuriL.pop()
                continue

            self.m_lineNumber = lineNumber

            if chunkType == self.CHUNK_XML_START_TAG:
                self.m_namespaceUri = unpack('<L', self.buff.read(4))[0]
                self.m_name = unpack('<L', self.buff.read(4))[0]

                # FIXME
                self.buff.read(4)  # flags

                attributeCount = unpack('<L', self.buff.read(4))[0]
                self.m_idAttribute = (attributeCount >> 16) - 1
                attributeCount = attributeCount & 0xFFFF
                self.m_classAttribute = unpack('<L', self.buff.read(4))[0]
                self.m_styleAttribute = (self.m_classAttribute >> 16) - 1

                self.m_classAttribute = (self.m_classAttribute & 0xFFFF) - 1

                for i in range(0, attributeCount * self.ATTRIBUTE_LENGHT):
                    self.m_attributes.append(unpack('<L', self.buff.read(4))[0])

                for i in range(self.ATTRIBUTE_IX_VALUE_TYPE, len(self.m_attributes), self.ATTRIBUTE_LENGHT):
                    self.m_attributes[i] = self.m_attributes[i] >> 24

                self.m_event = self.START_TAG
                break

            if chunkType == self.CHUNK_XML_END_TAG:
                self.m_namespaceUri = unpack('<L', self.buff.read(4))[0]
                self.m_name = unpack('<L', self.buff.read(4))[0]
                self.m_event = self.END_TAG
                break

            if chunkType == self.CHUNK_XML_TEXT:
                self.m_name = unpack('<L', self.buff.read(4))[0]

                # FIXME
                self.buff.read(4)
                self.buff.read(4)

                self.m_event = self.TEXT
                break

    def getPrefixByUri(self, uri):
        try:
            return self.m_uriprefix[uri]
        except KeyError:
            return -1

    def getPrefix(self):
        try:
            return self.sb.getString(self.m_uriprefix[self.m_namespaceUri])
        except KeyError:
            return u''

    def getName(self):
        if self.m_name == -1 or (self.m_event != self.START_TAG and self.m_event != self.END_TAG):
            return u''
        return self.sb.getString(self.m_name)

    def getText(self):
        if self.m_name == -1 or self.m_event != self.TEXT:
            return u''
        return self.sb.getString(self.m_name)

    def getNamespacePrefix(self, pos):
        prefix = self.m_prefixuriL[pos][0]
        return self.sb.getString(prefix)

    def getNamespaceUri(self, pos):
        uri = self.m_prefixuriL[pos][1]
        return self.sb.getString(uri)

    def getXMLNS(self):
        buff = ""
        for i in self.m_uriprefix:
            if i not in self.visited_ns:
                buff += "xmlns:%s=\"%s\"\n" % (
                    self.sb.getString(self.m_uriprefix[i]), self.sb.getString(self.m_prefixuri[self.m_uriprefix[i]]))
                self.visited_ns.append(i)
        return buff

    def getNamespaceCount(self, pos):
        pass

    def getAttributeOffset(self, index):
        # FIXME
        if self.m_event != self.START_TAG:
            logging.warning("Current event is not START_TAG.")

        offset = index * 5
        # FIXME
        if offset >= len(self.m_attributes):
            logging.warning("Invalid attribute index")

        return offset

    def getAttributeCount(self):
        if self.m_event != self.START_TAG:
            return -1

        return len(self.m_attributes) / self.ATTRIBUTE_LENGHT

    def getAttributePrefix(self, index):
        offset = self.getAttributeOffset(index)
        uri = self.m_attributes[offset + self.ATTRIBUTE_IX_NAMESPACE_URI]
        prefix = self.getPrefixByUri(uri)
        if prefix == -1:
            return ""
        return self.sb.getString(prefix)

    def getAttributeName(self, index):
        offset = self.getAttributeOffset(index)
        name = self.m_attributes[offset + self.ATTRIBUTE_IX_NAME]
        if name == -1:
            return ""
        return self.sb.getString(name)

    def getAttributeValueType(self, index):
        offset = self.getAttributeOffset(index)
        return self.m_attributes[offset + self.ATTRIBUTE_IX_VALUE_TYPE]

    def getAttributeValueData(self, index):
        offset = self.getAttributeOffset(index)
        return self.m_attributes[offset + self.ATTRIBUTE_IX_VALUE_DATA]

    def getAttributeValue(self, index):
        offset = self.getAttributeOffset(index)
        valueType = self.m_attributes[offset + self.ATTRIBUTE_IX_VALUE_TYPE]
        if valueType == self.TYPE_STRING:
            valueString = self.m_attributes[offset + self.ATTRIBUTE_IX_VALUE_STRING]
            return self.sb.getString(valueString)
        return ""