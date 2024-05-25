package handler

import (
	"context"
	"io"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	pb "github.com/w1sq/SWE/BHW2/api/analysis"
	"github.com/w1sq/SWE/BHW2/gateway/internal/grpcclient"
)

type FileStorage interface {
	StoreFile(ctx context.Context, filename string, content []byte) (string, error)
	GetFile(ctx context.Context, fileID string) (string, []byte, error)
}

type Analysis interface {
	AnalyzeFile(ctx context.Context, fileID string) (*pb.AnalyzeFileResponse, error)
	GenerateWordCloud(ctx context.Context, fileID string) (*pb.WordCloudResponse, error)
}

type Handler struct {
	FileStorage FileStorage
	Analysis    Analysis
}

type UploadResponse struct {
	FileID string `json:"file_id"`
}

type DownloadResponse struct {
	Filename string `json:"filename"`
	Content  string `json:"content"`
}

type AnalyzeResponse struct {
	Paragraphs int32 `json:"paragraphs"`
	Words      int32 `json:"words"`
	Characters int32 `json:"characters"`
}

type ErrorResponse struct {
	Error string `json:"error"`
}

func RegisterRoutes(r *gin.Engine, fileStorage *grpcclient.FileStorageClient, analysis *grpcclient.AnalysisClient) {
	h := &Handler{FileStorage: fileStorage, Analysis: analysis}
	r.POST("/upload", h.uploadHandler)
	r.GET("/file/:id", h.downloadHandler)
	r.POST("/analyze/:id", h.analyzeHandler)
	r.GET("/wordcloud/:id", h.wordCloudHandler)
}

// uploadHandler godoc
// @Summary Upload a file
// @Description Uploads a file and stores it in the file storage service
// @Tags files
// @Accept multipart/form-data
// @Produce json
// @Param file formData file true "File to upload"
// @Success 200 {object} UploadResponse
// @Failure 400 {object} ErrorResponse
// @Failure 500 {object} ErrorResponse
// @Router /upload [post]
func (h *Handler) uploadHandler(c *gin.Context) {
	file, header, err := c.Request.FormFile("file")
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "file is required"})
		return
	}
	defer file.Close()
	content, err := io.ReadAll(file)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "failed to read file"})
		return
	}
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	fileID, err := h.FileStorage.StoreFile(ctx, header.Filename, content)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "failed to store file"})
		return
	}
	c.JSON(http.StatusOK, UploadResponse{FileID: fileID})
}

// downloadHandler godoc
// @Summary Download a file
// @Description Downloads a file by its ID from the file storage service
// @Tags files
// @Produce application/octet-stream
// @Param id path string true "File ID"
// @Success 200 {file} file
// @Failure 404 {object} ErrorResponse
// @Failure 500 {object} ErrorResponse
// @Router /file/{id} [get]
func (h *Handler) downloadHandler(c *gin.Context) {
	fileID := c.Param("id")
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	filename, content, err := h.FileStorage.GetFile(ctx, fileID)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "file not found"})
		return
	}
	c.Header("Content-Disposition", "attachment; filename="+filename)
	c.Data(http.StatusOK, "application/octet-stream", content)
}

// analyzeHandler godoc
// @Summary Analyze a file
// @Description Requests analysis of a file by its ID from the analysis service
// @Tags analysis
// @Produce json
// @Param id path string true "File ID"
// @Success 200 {object} AnalyzeResponse
// @Failure 500 {object} ErrorResponse
// @Router /analyze/{id} [post]
func (h *Handler) analyzeHandler(c *gin.Context) {
	fileID := c.Param("id")
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	resp, err := h.Analysis.AnalyzeFile(ctx, fileID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "failed to analyze file"})
		return
	}
	c.JSON(http.StatusOK, AnalyzeResponse{
		Paragraphs: resp.Paragraphs,
		Words:      resp.Words,
		Characters: resp.Characters,
	})
}

// wordCloudHandler godoc
// @Summary Get word cloud image for a file
// @Description Generates a word cloud image for the file content using QuickChart API via analysis service
// @Tags analysis
// @Produce png
// @Param id path string true "File ID"
// @Success 200 {file} file
// @Failure 404 {object} ErrorResponse
// @Failure 500 {object} ErrorResponse
// @Router /wordcloud/{id} [get]
func (h *Handler) wordCloudHandler(c *gin.Context) {
	fileID := c.Param("id")
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	resp, err := h.Analysis.GenerateWordCloud(ctx, fileID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "failed to generate word cloud"})
		return
	}
	c.Data(http.StatusOK, "image/png", resp.Image)
}
