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

import logging
import configparser

class ConfigReader():

    CONFIG_FILE = './droidtrail/config/droidtrail.cfg'

    def __init__(self):
        global CONFIG_FILE
        logging.debug("Instantiating the '%s' class" % (self.__class__.__name__))
        self._config = configparser.ConfigParser()
        self._config.read(self.__class__.CONFIG_FILE)
        self._cfg = dict()

    def run(self):
        if not self._config.has_option('DroidTrail', 'dir_in') \
                or not self._config.has_option('DroidTrail', 'dir_out') \
                or not self._config.has_option('DroidTrail', 'white_list_arch_ext'):
            print("\n### ERROR ### Config element are not defined in the config file\n")
            exit()
        else:
            ### parse the config file
            logging.debug("Loading config from '%s'" % (self.__class__.CONFIG_FILE))

            ### parse dir_in config
            self._cfg['dir_in'] = self._config.get('DroidTrail', 'dir_in')
            logging.debug("Setting '%s' as input dir" % (self._cfg['dir_in']))

            ### parse dir_out config
            self._cfg['dir_out'] = self._config.get('DroidTrail', 'dir_out')
            logging.debug("Setting '%s' as output dir" % (self._cfg['dir_out']))

            ### parse white_list_arch_ext config
            self._cfg['white_list_arch_ext'] = self._config.get('DroidTrail', 'white_list_arch_ext').split(',')
            logging.debug("Setting '%s' as white listed archive extensions" % (self._cfg['white_list_arch_ext']))

            ### parse white_list app
            if self._config.has_option('DroidTrail', 'white_list'):
                self._cfg['white_list'] = self._config.get('DroidTrail', 'white_list').split(',')
                logging.debug("Setting '%s' as white listed apps" % (self._cfg['white_list']))
            else:
                logging.debug("White list is not defined")

            ### parse black_list app
            if self._config.has_option('DroidTrail', 'black_list'):
                self._cfg['black_list'] = self._config.get('DroidTrail', 'black_list').split(',')
                logging.debug("Setting '%s' as black listed apps" % (self._cfg['black_list']))
            else:
                logging.debug("Black list is not defined")

            ### parse passwords config
            if self._config.has_option('DroidTrail', 'passwords'):
                self._cfg['passwords'] = self._config.get('DroidTrail', 'passwords').split(',')
                logging.debug("Setting '%s' as passwords list" % (self._cfg['passwords']))
            else:
                logging.debug("Passwords field is not defined")

            ### parse proxy config
            if self._config.has_option('DroidTrail', 'proxy'):
                self._cfg['proxy'] = self._config.get('DroidTrail', 'proxy')
                logging.debug("Setting '%s' as proxy" % (self._cfg['proxy']))
            else:
                logging.debug("Proxy is not defined")

            logging.debug("######## done")
        return self._cfg