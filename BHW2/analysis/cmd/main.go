package main

import (
	"log"
	"net"
	"os"

	"github.com/w1sq/SWE/BHW2/analysis/internal/server"
	pb "github.com/w1sq/SWE/BHW2/api/analysis"

	"google.golang.org/grpc"
)

func main() {
	fileStorageAddr := os.Getenv("FILE_STORAGE_ADDR")
	if fileStorageAddr == "" {
		fileStorageAddr = "file-storage:50051"
	}
	fileStorageClient, err := server.NewFileStorageClient(fileStorageAddr)
	if err != nil {
		log.Fatalf("failed to connect to file storage service: %v", err)
	}

	lis, err := net.Listen("tcp", ":50052")
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}

	grpcServer := grpc.NewServer()
	pb.RegisterAnalysisServiceServer(grpcServer, server.NewAnalysisServer(fileStorageClient))

	log.Println("Analysis Service listening on :50052")
	if err := grpcServer.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
