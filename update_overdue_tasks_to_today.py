from todoist_api_python.api import TodoistAPI
from dotenv import load_dotenv
from datetime import datetime

import json
import requests
import subprocess
import sys
import os
import pprint

load_dotenv()

TODOIST_TOKEN = os.getenv("TODOIST_TOKEN", "")

class Todoist:
    def __init__(self, token):
        self.api = TodoistAPI(token)

    def add_child_task(self, todo, parent_task_id):
        task = self.api.add_task(
                content=todo['content'],
                project_id=todo['project_id'],
                section_id=todo['section_id'],
                due_string=todo['due'],
                parent_id=parent_task_id
                )
        return task

    def add_task(self, todo):
        task = self.api.add_task(
                content=todo['content'],
                project_id=todo['project_id'],
                section_id=todo['section_id'],
                due_string=todo['due'],
                )
        return task

    def get_projects(self):
        return self.api.get_projects()

    def get_project_sections(self, proj_id):
        return self.api.get_sections(project_id=proj_id)

    def get_filtered_tasks(self, filterStr):
        return self.api.get_tasks(filter=filterStr)

    def update_tasks_to_today(self, tasks):
        today = datetime.today()
        todayDate = today.strftime("%Y-%m-%d")
        for task in tasks:
            self.api.update_task(task_id=task.id, due_string=task.due.string, due_date=todayDate)
            print("Task: '" + task.content + "' has been moved to today")

    def send_notification(self, title, message, priority, tags):
        requests.post("https://ntfy.sh/todoist_updates_65279986",
            data=message,
            headers={
                "Title": title,
                "Priority": priority,
                "Tags": tags
            })

def main():
    todoist = Todoist(TODOIST_TOKEN)
    try:
        overdue_tasks = todoist.get_filtered_tasks("overdue")
        if len(overdue_tasks) != 0:
            todoist.update_tasks_to_today(overdue_tasks)
            todoist.send_notification("Tasks successfully moved", "Yesterday's tasks have been moved to today.", "low", "pushpin")
    except Exception as error:
        todoist.send_notification("Tasks could not be moved", "Yesterday's tasks have not been moved to today.", "high", "no_entry_sign")
        print(error)

if __name__ == "__main__":
    main()

