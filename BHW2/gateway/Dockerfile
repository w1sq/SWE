FROM golang:1.24-alpine AS builder

WORKDIR /app

# Install protoc and required tools
RUN apk add --no-cache protobuf-dev
RUN go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
RUN go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest

# Copy the shared api module
COPY api ./api

# Copy go.mod and go.sum for dependency resolution
COPY gateway/go.mod gateway/go.sum ./

# Download dependencies
RUN go mod download

# Copy gateway module
COPY gateway/. ./

# Build the application
RUN go build -o gateway ./cmd/main.go

FROM alpine:latest

WORKDIR /root/
COPY --from=builder /app/gateway .
EXPOSE 8080

CMD ["./gateway"]