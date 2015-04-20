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
import shutil
import logging
from utils.utils import Utils

class FileExtractor():
    def __init__(self, config):
        logging.debug("Instantiating the '%s' class" % (self.__class__.__name__))
        self._cfg = config

    def run(self):
        logging.debug("Extracting files...")
        while Utils.compute_file_number(self._cfg['dir_in']) > 0:
            self._walk_dir(self._cfg['dir_in'], self._cfg['dir_out'])
        self._remove_dir_content(self._cfg['dir_in'])

    def _walk_dir(self, dir, path_out):
        try:
            for root, dirs, files in os.walk(dir):
                for file in files:
                    file.replace('$', '\$')

                    if Utils.is_zip(root, file) or \
                            Utils.is_rar(root, file) or \
                            Utils.is_tar(root, file):
                        self._extract_file(root, file)
                        self._remove_file(root, file)
                    else:
                        if Utils.is_apk(root, file):
                            self._rename_file(root, path_out, file)
                        else:
                            self._remove_file(root, file)
        except OSError, e:
            logging.error("Error walking dir '%s': %s" % (dir, e))
            raise OSError

    def _extract_file(self, path_in, file):
        logging.debug("Extracting file '%s'" % (os.path.join(path_in, file)))

        exit_status = False
        for password in self._cfg['passwords']:
            if not exit_status:
                if password == 'None':
                    password = None
                    exit_status = self._extract(path_in, file, password)
                elif password[-1] == '*':
                    password = password[:-1] + os.path.splitext(file)[0][-1]
                    exit_status = self._extract(path_in, file, password)
                else:
                    exit_status = self._extract(path_in, file, password)

    def _extract(self, path_in, file, password):
        try:
            if Utils.is_zip(path_in, file):
                Utils.extract_zip(path_in, file, path_in, password)
            elif Utils.is_rar(path_in, file):
                Utils.extract_rar(path_in, file, path_in, password)
            elif Utils.is_tar(path_in, file):
                Utils.extract_tar(path_in, file, path_in)
        except OSError, e:
            return False
        return True

    def _rename_file(self, path_in, path_out, file):
        logging.debug("Renaming file '%s'" % (os.path.join(path_in, file)))
        md5 = Utils.compute_md5_file(path_in, file)
        ext = os.path.splitext(file)[1]
        if ext != '.apk':
            ext = '.apk'
        file_new = md5 + ext

        try:
            os.rename(os.path.join(path_in, file).encode('utf-8').strip(),
                os.path.join(path_out, file_new).encode('utf-8').strip())
        except OSError, e:
            logging.error("Error renaming file '%s': %s" % (os.path.join(path_in, file), e))
            raise OSError

    def _remove_file(self, path_in, file):
        logging.debug("Removing file '%s'" % (os.path.join(path_in, file)))
        try:
            os.remove(os.path.join(path_in, file).encode('utf-8').strip())
        except OSError, e:
            logging.error("Error removing file '%s': %s" % (os.path.join(path_in, file), e))
            raise OSError

    def _remove_dir_content(self, dir):
        logging.debug("Removing dir '%s' content" % (dir))
        try:
            for elem in os.listdir(dir):
                elem_path = os.path.join(dir, elem)
                if os.path.isdir(elem_path):
                    shutil.rmtree(elem_path)
        except OSError, e:
            logging.error("Error removing dir '%s' content: %s" % (dir, e))
            raise OSError