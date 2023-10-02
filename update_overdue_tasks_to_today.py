from todoist_api_python.api import TodoistAPI
import json
import requests
import subprocess
import sys

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
        for task in tasks:
            self.api.update_task(task_id=task.id, due_string="Today")
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
    token = 'f7bc5c37b3e3a745a8f375ff9f265b97b24ef468'
    todoist = Todoist(token)
    try:
        overdue_tasks = todoist.get_filtered_tasks("overdue")
        if len(overdue_tasks) != 0:
            todoist.update_tasks_to_today(overdue_tasks)
            todoist.send_notification("Tasks successfully moved", "Yesterday's tasks have been moved to today.", "high", "pushpin")
    except Exception as error:
        todoist.send_notification("Tasks could not be moved", "Yesterday's tasks have not been moved to today.", "high", "no_entry_sign")
        print(error)

if __name__ == "__main__":
    main()

