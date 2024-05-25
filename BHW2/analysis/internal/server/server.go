package server

import (
	"bytes"
	"context"
	"encoding/json"
	"io"
	"net/http"
	"strings"

	pb "github.com/w1sq/SWE/BHW2/api/analysis"
)

var httpPost = http.Post

type FileStorage interface {
	GetFile(ctx context.Context, fileID string) (string, []byte, error)
}

type AnalysisServer struct {
	pb.UnimplementedAnalysisServiceServer
	FileStorage FileStorage
}

func NewAnalysisServer(fileStorage *FileStorageClient) *AnalysisServer {
	return &AnalysisServer{FileStorage: fileStorage}
}

func (s *AnalysisServer) AnalyzeFile(ctx context.Context, req *pb.AnalyzeFileRequest) (*pb.AnalyzeFileResponse, error) {
	_, content, err := s.FileStorage.GetFile(ctx, req.FileId)
	if err != nil {
		return nil, err
	}

	text := string(content)

	paragraphs := 0
	for _, p := range strings.Split(text, "\n") {
		if strings.TrimSpace(p) != "" {
			paragraphs++
		}
	}

	wordCount := len(strings.Fields(text))

	charCount := len([]rune(text))

	return &pb.AnalyzeFileResponse{
		Paragraphs: int32(paragraphs),
		Words:      int32(wordCount),
		Characters: int32(charCount),
	}, nil
}

func (s *AnalysisServer) GenerateWordCloud(ctx context.Context, req *pb.WordCloudRequest) (*pb.WordCloudResponse, error) {
	_, content, err := s.FileStorage.GetFile(ctx, req.FileId)
	if err != nil {
		return nil, err
	}

	payload := map[string]interface{}{
		"text":   string(content),
		"format": "png",
		"width":  800,
		"height": 800,
	}
	payloadBytes, _ := json.Marshal(payload)

	resp, err := httpPost("https://quickchart.io/wordcloud", "application/json", bytes.NewReader(payloadBytes))
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return nil, io.ErrUnexpectedEOF
	}

	img, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	return &pb.WordCloudResponse{
		Image: img,
	}, nil
}
