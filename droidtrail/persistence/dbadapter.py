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
#import MySQLdb
#from MySQLdb import OperationalError

class DbAdapter():
    """
    import MySQLdb; db = MySQLdb.connect(host="10.6.20.20", user="root", passwd="*****", db="ipfeeder")
    """

    def __init__(self):
        logging.debug("Instantiating the '%s' class" % (self.__class__.__name__))
        self.db_host = ''
        self.db_user = ''
        self.db_password = ''
        self.db_name = ''
        #TODO: t.b.d.

    def connect(self):
        logging.debug('Connecting to...')
        '''
        try:
            return MySQLdb.connect(
                host=self.db_host,
                user=self.db_user,
                passwd=self.db_password,
                db=self.db_name)
        except OperationalError as ex:
            logging.debug('Connection Error')
            return None
        '''

    def cursor(self):
        return self.connect().cursor()