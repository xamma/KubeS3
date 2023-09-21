# syntax=docker/dockerfile:1

# Use ARG for Python version, default to 3.11
ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim as base

# set ENVs for stdout and debug
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create non root user
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Copy the requirements file separately to leverage Docker's caching
COPY /src/requirements.txt /opt/requirements.txt

# Download dependencies with caching
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install -r /opt/requirements.txt

# Switch to non-privileged user
USER appuser

# Copy the source code into the container
COPY /src/main /app

# Expose the port that the application listens on
EXPOSE 8000

# Run the application
CMD python api.py
# CMD sh -c "sleep infinity"