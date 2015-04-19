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

__author__ = 'bl4ckh0l3'
__license__ = 'GPL v2'
__maintainer__ = 'bl4ckh0l3'
__email__ = 'bl4ckh0l3z@gmail.com'

import os
import logging
from androguard.apk import APK

import sys
sys.path.append('../../')
from utils.utils import Utils

class TrailsDumper():

    def __init__(self, config):
        logging.debug("Instantiating the '%s' class" % (self.__class__.__name__))
        self._cfg = config

    def run(self):
        logging.debug("Dumping trails...")
        trails_list = []
        try:
            for root, dirs, files in os.walk(self._cfg['dir_out']):
                for file in files:
                    if Utils.is_apk(root, file):
                        apk_file = APK(root, file)
                        trails = self._dump_trails(apk_file)
                        if len(trails) > 0:
                            trails_list.append(trails)
                        else:
                            logging.error("Empty dict for '%s'" % (os.path.join(root, file)))
                    else:
                        logging.error("Unsupported file type '%s' for '%s'" % (
                            os.path.splitext(file)[1], os.path.join(root, file)))
        except OSError, e:
            logging.error("Error dumping trails: %s" % (e))
            raise OSError
        return trails_list

    def _dump_trails(self, apk_file):
        logging.debug("Dumping trails from '%s'" % (apk_file.get_filename()))
        trails = dict()
        trails['app_trails'] = self._dump_app_trails(apk_file)
        trails['file_trails'] = self._dump_file_trails(apk_file)
        trails['cert_trails'] = self._dump_cert_trails(apk_file)
        return trails

    def _dump_app_trails(self, apk_file):
        logging.debug("Dumping app_trails")
        app_trails = dict()
        app_trails['app_name'] = apk_file.get_app_name()
        app_trails['app_version'] = apk_file.get_androidversion_name()
        app_trails['app_package_name'] = apk_file.get_package()
        app_trails['app_main_activity_name'] = apk_file.get_main_activity()
        app_trails['app_activities_names'] = apk_file.get_activities()
        app_trails['apps_services_names'] = apk_file.get_services()
        app_trails['apps_receivers_names'] = apk_file.get_receivers()
        app_trails['apps_libraries_names'] = apk_file.get_libraries()
        app_trails['app_permissions'] = apk_file.get_permissions()
        app_trails['app_min_sdk'] = apk_file.get_min_sdk_version()
        app_trails['app_max_sdk'] = apk_file.get_max_sdk_version()
        app_trails['app_target_sdk'] = apk_file.get_target_sdk_version()
        return app_trails

    def _dump_file_trails(self, apk_file):
        logging.debug("Dumping file_trails")
        path = apk_file.get_path()
        file = apk_file.get_filename()
        file_trails = dict()
        file_trails['file_name'] = file
        file_trails['file_md5_sum'] = Utils.compute_md5(path, file)
        file_trails['file_sha256_sum'] = Utils.compute_sha256(path, file)
        file_trails['file_dimension'] = Utils.get_size(path, file)
        return file_trails

    def _dump_cert_trails(self, apk_file):
        logging.debug("Dumping cert_trails")
        cert_trails = dict()
        issuer, subject = apk_file.get_certificate_data()
        cert_trails['cert_subject'] = subject
        cert_trails['cert_issuer'] = issuer
        cert_trails['cert_serial_number'] = apk_file.get_serial_number()
        cert_trails['cert_finger_md5'] = apk_file.get_fingerprint_md5()
        cert_trails['cert_finger_sha1'] = apk_file.get_fingerprint_sha1()
        return cert_trails