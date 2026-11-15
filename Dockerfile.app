# Release
FROM debian:bookworm-slim
WORKDIR /app
COPY --from=app-only app /app/app
CMD ["/app/app"]

