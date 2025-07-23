from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
import uuid
import asyncio
from . import firecracker

app = FastAPI()

jobs = {}

class Task(BaseModel):
    task: str

@app.post("/schedule")
async def schedule_task(task: Task, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "queued", "task": task.task}
    
    # This is where you would launch the Firecracker VM
    config_path = firecracker.create_vm_config(job_id)
    socket_path = firecracker.start_vm(job_id, config_path)
    
    jobs[job_id]["socket_path"] = socket_path # Store the socket path for later
    
    background_tasks.add_task(run_agent_job, job_id)
    return {"job_id": job_id}

@app.get("/status/{job_id}")
async def get_status(job_id: str):
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

async def run_agent_job(job_id: str):
    jobs[job_id]["status"] = "running"
    print(f"Running job {job_id} for task: {jobs[job_id]['task']}")
    
    # Simulate a long-running agent task
    await asyncio.sleep(30) 
    
    # In a real implementation, you would get the project folder path
    project_folder = "/path/to/generated/project" 
    
    jobs[job_id]["status"] = "completed"
    jobs[job_id]["project_folder"] = project_folder
    
    # Stop the VM after the job is done
    firecracker.stop_vm(jobs[job_id]["socket_path"])
    
    print(f"Job {job_id} completed.") 