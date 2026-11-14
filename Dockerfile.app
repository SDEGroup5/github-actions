# Building
FROM python:3.14.8-alpine3.24
# Preliminary steps
WORKDIR /app
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

# Release
FROM alpine:3.24.2
WORKDIR /app
COPY --from=0 /app/bin/app /app/app
COPY --from=0 /json/data.json /json/data.json
RUN chmod +x /app/app
CMD ["/app/app"]