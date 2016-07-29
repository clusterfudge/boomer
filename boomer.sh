#!/usr/bin/env bash

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

function usage {
  echo
  echo "Quickly start, stop or restart Boomer's esential services in detached screens"
  echo
  echo "usage: $0 [-h] (start [-v|-c]|stop|restart)"
  echo "      -h             this help message"
  echo "      start          starts boomer-service, boomer-skills, boomer-voice and boomer-cli in quiet mode"
  echo "      start -v       starts boomer-service, boomer-skills and boomer-voice"
  echo "      start -c       starts boomer-service, boomer-skills and boomer-cli"
  echo "      stop           stops boomer-service, boomer-skills and boomer-voice"
  echo "      restart        restarts boomer-service, boomer-skills and boomer-voice"
  echo
  echo "screen tips:"
  echo "            run 'screen -list' to see all running screens"
  echo "            run 'screen -r <screen-name>' (e.g. 'screen -r boomer-service') to reatach a screen"
  echo "            press ctrl + a, ctrl + d to detace the screen again"
  echo "            See the screen man page for more details"
  echo
}

mkdir -p $DIR/logs

function verify-start {
    if ! screen -list | grep -q "$1";
    then
      echo "$1 failed to start. The log is below:"
      echo
      tail $DIR/logs/$1.log
    exit 1
    fi
}

function start-boomer {
  screen -mdS boomer-$1$2 -c $DIR/boomer-$1.screen $DIR/start.sh $1 $2
  sleep 1
  verify-start boomer-$1$2
  echo "Boomer $1$2 started"
}

function stop-boomer {
    if screen -list | grep -q "$1";
    then
      screen -XS boomer-$1 quit
      echo "Boomer $1 stopped"
    fi
}

function restart-boomer {
    if screen -list | grep -q "quiet";
    then
      $0 stop
      sleep 1
      $0 start
    elif screen -list | grep -q "cli" && ! screen -list | grep -q "quiet";
    then
      $0 stop
      sleep 1
      $0 start -c
    elif screen -list | grep -q "voice" && ! screen -list | grep -q "quiet";
    then
      $0 stop
      sleep 1
      $0 start -v
    else
      echo "An error occurred"
    fi
}

set -e

if [[ -z "$1" || "$1" == "-h" ]]
then
  usage
  exit 1
elif [[ "$1" == "start" && -z "$2" ]]
then
  start-boomer service
  start-boomer skills
  start-boomer voice
  start-boomer cli --quiet
  exit 0
elif [[ "$1" == "start" && "$2" == "-v" ]]
then
  start-boomer service
  start-boomer skills
  start-boomer voice
  exit 0
elif [[ "$1" == "start" && "$2" == "-c" ]]
then
  start-boomer service
  start-boomer skills
  start-boomer cli
  exit 0
elif [[ "$1" == "stop" && -z "$2" ]]
then
  stop-boomer service
  stop-boomer skills
  stop-boomer voice
  stop-boomer cli
  exit 0
elif [[ "$1" == "restart" && -z "$2" ]]
then
  restart-boomer
  exit 0
else
  usage
  exit 1
fi
