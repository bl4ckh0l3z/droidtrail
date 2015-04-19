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
from config.configreader import ConfigReader
from dependencies.checkdependencies import CheckDependencies
from extract.extractor import FileExtractor
from fingerprint.fingerprintmaker import FingerprintMaker
from trails.trailsdumper import TrailsDumper
from utils.utils import Utils


class Core:
    def __init__(self):
        logging.debug("Instantiating the '%s' class" % (self.__class__.__name__))
        utils = Utils()
        check_dependecies = CheckDependencies()
        check_passed = check_dependecies.run()
        if not check_passed:
            exit()
        else:
            config_reader = ConfigReader()
            self._cfg = config_reader.run()
            self._extractor = FileExtractor(self._cfg, utils)
            self._trails_dumper = TrailsDumper(self._cfg, utils)
            self._fingerprint_maker = FingerprintMaker(self._cfg, utils)

    def run(self):
        print("Running...")
        self._extractor.run()
        trails_list = self._trails_dumper.run()
        if len(trails_list) > 0:
            #TODO: save trails_list to files
            fingerprints_list = self._fingerprint_maker.run(trails_list)
            if len(fingerprints_list) > 0:
                pass
                #TODO: save fingerprint_list to files
            else:
                logging.debug('Empty fingerprint_list')
        else:
            logging.debug('Empty trails_list')
        print("Done...")


if __name__ == "__main__":
    log_file = './logs/droidtrail.log'
    logging.basicConfig(filename=log_file,
                        level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%d-%m-%Y %H:%M')
    logging.debug("Setting '%s' as log file" % (log_file))

    logging.debug('#####################################')
    logging.debug('#####    Starting DroidTrail    #####')
    logging.debug('#####################################')
    core = Core()
    core.run()