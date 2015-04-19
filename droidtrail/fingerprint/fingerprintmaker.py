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

class FingerprintMaker():

    def __init__(self, config, utils):
        logging.debug("Instantiating the '%s' class" % (self.__class__.__name__))
        self._cfg = config
        self._utils = utils

    def run(self, trails_list):
        logging.debug("Extracting fingerprints...")
        try:
            for root, dirs, files in os.walk(self._cfg['dir_out']):
                for file in files:
                    if self._utils.is_apk(root, file):
                        self._extract_fingerprint(root, file)
                    else:
                        logging.error("Unsupported file type '%s' for '%s'" % (os.path.splitext(file)[1], os.path.join(root, file)))
        except OSError, e:
            logging.error("Error extracting fingerprints: %s" % (e))
            raise OSError

    def _extract_fingerprint(self, path_in, file):
        logging.debug("Extract fingerprint from '%s'" % (os.path.join(path_in, file)))
        #TODO: t.b.d.