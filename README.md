# 🚤 Glider Utilities (GUTILS)

[![Build Status](https://travis-ci.org/SECOORA/GUTILS.svg?branch=master)](https://travis-ci.org/SECOORA/GUTILS)
[![license](https://img.shields.io/github/license/SECOORA/GUTILS.svg)](https://github.com/SECOORA/GUTILS/blob/master/LICENSE.txt)
[![GitHub release](https://img.shields.io/github/release/SECOORA/GUTILS.svg)]()

🐍 + 🌊 + 🚤

A python framework for working with the data from Autonomous Underwater Vehicles (AUVs)

Supports:

+  Teledyne Webb Slocum Gliders


## Resources

+  **Documentation:** https://secoora.github.io/GUTILS/docs/
+  **API:** https://secoora.github.io/GUTILS/docs/api/gutils.html
+  **Source Code:** https://github.com/secoora/GUTILS/
+  **Git clone URL:** https://github.com/secoora/GUTILS.git


## Installation

GUTILS is available through [`conda`](http://conda.pydata.org/docs/install/quick.html) and was designed with Python 3.5 or above in mind. I backported it to 2.7 by request. Please use 3.5+ if possible as the [gwt project](https://github.com/TEOS-10/GSW-Python) will soon end support for 2.7.

```bash
$ conda create -n gutils python=3.5
$ source activate gutils
$ conda install -c conda-forge gutils
```


## Testing

To run the "long" tests you will need [this](https://github.com/SECOORA/SGS) cloned somewhere. Then set the env variable `GUTILS_TEST_CONFIG_DIRECTORY` to the config directory, ie `export GUTILS_TEST_CONFIG_DIRECTORY=/data/Development/secoora/sgs/SGS/config`
