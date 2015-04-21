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

class CSVAdapter():

    TRAILS_NAME = 'trails_list.csv'
    FINGERPRINTS_NAME = 'fingerprints_list.csv'
    config = ''

    @staticmethod
    def save_trails(trails_list):
        logging.debug("CSVAdapter is storing trails...")
        CSVAdapter._clear_trails()
        try:
            file_trails_name = os.path.join(CSVAdapter.config['dir_out'], CSVAdapter.TRAILS_NAME)
            file_trails = open(file_trails_name, 'w')
            for i in range(len(trails_list)):
                trails = trails_list[i]
                trails_elem_string = ''
                for trails_index in trails:
                    for trails_elem in trails[trails_index]:
                        trails_elem_string += str((trails[trails_index])[trails_elem]) + ','
                trails_elem_string = trails_elem_string[:-1]
                file_trails.write(trails_elem_string + '\n')
            file_trails.close()
        except OSError, e:
            logging.error("Error saving trails in csv format: %s" % (e))
            raise OSError

    @staticmethod
    def save_fingerprints(fingerprints_list):
        logging.debug("CSVAdapter is storing fingerprints...")
        CSVAdapter._clear_fingerprints()
        try:
            file_fingerprints_name = os.path.join(CSVAdapter.config['dir_out'], CSVAdapter.FINGERPRINTS_NAME)
            file_fingerprints = open(file_fingerprints_name, 'w')
            for i in range(len(fingerprints_list)):
                fingerprint = fingerprints_list[i]
                fing_elem_string = ''
                for fing_elem in fingerprint:
                    fing_elem_string += fingerprint[fing_elem] + ','
                fing_elem_string = fing_elem_string[:-1]
                file_fingerprints.write(fing_elem_string + '\n')
            file_fingerprints.close()
        except OSError, e:
            logging.error("Error saving fingerprints in csv format: %s" % (e))
            raise OSError

    @staticmethod
    def _clear_trails():
        try:
            if os.path.exists(os.path.join(CSVAdapter.config['dir_out'], CSVAdapter.TRAILS_NAME)):
                os.remove(os.path.join(CSVAdapter.config['dir_out'], CSVAdapter.TRAILS_NAME))
        except OSError, e:
            logging.error("Error removing file '%s': %s" % (os.path.join(CSVAdapter.config['dir_out'], CSVAdapter.TRAILS_NAME), e))
            raise OSError

    @staticmethod
    def _clear_fingerprints():
        try:
            if os.path.exists(os.path.join(CSVAdapter.config['dir_out'], CSVAdapter.FINGERPRINTS_NAME)):
                os.remove(os.path.join(CSVAdapter.config['dir_out'], CSVAdapter.FINGERPRINTS_NAME))
        except OSError, e:
            logging.error("Error removing file '%s': %s" % (os.path.join(CSVAdapter.config['dir_out'], CSVAdapter.FINGERPRINTS_NAME), e))
            raise OSError