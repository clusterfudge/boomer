from setuptools import setup

from boomer.util.setup_base import get_version, place_manifest

__author__ = 'seanfitz'

place_manifest("skills-sdk-MANIFEST.in")

setup(
    name="boomer-skills-sdk",
    version=get_version(),
    install_requires=[
        "mustache==0.1.4",
        "configobj==5.0.6",
        "pyee==1.0.1",
        "adapt-parser==0.2.1",
        "websocket-client==0.32.0"
    ],
    packages=[
        "boomer.configuration",
        "boomer.dialog",
        "boomer.filesystem",
        "boomer.messagebus",
        "boomer.messagebus.client",
        "boomer.session",
        "boomer.skills.intent",
        "boomer.skills",
        "boomer.util",
        "boomer"
    ],
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'boomer-skill-container=boomer.skills.container:main'
        ]
    }
)
