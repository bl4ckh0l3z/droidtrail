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
from stringblock import StringBlock
from buffhandle import BuffHandle
from arscheader import ARSCHeader
from arscrestablepackage import ARSCResTablePackage
from arscrestype import ARSCResType
from arscrestypespec import ARSCResTypeSpec
from arscrestableentry import ARSCResTableEntry

import sys
sys.path.append('../../')
from utils.utils import Utils

class ARSCParser:

    RES_TABLE_PACKAGE_TYPE = 0x0200
    RES_TABLE_TYPE_TYPE = 0x0201
    RES_TABLE_TYPE_SPEC_TYPE = 0x0202

    DIMENSION_UNITS = ["px", "dip", "sp", "pt", "in", "mm"]
    COMPLEX_UNIT_MASK = 15

    def __init__(self, raw_buff):
        self.analyzed = False
        self.buff = BuffHandle(raw_buff)
        #print "SIZE", hex(self.buff.size())

        self.header = ARSCHeader(self.buff)
        self.packageCount = unpack('<i', self.buff.read(4))[0]

        #print hex(self.packageCount)

        self.stringpool_main = StringBlock(self.buff)

        self.next_header = ARSCHeader(self.buff)
        self.packages = {}
        self.values = {}

        for i in range(0, self.packageCount):
            current_package = ARSCResTablePackage(self.buff)
            package_name = current_package.get_name()

            self.packages[package_name] = []

            mTableStrings = StringBlock(self.buff)
            mKeyStrings = StringBlock(self.buff)

            #self.stringpool_main.show()
            #self.mTableStrings.show()
            #self.mKeyStrings.show()

            self.packages[package_name].append(current_package)
            self.packages[package_name].append(mTableStrings)
            self.packages[package_name].append(mKeyStrings)

            pc = PackageContext(current_package, self.stringpool_main, mTableStrings, mKeyStrings)

            current = self.buff.get_idx()
            while not self.buff.end():
                header = ARSCHeader(self.buff)
                self.packages[package_name].append(header)

                if header.type == self.RES_TABLE_TYPE_SPEC_TYPE:
                    self.packages[package_name].append(ARSCResTypeSpec(self.buff, pc))

                elif header.type == self.RES_TABLE_TYPE_TYPE:
                    a_res_type = ARSCResType(self.buff, pc)
                    self.packages[package_name].append(a_res_type)

                    entries = []
                    for i in range(0, a_res_type.entryCount):
                        current_package.mResId = current_package.mResId & 0xffff0000 | i
                        entries.append((unpack('<i', self.buff.read(4))[0], current_package.mResId))

                    self.packages[package_name].append(entries)

                    for entry, res_id in entries:
                        if self.buff.end():
                            break

                        if entry != -1:
                            ate = ARSCResTableEntry(self.buff, res_id, pc)
                            self.packages[package_name].append(ate)

                elif header.type == self.RES_TABLE_PACKAGE_TYPE:
                    break
                else:
                    logging.warning("unknown type")
                    break

                current += header.size
                self.buff.set_idx(current)

    def _analyse(self):
        if self.analyzed:
            return

        self.analyzed = True

        for package_name in self.packages:
            self.values[package_name] = {}

            nb = 3
            for header in self.packages[package_name][nb:]:
                if isinstance(header, ARSCHeader):
                    if header.type == self.RES_TABLE_TYPE_TYPE:
                        a_res_type = self.packages[package_name][nb + 1]

                        if a_res_type.config.get_language() not in self.values[package_name]:
                            self.values[package_name][a_res_type.config.get_language()] = {}
                            self.values[package_name][a_res_type.config.get_language()]["public"] = []

                        c_value = self.values[package_name][a_res_type.config.get_language()]

                        entries = self.packages[package_name][nb + 2]
                        nb_i = 0
                        for entry, res_id in entries:
                            if entry != -1:
                                ate = self.packages[package_name][nb + 3 + nb_i]

                                #print ate.is_public(), a_res_type.get_type(), ate.get_value(), hex(ate.mResId)
                                if ate.get_index() != -1:
                                    c_value["public"].append((a_res_type.get_type(), ate.get_value(), ate.mResId))

                                if a_res_type.get_type() not in c_value:
                                    c_value[a_res_type.get_type()] = []

                                if a_res_type.get_type() == "string":
                                    c_value["string"].append(self.get_resource_string(ate))

                                elif a_res_type.get_type() == "id":
                                    if not ate.is_complex():
                                        c_value["id"].append(self.get_resource_id(ate))

                                elif a_res_type.get_type() == "bool":
                                    if not ate.is_complex():
                                        c_value["bool"].append(self.get_resource_bool(ate))

                                elif a_res_type.get_type() == "integer":
                                    c_value["integer"].append(self.get_resource_integer(ate))

                                elif a_res_type.get_type() == "color":
                                    c_value["color"].append(self.get_resource_color(ate))

                                elif a_res_type.get_type() == "dimen":
                                    c_value["dimen"].append(self.get_resource_dimen(ate))

                                #elif a_res_type.get_type() == "style":
                                #    c_value["style"].append(self.get_resource_style(ate))

                                nb_i += 1
                nb += 1

    def get_resource_string(self, ate):
        return [ate.get_value(), ate.get_key_data()]

    def get_resource_id(self, ate):
        x = [ate.get_value()]
        if ate.key.get_data() == 0:
            x.append("false")
        elif ate.key.get_data() == 1:
            x.append("true")
        return x

    def get_resource_bool(self, ate):
        x = [ate.get_value()]
        if ate.key.get_data() == 0:
            x.append("false")
        elif ate.key.get_data() == -1:
            x.append("true")
        return x

    def get_resource_integer(self, ate):
        return [ate.get_value(), ate.key.get_data()]

    def get_resource_color(self, ate):
        entry_data = ate.key.get_data()
        return [ate.get_value(), "#%02x%02x%02x%02x" % (((entry_data >> 24) & 0xFF), ((entry_data >> 16) & 0xFF), ((entry_data >> 8) & 0xFF), (entry_data & 0xFF))]

    def get_resource_dimen(self, ate):
        try:
            return [ate.get_value(), "%s%s" % (Utils.complex_to_float(ate.key.get_data()), self.DIMENSION_UNITS[ate.key.get_data() & self.COMPLEX_UNIT_MASK])]
        except Exception, why:
            logging.warning(why.__str__())
            return [ate.get_value(), ate.key.get_data()]

    # FIXME
    def get_resource_style(self, ate):
        return ["", ""]

    def get_packages_names(self):
        return self.packages.keys()

    def get_locales(self, package_name):
        self._analyse()
        return self.values[package_name].keys()

    def get_types(self, package_name, locale):
        self._analyse()
        return self.values[package_name][locale].keys()

    def get_public_resources(self, package_name, locale='\x00\x00'):
        self._analyse()

        buff = '<?xml version="1.0" encoding="utf-8"?>\n'
        buff += '<resources>\n'

        try:
            for i in self.values[package_name][locale]["public"]:
                buff += '<public type="%s" name="%s" id="0x%08x" />\n' % (i[0], i[1], i[2])
        except KeyError:
            pass

        buff += '</resources>\n'

        return buff.encode('utf-8')

    def get_string_resources(self, package_name, locale='\x00\x00'):
        self._analyse()

        buff = '<?xml version="1.0" encoding="utf-8"?>\n'
        buff += '<resources>\n'

        try:
            for i in self.values[package_name][locale]["string"]:
                buff += '<string name="%s">%s</string>\n' % (i[0], i[1])
        except KeyError:
            pass

        buff += '</resources>\n'

        return buff.encode('utf-8')

    def get_strings_resources(self):
        self._analyse()

        buff = '<?xml version="1.0" encoding="utf-8"?>\n'

        buff += "<packages>\n"
        for package_name in self.get_packages_names():
            buff += "<package name=\"%s\">\n" % package_name

            for locale in self.get_locales(package_name):
                buff += "<locale value=%s>\n" % repr(locale)

                buff += '<resources>\n'
                try:
                    for i in self.values[package_name][locale]["string"]:
                        buff += '<string name="%s">%s</string>\n' % (i[0], i[1])
                except KeyError:
                    pass

                buff += '</resources>\n'
                buff += '</locale>\n'

            buff += "</package>\n"

        buff += "</packages>\n"

        return buff.encode('utf-8')

    def get_id_resources(self, package_name, locale='\x00\x00'):
        self._analyse()

        buff = '<?xml version="1.0" encoding="utf-8"?>\n'
        buff += '<resources>\n'

        try:
            for i in self.values[package_name][locale]["id"]:
                if len(i) == 1:
                    buff += '<item type="id" name="%s"/>\n' % (i[0])
                else:
                    buff += '<item type="id" name="%s">%s</item>\n' % (i[0], i[1])
        except KeyError:
            pass

        buff += '</resources>\n'

        return buff.encode('utf-8')

    def get_bool_resources(self, package_name, locale='\x00\x00'):
        self._analyse()

        buff = '<?xml version="1.0" encoding="utf-8"?>\n'
        buff += '<resources>\n'

        try:
            for i in self.values[package_name][locale]["bool"]:
                buff += '<bool name="%s">%s</bool>\n' % (i[0], i[1])
        except KeyError:
            pass

        buff += '</resources>\n'

        return buff.encode('utf-8')

    def get_integer_resources(self, package_name, locale='\x00\x00'):
        self._analyse()

        buff = '<?xml version="1.0" encoding="utf-8"?>\n'
        buff += '<resources>\n'

        try:
            for i in self.values[package_name][locale]["integer"]:
                buff += '<integer name="%s">%s</integer>\n' % (i[0], i[1])
        except KeyError:
            pass

        buff += '</resources>\n'

        return buff.encode('utf-8')

    def get_color_resources(self, package_name, locale='\x00\x00'):
        self._analyse()

        buff = '<?xml version="1.0" encoding="utf-8"?>\n'
        buff += '<resources>\n'

        try:
            for i in self.values[package_name][locale]["color"]:
                buff += '<color name="%s">%s</color>\n' % (i[0], i[1])
        except KeyError:
            pass

        buff += '</resources>\n'

        return buff.encode('utf-8')

    def get_dimen_resources(self, package_name, locale='\x00\x00'):
        self._analyse()

        buff = '<?xml version="1.0" encoding="utf-8"?>\n'
        buff += '<resources>\n'

        try:
            for i in self.values[package_name][locale]["dimen"]:
                buff += '<dimen name="%s">%s</dimen>\n' % (i[0], i[1])
        except KeyError:
            pass

        buff += '</resources>\n'

        return buff.encode('utf-8')

    def get_id(self, package_name, rid, locale='\x00\x00'):
        self._analyse()

        try:
            for i in self.values[package_name][locale]["public"]:
                if i[2] == rid:
                    return i
        except KeyError:
            return None

    def get_string(self, package_name, name, locale='\x00\x00'):
        self._analyse()

        try:
            for i in self.values[package_name][locale]["string"]:
                if i[0] == name:
                    return i
        except KeyError:
            return None

    def get_items(self, package_name):
        self._analyse()
        return self.packages[package_name]


class PackageContext:
    def __init__(self, current_package, stringpool_main, mTableStrings, mKeyStrings):
        self.stringpool_main = stringpool_main
        self.mTableStrings = mTableStrings
        self.mKeyStrings = mKeyStrings
        self.current_package = current_package

    def get_mResId(self):
        return self.current_package.mResId

    def set_mResId(self, mResId):
        self.current_package.mResId = mResId