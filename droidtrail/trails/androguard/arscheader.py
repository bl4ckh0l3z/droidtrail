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

from struct import unpack

class ARSCHeader:

    def __init__(self, buff):
        self.start = buff.get_idx()
        self.type = unpack('<h', buff.read(2))[0]
        self.header_size = unpack('<h', buff.read(2))[0]
        self.size = unpack('<i', buff.read(4))[0]

        #print "ARSCHeader", hex(self.start), hex(self.type), hex(self.header_size), hex(self.size)

