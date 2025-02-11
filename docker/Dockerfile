# syntax=docker/dockerfile:1

# Use the official Ubuntu image
FROM ubuntu:24.04

# Set the working directory
WORKDIR /

# Set non-interactive environment
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

# Install system dependencies and add the Python 3.11 PPA
RUN apt-get update && apt-get install -y \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y \
    zip \
    unzip \
    git \
    curl \
    python3.11 \
    python3.11-venv \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Copy the Moonshot application
COPY /moonshot /moonshot

# Set the working directory
WORKDIR /moonshot

# Copy the environment configuration file
RUN cp .env.example .env

# Create a virtual environment for Python 3.11.5 and install dependencies
RUN python3.11 -m venv venv
RUN ./venv/bin/pip install --upgrade pip
RUN ./venv/bin/pip install -r requirements.txt

# Add the virtual environment to the PATH
ENV PATH="/moonshot/venv/bin:$PATH"

# Copy the entry.sh script into the container
COPY ./entry.sh /entry.sh

# Make the script executable
RUN chmod +x /entry.sh

# Expose port 8000
EXPOSE 8000

# Use entry.sh as the entry point
ENTRYPOINT ["/entry.sh"]
