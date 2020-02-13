import os
import sys
from dinkum.dinkum import Dinkum
import dinkum


def decode_binary(source_directory, destination_directory, cache_directory=None):
    ascii_dir = os.path.join(source_directory, 'decode_result')
    if not os.path.exists(destination_directory):
        os.makedirs(ascii_dir)
    path_exists = os.path.exists(ascii_dir)
    if not path_exists:
        os.makedirs(ascii_dir)
    my_dinkum = Dinkum()
    my_dinkum.load_files(source_directory, None, True)
    if cache_directory:
        cache_directory = ' -c ' + cache_directory + ' '
    else:
        cache_directory = ' '
    decoded_files = []
    for file_name, file_path_list in my_dinkum.decode():
        reorder_list = my_dinkum.reorder_files(file_path_list)
        flight_file = file_name + os.path.splitext(reorder_list[0])[-1]
        print(os.path.join(ascii_dir, flight_file))
        science_file = file_name + os.path.splitext(reorder_list[1])[-1]
        print(os.path.join(ascii_dir, science_file))
        command_decode_flight = os.path.dirname(__file__) + '/bin/dbd2asc' + cache_directory + reorder_list[
            0] + ' > ' + os.path.join(ascii_dir, flight_file)
        command_decode_science = os.path.dirname(__file__) + '/bin/dbd2asc' + cache_directory + reorder_list[
            1] + ' > ' + os.path.join(ascii_dir, science_file)
        decoded_files.append([os.path.join(ascii_dir, flight_file), os.path.join(ascii_dir, science_file)])
        os.system(command_decode_flight)
        os.system(command_decode_science)
    return decoded_files, ascii_dir


def merge_ascii(source_directory, destination_directory, cache_directory=None, merge_by_dinkum=False):
    decoded_files_list, decoded_files_directory = decode_binary(source_directory, destination_directory,
                                                                cache_directory)
    if merge_by_dinkum:
        dinkum.dinkumMergeAscii(decoded_files_directory, destination_directory)
    else:
        for pair_files in decoded_files_list:
            after_merge = os.path.basename(pair_files[0]).replace('-', '_')
            after_merge = after_merge.replace('.', '_')
            merge_file = after_merge + '.dat'
            print(os.path.join(decoded_files_directory, merge_file))
            command_merge_files = os.path.dirname(__file__) + '/bin/dba_merge ' + pair_files[0] + ' ' + pair_files[
                1] + ' > ' + os.path.join(destination_directory, merge_file)
            os.system(command_merge_files)


if __name__ == "__main__":
    source_directory = sys.argv[1]
    destination_directory = sys.argv[2]
    if len(sys.argv) >= 4:
        cache_directory = sys.argv[3]
    else:
        cache_directory = None
    if len(sys.argv) >= 5:
        merge_by_dinkum = bool(sys.argv[4])
    else:
        merge_by_dinkum = False
    merge_ascii(source_directory, destination_directory, cache_directory, merge_by_dinkum=merge_by_dinkum)


