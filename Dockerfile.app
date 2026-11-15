# Release
FROM alpine:3.24
WORKDIR /app
COPY --from=app-only app/app-linux-amd64 /app/app
CMD ["/app/app"]
