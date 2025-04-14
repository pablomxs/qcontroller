from fastapi import APIRouter, UploadFile, File, HTTPException
from app.qlogic.parser import parse_log
from app.qlogic.evaluator import evaluate_sensors
import traceback
import logging

logger = logging.getLogger(__name__)

# Adding prefix to the router to handle versioning
router = APIRouter(prefix="/api/v1")

@router.get("/health")
def healthcheck():
    return {
        "status": "Healthy"
    }

@router.post("/evaluate")
async def evaluate_log(file: UploadFile = File(...)):
    # Validate the file type, must be a .log file
    if not file.filename.endswith(".log"):
        logger.error("Invalid file type: %s", file.filename)
        raise HTTPException(status_code=400, detail="File must be a .log file")
    
    content = await file.read()

    try:
        parsed_data = parse_log(content.decode("utf-8"))
        result = evaluate_sensors(parsed_data)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Logging the full traceback for debugging purposes
        logger.error(f"Unhandled error:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
