# Use any Debian/Ubuntu-based image
FROM mcr.microsoft.com/devcontainers/base:ubuntu

# Install Terraform and dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    unzip \
    direnv \
    jq \
    curl \
    software-properties-common \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set up direnv hook for bash (default shell inside container)
RUN echo 'eval "$(direnv hook bash)"' >> /etc/bash.bashrc

# Copy the requirements.txt file into the container
COPY requirements.txt /home/vscode/requirements.txt

# Switch to the vscode user
USER vscode

# Install Python dependencies
RUN pip install -r /home/vscode/requirements.txt

# Install Playwright and its browser dependencies
RUN playwright install
