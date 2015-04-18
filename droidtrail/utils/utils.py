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
import hashlib
import logging
import zipfile
import rarfile
import tarfile

class Utils():

    def __init__(self):
        logging.debug("Instantiating the '%s' class" % (self.__class__.__name__))

    def is_apk(self, path, file):
        try:
            f = open(os.path.join(path, file), 'r')
            val = f.read()
            if 'PK' in val[0:100] and 'AndroidManifest.xml' in val \
                    and 'META-INF/MANIFEST.MF' in val:
                return True
        except OSError, e:
            logging.error("Error in is_apk for '%s': %s" % (file, e))
            raise OSError
        return False

    def is_axml(self, path, file):
        try:
            f = open(os.path.join(path, file), 'r')
            val = f.read(7)
            if val[0:4] == "\x03\x00\x08\x00":
                return True
        except OSError, e:
            logging.error("Error in is_axml for '%s': %s" % (file, e))
            raise OSError
        return False

    def is_zip(self, path, file):
        try:
            if zipfile.is_zipfile(os.path.join(path, file)) and \
                    (os.path.splitext(file)[1] == '.zip' or \
                             os.path.splitext(file)[1] == '.7z'):
                return True
        except OSError, e:
            logging.error("Error in is_zip for '%s': %s" % (file, e))
            raise OSError
        return False

    def extract_zip(self, path, file, path_out, password):
        # FIXME: for the future please use zipfile.extract(...), but at this time it gives 'Bad password' for some zip file
        try:
            if password is None:
                password = ''
            exit_status = os.system('7z x "%s" -y -p"%s" -o"%s" > /dev/null' % (os.path.join(path, file), password, path_out))
            if exit_status != 0:
                raise OSError
        except OSError, e:
            logging.error("Error extracting file '%s': %s" % (os.path.join(path, file), e))
            raise OSError

    def is_rar(self, path, file):
        try:
            if rarfile.is_rarfile(os.path.join(path, file)):
                return True
        except OSError, e:
            logging.error("Error in is_rar for '%s': %s" % (file, e))
            raise OSError
        return False

    def extract_rar(self, path, file, path_out, password):
        try:
            rar = rarfile.RarFile(os.path.join(path, file))
            rar.extractall(path_out, None, password)
            rar.close()
        except rarfile.Error, e:
            logging.error("Error extracting file '%s': %s" % (os.path.join(path, file), e))
            raise OSError

    def is_tar(self, path, file):
        try:
            if tarfile.is_tarfile(os.path.join(path, file)):
                return True
        except OSError, e:
            logging.error("Error in is_tar for '%s': %s" % (file, e))
            raise OSError
        return False

    def extract_tar(self, path, file, path_out):
        try:
            tar = tarfile.open(os.path.join(path, file))
            tar.extractall(path_out)
            tar.close
        except tarfile.TarError, e:
            logging.error("Error extracting file '%s': %s" % (os.path.join(path, file), e))
            raise OSError

    def compute_md5(self, path, file):
        try:
            md5 = hashlib.md5(open(os.path.join(path, file), 'rb').read()).hexdigest()
        except OSError, e:
            logging.error("Error computing md5 of '%s': %s" % (file, e))
            raise OSError
        return md5

    def compute_sha256(self, path, file):
        try:
            sha256 = hashlib.sha256(open(os.path.join(path, file), 'rb').read()).hexdigest()
        except OSError, e:
            logging.error("Error computing sha256 of '%s': %s" % (file, e))
            raise OSError
        return sha256

    def get_size(self, path, file):
        size = os.path.getsize(os.path.join(path, file))
        return size

    def compute_dir_size(self, dir):
        try:
            size = os.path.getsize(dir)
            for item in os.listdir(dir):
                item_path = os.path.join(dir, item)
                if os.path.isfile(item_path):
                    size += os.path.getsize(item_path)
                elif os.path.isdir(item_path):
                    size += self.compute_dir_size(item_path)
        except OSError, e:
            logging.error("Error computing dir size of '%s': %s" % (dir, e))
            raise OSError
        return size

    def compute_file_number(self, dir):
        file_number = 0
        try:
            for item in os.listdir(dir):
                item_path = os.path.join(dir, item)
                if os.path.isfile(item_path):
                    file_number += 1
                elif os.path.isdir(item_path):
                    file_number += self.compute_file_number(item_path)
        except OSError, e:
            logging.error("Error computing file number in '%s': %s" % (dir, e))
            raise OSError
        return file_number

    def complex_to_float(self, complex_value):
        RADIX_MULTS = [0.00390625, 3.051758E-005, 1.192093E-007, 4.656613E-010]
        float_value = float(complex_value & 0xFFFFFF00) * RADIX_MULTS[(complex_value >> 4) & 3]
        return float_value

    def long_to_int(self, long_value):
        if long_value > 0x7fffffff:
            long_value = (0x7fffffff & long_value) - 0x80000000
        return long_value