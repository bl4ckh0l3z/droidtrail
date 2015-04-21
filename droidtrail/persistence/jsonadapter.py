#coding:utf-8;
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
import json
import logging

class JSONAdapter():

    TRAILS_NAME = 'trails_list.json'
    FINGERPRINTS_NAME = 'fingerprints_list.json'
    config = ''

    @staticmethod
    def save_trails(trails_list):
        logging.debug("JSONAdapter is storing trails...")
        JSONAdapter._clear_trails()
        try:
            file_trails_name = os.path.join(JSONAdapter.config['dir_out'], JSONAdapter.TRAILS_NAME)
            file_trails = open(file_trails_name, 'w')
            file_trails.write('{"trails": [')
            for i in range(len(trails_list)):
                trails = trails_list[i]
                if i != len(trails_list)-1:
                    file_trails.write(json.dumps(trails) + ',')
                else:
                    file_trails.write(json.dumps(trails))
            file_trails.write(']}')
            file_trails.close()
        except OSError, e:
            logging.error("Error saving trails in json format: %s" % (e))
            raise OSError

    @staticmethod
    def save_fingerprints(fingerprints_list):
        logging.debug("JSONAdapter is storing fingerprints...")
        JSONAdapter._clear_fingerprints()
        try:
            file_fingerprints_name = os.path.join(JSONAdapter.config['dir_out'], JSONAdapter.FINGERPRINTS_NAME)
            file_fingerprints = open(file_fingerprints_name, 'w')
            file_fingerprints.write('{"fingerprints": [')
            for i in range(len(fingerprints_list)):
                fingerprint = fingerprints_list[i]
                if i != len(fingerprints_list)-1:
                    file_fingerprints.write(json.dumps(fingerprint) + ',')
                else:
                    file_fingerprints.write(json.dumps(fingerprint))
            file_fingerprints.write(']}')
            file_fingerprints.close()
        except OSError, e:
            logging.error("Error saving fingerprints in json format: %s" % (e))
            raise OSError

    @staticmethod
    def _clear_trails():
        try:
            if os.path.exists(os.path.join(JSONAdapter.config['dir_out'], JSONAdapter.TRAILS_NAME)):
                os.remove(os.path.join(JSONAdapter.config['dir_out'], JSONAdapter.TRAILS_NAME))
        except OSError, e:
            logging.error("Error removing file '%s': %s" % (os.path.join(JSONAdapter.config['dir_out'], JSONAdapter.TRAILS_NAME), e))
            raise OSError

    @staticmethod
    def _clear_fingerprints():
        try:
            if os.path.exists(os.path.join(JSONAdapter.config['dir_out'], JSONAdapter.FINGERPRINTS_NAME)):
                os.remove(os.path.join(JSONAdapter.config['dir_out'], JSONAdapter.FINGERPRINTS_NAME))
        except OSError, e:
            logging.error("Error removing file '%s': %s" % (os.path.join(JSONAdapter.config['dir_out'], JSONAdapter.FINGERPRINTS_NAME), e))
            raise OSError