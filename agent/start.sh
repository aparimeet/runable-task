#!/bin/bash
set -e

# Start Xvfb
Xvfb :1 -screen 0 1280x800x24 &
export DISPLAY=:1

# Start VNC server
x11vnc -passwdfile /home/agent/.vnc/passwd -display :1 -N -forever -shared &

# Start noVNC
/usr/share/novnc/utils/launch.sh --vnc localhost:5900 --listen 6080 &

# Start Jupyter
jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --NotebookApp.token='' --NotebookApp.password='' 