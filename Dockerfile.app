# Building
FROM python:3.14.8-alpine3.24 AS builder
# Preliminary steps
WORKDIR /app
# Install dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir nuitka dotenv
# Nuitka build requirements
RUN apk add --no-cache build-base
RUN pip install --no-cache-dir patchelf
# Configuration
ENV OUTPUT_DIR=/app/bin
ENV OUTPUT_FILENAME=app
# Create output directory
RUN mkdir -p ${OUTPUT_DIR}
# Copy source code
COPY . .
# Build the application
RUN python -m nuitka \
    --standalone --onefile \
    --output-dir=${OUTPUT_DIR} \
    --output-filename=${OUTPUT_FILENAME} \
    src/main.py
# Link shared libraries
RUN mkdir -p /runtime-libs/tmp && chmod 1777 /runtime-libs/tmp && \
    { ldd ${OUTPUT_DIR}/${OUTPUT_FILENAME}; \
      find /usr/local/lib/python3.14 ${OUTPUT_DIR} -type f \
          \( -name '*.so' -o -name '*.so.*' \) \
          -exec sh -c 'for object do ldd "$object" || true; done' sh {} +; \
    } > /tmp/shared-dependencies && \
    if grep -q 'not found' /tmp/shared-dependencies; then \
        cat /tmp/shared-dependencies; exit 1; \
    fi && \
    awk '/=>/ { print $3 } /^\// { print $1 }' /tmp/shared-dependencies \
        | sort -u | while IFS= read -r library; do \
        [ -f "$library" ] || continue; \
        mkdir -p "/runtime-libs$(dirname "$library")"; \
        cp "$library" "/runtime-libs$library"; \
    done

# Release
FROM scratch
WORKDIR /app
COPY --from=builder /app/bin/app /app/app
COPY --from=builder /runtime-libs/ /
#COPY --from=builder /app/json/data.json /app/json/data.json
CMD ["/app/app"]
