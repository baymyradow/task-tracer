import os
import json
import typer
from datetime import datetime
from rich.console import Console
from rich.table import Table
from .enums import TaskStatus

TASKS_JSON = 'tasks.json'

app = typer.Typer()

console = Console()

def load_tasks():
    if not os.path.exists(TASKS_JSON):
        with open(TASKS_JSON, 'w') as file:
            json.dump([], file)
        return []
    with open(TASKS_JSON, 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []
        

def save_tasks(tasks):
    with open(TASKS_JSON, 'w') as file:
        json.dump(tasks, file)

def get_next_id(tasks):
    return max([task['id'] for task in tasks], default=0) + 1

@app.command(name='add')
def create_task(description: str):
    tasks = load_tasks()
    task_id = get_next_id(tasks)
    current_time = datetime.now()
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    
    new_task = {
        'id': task_id,
        'description': description,
        'status': TaskStatus.TODO,
        'created_at': formatted_time,
        'updated_at': formatted_time
    }
    tasks.append(new_task)
    save_tasks(tasks)
    console.print(f'[green]Task created successfully. (ID: {task_id})[/green]')


@app.command(name='list')
def get_tasks_list(status: TaskStatus | None = None):
    tasks = load_tasks()
    if status:
        tasks = [task for task in tasks if task['status'] == status]
    if not tasks:
        console.print('[red]No tasks found.[/red]')
        return

    table = Table(header_style='bold magenta')
    table.add_column('#')
    table.add_column('Description')
    table.add_column('Status')
    table.add_column('Created at')
    table.add_column('Updated at')

    for task in tasks:
        if task['status'] == TaskStatus.TODO:
            status_color = 'red'
        elif task['status'] == TaskStatus.INPROGRESS:
            status_color = 'yellow'
        elif task['status'] == TaskStatus.DONE:
            status_color = 'green'
        table.add_row(
            str(task['id']),
            task['description'],
            f'[{status_color}]{task["status"]}[/{status_color}]',
            task['created_at'],
            task['updated_at']
        )
    console.print(table)

@app.command(name='update')
def update_task(task_id: int, description: str):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['description'] = description
            task['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_tasks(tasks)
            console.print(f'[green]Task updated successfully. (ID: {task_id})[/green]')
            return
    console.print(f'[red]Task not found with given id. (ID: {task_id})[/red]')


@app.command(name='delete')
def delete_task(task_id: int):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            tasks.remove(task)
            save_tasks(tasks)
            console.print(f'[green]Task deleted successfully. (ID: {task_id})[/green]')
            return
    console.print(f'[red]Task not found with given id. (ID: {task_id})[/red]')
                

    








        