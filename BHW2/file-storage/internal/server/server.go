package server

import (
	"context"
	"fmt"
	"os"
	"path/filepath"
	"time"

	pb "github.com/w1sq/SWE/BHW2/api/file-storage"
)

type FileStorageServer struct {
	pb.UnimplementedFileStoringServiceServer
	storageDir string
}

func NewFileStorageServer() *FileStorageServer {
	const dir = "./data"
	os.MkdirAll(dir, 0755)
	return &FileStorageServer{storageDir: dir}
}

func (s *FileStorageServer) StoreFile(ctx context.Context, req *pb.StoreFileRequest) (*pb.StoreFileResponse, error) {
	fileID := generateFileID()
	filePath := filepath.Join(s.storageDir, fileID)
	err := os.WriteFile(filePath, req.Content, 0644)
	if err != nil {
		return nil, fmt.Errorf("failed to store file: %w", err)
	}
	metaPath := filePath + ".meta"
	os.WriteFile(metaPath, []byte(req.Filename), 0644)
	return &pb.StoreFileResponse{FileId: fileID}, nil
}

func (s *FileStorageServer) GetFile(ctx context.Context, req *pb.GetFileRequest) (*pb.GetFileResponse, error) {
	filePath := filepath.Join(s.storageDir, req.FileId)
	content, err := os.ReadFile(filePath)
	if err != nil {
		return nil, fmt.Errorf("file not found: %w", err)
	}
	metaPath := filePath + ".meta"
	filename, err := os.ReadFile(metaPath)
	if err != nil {
		filename = []byte("unknown")
	}
	return &pb.GetFileResponse{Filename: string(filename), Content: content}, nil
}

func generateFileID() string {
	return fmt.Sprintf("%d", time.Now().UnixNano())
}
