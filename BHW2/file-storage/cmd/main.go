package main

import (
	"log"
	"net"

	pb "github.com/w1sq/SWE/BHW2/api/file-storage"
	"github.com/w1sq/SWE/BHW2/file-storage/internal/server"

	"google.golang.org/grpc"
)

func main() {
	lis, err := net.Listen("tcp", ":50051")
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}

	grpcServer := grpc.NewServer()
	pb.RegisterFileStoringServiceServer(grpcServer, server.NewFileStorageServer())

	log.Println("File Storage Service listening on :50051")
	if err := grpcServer.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
