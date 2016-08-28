# This file is part of Boomer Core.
#
# Boomer Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Boomer Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Boomer Core.  If not, see <http://www.gnu.org/licenses/>.
#
# Forked from Mycroft Core on 2017-07-29
import collections

import requests
from configobj import ConfigObj
from genericpath import exists, isfile
from os.path import join, dirname, expanduser

from boomer.identity import IdentityManager
from boomer.util import str2bool
from boomer.util.log import getLogger

__author__ = 'seanfitz, jdorleans'

logger = getLogger(__name__)

DEFAULT_CONFIG = join(dirname(__file__), 'boomer.ini')
SYSTEM_CONFIG = '/etc/boomer/boomer.ini'
USER_CONFIG = join(expanduser('~'), '.boomer/boomer.ini')


class ConfigurationLoader(object):
    """
    A utility for loading Boomer configuration files.
    """

    @staticmethod
    def load(locations=None):
        """
        Loads default or specified configuration files
        """
        config = {}
        locations = locations or [DEFAULT_CONFIG, SYSTEM_CONFIG, USER_CONFIG]

        for location in locations:
            config = ConfigurationLoader.__load(config, location)

        return config

    @staticmethod
    def __load(config, location):
        if exists(location) and isfile(location):
            try:
                cobj = ConfigObj(location)
                config = ConfigurationLoader.__merge(config, cobj)
                logger.debug("Configuration '%s' loaded" % location)
            except Exception, e:
                logger.error("Error loading configuration '%s'" % location)
                logger.error(repr(e))
        else:
            logger.debug("Configuration '%s' not found" % location)
        return config

    @staticmethod
    def __merge(config, cobj):
        for k, v in cobj.iteritems():
            if isinstance(v, collections.Mapping):
                config[k] = ConfigurationLoader.__merge(config.get(k, {}), v)
            else:
                config[k] = cobj[k]
        return config


class ConfigurationManager(object):
    """
    Static management utility for calling up cached configuration.
    """
    __config = None

    @staticmethod
    def get(locations=None):
        """
        Get cached configuration.

        :return: A dictionary representing Boomer configuration.
        """
        if not ConfigurationManager.__config:
            ConfigurationManager.__config = ConfigurationLoader.load(locations)

        return ConfigurationManager.__config
