import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import search, coach, health
from api.middleware import add_metrics
from api.dependencies import index_manager
from api.config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Compass API",
    description="Safety-First Coaching with Bounded LLM & Evidence Gate",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Add metrics middleware
app.middleware("http")(add_metrics)

# Include routers
app.include_router(search.router, tags=["search"])
app.include_router(coach.router, tags=["coach"])
app.include_router(health.router, tags=["health"])

@app.on_event("startup")
async def startup_event():
    """Load indices on application startup."""
    logger.info("Starting up Compass application...")
    
    try:
        # Check if indices exist
        import os
        # Detect if we're running in Docker or locally
        current_dir = os.getcwd()
        logger.info(f"Current working directory: {current_dir}")
        
        if current_dir == "/app":
            # We're in Docker container
            project_root = "/app"
            logger.info("Detected Docker environment")
        else:
            # We're in local development
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            logger.info("Detected local development environment")
        
        manifest_path = os.path.join(project_root, config["index_dir"], "index_manifest.json")
        cases_path = os.path.join(project_root, config["cases_path"])
        
        logger.info(f"Project root: {project_root}")
        logger.info(f"Looking for manifest at: {manifest_path}")
        logger.info(f"Looking for cases at: {cases_path}")
        logger.info(f"Manifest exists: {os.path.exists(manifest_path)}")
        logger.info(f"Cases exists: {os.path.exists(cases_path)}")
        
        if os.path.exists(manifest_path) and os.path.exists(cases_path):
            logger.info("Found existing indices, loading them...")
            
            # Import here to avoid circular imports
            from services.embedding_service import EmbeddingService
            
            # Load indices with absolute paths
            embedding_service = EmbeddingService(config["embed_model"])
            
            # Temporarily update the index_manager config to use absolute paths
            original_config = index_manager.config.copy()
            index_manager.config["index_dir"] = os.path.join(project_root, config["index_dir"])
            index_manager.config["cases_path"] = os.path.join(project_root, config["cases_path"])
            
            logger.info(f"Updated index_manager config:")
            logger.info(f"  index_dir: {index_manager.config['index_dir']}")
            logger.info(f"  cases_path: {index_manager.config['cases_path']}")
            
            load_success = index_manager.load_indices(embedding_service)
            if load_success:
                logger.info("Successfully loaded indices on startup")
            else:
                logger.error("Failed to load indices on startup")
                # Restore original config
                index_manager.config = original_config
        else:
            logger.warning("No indices found on startup. Please run /index endpoint to build them.")
            logger.warning(f"Manifest path: {manifest_path}")
            logger.warning(f"Cases path: {cases_path}")
            logger.warning(f"Manifest exists: {os.path.exists(manifest_path)}")
            logger.warning(f"Cases exists: {os.path.exists(cases_path)}")
            
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        logger.warning("Application will start without indices. Please run /index endpoint to build them.")

if __name__ == "__main__":
    # Run the FastAPI app
    import uvicorn
    uvicorn.run("app_new:app", host="0.0.0.0", port=8000, reload=True) 