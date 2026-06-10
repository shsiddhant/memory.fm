
FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install gcc for Cythonize
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# UV Cache
ENV UV_CACHE_DIR="/app/.uv_cache"

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Change the working directory to the `app` directory
WORKDIR /app


# Copy dependencies list
COPY pyproject.toml uv.lock requirements.txt ./

# Install dependencies
RUN --mount=type=cache,target=UV_CACHE_DIR \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

# Copy the project into the image

# 1. Source Code
COPY src/ ./src/

# 2. FastAPI app
COPY apps/api/ ./apps/api/

# 3. Alembic Migration
COPY apps/alembic ./apps/alembic/

# 4. Entrypoint

COPY entrypoint.sh ./entrypoint.sh

# Sync the project
RUN --mount=type=cache,target=UV_CACHE_DIR \
    uv sync --locked

# Expose the port that the application listens on.
EXPOSE 8000

# Make entrypoint executable
RUN chmod +x ./entrypoint.sh && \
    chown -R appuser:appuser /app

USER appuser

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Set FastAPI app as default command
CMD ["uv", "run", "uvicorn", "apps.api.main:app", "--host=0.0.0.0", "--port=8000"]
