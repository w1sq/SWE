package server

import (
	"context"
	"time"

	pb "github.com/w1sq/SWE/BHW2/api/file-storage"
	"google.golang.org/grpc"
)

type FileStorageClient struct {
	client pb.FileStoringServiceClient
}

func NewFileStorageClient(addr string) (*FileStorageClient, error) {
	conn, err := grpc.Dial(addr, grpc.WithInsecure(), grpc.WithBlock(), grpc.WithTimeout(3*time.Second))
	if err != nil {
		return nil, err
	}
	client := pb.NewFileStoringServiceClient(conn)
	return &FileStorageClient{client: client}, nil
}

func (f *FileStorageClient) GetFile(ctx context.Context, fileID string) (string, []byte, error) {
	resp, err := f.client.GetFile(ctx, &pb.GetFileRequest{FileId: fileID})
	if err != nil {
		return "", nil, err
	}
	return resp.Filename, resp.Content, nil
}
