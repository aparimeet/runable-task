from .shell import execute_shell_command

def _run_xdotool(command):
    return execute_shell_command(f"xdotool {command}")

def mouse_move(x, y):
    return _run_xdotool(f"mousemove {x} {y}")

def mouse_click(button=1):
    return _run_xdotool(f"click {button}")

def type_text(text):
    return _run_xdotool(f"type '{text}'")

def send_key(key):
    return _run_xdotool(f"key {key}") 