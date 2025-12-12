import json
import os
from flask import Flask, render_template, request

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def loadTasks():
    with open(os.path.join(BASE_DIR, "tasks.json"), "r") as jsonFile:
        return json.load(jsonFile)

@app.post("/update-task")
def updateTasks():
    data = request.form

    taskID = data.get("taskID")
    field = data.get("field")
    value = data.get("value")

    with open(os.path.join(BASE_DIR, "tasks.json"), "r") as jsonFile:
        jsonData = json.load(jsonFile)
        
        for element in jsonData:
            if element["id"] == int(taskID):
                element[field] = str(value).strip()
    
    with open(os.path.join(BASE_DIR, "tasks.json"), "w") as jsonFile:
        json.dump(jsonData, jsonFile, indent=4)

    return ""

@app.post("/delete-task")
def deleteTask():
    data = request.form

    taskID = data.get("taskID")

    with open(os.path.join(BASE_DIR, "tasks.json"), "r") as jsonFile:
        jsonData = json.load(jsonFile)

        for element in jsonData:
            if element["id"] == int(taskID):
                jsonData.pop(jsonData.index(element))
    
    with open(os.path.join(BASE_DIR, "tasks.json"), "w") as jsonFile:
        json.dump(jsonData, jsonFile, indent=4)

    return ""

@app.post("/add-task")
def addTask():
    with open(os.path.join(BASE_DIR, "tasks.json"), "r") as jsonFile:
        jsonData = json.load(jsonFile)

    id = 0
    for element in jsonData:
        id += 1
    id += 1

    newTask = {
        "id": id,
        "taskName": "New Task",
        "dueDate": "-",
        "dueTime": "-"
    }

    jsonData.append(newTask)

    with open(os.path.join(BASE_DIR, "tasks.json"), "w") as jsonFile:
        json.dump(jsonData, jsonFile, indent=4)

    return render_template("partials/tasks.html", t=newTask)

@app.route("/")
def main():
    tasks = loadTasks()
    return render_template("index.html", tasks=tasks)

if __name__ == "__main__":
    app.run(debug=True)