SERVICES := gateway file-storage analysis
PROTO_FILES := $(wildcard api/*/*.proto)

.PHONY: all proto build docker

all: proto build

proto:
	@for proto in $(PROTO_FILES); do \
	  dir=$$(dirname $$proto); \
	  protoc -I=$$dir \
	    --go_out=$$dir --go_opt=paths=source_relative \
	    --go-grpc_out=$$dir --go-grpc_opt=paths=source_relative \
	    $$proto; \
	done

build:
	@for service in $(SERVICES); do \
	  cd $$service && go build ./... ; \
	done

docker:
	@for service in $(SERVICES); do \
	  docker build -t $$service ./$$service ; \
	done