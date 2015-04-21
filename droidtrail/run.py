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

import sys
import getopt
import logging
from config.configreader import ConfigReader
from dependencies.checkdependencies import CheckDependencies
from extract.extractor import FileExtractor
from fingerprint.fingerprintmaker import FingerprintMaker
from trails.trailsdumper import TrailsDumper
from persistence.jsonadapter import JSONAdapter
from persistence.csvadapter import CSVAdapter
from persistence.xmladapter import XMLAdapter

class Core:

    def __init__(self, trails, fingerprints, mode, output):
        logging.debug("Instantiating the '%s' class" % (self.__class__.__name__))

        self._trails = trails
        self._fingerprints = fingerprints
        self._mode = mode
        self._output = output

        check_passed = CheckDependencies.run()
        if not check_passed:
            exit()
        else:
            self._cfg = ConfigReader.run()
            self._extractor = FileExtractor(self._cfg)
            if self._trails:
                self._trails_dumper = TrailsDumper(self._cfg)
            if self._fingerprints:
                self._fingerprint_maker = FingerprintMaker(self._cfg)
            if 'json' in self._output:
                JSONAdapter.config = self._cfg
            if 'csv' in self._output:
                CSVAdapter.config = self._cfg
            if 'xml' in self._output:
                XMLAdapter.config = self._cfg

    def run(self):
        print("Running...")
        self._extractor.run()
        trails_list = self._trails_dumper.run(self._mode)
        if len(trails_list) > 0:
            if 'json' in self._output:
                JSONAdapter.save_trails(trails_list)
            if 'csv' in self._output:
                CSVAdapter.save_trails(trails_list)
            if 'xml' in self._output:
                XMLAdapter.save_trails(trails_list)
            fingerprints_list = self._fingerprint_maker.run(trails_list, self._mode)
            if len(fingerprints_list) > 0:
                if 'json' in self._output:
                    JSONAdapter.save_fingerprints(fingerprints_list)
                if 'csv' in self._output:
                    CSVAdapter.save_fingerprints(fingerprints_list)
                if 'xml' in self._output:
                    XMLAdapter.save_fingerprints(fingerprints_list)
            else:
                logging.debug('Empty fingerprints_list')
        else:
            logging.debug('Empty trails_list')
        print("Done...")

def usage():
    print "\nThis is the usage function\n"
    print 'Usage: ./run_droidtrail.sh [options]'
    print '\n-h Show this help'
    print '-t Extract trails'
    print '-f Extract fingerprints'
    print '-m Specify the mode for trails/fingerprints extraction (i.e. long, short)'
    print '-o Specify the output file format (i.e. json, csv, xml)'
    print '\nDefault ./run_droidtrail.sh -t -f -m long -o csv\n'

def options():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:m:tf", ["help", "output=", "mode=", "trails", "fingerprints"])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)
    output = 'csv'
    mode = 'long'
    trails = False
    fingerprints = False
    if '-t' not in opts and '-f' not in opts:
        trails = True
        fingerprints = True
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-o", "--output"):
            if a == 'csv' or a == 'json' or a == 'xml':
                output = a
            else:
                usage()
                sys.exit()
        elif o in ("-m", "--mode"):
            if a == 'long' or a == 'short':
                mode = a
            else:
                usage()
                sys.exit()
        elif o in ("-t", "--trails"):
            trails = True
        elif o in ("-f", "--fingerprints"):
            fingerprints = True
        else:
            assert False, "Unhandled option"
    return trails, fingerprints, mode, output

def main():
    trails, fingerprints, mode, output = options()
    log_file = './logs/droidtrail.log'
    logging.basicConfig(filename=log_file,
                        level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%d-%m-%Y %H:%M')
    logging.debug("Setting '%s' as log file" % (log_file))

    logging.debug('#####################################')
    logging.debug('#####    Starting DroidTrail    #####')
    logging.debug('#####################################')
    core = Core(trails, fingerprints, mode, output)
    core.run()

if __name__ == "__main__":
    main()