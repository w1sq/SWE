package handler

import (
	"context"
	"io"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/w1sq/SWE/BHW2/gateway/internal/grpcclient"
)

type Handler struct {
	FileStorage *grpcclient.FileStorageClient
	Analysis    *grpcclient.AnalysisClient
}

type UploadResponse struct {
	FileID string `json:"file_id"`
}

type DownloadResponse struct {
	Filename string `json:"filename"`
	Content  string `json:"content"` // base64 encoded
}

type AnalyzeResponse struct {
	// Add fields as needed based on your proto
	Message string `json:"message"`
}

type ErrorResponse struct {
	Error string `json:"error"`
}

func RegisterRoutes(r *gin.Engine, fileStorage *grpcclient.FileStorageClient, analysis *grpcclient.AnalysisClient) {
	h := &Handler{FileStorage: fileStorage, Analysis: analysis}
	r.POST("/upload", h.uploadHandler)
	r.GET("/file/:id", h.downloadHandler)
	r.POST("/analyze/:id", h.analyzeHandler)
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
	c.JSON(http.StatusOK, resp)
}
