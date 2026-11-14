# Building
FROM python:3.14-slim-bookworm AS builder
# Preliminary steps
WORKDIR /app
RUN pip install --no-cache-dir --upgrade pip
# Nuitka build requirements
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential patchelf \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir nuitka python-dotenv==1.1.1
# Configuration
ENV OUTPUT_DIR=/app/bin
ENV OUTPUT_FILENAME=app
# Create output directory
RUN mkdir -p ${OUTPUT_DIR}
# Copy source code
COPY . .
# Build the application
RUN python -m nuitka \
    --mode=onefile \
    --output-dir=${OUTPUT_DIR} \
    --output-filename=${OUTPUT_FILENAME} \
    src/main.py

# Export only the executable, without a runtime image.
FROM scratch AS binary
COPY --from=builder /app/bin/app /app

# Release
FROM debian:bookworm-slim AS runtime
WORKDIR /app
COPY --from=builder /app/bin/app /app/app
COPY json/data.json /app/json/data.json
RUN chmod +x /app/app
CMD ["/app/app"]
