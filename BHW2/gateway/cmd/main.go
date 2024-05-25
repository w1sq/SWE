package main

import (
	"context"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/w1sq/SWE/BHW2/gateway/internal/grpcclient"
	"github.com/w1sq/SWE/BHW2/gateway/internal/handler"

	"github.com/gin-gonic/gin"
	swaggerFiles "github.com/swaggo/files"
	ginSwagger "github.com/swaggo/gin-swagger"
	_ "github.com/w1sq/SWE/BHW2/gateway/docs"
)

func main() {
	fileStorageAddr := os.Getenv("FILE_STORAGE_ADDR")
	if fileStorageAddr == "" {
		fileStorageAddr = "localhost:50051"
	}
	analysisAddr := os.Getenv("ANALYSIS_ADDR")
	if analysisAddr == "" {
		analysisAddr = "localhost:50052"
	}

	fileStorageClient, err := grpcclient.NewFileStorageClient(fileStorageAddr)
	if err != nil {
		log.Fatalf("failed to connect to file storage service: %v", err)
	}
	analysisClient, err := grpcclient.NewAnalysisClient(analysisAddr)
	if err != nil {
		log.Fatalf("failed to connect to analysis service: %v", err)
	}

	r := gin.Default()
	handler.RegisterRoutes(r, fileStorageClient, analysisClient)

	r.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))

	srv := &http.Server{
		Addr:    ":8000",
		Handler: r,
	}

	go func() {
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("listen: %s\n", err)
		}
	}()

	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit
	log.Println("Shutting down server...")

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	if err := srv.Shutdown(ctx); err != nil {
		log.Fatal("Server forced to shutdown: ", err)
	}
	log.Println("Server exiting")
}
