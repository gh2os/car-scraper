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
    fonts-liberation \
    libnss3 \
    libxss1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libdrm2 \
    libgbm1 \
    chromium \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set up direnv hook for bash
RUN echo 'eval "$(direnv hook bash)"' >> /etc/bash.bashrc

# Copy and install Python dependencies
COPY requirements.txt /tmp/

USER vscode

RUN pip install --no-cache-dir --requirement /tmp/requirements.txt

# Optional: Set display to avoid Chrome crash
ENV DISPLAY=:99