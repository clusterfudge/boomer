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
import tornado.ioloop as ioloop
import tornado.web as web

from boomer.configuration import ConfigurationManager
from boomer.messagebus.service.ws import WebsocketEventHandler

__author__ = 'seanfitz'

settings = {
    'debug': True
}


def validate_param(value, name):
    if not value:
        raise ValueError("Missing or empty %s in boomer.ini "
                         "[messagebus_service] section", name)


def main():
    import tornado.options
    tornado.options.parse_command_line()
    config = ConfigurationManager.get()
    service_config = config.get("messagebus_service")

    route = service_config.get('route')
    validate_param(route, 'route')

    routes = [
        (route, WebsocketEventHandler)
    ]

    application = web.Application(routes, **settings)
    host = service_config.get("host")
    port = service_config.get("port")
    validate_param(host, 'host')
    validate_param(port, 'port')

    application.listen(port, host)
    loop = ioloop.IOLoop.instance()
    loop.start()


if __name__ == "__main__":
    main()
