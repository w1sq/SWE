package main

import (
	"log"
	"net"

	"github.com/w1sq/SWE/BHW2/analysis/internal/server"
	pb "github.com/w1sq/SWE/BHW2/api/analysis"

	"google.golang.org/grpc"
)

func main() {
	lis, err := net.Listen("tcp", ":50052")
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}

	grpcServer := grpc.NewServer()
	pb.RegisterAnalysisServiceServer(grpcServer, server.NewAnalysisServer())

	log.Println("Analysis Service listening on :50052")
	if err := grpcServer.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
