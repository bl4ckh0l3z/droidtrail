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

    @staticmethod
    def run():
        config = configparser.ConfigParser()
        config.read(ConfigReader.CONFIG_FILE)
        cfg = dict()
        
        if not config.has_option('DroidTrail', 'dir_in') \
                or not config.has_option('DroidTrail', 'dir_out') \
                or not config.has_option('DroidTrail', 'white_list_arch_ext'):
            print("\n### ERROR ### Config element are not defined in the config file\n")
            exit()
        else:
            ### parse the config file
            logging.debug("Loading config from '%s'" % (ConfigReader.CONFIG_FILE))

            ### parse dir_in config
            cfg['dir_in'] = config.get('DroidTrail', 'dir_in')
            logging.debug("Setting '%s' as input dir" % (cfg['dir_in']))

            ### parse dir_out config
            cfg['dir_out'] = config.get('DroidTrail', 'dir_out')
            logging.debug("Setting '%s' as output dir" % (cfg['dir_out']))

            ### parse white_list_arch_ext config
            cfg['white_list_arch_ext'] = config.get('DroidTrail', 'white_list_arch_ext').split(',')
            logging.debug("Setting '%s' as white listed archive extensions" % (cfg['white_list_arch_ext']))

            ### parse white_list app
            if config.has_option('DroidTrail', 'white_list'):
                cfg['white_list'] = config.get('DroidTrail', 'white_list').split(',')
                logging.debug("Setting '%s' as white listed apps" % (cfg['white_list']))
            else:
                logging.debug("White list is not defined")

            ### parse black_list app
            if config.has_option('DroidTrail', 'black_list'):
                cfg['black_list'] = config.get('DroidTrail', 'black_list').split(',')
                logging.debug("Setting '%s' as black listed apps" % (cfg['black_list']))
            else:
                logging.debug("Black list is not defined")

            ### parse passwords config
            if config.has_option('DroidTrail', 'passwords'):
                cfg['passwords'] = config.get('DroidTrail', 'passwords').split(',')
                logging.debug("Setting '%s' as passwords list" % (cfg['passwords']))
            else:
                logging.debug("Passwords field is not defined")

            ### parse proxy config
            if config.has_option('DroidTrail', 'proxy'):
                cfg['proxy'] = config.get('DroidTrail', 'proxy')
                logging.debug("Setting '%s' as proxy" % (cfg['proxy']))
            else:
                logging.debug("Proxy is not defined")

            logging.debug("######## done")
        return cfg