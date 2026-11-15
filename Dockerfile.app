# Release
FROM alpine:3.24
WORKDIR /app
COPY --from=app-only app /app/app
CMD ["/app/app"]
