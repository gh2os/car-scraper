# Use official Debian-based Python image
FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    unzip \
    direnv \
    jq \
    curl \
    software-properties-common \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set up direnv hook for bash
RUN echo 'eval "$(direnv hook bash)"' >> /etc/bash.bashrc

# Copy and install Python dependencies
COPY requirements.txt /tmp/

USER vscode

RUN pip install --no-cache-dir --requirement /tmp/requirements.txt