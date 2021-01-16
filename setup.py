
from setuptools import setup, find_packages
from smx10fanctl.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='smx10fanctl',
    version=VERSION,
    description='A fancontroller for Supermicro boards using IPMI raw commands',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Haije Ploeg',
    author_email='ploeg.haije@gmail.com',
    url='https://github.com/haijeploeg/smx10fanctl',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    install_requires=['cement==3.0.4',
                      'wheel>=0.31.0',
                      'pyyaml',
                      'colorlog',
                      'psutil'],
    entry_points="""
        [console_scripts]
        smx10fanctl = smx10fanctl.main:main
    """,
)
