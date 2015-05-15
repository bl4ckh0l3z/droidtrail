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
from itertools import starmap

__author__ = 'desnos'
__license__ = 'GPL v2'
__maintainer__ = 'bl4ckh0l3'
__email__ = 'bl4ckh0l3z@gmail.com'

import os
import re
import chilkat
import StringIO
import logging
import zipfile
from xml.dom import minidom
from axmlprinter import AXMLPrinter
from arscparser import ARSCParser


class APK:
    def __init__(self, path, filename):
        self.path = path
        self.filename = filename

        self.xml = {}
        self.axml = {}
        self.arsc = {}

        self.package = ""
        self.androidversion = {}
        self.permissions = []
        self.valid_apk = False

        self.files = {}
        fd = open(os.path.join(path, filename), "rb")
        self.__raw = fd.read()
        fd.close()

        try:
            self.zip = zipfile.ZipFile(StringIO.StringIO(self.__raw), mode='r')

            for i in self.zip.namelist():
                if i == "AndroidManifest.xml":
                    self.axml[i] = AXMLPrinter(self.zip.read(i))
                    try:
                        self.xml[i] = minidom.parseString(self.axml[i].get_buff())
                    except:
                        self.xml[i] = None

                    if self.xml[i] != None:
                        self.package = self.xml[i].documentElement.getAttribute("package")

                        self.androidversion["Code"] = self.xml[i].documentElement.getAttribute("android:versionCode")
                        self.androidversion["Name"] = self.xml[i].documentElement.getAttribute("android:versionName")

                        for item in self.xml[i].getElementsByTagName('uses-permission'):
                            self.permissions.append(str(item.getAttribute("android:name")))

                        self.app_name = self._get_app_name()

                        self.valid_apk = True
        except:
            self.valid_apk = False
            logging.error("Ignoring '%s', exception creating APK instance" % (filename))

    def get_android_manifest(self):
        return self.xml["AndroidManifest.xml"]

    def is_valid_APK(self):
        return self.valid_apk

    def get_filename(self):
        return self.filename

    def get_path(self):
        return self.path

    def get_package(self):
        if self.package == '' or self.package == None:
            self.package = 'None'
        return self.package

    def get_androidversion_code(self):
        if self.androidversion["Code"] == '' or self.androidversion["Code"] == None:
            self.androidversion["Code"] = 'None'
        return self.androidversion["Code"]

    def get_androidversion_name(self):
        if self.androidversion["Name"] == '' or self.androidversion["Name"] == None:
            self.androidversion["Name"] = 'None'
        return self.androidversion["Name"]

    def get_files(self):
        return self.zip.namelist()

    def get_file(self, filename):
        try:
            return self.zip.read(filename)
        except KeyError:
            return ""

    def get_android_resources(self):
        try:
            return self.arsc["resources.arsc"]
        except KeyError:
            try:
                self.arsc["resources.arsc"] = ARSCParser(self.zip.read("resources.arsc"))
                return self.arsc["resources.arsc"]
            except KeyError:
                return None

    def get_app_name(self):
        return self.app_name

    def _get_app_name(self):
        app = self.get_android_manifest_xml().getElementsByTagName("application")[0]
        name = app.getAttribute("android:label")
        if name.startswith("@"):
            try:
                package_parser = self.get_android_resources()
                name = ''
                for package_name in package_parser.get_packages_names():
                    name = package_parser.get_string(package_name, 'app_name')
                    if name:
                        name = name[1]
                        break
            except:
                self.valid_apk = False
                logging.error("Ignoring '%s', exception creating APK instance" % (self.filename))
        if name == '' or name == None:
            name = 'None'
        return name

    def get_elements(self, tag_name, attribute):
        l = []
        for i in self.xml:
            for item in self.xml[i].getElementsByTagName(tag_name):
                value = item.getAttribute(attribute)
                value = self.format_value(value)
                l.append(str(value))
        return l

    def format_value(self, value):
        if len(value) > 0:
            if value[0] == ".":
                value = self.package + value
            else:
                v_dot = value.find(".")
                if v_dot == 0:
                    value = self.package + "." + value
                elif v_dot == -1:
                    value = self.package + "." + value
        return value

    def get_element(self, tag_name, attribute):
        for i in self.xml:
            for item in self.xml[i].getElementsByTagName(tag_name):
                value = item.getAttribute(attribute)
                if len(value) > 0:
                    return value
        return None

    def get_main_activity(self):
        x = set()
        y = set()

        for i in self.xml:
            for item in self.xml[i].getElementsByTagName("activity"):
                for sitem in item.getElementsByTagName("action"):
                    val = sitem.getAttribute("android:name")
                    if val == "android.intent.action.MAIN":
                        x.add(item.getAttribute("android:name"))

                for sitem in item.getElementsByTagName("category"):
                    val = sitem.getAttribute("android:name")
                    if val == "android.intent.category.LAUNCHER":
                        y.add(item.getAttribute("android:name"))
        z = x.intersection(y)
        if len(z) > 0:
            return self.format_value(z.pop())
        return ''

    def get_activities(self):
        activities_list = ''
        activities = list(set(self.get_elements("activity", "android:name")))
        for i in sorted(activities):
            if len(activities) == 1 or i == activities[len(activities) - 1]:
                activities_list += i
            else:
                activities_list += i + '|'
        if len(activities) == 0:
            activities_list = 'None'
        return activities_list

    def get_services(self):
        services_list = ''
        services = list(set(self.get_elements("service", "android:name")))
        for i in sorted(services):
            if len(services) == 1 or i == services[len(services) - 1]:
                services_list += i
            else:
                services_list += i + '|'
        if len(services) == 0:
            services_list = 'None'
        return services_list

    def get_receivers(self):
        receivers_list = ''
        receivers = list(set(self.get_elements("receiver", "android:name")))
        for i in sorted(receivers):
            if len(receivers) == 1 or i == receivers[len(receivers) - 1]:
                receivers_list += i
            else:
                receivers_list += i + '|'
        if len(receivers) == 0:
            receivers_list = 'None'
        return receivers_list

    def get_providers(self):
        providers_list = ''
        providers = list(set(self.get_elements("provider", "android:name")))
        for i in sorted(providers):
            if len(providers) == 1 or i == providers[len(providers) - 1]:
                providers_list += i
            else:
                providers_list += i + '|'
        if len(providers) == 0:
            providers_list = 'None'
        return providers_list

    def get_intent_filters(self, category, name):
        d = {}

        d["action"] = []
        d["category"] = []

        for i in self.xml:
            for item in self.xml[i].getElementsByTagName(category):
                if self.format_value(item.getAttribute("android:name")) == name:
                    for sitem in item.getElementsByTagName("intent-filter"):
                        for ssitem in sitem.getElementsByTagName("action"):
                            if ssitem.getAttribute("android:name") not in d["action"]:
                                d["action"].append(ssitem.getAttribute("android:name"))
                        for ssitem in sitem.getElementsByTagName("category"):
                            if ssitem.getAttribute("android:name") not in d["category"]:
                                d["category"].append(ssitem.getAttribute("android:name"))

        if not d["action"]:
            del d["action"]

        if not d["category"]:
            del d["category"]

        return d

    def get_permissions(self):
        permissions_list = ''
        permissions = list(set(self.permissions))
        for i in sorted(permissions):
            if len(permissions) == 1 or i == permissions[len(permissions) - 1]:
                permissions_list += i
            else:
                permissions_list += i + '|'
        if len(permissions) == 0:
            permissions_list = 'None'
        return permissions_list

    def get_max_sdk_version(self):
        max_sdk_version = self.get_element("uses-sdk", "android:maxSdkVersion")
        if max_sdk_version == None:
            max_sdk_version = 'None'
        return max_sdk_version

    def get_min_sdk_version(self):
        min_sdk_version = self.get_element("uses-sdk", "android:minSdkVersion")
        if min_sdk_version == None:
            min_sdk_version = 'None'
        return min_sdk_version

    def get_target_sdk_version(self):
        target_sdk_version = self.get_element("uses-sdk", "android:targetSdkVersion")
        if target_sdk_version == None:
            target_sdk_version = 'None'
        return target_sdk_version

    def get_libraries(self):
        libraries_list = ''
        libraries = list(set(self.get_elements("uses-library", "android:name")))
        for i in sorted(libraries):
            if len(libraries) == 1 or i == libraries[len(libraries) - 1]:
                libraries_list += i
            else:
                libraries_list += i + '|'
        if len(libraries) == 0:
            libraries_list = 'None'
        return libraries_list

    def get_android_manifest_axml(self):
        try:
            return self.axml["AndroidManifest.xml"]
        except KeyError:
            return None

    def get_android_manifest_xml(self):
        try:
            return self.xml["AndroidManifest.xml"]
        except KeyError:
            return None

    def get_certificate(self, filename):
        cert = chilkat.CkCert()
        try:
            f = self.get_file(filename)
            data = chilkat.CkByteData()
            data.append2(f, len(f))
            success = cert.LoadFromBinary(data)
            if success == False:
                cert = None
        except:
            self.valid_apk = False
            success = False
            cert = None
            logging.error("Ignoring '%s', exception extracting certificate" % (filename))
        return success, cert

    def get_signature_name(self):
        signature_expr = re.compile("^(META-INF/)(.*)(\.RSA)$")
        for i in self.get_files():
            if signature_expr.search(i):
                return i
        return None

    def get_signature(self):
        signature_expr = re.compile("^(META-INF/)(.*)(\.RSA)$")
        for i in self.get_files():
            if signature_expr.search(i):
                return self.get_file(i)
        return None

    def get_serial_number(self):
        serial_number = 'None'
        signature_name = self.get_signature_name()
        success, cert = self.get_certificate(signature_name)
        if success == True:
            serial_number = cert.serialNumber()
        return serial_number

    def get_fingerprint_sha1(self):
        sha1_thumbprint = 'None'
        signature_name = self.get_signature_name()
        success, cert = self.get_certificate(signature_name)
        if success == True:
            sha1_thumbprint = cert.sha1Thumbprint()
        return sha1_thumbprint

    def get_certificate_data(self):
        signature_name = self.get_signature_name()
        success, cert = self.get_certificate(signature_name)
        if success == True:
            issuer = self.get_certificate_issuer(cert)
            subject = self.get_certificate_subject(cert)
        else:
            issuer = "Issuer: None"
            subject = "Subject: None"
        return issuer, subject

    def get_certificate_issuer(self, cert):
        issuer = "Issuer: C=%s, CN=%s, DN=%s, E=%s, L=%s, O=%s, OU=%s, S=%s" % (
            cert.issuerC().decode('latin-1'), cert.issuerCN().decode('latin-1'), cert.issuerDN().decode('latin-1'),
            cert.issuerE().decode('latin-1'), cert.issuerL().decode('latin-1'), cert.issuerO().decode('latin-1'),
            cert.issuerOU().decode('latin-1'), cert.issuerS().decode('latin-1'))
        return issuer

    def get_certificate_subject(self, cert):
        subject = "Subject: C=%s, CN=%s, DN=%s, E=%s, L=%s, O=%s, OU=%s, S=%s" % (
            cert.subjectC().decode('latin-1'), cert.subjectCN().decode('latin-1'), cert.subjectDN().decode('latin-1'),
            cert.subjectE().decode('latin-1'), cert.subjectL().decode('latin-1'), cert.subjectO().decode('latin-1'),
            cert.subjectOU().decode('latin-1'), cert.subjectS().decode('latin-1'))
        return subject