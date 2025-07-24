import os
import subprocess
import json

def setup_network_tap(job_id):
    """Sets up a TAP network device for the VM."""
    tap_name = f"fc-tap-{job_id}"
    host_ip = "172.16.0.1"
    guest_ip = "172.16.0.2"
    subnet_mask = "24"

    subprocess.run("sudo modprobe tun", shell=True, check=True)
    subprocess.run(f"sudo ip tuntap add dev {tap_name} mode tap", shell=True, check=True)
    subprocess.run(f"sudo ip addr add {host_ip}/{subnet_mask} dev {tap_name}", shell=True, check=True)
    subprocess.run(f"sudo ip link set dev {tap_name} up", shell=True, check=True)
    
    return tap_name, guest_ip

def cleanup_network_tap(tap_name):
    """Cleans up the TAP network device."""
    print(f"Cleaning up TAP device {tap_name}")
    subprocess.run(f"sudo ip link del {tap_name}", shell=True)

def create_vm_config(job_id, kernel_image="vmlinux", rootfs="rootfs.ext4"):
    """Creates a Firecracker VM configuration file."""
    
    #tap_name, guest_ip = setup_network_tap(job_id)
    
    config = {
        "boot-source": {
            "kernel_image_path": kernel_image,
            #"boot_args": f"console=ttyS0 reboot=k panic=1 ip={guest_ip}::172.16.0.1:255.255.255.0::eth0:off"
            "boot_args": f"console=ttyS0 reboot=k panic=1 pci=off"
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
        # "network-interfaces": [
        #     {
        #         "iface_id": "eth0",
        #         "guest_mac": "AA:FC:00:00:00:01",
        #         "host_dev_name": tap_name
        #     }
        # ]
    }
    
    config_path = f"/tmp/firecracker-{job_id}.json"
    with open(config_path, "w") as f:
        json.dump(config, f)
        
    #return config_path, guest_ip
    return config_path

def start_vm(job_id, config_path):
    """Starts a Firecracker VM."""
    
    socket_path = f"/tmp/firecracker-{job_id}.socket"
    
    # In a real implementation, you would need to handle the Firecracker binary path
    command = f"firecracker --api-sock {socket_path} --config-file {config_path}"
    
    print(f"Starting VM for job {job_id} with command: {command}")
    # This is a placeholder. A real implementation would run this in the background
    # and manage the process.
    
    subprocess.Popen(command, shell=True)
    
    return socket_path

def stop_vm(socket_path):
    """Stops a Firecracker VM."""

    #Simulate stopping of VM
    print(f"Stopping VM at {socket_path}")

    # try:
    #     # Use curl to send the shutdown command via the API socket
    #     command = f"curl --unix-socket {socket_path} -i -X PUT 'http://localhost/actions' -d '{{ \"action_type\": \"SendCtrlAltDel\" }}'"
    #     subprocess.run(command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    #     print(f"Successfully sent shutdown command to VM at {socket_path}")
    # except subprocess.CalledProcessError as e:
    #     print(f"Failed to stop VM at {socket_path}: {e}")
    # finally:
    #     # Cleanup network
    #     job_id = os.path.basename(socket_path).split('.')[0].replace('firecracker-', '')
    #     tap_name = f"fc-tap-{job_id}"
    #     cleanup_network_tap(tap_name)