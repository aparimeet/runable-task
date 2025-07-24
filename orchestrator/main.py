from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
import uuid
import asyncio
import httpx
from . import firecracker

app = FastAPI()

jobs = {}

class Task(BaseModel):
    task: str

@app.post("/schedule")
async def schedule_task(task: Task, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "queued", "task": task.task}
    
    #config_path, guest_ip = firecracker.create_vm_config(job_id)
    config_path = firecracker.create_vm_config(job_id)
    socket_path = firecracker.start_vm(job_id, config_path)

    jobs[job_id]["socket_path"] = socket_path
    #jobs[job_id]["guest_ip"] = guest_ip

    background_tasks.add_task(run_agent_job, job_id)
    return {"job_id": jobs[job_id]}

@app.get("/status/{job_id}")
async def get_status(job_id: str):
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if job["status"] == "complete":
        return f"Job completed. Download folder at: {job['project_folder']}\n"
    else:
        return f"Job not completed. Current job status: {job['status']}\n"


async def run_agent_job(job_id: str):
    project_folder = "path/to/example/project"
    jobs[job_id]["status"] = "running"
    jobs[job_id]["project_folder"] = project_folder

    task = jobs[job_id]['task']
    #guest_ip = jobs[job_id]['guest_ip']
    #agent_url = f"http://{guest_ip}:8000/run"

    #print(f"Running job {job_id} for task: {task} on VM with IP {guest_ip}")
    print(f"Running job {job_id} for task: {task} on VM")

    # Simulate agent task
    await asyncio.sleep(30)

    # try:
    #     async with httpx.AsyncClient() as client:
    #         response = await client.post(agent_url, json={"task": task}, timeout=120)
    #         response.raise_for_status()
            
    #         agent_result = response.json()
    #         jobs[job_id]["status"] = "completed"
    #         jobs[job_id]["result"] = agent_result
            
    # except httpx.RequestError as e:
    #     jobs[job_id]["status"] = "failed"
    #     jobs[job_id]["error"] = f"Agent communication error: {e}"
    # except Exception as e:
    #     jobs[job_id]["status"] = "failed"
    #     jobs[job_id]["error"] = f"An unexpected error occurred: {e}"
    # finally:
    #     # Stop the VM after the job is done
    #     firecracker.stop_vm(jobs[job_id]["socket_path"])
    #     print(f"Job {job_id} finished.")

    # Stop the VM after the job is done
    firecracker.stop_vm(jobs[job_id]["socket_path"])
    jobs[job_id]["status"] = "complete"
    print(f"Job {job_id} finished. Download folder at {jobs[job_id]["project_folder"]}")
