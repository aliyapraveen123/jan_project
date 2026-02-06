#!/bin/bash

# Install system dependencies for FFmpeg (needed for audio processing)
apt-get update && apt-get install -y ffmpeg

# Install Python dependencies
pip install -r requirements.txt
