import os
from fastapi import FastAPI
from pydantic import BaseModel
from . import context
from .tools import filesystem, shell, gui, code_executor

app = FastAPI()

class Agent:
    def __init__(self, task):
        self.task = task
        self.workspace = f"/app/workspace/{os.getpid()}"
        os.makedirs(self.workspace, exist_ok=True)
        os.chdir(self.workspace)
        
        initial_plan = f"The initial task is: {self.task}. I need to figure out how to accomplish this."
        context.set_plan(initial_plan)

    def run(self):
        while True:
            ctx = context.get_context()
            print("Current plan:", ctx["plan"])

            # 1. Create a file
            action_result = filesystem.create_file("test.txt", "Hello from the agent!")
            context.update_history("filesystem.create_file", action_result)
            
            # 2. List files
            action_result = shell.execute_shell_command("ls -l")
            context.update_history("shell.execute_shell_command", action_result)
            
            # 3. Run some python code
            action_result = code_executor.execute_code("print('Hello from Jupyter!')")
            context.update_history("code_executor.execute_code", action_result)

            break

        final_summary = "I have created a file, listed the files in the directory, and executed a print statement in python."
        context.set_summary(final_summary)
        print("Agent finished task.")
        return context.get_context()

class Task(BaseModel):
    task: str

@app.post("/run")
async def run_agent(task: Task):
    agent = Agent(task.task)
    result = agent.run()
    return {"status": "completed", "result": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 