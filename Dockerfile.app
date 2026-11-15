# Release
FROM alpine:3.24
WORKDIR /app
COPY --from=app-only /app/app /app/app
#COPY --from=builder /app/json/data.json /app/json/data.json
CMD ["/app/app"]
