import os
import subprocess

def create_vm_config(job_id, kernel_image="vmlinux", rootfs="rootfs.ext4"):
    """Creates a Firecracker VM configuration file."""
    
    config = {
        "boot-source": {
            "kernel_image_path": kernel_image,
            "boot_args": "console=ttyS0 reboot=k panic=1 pci=off"
        },
        "drives": [
            {
                "drive_id": "rootfs",
                "path_on_host": rootfs,
                "is_root_device": True,
                "is_read_only": False
            }
        ],
        "machine-config": {
            "vcpu_count": 1,
            "mem_size_mib": 256
        }
    }
    
    config_path = f"/tmp/firecracker-{job_id}.json"
    with open(config_path, "w") as f:
        import json
        json.dump(config, f)
        
    return config_path

def start_vm(job_id, config_path):
    """Starts a Firecracker VM."""
    
    socket_path = f"/tmp/firecracker-{job_id}.socket"
    
    # In a real implementation, you would need to handle the Firecracker binary path
    command = f"firecracker --api-sock {socket_path} --config-file {config_path}"
    
    print(f"Starting VM for job {job_id} with command: {command}")
    # This is a placeholder. A real implementation would run this in the background
    # and manage the process.
    
    # subprocess.Popen(command, shell=True)
    
    return socket_path

def stop_vm(socket_path):
    """Stops a Firecracker VM."""
    
    # A real implementation would use the Firecracker API to shut down the VM.
    print(f"Stopping VM at {socket_path}") 