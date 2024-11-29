# Flask - Celery - Redis - Flower using Uv on Docker

This project demonstrates how to set up a **Flask** application with **Celery** for background task processing, **Redis** as the message broker, **Flower** for monitoring Celery tasks, and **`uv`** (a fast Python package manager written in Rust) for dependency management — all within a **Docker** containerized environment.

## Features

- **Flask**: A lightweight web application framework.
- **Celery**: An asynchronous task queue/job queue system.
- **Redis**: Message broker for Celery.
- **Flower**: Real-time monitoring of Celery tasks.
- **`uv`**: Fast Python package manager written in Rust (optional, but recommended).
- **Docker**: Containerized deployment for Flask, Redis, Celery, and Flower.

## Prerequisites

Before you begin, ensure that the following are installed on your system:

- **Docker** and **Docker Compose**.
- **`uv`** (optional but recommended for development), which is a fast Python package manager written in Rust.
  
  To install `uv`, use:

  ```bash
  pipx install uv

## Clone Repository
-
  ```bash
  git clone https://github.com/tamamhuda/flask_celery_redis_flower
-
  ```bash
  cd flask_celery_redis_flower

## Run Docker Compose
-
  To run `docker compose`, use:

  ```bash
  docker compose up --build
