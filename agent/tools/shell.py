import subprocess

def execute_shell_command(command, timeout=60):
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=True, # This will raise a CalledProcessError for non-zero exit codes
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"
    except subprocess.TimeoutExpired:
        return "Error: Command timed out" 