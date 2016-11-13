# Copyright 2016 Boomer AI, Inc.
#
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


from adapt.engine import IntentDeterminationEngine
from boomer.messagebus.message import Message
from boomer.metrics import MetricsAggregator, Stopwatch
from boomer.skills.core import open_intent_envelope, BoomerSkill
from boomer.util.log import getLogger

__author__ = 'seanfitz'

logger = getLogger(__name__)


class IntentSkill(BoomerSkill):
    def __init__(self):
        BoomerSkill.__init__(self, name="IntentSkill")
        self.engine = IntentDeterminationEngine()

    def initialize(self):
        self.emitter.on('register_vocab', self.handle_register_vocab)
        self.emitter.on('register_intent', self.handle_register_intent)
        self.emitter.on('recognizer_loop:utterance', self.handle_utterance)
        self.emitter.on('detach_intent', self.handle_detach_intent)

    def handle_utterance(self, message):
        timer = Stopwatch()
        timer.start()

        metrics = MetricsAggregator()
        utterances = message.metadata.get('utterances', '')

        best_intent = None

        for utterance in utterances:
            metrics.increment("utterances.count")
            for intent in self.engine.determine_intent(
                    utterance, num_results=100):
                metrics.increment("intents.count")
                intent['utterance'] = utterance
                if not best_intent or best_intent.get('confidence') < intent.get('confidence'):
                    best_intent = intent

        if best_intent and best_intent.get('confidence', 0.0) > 0.0:
            reply = message.reply(
                best_intent.get('intent_type'), metadata=best_intent)
            self.emitter.emit(reply)
        elif len(utterances) == 1:
            self.emitter.emit(
                Message("intent_failure",
                        metadata={"utterance": utterances[0]}))
        else:
            self.emitter.emit(
                Message("multi_utterance_intent_failure",
                        metadata={"utterances": utterances}))
        metrics.timer("parse.time", timer.stop())
        metrics.flush()

    def handle_register_vocab(self, message):
        start_concept = message.metadata.get('start')
        end_concept = message.metadata.get('end')
        regex_str = message.metadata.get('regex')
        alias_of = message.metadata.get('alias_of')
        if regex_str:
            self.engine.register_regex_entity(regex_str)
        else:
            self.engine.register_entity(
                start_concept, end_concept, alias_of=alias_of)

    def handle_register_intent(self, message):
        intent = open_intent_envelope(message)
        self.engine.register_intent_parser(intent)

    def handle_detach_intent(self, message):
        intent_name = message.metadata.get('intent_name')
        new_parsers = [
            p for p in self.engine.intent_parsers if p.name != intent_name]
        self.engine.intent_parsers = new_parsers

    def stop(self):
        pass


def create_skill():
    return IntentSkill()
