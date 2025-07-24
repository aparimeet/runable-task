import atexit
import subprocess
from jupyter_client import BlockingKernelClient
from jupyter_client.connect import find_connection_file
import time

class CodeExecutor:
    def __init__(self):
        # Start a Jupyter kernel as a subprocess
        self.kernel_process = subprocess.Popen(['jupyter', 'kernel', '--KernelManager.autorestart=True'])
        
        # Wait for the connection file to be created
        self.connection_file = ""
        for _ in range(10):
            try:
                self.connection_file = find_connection_file()
                break
            except RuntimeError:
                time.sleep(0.5)
        
        if not self.connection_file:
            raise RuntimeError("Could not find Jupyter kernel connection file.")

        self.kc = BlockingKernelClient()
        self.kc.load_connection_file(self.connection_file)
        self.kc.start_channels()
        atexit.register(self.__del__)

    def __del__(self):
        if hasattr(self, 'kc'):
            self.kc.stop_channels()
        if hasattr(self, 'kernel_process') and self.kernel_process.poll() is None:
            self.kernel_process.terminate()
            self.kernel_process.wait()

    def execute_code(self, code):
        self.kc.execute(code)
        reply = self.kc.get_shell_msg(timeout=5)
        
        # This is a simplified way to get output. 
        # A real implementation would handle different message types.
        if reply['content']['status'] == 'ok':
            return reply['content']
        else:
            return reply['content']['traceback']

# This will be instantiated on demand
code_executor = None

def get_code_executor():
    global code_executor
    if code_executor is None:
        code_executor = CodeExecutor()
    return code_executor 