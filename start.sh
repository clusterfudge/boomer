#!/usr/bin/env bash
TOP=$(cd $(dirname $0) && pwd -L)
VIRTUALENV_ROOT=${VIRTUALENV_ROOT:-"${HOME}/.virtualenvs/boomer"}

case $1 in
	"service") SCRIPT=${TOP}/boomer/messagebus/service/main.py ;;
	"skills") SCRIPT=${TOP}/boomer/skills/main.py ;;
	"skill_container") SCRIPT=${TOP}/boomer/skills/container.py ;;
	"voice") SCRIPT=${TOP}/boomer/client/speech/main.py ;;
	"cli") SCRIPT=${TOP}/boomer/client/text/cli.py ;;
	"audiotest") SCRIPT=${TOP}/boomer/util/audio_test.py ;;
	"collector") SCRIPT=${TOP}/boomer_data_collection/cli.py ;;
	"unittest") SCRIPT=${TOP}/test/test_runner.py ;;
	"audioaccuracytest") SCRIPT=${TOP}/audio-accuracy-test/audio_accuracy_test.py ;;
	"sdkdoc") SCRIPT=${TOP}/doc/generate_sdk_docs.py ;;
        "enclosure") SCRIPT=${TOP}/boomer/client/enclosure/enclosure.py ;;
        "pairing") SCRIPT=${TOP}/boomer/pairing/client.py ;;
	*) echo "Usage: start.sh [service | skills | skill_container | voice | cli | audiotest | collector | unittest | enclosure | pairing | sdkdoc ]"; exit ;;
esac

echo "Starting $@"

shift

source ${VIRTUALENV_ROOT}/bin/activate
PYTHONPATH=${TOP} python ${SCRIPT} $@
