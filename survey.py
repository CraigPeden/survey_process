#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import Statements
# csv       CSV File Reading and Writing for comma seperated value files
# time      Python library to compute time
# sys       System-specific parameters and functions

import unicodecsv as csv
import time
import sys

# bs4 == Beautiful Soup 4.x   General Parsing Library

from bs4 import UnicodeDammit

# Automated parsing, cleaning and output of Edinburgh's raw survey output taken from Coursera.


class Survey(object):
    #   __init__            is triggered when an instance of the class is instanciated.
    #
    #   input_file_name     is the location of the survey file that is to be processed. This
    #                       will be taken from the first command line argument
    def __init__(self, input_file_name):

        # Open the file, and determine it's encoding using the UnicodeDammit library of bs4
        with open(input_file_name, 'rU') as csvfile:
            self.enc = UnicodeDammit(csvfile.read()).original_encoding

    #   Function that will actually do the processing of the survey
    #   and then spit out the cleaned version.
    def processing(self, input_file_name, output_file_name):
        # 1.    Opens the survey file in Universal Mode
        # 2.    For as many columns as there is in the second line
        #       search each line for the relevant columns we're looking
        #       for then store the index of said column.
        # 3.    For each line in the survey, get the actual value and
        #       store it in a dictionary to be outputted
        # 4.    Write the headers for the output
        # 5.    Write the dictionary to the output

        # The parsing is split in two because a lot of it can be picked using Unicodecsv's
        # dictreader class which makes things easy. But some have to be done more manually
        # using just the default reader because their column header is not unique (i.e Y/N)

        with open(input_file_name, 'rU') as csvfile:
            lines = [x for x in csv.reader([y.replace('\0', '') for y in csvfile], encoding=self.enc)]

            agecolumns = []
            work = []

            for number in range(0, len(lines[1])):
                if "subject area related" in lines[1][number]:
                    if lines[2][number] == "Yes":
                        area_related = number
                if "Is English your first language" in lines[1][number]:
                    if lines[2][number] == "Yes":
                        english_columns = number
                if "What is your age" in lines[1][number]:
                    agecolumns.append([lines[2][number], number])
                if "What is your current area of employment" in lines[1][number]:
                    work.append([lines[2][number], number])
                if "offering" in lines[2][number]:
                    offering = number

            english = {}
            same_subject = {}
            age = {}
            job = {}
            offer = {}

            for line in lines:
                for ages in agecolumns:
                    if line[ages[1]] == "1":
                        age[line[0]] = ages[0]

                for jobs in work:
                    if line[jobs[1]] == "1":
                        job[line[0]] = jobs[0]

                try:
                    if line[area_related] == "1":
                        same_subject[line[0]] = "Yes"
                    else:
                        same_subject[line[0]] = "No"

                except:
                    same_subject[line[0]] = "Unknown"

                try:
                    if line[english_columns] == "1":
                        english[line[0]] = "Yes"
                    else:
                        english[line[0]] = "No"

                except:
                    english[line[0]] = "Unknown"

                try:
                    if line[offering] == "1":
                        offer[line[0]] = "1"
                    else:
                        offer[line[0]] = "0"
                except:
                    offer[line[0]] = "Unknown"

        with open(input_file_name, 'rU') as csvfile:
            f = csv.DictReader([y.replace('\0', '') for y in csvfile.readlines()[2:]], encoding=self.enc)
            with open(output_file_name, 'w') as csvoutfile:
                fieldnames = ['session_user_id', 'coursera_user_id', 'submission_time', 'english', 'cert', 'learn_new', 'improve', 'new_people', 'try_online', 'try_MOOC', 'browse_ed', 'unsure', 'gender', 'age', 'academic_level', 'same_subject']
                writer = csv.DictWriter(csvoutfile, fieldnames=fieldnames)
                writer.writeheader()

                for line in f:
                    output = {}
                    output['session_user_id'] = line.get('session_user_id').encode('utf8')
                    output['coursera_user_id'] = line.get('coursera_user_id').encode('utf8')
                    output['submission_time'] = line.get('submission_time').encode('utf8')

                    output['english'] = english[output['session_user_id']]

                    if line.get(u'To get a certificate').encode('utf8') is "1":
                        output['cert'] = 1
                    else:
                        output['cert'] = 0

                    if line.get(u'Learn new things').encode('utf8') is "1":
                        output['learn_new'] = 1
                    else:
                        output['learn_new'] = 0

                    if line.get(u'Improve my career options').encode('utf8') is "1":
                        output['improve'] = 1
                    else:
                        output['improve'] = 0

                    if line.get(u'Meet new people').encode('utf8') is "1":
                        output['new_people'] = 1
                    else:
                        output['new_people'] = 0

                    if line.get(u'Try online education').encode('utf8') is "1":
                        output['try_online'] = 1
                    else:
                        output['try_online'] = 0

                    if line.get(u'See what MOOCs are').encode('utf8') is "1":
                        output['try_MOOC'] = 1
                    else:
                        output['try_MOOC'] = 0

                    if line.get(u'Unsure').encode('utf8') is "1":
                        output['unsure'] = 1
                    else:
                        output['unsure'] = 0

                    if line.get(u'Male').encode('utf8') is "1":
                        output['gender'] = "Male"
                    elif line.get(u'Female').encode('utf8') is "1":
                        output['gender'] = "Female"
                    else:
                        output['gender'] = "Prefer not to say"

                    try:
                        output['browse_ed'] = offer[output['session_user_id']]
                    except:
                        output['browse_ed'] = "N/A"
                    try:
                        output['same_subject'] = same_subject[output['session_user_id']]
                    except:
                        output['same_subject'] = "N/A"
                    try:
                        output['age'] = age[output['session_user_id']]
                    except:
                        output['age'] = "N/A"
                    try:
                        output['academic_level'] = job[output['session_user_id']]
                    except:
                        output['academic_level'] = "N/A"

                    writer.writerow(output)

start_time = time.time()

# Name of the input file and the output file
input_file_name = sys.argv[1]
output_file_name = "clean.csv"

a = Survey(input_file_name)
a.processing(input_file_name, output_file_name)

print "--- %s seconds ---" % (time.time() - start_time)
