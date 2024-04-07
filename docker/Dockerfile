# syntax=docker/dockerfile:1.4

# Separate builder image that builds the required venv
FROM python:3.12.2-bullseye AS builder

# Set working directory
WORKDIR /app

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/opt/venv/bin:$PATH"

# Install OS package dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential && \
    rm -rf /var/lib/apt/lists/*

# Setup the virtualenv
RUN python3 -m venv /opt/venv

# Install Python dependencies
COPY --link app/requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# Runner image, uses a slim image and copies the app code + venv
FROM python:3.12.2-slim-bullseye AS runner-image

# Set environment variables
ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Install any runtime dependencies
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        curl && \
	apt-get clean && rm -rf /var/lib/apt/lists/*

# Create a non-root user to run the script from
RUN useradd --create-home -u 1000 python

# Copy the venv created in the buidler image and the app code
# Use `chown` and `chmod` to set the correct permissions
# TODO: Check --chmod to set the correct permissions. Should be 500 and 400
COPY --link --from=builder --chown=1000:1000 /opt/venv /opt/venv
COPY --link --chown=1000:1000 ./app /home/python/app

# Run as the python user from this point
USER 1000

ENV PATH="/opt/venv/bin:$PATH"


WORKDIR /home/python/app
ENTRYPOINT ["python", "application.py"]
