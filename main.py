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

    json_fname = '%s.json' % str(datetime.date.today())
    if os.path.exists(json_fname):
        with open(json_fname) as f:
            json_fname = json.load(f)

    with open(path, 'r') as csvfile:
        fieldnames = ("User", "Email", "Client", "Project", "Task", "Description", "Billable", "Start date", "Start time", "End date", "End time", "Duration", "Tags", "Amount ()")
        reader = csv.DictReader(csvfile, fieldnames)
        next(reader, None)

        json_result = []
        project_list = []
        for row in reader:
            project = row["Project"]
            if project not in project_list :
                project_list.append(project)
            description = row["Description"]
            ticketid = get_ticketid(description)
            to_remove = '#%s_' % ticketid
            comment = (str(description)).replace(to_remove, '')
            duration = get_hour(row["Duration"])

            # 一つのエントリ
            json_result.append({"ticketid": ticketid, "comment": comment, "duration":  duration, "project": project})

    summarized = summarize(json_result, project_list)

    with open(json_fname, 'w') as f:
        json.dump(summarized, f)
        f.write('\n')
    return json_fname


def summarize(reportitem, project_list):

    result = []
    for project in project_list:
        project_duration = 0.0
        tmp_items = []
        for item in reportitem:
            if item["project"] == project:
                tmp_items.append(item)
                project_duration += item['duration']
        result.append({'project': project, 'duration': round(project_duration, 2), 'data': tmp_items})

    return result


def create_report(path):
    print("No implementation.")
    return


if __name__ == '__main__':
    report_src = ''
    for file in glob.glob('*.csv'):
        report_src = get_reportitem(file)
    create_report(report_src)