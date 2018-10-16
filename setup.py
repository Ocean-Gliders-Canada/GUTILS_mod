#!/usr/bin/env python

from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


def version():
    with open('VERSION') as f:
        return f.read().strip()


#reqs = [line.strip() for line in open('requirements.txt') if not line.startswith('#')]  # MOD
reqs=[]  # MOD, use environment.yml


setup(
    name='gutils',
    version=version(),
    description='A set of Python utilities for reading, merging, and post '
                'processing Teledyne Webb Slocum Glider data.',
    long_description=readme(),
    author='Kyle Wilcox',
    author_email='kyle@axiomdatascience.com',
    install_requires=reqs,
    url='https://github.com/SECOORA/GUTILS',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'gutils_create_nc = gutils.nc:main_create',
            'gutils_check_nc = gutils.nc:main_check',
            'gutils_binary_to_ascii_watch = gutils.watch.binary:main_to_ascii',
            'gutils_ascii_to_netcdf_watch = gutils.watch.ascii:main_to_netcdf',
            'gutils_netcdf_to_ftp_watch = gutils.watch.netcdf:main_to_ftp',
            'gutils_netcdf_to_erddap_watch = gutils.watch.netcdf:main_to_erddap',
        ]
    },
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering'
    ],
)
