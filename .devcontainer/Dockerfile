# .devcontainer/Dockerfile

FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

ARG DEBIAN_FRONTEND=noninteractive
ARG USER=vscode

# --- Install system dependencies ---
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    make \
    build-essential \
    git \
    curl \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    llvm \
    libncurses5-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libffi-dev \
    liblzma-dev \
    python3-dev \
    python3-pip \
    bash-completion \
    && rm -rf /var/lib/apt/lists/*

# --- Install pyenv + Poetry ---
USER ${USER}
ENV HOME="/home/${USER}"
ENV PYENV_ROOT="${HOME}/.pyenv"
ENV PATH="${PYENV_ROOT}/shims:${PYENV_ROOT}/bin:${HOME}/.local/bin:$PATH"

ARG PYTHON_VERSION=3.10

RUN curl https://pyenv.run | bash && \
    pyenv install ${PYTHON_VERSION} && \
    pyenv global ${PYTHON_VERSION} && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    poetry self update 1.8.4 && \
    poetry config virtualenvs.in-project false
