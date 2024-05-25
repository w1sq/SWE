package grpcclient

import (
	"context"
	"time"

	pb "github.com/w1sq/SWE/BHW2/api/analysis"

	"google.golang.org/grpc"
)

type AnalysisClient struct {
	client pb.AnalysisServiceClient
}

func NewAnalysisClient(addr string) (*AnalysisClient, error) {
	conn, err := grpc.Dial(addr, grpc.WithInsecure(), grpc.WithBlock(), grpc.WithTimeout(3*time.Second))
	if err != nil {
		return nil, err
	}
	client := pb.NewAnalysisServiceClient(conn)
	return &AnalysisClient{client: client}, nil
}

func (a *AnalysisClient) AnalyzeFile(ctx context.Context, fileID string) (*pb.AnalyzeFileResponse, error) {
	return a.client.AnalyzeFile(ctx, &pb.AnalyzeFileRequest{FileId: fileID})
}

func (a *AnalysisClient) GenerateWordCloud(ctx context.Context, fileID string) (*pb.WordCloudResponse, error) {
	return a.client.GenerateWordCloud(ctx, &pb.WordCloudRequest{FileId: fileID})
}
