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

__author__ = 'bl4ckh0l3z'
__license__ = 'GPL v2'
__maintainer__ = 'bl4ckh0l3z'
__email__ = 'bl4ckh0l3z@gmail.com'

import os
import sys
import logging
import subprocess
import configparser

class CheckDependencies():

    DEPENDENCIES_FILE = './droidtrail/dependencies/dependencies.cfg'

    def __init__(self):
        logging.debug("Instantiating the '%s' class" % (self.__class__.__name__))
        self._config = configparser.ConfigParser()
        self._config.read(self.__class__.DEPENDENCIES_FILE)

    def run(self):
        check_passed = None
        logging.debug("Check dependencies...")
        print("Check dependencies...")
        if not self._python_version_check() or \
                not self._python_modules_check() or \
                not self._external_tools_check():
            check_passed = False
            logging.error("Check dependencies failed")
            print("Check dependencies failed")
        else:
            check_passed = True
            logging.info("Check dependencies passed")
            print("Check dependencies passed")
        return check_passed

    # Python version check (anyway there is dedicated virtualenv)
    def _python_version_check(self):
        exit_status = None
        if not self._config.has_option('DroidTrail', 'python_version_major') \
                or not self._config.has_option('DroidTrail', 'python_version_minor'):
            logging.error("No config values for 'python_version_major' and/or 'python_version_minor'")
            exit_status = False
        else:
            py_major, py_minor = sys.version_info[:2]
            py_version = sys.version.split()[0]
            if py_major != int(self._config.get('DroidTrail', 'python_version_major')) and \
                    py_minor != int(self._config.get('DroidTrail', 'python_version_minor')):
                logging.error("You are using python %s, but version 2.7 is required" % (py_version))
                exit_status = False
            else:
                exit_status = True
        return exit_status

    # Python modules check (anyway there is dedicated virtualenv)
    def _python_modules_check(self):
        exit_status = 0
        if not self._config.has_option('DroidTrail', 'python_modules'):
            logging.error("No config value for 'python_modules'")
            exit_status = 1
        else:
            modules = self._config.get('DroidTrail', 'python_modules').split(',')
            for module in modules:
                try:
                    __import__(module)
                except ImportError:
                    logging.error("No module '%s'" % (module))
                    exit_status += 1
        if exit_status > 0:
            exit_status = False
        else:
            exit_status = True
        return exit_status

    # External tools check
    def _external_tools_check(self):
        exit_status = 0
        if not self._config.has_option('DroidTrail', 'ext_tools'):
            logging.error("No config value for 'ext_tools'")
            exit_status = 1
        else:
            ext_tools = self._config.get('DroidTrail', 'ext_tools').split(',')
            dev_null = open(os.devnull, 'w')
            for ext_tool in ext_tools:
                try:
                    subprocess.call(ext_tool, stdout=dev_null, stderr=dev_null)
                except OSError:
                    logging.error("No '%s' tool" % (ext_tool))
                    exit_status += 1
        if exit_status > 0:
            exit_status = False
        else:
            exit_status = True
        return exit_status