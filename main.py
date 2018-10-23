import csv
import json


def get_hour(time_str):
    h, m, s = time_str.split(':')
    return round(float(int(h) * 3600 + int(m) * 60 + int(s)) / 3600.0, 2)

csvfile = open('sample_file.csv', 'r')
jsonfile = open('file.json', 'w')

fieldnames = ("User", "Email", "Client", "Project", "Task", "Description", "Billable", "Start date", "Start time", "End date", "End time", "Duration", "Tags", "Amount ()")
reader = csv.DictReader(csvfile, fieldnames)
next(reader, None)
json_result = []
for row in reader:
    json_result.append(row)
    print("Description: %s" % row["Description"])
    print("Duration (h): %s" % get_hour(row["Duration"]))

# json.dump(json_result, jsonfile)
# jsonfile.write('\n')