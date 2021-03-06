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

import json

__author__ = 'seanfitz'


class Message(object):
    def __init__(self, message_type, data={}, context=None):
        self.message_type = message_type
        self.data = data
        self.context = context

    def serialize(self):
        return json.dumps({
            'message_type': self.message_type,
            'data': self.data,
            'context': self.context
        })

    @staticmethod
    def deserialize(json_str):
        json_message = json.loads(json_str)
        return Message(json_message.get('message_type'),
                       data=json_message.get('data'),
                       context=json_message.get('context'))

    def reply(self, message_type, data, context={}):
        if not context:
            context = {}
        new_context = self.context if self.context else {}
        for key in context:
            new_context[key] = context[key]
        if 'target' in data:
            new_context['target'] = data['target']
        elif 'client_name' in context:
            context['target'] = context['client_name']
        return Message(message_type, data, context=new_context)

    def publish(self, message_type, data, context={}):
        if not context:
            context = {}
        new_context = self.context.copy() if self.context else {}
        for key in context:
            new_context[key] = context[key]

        if 'target' in new_context:
            del new_context['target']

        return Message(message_type, data, context=new_context)
