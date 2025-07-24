# runable-task

This project uses an orchestrator to manage tasks running inside Firecracker microVMs.

## Prerequisites

Before you begin, ensure you have the following installed and configured:

1.  **Firecracker:** The `firecracker` binary must be in your system's `PATH`.
2.  **Kernel and Root Filesystem:** A `vmlinux` kernel file and `rootfs.ext4` root filesystem must be present in the `orchestrator` directory.
3.  **Permissions:** The user running the orchestrator must have passwordless `sudo` privileges for the `modprobe` and `ip` commands, as they are required to set up network devices for Firecracker.

## Setup

### Orchestrator

1.  Install the required dependencies from the project root:
    ```bash
    pip install -r orchestrator/requirements.txt
    ```

### Agent

The agent runs inside a Docker container.

1.  From the project root, build the Docker image:
    ```bash
    docker build -t runable-agent ./agent
    ```

## Running the Orchestrator

1.  Start the FastAPI server from the project root directory.
    ```bash
    uvicorn orchestrator.main:app --host 127.0.0.1 --port 8000
    ```

## Interacting with the Orchestrator

### Schedule a Task

Use `curl` to send a POST request to the `/schedule` endpoint. This will create a new job and launch a Firecracker VM in the background.

```bash
curl -X POST "http://127.0.0.1:8000/schedule" \
-H "Content-Type: application/json" \
-d '{"task": "generate a simple python script"}'
```

This will return a `job_id`.

### Check Task Status

Use the `job_id` to check the status of the task. The status will transition from `queued` to `running` and finally to `completed`.

```bash
curl http://127.0.0.1:8000/status/{your_job_id}
```

Replace `{your_job_id}` with the ID you received from the schedule request.
