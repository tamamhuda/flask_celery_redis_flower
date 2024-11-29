# Install uv
FROM python:3.12-slim

# Download the latest installer
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Change the working directory to the `app` directory
WORKDIR /app

# # Install dependencies
COPY pyproject.toml .

RUN uv venv /opt/venv
# # # Use the virtual environment automatically
ENV VIRTUAL_ENV=/opt/venv
# # Place entry points in the environment at the front of the path
ENV PATH="/opt/venv/bin:$PATH"

RUN uv pip install -r pyproject.toml
# COPY . .
# RUN uv pip install -e .

# Copy the app files into the container
COPY . .

# Expose port for Flask
EXPOSE 5001

CMD ["gunicorn", "--bind", "0.0.0.0:5001" ,"--workers", "3", "app:app"]