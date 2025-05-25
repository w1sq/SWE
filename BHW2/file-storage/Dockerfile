FROM golang:1.24-alpine AS builder

WORKDIR /app

# Copy go.mod and go.sum for dependency resolution
COPY file-storage/go.mod file-storage/go.sum ./

# Copy the shared api module
COPY api ./api

# Download dependencies (using the local api module)
RUN go mod download

# Copy the rest of the service source code
COPY file-storage/. ./

# Build the service
RUN go build -o file-storage ./cmd/main.go

# Final image
FROM alpine:latest

WORKDIR /root/
COPY --from=builder /app/file-storage .
EXPOSE 50051

CMD ["./file-storage"]