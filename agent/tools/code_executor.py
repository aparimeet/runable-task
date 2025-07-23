import jupyter_client

class CodeExecutor:
    def __init__(self):
        self.kc = jupyter_client.KernelClient()
        self.kc.load_connection_file()
        self.kc.start_channels()

    def execute(self, code):
        self.kc.execute(code)
        reply = self.kc.get_shell_msg(timeout=60)
        
        # We can also get iopub messages for rich output (e.g., plots)
        # For now, we'll focus on the execution result
        
        status = reply['content']['status']
        if status == 'ok':
            return "Execution successful."
        elif status == 'error':
            error_content = reply['content']
            return f"Error: {error_content['ename']}: {error_content['evalue']}"

    def __del__(self):
        self.kc.stop_channels()

# This is a singleton to ensure we use the same kernel client
code_executor = CodeExecutor()

def execute_code(code):
    return code_executor.execute(code) 