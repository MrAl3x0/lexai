FROM mcr.microsoft.com/devcontainers/python:3.9

RUN apt-get update && \
  apt-get install -y git-lfs && \
  git lfs install && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*