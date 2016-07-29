from setuptools import setup

from boomer.util.setup_base import (
    find_all_packages,
    required,
    get_version,
    place_manifest
)

__author__ = 'seanfitz'

place_manifest('boomer-base-MANIFEST.in')

setup(
    name="Boomer",
    version=get_version(),
    install_requires=required('requirements.txt'),
    packages=find_all_packages("boomer"),
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'boomer-speech-client=boomer.client.speech.main:main',
            'boomer-messagebus=boomer.messagebus.service.main:main',
            'boomer-skills=boomer.skills.main:main',
            'boomer-echo-observer=boomer.messagebus.client.ws:echo',
            'boomer-audio-test=boomer.util.audio_test:main',
            'boomer-enclosure-client=boomer.client.enclosure.enclosure:main'
        ]
    }
)
