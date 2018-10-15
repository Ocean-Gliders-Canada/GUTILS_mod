#!python
# coding=utf-8
import os
import shutil
from glob import glob
from collections import namedtuple

import netCDF4 as nc4
from lxml import etree

from gutils import safe_makedirs
from gutils.nc import check_dataset, create_dataset, merge_profile_netcdf_files
from gutils.slocum import SlocumReader
from gutils.tests import resource, GutilsTestClass
from gutils.watch.netcdf import netcdf_to_erddap_dataset

from pocean.dsg import ContiguousRaggedTrajectoryProfile

import logging
L = logging.getLogger(__name__)  # noqa


def decoder(x):
    return str(x.decode('utf-8'))


class TestCreateGliderScript(GutilsTestClass):

    def tearDown(self):
        outputs = [
            resource('slocum', 'real', 'netcdf')
        ]
        for d in outputs:
            try:
                shutil.rmtree(d)
            except (IOError, OSError):
                pass

    def test_defaults(self):
        out_base = resource('slocum', 'real', 'netcdf', 'bass-20160909T1733')
        args = dict(
            file=resource('slocum', 'usf_bass_2016_253_0_6_sbd.dat'),
            reader_class=SlocumReader,
            config_path=resource('slocum', 'config', 'bass-20160909T1733'),
            output_path=out_base,
            subset=False,
            template='trajectory',
            profile_id_type=1,
            tsint=10,
            filter_distance=1,
            filter_points=5,
            filter_time=10,
            filter_z=1
        )
        create_dataset(**args)

        output_files = sorted(os.listdir(out_base))
        output_files = [ os.path.join(out_base, o) for o in output_files ]
        assert len(output_files) == 32

        # First profile
        with nc4.Dataset(output_files[0]) as ncd:
            assert ncd.variables['profile_id'].ndim == 0
            assert ncd.variables['profile_id'][0] == 1473499507

        # Last profile
        with nc4.Dataset(output_files[-1]) as ncd:
            assert ncd.variables['profile_id'].ndim == 0
            assert ncd.variables['profile_id'][0] == 1473509118

        # Check netCDF file for compliance
        ds = namedtuple('Arguments', ['file'])
        for o in output_files:
            assert check_dataset(ds(file=o)) == 0

    def test_all_ascii(self):
        out_base = resource('slocum', 'real', 'netcdf', 'bass-20160909T1733')
        safe_makedirs(out_base)

        for f in glob(resource('slocum', 'usf_bass*.dat')):
            args = dict(
                file=f,
                reader_class=SlocumReader,
                config_path=resource('slocum', 'config', 'bass-20160909T1733'),
                output_path=out_base,
                subset=False,
                template='ioos_ngdac',
                profile_id_type=2,
                tsint=10,
                filter_distance=1,
                filter_points=5,
                filter_time=10,
                filter_z=1
            )
            create_dataset(**args)

        output_files = sorted(os.listdir(out_base))
        output_files = [ os.path.join(out_base, o) for o in output_files ]

        # First profile
        with nc4.Dataset(output_files[0]) as ncd:
            assert ncd.variables['profile_id'].ndim == 0
            assert ncd.variables['profile_id'][0] == 0

        # Last profile
        with nc4.Dataset(output_files[-1]) as ncd:
            assert ncd.variables['profile_id'].ndim == 0
            assert ncd.variables['profile_id'][0] == len(output_files) - 1

        # Check netCDF file for compliance
        ds = namedtuple('Arguments', ['file'])
        for o in output_files:
            assert check_dataset(ds(file=o)) == 0

    def test_delayed(self):
        out_base = resource('slocum', 'real', 'netcdf', 'modena-2015')

        args = dict(
            file=resource('slocum', 'modena_2015_175_0_9_dbd.dat'),
            reader_class=SlocumReader,
            config_path=resource('slocum', 'config', 'modena-2015'),
            output_path=out_base,
            subset=False,
            template='trajectory',
            profile_id_type=1,
            tsint=10,
            filter_distance=1,
            filter_points=5,
            filter_time=10,
            filter_z=1
        )
        create_dataset(**args)

        output_files = sorted(os.listdir(out_base))
        output_files = [ os.path.join(out_base, o) for o in output_files ]
        assert len(output_files) == 6

        # First profile
        with nc4.Dataset(output_files[0]) as ncd:
            assert ncd.variables['profile_id'].ndim == 0
            assert ncd.variables['profile_id'][0] == 1435257435

        # Last profile
        with nc4.Dataset(output_files[-1]) as ncd:
            assert ncd.variables['profile_id'].ndim == 0
            assert ncd.variables['profile_id'][0] == 1435264145

        # Check netCDF file for compliance
        ds = namedtuple('Arguments', ['file'])
        for o in output_files:
            assert check_dataset(ds(file=o)) == 0


class TestGliderCheck(GutilsTestClass):

    def setUp(self):
        super(TestGliderCheck, self).setUp()

        self.args = namedtuple('Check_Arguments', ['file'])

    def test_passing_testing_compliance(self):
        args = self.args(file=resource('should_pass.nc'))
        assert check_dataset(args) == 0

    def test_failing_testing_compliance(self):
        args = self.args(file=resource('should_fail.nc'))
        assert check_dataset(args) == 1


class TestProfileNetcdfMerge(GutilsTestClass):

    def test_small_merge(self):
        folder = resource('slocum', 'merge', 'small')
        output = resource('slocum', 'merge', 'output', 'small.nc')
        merge_profile_netcdf_files(folder, output)

        with ContiguousRaggedTrajectoryProfile(output) as ncd:
            assert ncd.is_valid()

    def test_large_merge(self):
        folder = resource('slocum', 'merge', 'large')
        output = resource('slocum', 'merge', 'output', 'large.nc')
        merge_profile_netcdf_files(folder, output)

        with ContiguousRaggedTrajectoryProfile(output) as ncd:
            assert ncd.is_valid()


class TestNetcdfToErddap(GutilsTestClass):

    def test_appending_variables(self):
        datasets_path = resource('erddap', 'datasets.xml')
        netcdf_files = [
            resource('erddap', '1.nc'),  # Creates datasets.xml
            resource('erddap', '2.nc'),  # Adds additional variables
            resource('erddap', '3.nc')   # Should not remove any variables
        ]

        for n in netcdf_files:
            netcdf_to_erddap_dataset(datasets_path, n, None)

        xmltree = etree.parse(datasets_path).getroot()
        find_dataset = etree.XPath("//erddapDatasets/dataset")
        ds = find_dataset(xmltree)[0]
        vs = [ d.findtext('sourceName') for d in ds.iter('dataVariable') ]

        # Temperatuer is only in 2.nc and not 1.nc or 3.nc. Make sure
        # it was carried through correctly
        assert 'temperature' in vs
        assert 'conductivity' in vs
        assert 'salinity' in vs
        assert 'density' in vs

        os.remove(datasets_path)
