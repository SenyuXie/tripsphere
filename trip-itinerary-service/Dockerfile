# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Install the project into `/app`
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Ensure installed tools can be executed out of the box
ENV UV_TOOL_BIN_DIR=/usr/local/bin

# Install the project's dependencies using the lockfile and settings
COPY libs /app/libs
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

# Install OpenTelemetry auto instrumentation
RUN --mount=type=cache,target=/root/.cache/uv \
    uv run opentelemetry-bootstrap -a requirements | uv pip install --requirement -

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT []

ENV OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED="true" \
    OTEL_SERVICE_NAME="trip-itinerary-service" \
    OTEL_EXPORTER_OTLP_ENDPOINT="http://otel-collector:4317"

# Run the gRPC server by default
CMD ["python", "-m", "itinerary.server"]