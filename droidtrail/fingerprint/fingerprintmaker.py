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
from utils.utils import Utils


class FingerprintMaker():
    def __init__(self, config):
        logging.debug("Instantiating the '%s' class" % (self.__class__.__name__))
        self._cfg = config

    def run(self, trails_list, mode='long'):
        logging.debug("Extracting fingerprints...")
        fingerprints_list = []
        for trails in trails_list:
            fingerprint = self._extract_fingerprint(trails, mode)
            if len(fingerprint) > 0 and fingerprint not in fingerprints_list:
                fingerprints_list.append(fingerprint)
            else:
                logging.error("Empty dict")
        return fingerprints_list

    def _extract_fingerprint(self, trails, mode):
        app_trails = trails['app_trails']
        logging.debug("Extracting fingerprint for '%s'" % (app_trails['app_name']))
        fingerprint = dict()
        fingerprint['index'] = Utils.compute_md5_value(app_trails['app_package_name'])
        elem = app_trails['app_name'] + ',' + app_trails['app_version'] + ',' + \
               app_trails['app_package_name'] + ',' + app_trails['app_permissions']
        if mode == 'long':
            elem += app_trails['app_activities_names'] + ',' + \
                    app_trails['app_services_names'] + ',' + \
                    app_trails['app_receivers_names']
        fingerprint['elem'] = Utils.compute_sha256_value(elem.encode('utf-8'))
        return fingerprint