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

# Switch to the vscode user
USER vscode