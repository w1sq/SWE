package server

import (
	"bytes"
	"context"
	"errors"
	"io"
	"net/http"
	"testing"

	pb "github.com/w1sq/SWE/BHW2/api/analysis"
)

type mockFileStorage struct{}

func (m *mockFileStorage) GetFile(ctx context.Context, fileID string) (string, []byte, error) {
	if fileID == "empty" {
		return "empty.txt", []byte(""), nil
	}
	if fileID == "newlines" {
		return "newlines.txt", []byte("\n\n\n"), nil
	}
	return "test.txt", []byte("Hello\nWorld\n\nTest file."), nil
}

type errorFileStorage struct{}

func (e *errorFileStorage) GetFile(ctx context.Context, fileID string) (string, []byte, error) {
	return "", nil, errors.New("not found")
}

type errorHTTPFileStorage struct{}

func (e *errorHTTPFileStorage) GetFile(ctx context.Context, fileID string) (string, []byte, error) {
	return "", nil, errors.New("file storage error")
}

func TestAnalyzeFile_Success(t *testing.T) {
	s := &AnalysisServer{FileStorage: &mockFileStorage{}}
	resp, err := s.AnalyzeFile(context.Background(), &pb.AnalyzeFileRequest{FileId: "1"})
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if resp.Paragraphs != 3 {
		t.Errorf("expected 3 paragraphs, got %d", resp.Paragraphs)
	}
	if resp.Words != 4 {
		t.Errorf("expected 4 words, got %d", resp.Words)
	}
	if resp.Characters != 23 {
		t.Errorf("expected 23 characters, got %d", resp.Characters)
	}
}

func TestAnalyzeFile_Error(t *testing.T) {
	s := &AnalysisServer{FileStorage: &errorFileStorage{}}
	_, err := s.AnalyzeFile(context.Background(), &pb.AnalyzeFileRequest{FileId: "1"})
	if err == nil {
		t.Error("expected error, got nil")
	}
}

func TestAnalyzeFile_Empty(t *testing.T) {
	s := &AnalysisServer{FileStorage: &mockFileStorage{}}
	resp, err := s.AnalyzeFile(context.Background(), &pb.AnalyzeFileRequest{FileId: "empty"})
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if resp.Paragraphs != 0 || resp.Words != 0 || resp.Characters != 0 {
		t.Errorf("expected all zeros, got %v", resp)
	}
}

func TestAnalyzeFile_OnlyNewlines(t *testing.T) {
	s := &AnalysisServer{FileStorage: &mockFileStorage{}}
	resp, err := s.AnalyzeFile(context.Background(), &pb.AnalyzeFileRequest{FileId: "newlines"})
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if resp.Paragraphs != 0 || resp.Words != 0 || resp.Characters != 3 {
		t.Errorf("expected 0 paragraphs, 0 words, 3 characters, got %v", resp)
	}
}

func TestGenerateWordCloud_FileStorageError(t *testing.T) {
	s := &AnalysisServer{FileStorage: &errorHTTPFileStorage{}}
	_, err := s.GenerateWordCloud(context.Background(), &pb.WordCloudRequest{FileId: "fail"})
	if err == nil {
		t.Error("expected error, got nil")
	}
}

// Test GenerateWordCloud success (mock http)
func TestGenerateWordCloud_Success(t *testing.T) {
	s := &AnalysisServer{FileStorage: &mockFileStorage{}}

	// Patch http.Post for this test
	origPost := httpPost
	httpPost = func(url, contentType string, body io.Reader) (*http.Response, error) {
		return &http.Response{
			StatusCode: 200,
			Body:       io.NopCloser(bytes.NewReader([]byte("imagebytes"))),
		}, nil
	}
	defer func() { httpPost = origPost }()

	resp, err := s.GenerateWordCloud(context.Background(), &pb.WordCloudRequest{FileId: "1"})
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if string(resp.Image) != "imagebytes" {
		t.Errorf("expected imagebytes, got %s", string(resp.Image))
	}
}

// Test GenerateWordCloud http error
func TestGenerateWordCloud_HttpError(t *testing.T) {
	s := &AnalysisServer{FileStorage: &mockFileStorage{}}

	origPost := httpPost
	httpPost = func(url, contentType string, body io.Reader) (*http.Response, error) {
		return nil, errors.New("http error")
	}
	defer func() { httpPost = origPost }()

	_, err := s.GenerateWordCloud(context.Background(), &pb.WordCloudRequest{FileId: "1"})
	if err == nil {
		t.Error("expected error, got nil")
	}
}

// Test GenerateWordCloud non-200 status
func TestGenerateWordCloud_Non200(t *testing.T) {
	s := &AnalysisServer{FileStorage: &mockFileStorage{}}

	origPost := httpPost
	httpPost = func(url, contentType string, body io.Reader) (*http.Response, error) {
		return &http.Response{
			StatusCode: 500,
			Body:       io.NopCloser(bytes.NewReader([]byte("fail"))),
		}, nil
	}
	defer func() { httpPost = origPost }()

	_, err := s.GenerateWordCloud(context.Background(), &pb.WordCloudRequest{FileId: "1"})
	if err == nil {
		t.Error("expected error, got nil")
	}
}

// Test GenerateWordCloud read body error
func TestGenerateWordCloud_ReadBodyError(t *testing.T) {
	s := &AnalysisServer{FileStorage: &mockFileStorage{}}

	origPost := httpPost
	httpPost = func(url, contentType string, body io.Reader) (*http.Response, error) {
		return &http.Response{
			StatusCode: 200,
			Body:       io.NopCloser(badReader{}),
		}, nil
	}
	defer func() { httpPost = origPost }()

	_, err := s.GenerateWordCloud(context.Background(), &pb.WordCloudRequest{FileId: "1"})
	if err == nil {
		t.Error("expected error, got nil")
	}
}

type badReader struct{}

func (badReader) Read(p []byte) (int, error) { return 0, errors.New("read error") }
func (badReader) Close() error               { return nil }
