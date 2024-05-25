package handler

import (
	"bytes"
	"context"
	"errors"
	"mime/multipart"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/gin-gonic/gin"
	pb "github.com/w1sq/SWE/BHW2/api/analysis"
)

// Mocks for gRPC clients
type mockFileStorageClient struct{}

func (m *mockFileStorageClient) StoreFile(ctx context.Context, filename string, content []byte) (string, error) {
	if filename == "fail.txt" {
		return "", errors.New("store error")
	}
	return "file123", nil
}
func (m *mockFileStorageClient) GetFile(ctx context.Context, fileID string) (string, []byte, error) {
	if fileID == "notfound" {
		return "", nil, errors.New("not found")
	}
	return "test.txt", []byte("test content"), nil
}

type mockAnalysisClient struct{}

func (m *mockAnalysisClient) AnalyzeFile(ctx context.Context, fileID string) (*pb.AnalyzeFileResponse, error) {
	if fileID == "fail" {
		return nil, errors.New("fail")
	}
	return &pb.AnalyzeFileResponse{Paragraphs: 1, Words: 2, Characters: 3}, nil
}
func (m *mockAnalysisClient) GenerateWordCloud(ctx context.Context, fileID string) (*pb.WordCloudResponse, error) {
	return &pb.WordCloudResponse{Image: []byte("imagebytes")}, nil
}

type errorAnalysisClient struct{}

func (m *errorAnalysisClient) AnalyzeFile(ctx context.Context, fileID string) (*pb.AnalyzeFileResponse, error) {
	return nil, errors.New("fail")
}
func (m *errorAnalysisClient) GenerateWordCloud(ctx context.Context, fileID string) (*pb.WordCloudResponse, error) {
	return nil, errors.New("fail")
}

func TestUploadHandler_BadRequest(t *testing.T) {
	gin.SetMode(gin.TestMode)
	r := gin.New()
	h := &Handler{
		FileStorage: &mockFileStorageClient{},
		Analysis:    &mockAnalysisClient{},
	}
	r.POST("/upload", h.uploadHandler)

	w := httptest.NewRecorder()
	req := httptest.NewRequest("POST", "/upload", nil)
	r.ServeHTTP(w, req)

	if w.Code != http.StatusBadRequest {
		t.Errorf("expected 400, got %d", w.Code)
	}
}

func TestDownloadHandler_NotFound(t *testing.T) {
	gin.SetMode(gin.TestMode)
	r := gin.New()
	h := &Handler{
		FileStorage: &mockFileStorageClient{},
		Analysis:    &mockAnalysisClient{},
	}
	r.GET("/file/:id", h.downloadHandler)

	w := httptest.NewRecorder()
	req := httptest.NewRequest("GET", "/file/notfound", nil)
	r.ServeHTTP(w, req)

	if w.Code != http.StatusNotFound {
		t.Errorf("expected 404, got %d", w.Code)
	}
}

func TestAnalyzeHandler_Success(t *testing.T) {
	gin.SetMode(gin.TestMode)
	r := gin.New()
	h := &Handler{
		FileStorage: &mockFileStorageClient{},
		Analysis:    &mockAnalysisClient{},
	}
	r.POST("/analyze/:id", h.analyzeHandler)

	w := httptest.NewRecorder()
	req := httptest.NewRequest("POST", "/analyze/ok", bytes.NewBuffer(nil))
	r.ServeHTTP(w, req)

	if w.Code != http.StatusOK {
		t.Errorf("expected 200, got %d", w.Code)
	}
}

func TestUploadHandler_StoreError(t *testing.T) {
	gin.SetMode(gin.TestMode)
	r := gin.New()
	h := &Handler{
		FileStorage: &mockFileStorageClient{},
		Analysis:    &mockAnalysisClient{},
	}
	r.POST("/upload", h.uploadHandler)

	body := &bytes.Buffer{}
	writer := multipart.NewWriter(body)
	part, _ := writer.CreateFormFile("file", "fail.txt")
	part.Write([]byte("test"))
	writer.Close()

	req := httptest.NewRequest("POST", "/upload", body)
	req.Header.Set("Content-Type", writer.FormDataContentType())
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)

	if w.Code != http.StatusInternalServerError {
		t.Errorf("expected 500, got %d", w.Code)
	}
}

func TestWordCloudHandler_Error(t *testing.T) {
	gin.SetMode(gin.TestMode)
	r := gin.New()
	h := &Handler{
		FileStorage: &mockFileStorageClient{},
		Analysis:    &errorAnalysisClient{},
	}
	r.GET("/wordcloud/:id", h.wordCloudHandler)

	w := httptest.NewRecorder()
	req := httptest.NewRequest("GET", "/wordcloud/fail", nil)
	r.ServeHTTP(w, req)

	if w.Code != http.StatusInternalServerError {
		t.Errorf("expected 500, got %d", w.Code)
	}
}
