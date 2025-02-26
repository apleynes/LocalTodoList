from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
TASKS_FILE = "tasks.txt"
DONE_TASKS_FILE = "done-tasks.txt"

def read_tasks(tasks_file=TASKS_FILE):
    if not os.path.exists(tasks_file):
        return []

    tasks = []
    with open(tasks_file, "r") as f:
        for line in f:
            if line.strip():
                task_text, status = line.strip().split("|")
                tasks.append({"text": task_text, "done": status == "done"})
    return tasks

def write_tasks(tasks, tasks_file=TASKS_FILE, append=False):
    read_mode = "a" if append else "w"
    with open(tasks_file, read_mode) as f:
        for task in tasks:
            status = "done" if task["done"] else "pending"
            f.write(f"{task['text']}|{status}\n")

@app.route("/")
def index():
    # return "Hello world!"
    show_done = request.args.get("show_done", "true") == "true"
    tasks = read_tasks()
    return render_template("index.html", tasks=tasks, show_done=show_done)

@app.route("/add", methods=["POST"])
def add_task():
    task_text = request.form.get("task", "").strip()
    if task_text:
        tasks = read_tasks()
        tasks.append({"text": task_text, "done": False})
        write_tasks(tasks)
    return redirect(url_for("index", show_done=request.args.get("show_done", "true")))

@app.route("/toggle/<int:task_id>")
def toggle_task(task_id):
    tasks = read_tasks()
    if 0 <= task_id < len(tasks):
        tasks[task_id]["done"] = not tasks[task_id]["done"]
        write_tasks(tasks)
    return redirect(url_for("index", show_done=request.args.get("show_done", "true")))

@app.route("/clear-done")
def clear_done():
    tasks = read_tasks()
    done_tasks = [task for task in tasks if task["done"]]
    tasks = [task for task in tasks if not task["done"]]
    write_tasks(tasks)
    write_tasks(done_tasks, tasks_file=DONE_TASKS_FILE, append=True)
    return redirect(url_for("index", show_done=request.args.get("show_done", "true")))

@app.route("/toggle-show-done")
def toggle_show_done():
    current = request.args.get("show_done", "true")
    new_value = "false" if current == "true" else "true"
    return redirect(url_for("index", show_done=new_value))

if __name__ == "__main__":
    app.run(debug=True)
