#!/usr/bin/env python

__author__ = "Dani Estrella"
__version__ = "0.0.1"
__email__ = "daniestrella1@gmail.com"

import csv
import os

COMMENT_PREFIX = "//"
FILE_NAME = 'strings.csv'
CSV_DELIMITER = ','

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

PLATFORM_ANDROID = 'android'
PLATFORM_IOS = 'ios'
PLATFORM_ALL = 'all'

HEADER = "AUTO-GENERATED v" + __version__

def main():

    # Get csv file path
    file_path = os.path.join(DIR_PATH, FILE_NAME)

    # Read csv string values
    strings = read_file(file_path)

    # Write values on Android and iOS localized strings files
    write_files(strings)


def read_file(file_path):

    with open(file_path, 'rb') as csv_file:
        rows = csv.reader(csv_file, delimiter=CSV_DELIMITER)

        localized_strings = {PLATFORM_ANDROID: [], PLATFORM_IOS: []}

        for row_num, row in enumerate(rows):

            # Headers
            if row_num == 0:

                # Avoid empty headers
                if len(row) == 0:
                    print 'ERROR: invalid headers'
                    return []

                col_num = 0
                for header in row:

                    # Avoid add key and platform columns as languages
                    if col_num < 2:
                        col_num += 1
                        continue

                    localized_strings[PLATFORM_ANDROID].append([header, []])
                    localized_strings[PLATFORM_IOS].append([header, []])
                    col_num += 1

            # Check empty row
            elif len(row) == 0:
                continue

            else:

                for col_num, value in enumerate(row):

                    # Key column
                    if col_num == 0:
                        key = value

                    # Platform column
                    elif col_num == 1:
                        if len(value) == 0:
                            value = PLATFORM_ALL
                        platform = value

                    # Languages columns
                    else:
                        # value = value.encode('utf-8')
                        if platform == PLATFORM_ANDROID or platform == PLATFORM_ALL:
                            formatted_string = process_android_value(key, value)
                            localized_strings[PLATFORM_ANDROID][col_num - 2][1] += [formatted_string]

                        if platform == PLATFORM_IOS or platform == PLATFORM_ALL:
                            formatted_string = process_ios_value(key, value)
                            localized_strings[PLATFORM_IOS][col_num - 2][1] += [formatted_string]

    return localized_strings


def process_ios_value(key, value):

    # Check if is a comment
    if key.startswith(COMMENT_PREFIX):
        return "\n" + key

    # Add underscore before key to identify on code
    key = "_" + key

    return '"' + key + '"="' + value + '";'


def process_android_value(key, value):

    # Check if is a comment
    if key.startswith(COMMENT_PREFIX):

        # Remove prefix to write custom comment format
        key = key[len(COMMENT_PREFIX):]
        return "\n<!-- " + key + " -->"

    # Escape apostrophes
    value = value.replace("'", "\\'")

    return '<string name="' + key + '">' + value + '</string>'


def write_files(strings):

    # Write localized strings on file for each platform and language
    for platform in strings:
        for language_strings in strings[platform]:
            language = language_strings[0]
            values = language_strings[1]

            if platform == PLATFORM_ANDROID:
                write_android_file(language, values)
            elif platform == PLATFORM_IOS:
                write_ios_file(language, values)


def write_android_file(language, values):

    # Android extra values
    values.insert(0, "<!-- " + HEADER + " -->\n")
    values.insert(1, "<resources>\n")
    values.insert(len(values), "</resources>")

    dir_name = 'values-' + language
    language_dir = os.path.join(DIR_PATH, dir_name)

    print 'Writing Android ' + language + ' file'
    write_file(language_dir, 'strings.xml', values)


def write_ios_file(language, values):

    # iOS extra values
    values.insert(0, "//" + HEADER + "\n")

    dir_name = language + '.lproj'
    language_dir = os.path.join(DIR_PATH, dir_name)

    print 'Writing iOS ' + language + ' file'
    write_file(language_dir, 'Localizable.strings', values)


def write_file(file_path, file_name, values):

    # Create directory if not exists
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    file_path = os.path.join(file_path, file_name)

    f = open(file_path, 'w+')
    [f.write("%s\n" % string) for string in values]
    f.flush()
    f.close()


main()
