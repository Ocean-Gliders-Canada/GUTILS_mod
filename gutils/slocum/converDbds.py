import os
from dinkum.dinkum import Dinkum
import dinkum
# When using
# import converDbds
# converDbds.merge_binary(source_directory, destination_directory, cache_directory=None, merge_by_dinkum=False)
# set merge_by_dinkum to true will merge by dinkum function, otherwise will merge using slocum by default


def merge_binary(source_directory, destination_directory, cache_directory=None, merge_by_dinkum=False):
    ascii_dir = os.path.join(source_directory, 'decode_result')
    path_exists = os.path.exists(ascii_dir)
    if not path_exists:
        os.makedirs(ascii_dir)
    my_dinkum = Dinkum()
    my_dinkum.load_files(source_directory, None, True)
    if cache_directory:
        cache_directory = ' -c ' + cache_directory + ' '
    else:
        cache_directory = ' '
    for file_name, file_path_list in my_dinkum.decode():
        reorder_list = my_dinkum.reorder_files(file_path_list)
        flight_file = file_name + str.upper(os.path.splitext(reorder_list[0])[-1])
        science_file = file_name + str.upper(os.path.splitext(reorder_list[1])[-1])
        command_decode_flight = './bin/dbd2asc' + cache_directory + reorder_list[0] + ' > ' + os.path.join(ascii_dir, flight_file)
        command_decode_science = './bin/dbd2asc' + cache_directory + reorder_list[1] + ' > ' + os.path.join(ascii_dir, science_file)
        os.system(command_decode_flight)
        os.system(command_decode_science)
        if merge_by_dinkum:
            dinkum.dinkumMergeAscii(ascii_dir, destination_directory)
        else:
            merge_file = file_name + '.edba'
            command_merge_files = './bin/dba_merge ' + os.path.join(ascii_dir, flight_file) + ' ' + os.path.join(ascii_dir, science_file) + ' > ' + os.path.join(destination_directory, merge_file)
            os.system(command_merge_files)
        print('Wrote merge file(s) in', destination_directory)




