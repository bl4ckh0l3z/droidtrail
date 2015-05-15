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
from struct import unpack

class ARSCResTableConfig:
    def __init__(self, buff):
        self.start = buff.get_idx()
        self.size = unpack('<i', buff.read(4))[0]
        self.imsi = unpack('<i', buff.read(4))[0]
        self.locale = unpack('<i', buff.read(4))[0]
        self.screenType = unpack('<i', buff.read(4))[0]
        self.input = unpack('<i', buff.read(4))[0]
        self.screenSize = unpack('<i', buff.read(4))[0]
        self.version = unpack('<i', buff.read(4))[0]

        self.screenConfig = 0
        self.screenSizeDp = 0

        if self.size >= 32:
            self.screenConfig = unpack('<i', buff.read(4))[0]

            if self.size >= 36:
                self.screenSizeDp = unpack('<i', buff.read(4))[0]

        self.exceedingSize = self.size - 36
        if self.exceedingSize > 0:
            logging.warning("too much bytes !")
            self.padding = buff.read(self.exceedingSize)

        #print "ARSCResTableConfig", hex(self.start), hex(self.size), hex(self.imsi), hex(self.locale), repr(self.get_language()), repr(self.get_country()), hex(self.screenType), hex(self.input), hex(self.screenSize), hex(self.version), hex(self.screenConfig), hex(self.screenSizeDp)

    def get_language(self):
        x = self.locale & 0x0000ffff
        return chr(x & 0x00ff) + chr((x & 0xff00) >> 8)

    def get_country(self):
        x = (self.locale & 0xffff0000) >> 16
        return chr(x & 0x00ff) + chr((x & 0xff00) >> 8)