FROM golang:1.24-alpine AS builder

WORKDIR /app

# Copy go.mod and go.sum for dependency resolution
COPY analysis/go.mod analysis/go.sum ./

# Copy the shared api module
COPY api ./api

# Download dependencies (using the local api module)
RUN go mod download

# Copy the rest of the service source code
COPY analysis/. ./

# Build the service
RUN go build -o analysis ./cmd/main.go

# Final image
FROM alpine:latest

WORKDIR /root/
COPY --from=builder /app/analysis .
EXPOSE 50052

CMD ["./analysis"]