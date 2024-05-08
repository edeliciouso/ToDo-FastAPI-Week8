from fastapi import Body, FastAPI, HTTPException, Response, status
from pydantic import BaseModel

app = FastAPI()

todo_db = [{"id": 1, "title": "Do the project", "complete": False},
           {"id": 2, "title": "Wash the dishes", "complete": True},
           {"id": 3, "title": "Mop the floor", "complete": False}]

class tasks(BaseModel):
    id: int
    title: str
    complete: bool = False

# Get all Tasks / ToDos
@app.get("/tasks")
def get_tasks():
    return {"all_todo": todo_db}

# Create a Task / ToDo
@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_tasks(tasks: tasks):
    todo_db.append(tasks.model_dump())
    return {"new_todo": tasks}

# Find a Task / ToDo based on their ID
def find_task(id):
    for x in todo_db:
        if x["id"] == id:
            return x
    return None

# Search one Task / ToDo by ID
@app.get("/tasks/{id}")
def get_task(id: int, response: Response):
    task = find_task(id)
    if not task:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"warning": f"task with this ID of {id} is not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"task with this ID of {id} is not found")
    return {"todo_id": task}

# Find a Task / ToDo's index
def find_index(id):
    for i, j in enumerate(todo_db):
        if j["id"] == id:
            return i

# Delete a Task / ToDo
@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int):
    index = find_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"task with this ID of {id} is not found")
    todo_db.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update a Task / ToDo
@app.put("/tasks/{id}")
def update_task(id: int, task: tasks):
    index = find_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"task with this ID of {id} is not found")
    task_dict = task.model_dump()
    task_dict["id"] = id
    todo_db[index] = task_dict
    return {"updated_todo": task_dict}