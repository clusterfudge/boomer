#!/usr/bin/env bash
# exit on any error
set -Ee

MIMIC_DIR=mimic
let "CORES=$(nproc) - 1"

# download and install mimic
if [ ! -d ${MIMIC_DIR} ]; then
    git clone https://github.com/MycroftAI/mimic.git
    cd ${MIMIC_DIR}
    ./configure --with-audio=alsa
    make -j$CORES
else
    # ensure mimic is up to date
    cd ${MIMIC_DIR}
    git pull
    make clean
    ./configure --with-audio=alsa
    make -j$CORES
fi
