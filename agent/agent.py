import os
from . import context
from .tools import filesystem, shell, gui, code_executor

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

            # Simple "planner" - for now, we'll just execute a few commands
            # In a real agent, this would be an LLM call
            
            # 1. Create a file
            action_result = filesystem.create_file("test.txt", "Hello from the agent!")
            context.update_history("filesystem.create_file", action_result)
            
            # 2. List files
            action_result = shell.execute_shell_command("ls -l")
            context.update_history("shell.execute_shell_command", action_result)
            
            # 3. Run some python code
            action_result = code_executor.execute_code("print('Hello from Jupyter!')")
            context.update_history("code_executor.execute_code", action_result)

            # For now, we'll just run once and break
            break

        final_summary = "I have created a file, listed the files in the directory, and executed a print statement in python."
        context.set_summary(final_summary)
        print("Agent finished task.")


if __name__ == "__main__":
    import sys
    task = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "No task provided."
    agent = Agent(task)
    agent.run() 