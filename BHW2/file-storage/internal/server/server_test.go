package server

import (
	"context"
	"os"
	"testing"

	pb "github.com/w1sq/SWE/BHW2/api/file-storage"
)

func TestStoreAndGetFile(t *testing.T) {
	s := NewFileStorageServer()
	defer os.RemoveAll("./data")

	// Store file
	storeResp, err := s.StoreFile(context.Background(), &pb.StoreFileRequest{
		Filename: "test.txt",
		Content:  []byte("test content"),
	})
	if err != nil {
		t.Fatalf("StoreFile error: %v", err)
	}

	// Get file
	getResp, err := s.GetFile(context.Background(), &pb.GetFileRequest{
		FileId: storeResp.FileId,
	})
	if err != nil {
		t.Fatalf("GetFile error: %v", err)
	}
	if getResp.Filename != "test.txt" {
		t.Errorf("expected filename 'test.txt', got '%s'", getResp.Filename)
	}
	if string(getResp.Content) != "test content" {
		t.Errorf("expected content 'test content', got '%s'", string(getResp.Content))
	}
}

func TestGetFile_NotFound(t *testing.T) {
	s := NewFileStorageServer()
	_, err := s.GetFile(context.Background(), &pb.GetFileRequest{FileId: "nonexistent"})
	if err == nil {
		t.Error("expected error for nonexistent file, got nil")
	}
}
