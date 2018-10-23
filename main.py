import csv
import json
import re
import datetime
import os
import glob


def get_hour(time_str):
    h, m, s = time_str.split(':')
    return round(float(int(h) * 3600 + int(m) * 60 + int(s)) / 3600.0, 2)


def get_ticketid(description):
    # rを付けることを推奨。
    # バックスラッシュをそのままで分かりやすいため。
    content = r'%s' % description
    # ()で取りたい文字を
    pattern = '#(\d+)_.*'

    result = re.match(pattern, content)

    if result:  # none以外の場合
        # group()で全文字を
        # print(result.group())  # hellow python, 123,end
        # group(1)で数字を
        # print(result.group(1))  # 123
        return result.group(1)


def get_reportitem(path):

    reportitem = []
    json_fname = '%s.json' % str(datetime.date.today())
    if os.path.exists(json_fname):
        with open(json_fname) as f:
            reportitem = json.load(f)

    with open(path, 'r') as csvfile:
        fieldnames = ("User", "Email", "Client", "Project", "Task", "Description", "Billable", "Start date", "Start time", "End date", "End time", "Duration", "Tags", "Amount ()")
        reader = csv.DictReader(csvfile, fieldnames)
        next(reader, None)

        json_result = []
        project = ''
        total_duration = 0.0
        for row in reader:
            # json_result.append(row)
            project = row["Project"]
            print("Project: %s" % project)
            description = row["Description"]
            print("Description: %s" % description)
            ticketid = get_ticketid(description)
            print("Ticket id: %s" % ticketid)
            to_remove = '#%s_' % ticketid
            comment = (str(description)).replace(to_remove, '')
            print("Comment: %s" % comment)
            duration = get_hour(row["Duration"])
            print("Duration (h): %s" % duration)
            json_result.append({"ticketid": ticketid, "comment": comment, "duration":  duration})
            total_duration += duration

        reportitem.append({"project": project, "total_duration": round(total_duration, 2), "data": json_result})

    with open(json_fname, 'w') as f:
        json.dump(reportitem, f)
        f.write('\n')

    return json_fname


def create_report(path):
    print("No implementation.")
    return


if __name__ == '__main__':
    report_src = ''
    for file in glob.glob('*.csv'):
        report_src = get_reportitem(file)
    create_report(report_src)