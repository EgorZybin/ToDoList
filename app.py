import os
from flask import Flask, request, render_template
from datetime import date

app = Flask(__name__)

date_today = date.today().strftime("%m_%d_%y")
date_today2 = date.today().strftime("%d-%B-%Y")

if 'tasks.txt' not in os.listdir('.'):
    with open('tasks.txt', 'w') as f:
        f.write('')


def get_task_list():
    with open('tasks.txt', 'r') as f:
        tasklist = f.readlines()
    return tasklist


def create_new_task_list():
    os.remove('tasks.txt')
    with open('tasks.txt', 'w') as f:
        f.write('')


def update_task_list(tasklist):
    os.remove('tasks.txt')
    with open('tasks.txt', 'w') as f:
        f.writelines(tasklist)


@app.route('/')
def home():
    return render_template('home.html', datetoday2=date_today2, tasklist=get_task_list(), l=len(get_task_list()))


# Function to clear the to-do list
@app.route('/clear')
def clear_list():
    create_new_task_list()
    return render_template('home.html', datetoday2=date_today2, tasklist=get_task_list(), l=len(get_task_list()))


# Function to add a task to the to-do list
@app.route('/addtask', methods=['POST'])
def add_task():
    task = request.form.get('newtask')
    with open('tasks.txt', 'a') as f:
        f.writelines(task + '\n')
    return render_template('home.html', datetoday2=date_today2, tasklist=get_task_list(), l=len(get_task_list()))


# Function to remove a task from the to-do list
@app.route('/deltask', methods=['GET'])
def remove_task():
    task_index = int(request.args.get('deltaskid'))
    tasklist = get_task_list()
    print(task_index)
    print(tasklist)
    if task_index < 0 or task_index > len(tasklist):
        return render_template('home.html', datetoday2=date_today2, tasklist=tasklist, l=len(tasklist),
                               mess='Invalid Index...')
    else:
        removed_task = tasklist.pop(task_index)
    update_task_list(tasklist)
    return render_template('home.html', datetoday2=date_today2, tasklist=tasklist, l=len(tasklist))


if __name__ == '__main__':
    app.run(debug=True)
