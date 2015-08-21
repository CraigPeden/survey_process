import unicodecsv as csv
import time

# Name of the input file and the output file
input_file_name = "chickens-001entrypii.csv"
output_file_name = "chickens-001cleaned.csv"

start_time = time.time()

# with open(input_file_name, 'rb') as csvfile:
#     reader = csv.reader(csvfile)
#     line1 = [x for x in csv.reader(csvfile.readlines()[1].encode('utf8')) if not u'']
#     line2 = [x for x in csv.reader(csvfile.readlines()[0].encode('utf8')) if not u'']
#     print line1
#     print line2
#     if csvfile.readlines()[2][3].encode('utf8') is "email_address":
#         english = {}
#         for line in reader:
#             english[line[0]] = line[7]
#         print english
#     else:
#         print "nope"
#         english = {}
#         for line in reader:
#             english[line[0]] = line[5]
#         print english

with open(input_file_name, 'rb') as csvfile:
    f = csv.DictReader(csvfile.readlines()[2:])
    with open(output_file_name, 'w') as csvoutfile:
        fieldnames = ['session_user_id', 'coursera_user_id', 'submission_time', 'english', 'cert', 'learn_new', 'improve', 'new_people', 'try_online', 'try_MOOC', 'browse_ed', 'unsure', 'gender', 'age', 'academic_level', 'same_subject']
        writer = csv.DictWriter(csvoutfile, fieldnames=fieldnames)
        writer.writeheader()

        for line in f:
            output = {}
            output['session_user_id'] = line.get('session_user_id').encode('utf8')
            output['coursera_user_id'] = line.get('coursera_user_id').encode('utf8')
            output['submission_time'] = line.get('submission_time').encode('utf8')

            # output['english'] = english[output['session_user_id']]

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

            if line.get(u"Browse Edinburgh's offering").encode('utf8') is "1":
                output['browse_ed'] = 1
            else:
                output['browse_ed'] = 0

            if line.get(u'Unsure').encode('utf8') is "1":
                output['unsure'] = 1
            else:
                output['unsure'] = 0

            if line.get(u'Male').encode('utf8') is "1":
                output['gender'] = "Male"
            elif line.get(u'Female').encode('utf8') is "0":
                output['gender'] = "Female"
            else:
                output['gender'] = "Prefer not to say"

            if line.get(u'under 18').encode('utf8') is "1":
                output['age'] = "under 18"
            elif line.get(u'18 - 24').encode('utf8') is "1":
                output['age'] = "18 - 24"
            elif line.get(u'25 - 34').encode('utf8') is "1":
                output['age'] = "25 - 34"
            elif line.get(u'35 - 44').encode('utf8') is "1":
                output['age'] = "35 - 44"
            elif line.get(u'45 - 54').encode('utf8') is "1":
                output['age'] = "45 - 54"
            elif line.get(u'55 - 64').encode('utf8') is "1":
                output['age'] = "55 - 64"
            elif line.get(u'65 or over').encode('utf8') is "1":
                output['age'] = "65 or over"
            else:
                output['age'] = "Prefer not to say"

            output['academic_level'] = line.get('academic_level')
            output['same_subject'] = line.get('same_subject')

            writer.writerow(output)

print "--- %s seconds ---" % (time.time() - start_time)
