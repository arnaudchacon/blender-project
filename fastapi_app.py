from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
import subprocess
from fastapi.responses import FileResponse
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/convert-to-3d/")
async def convert_to_3d(file: UploadFile = File(...)):
    logger.info("Received file upload request.")

    # Read the uploaded file
    file_contents = await file.read()
    
    # Save the uploaded file temporarily
    temp_file_path = Path("uploaded_files") / file.filename
    with open(temp_file_path, "wb") as f:
        f.write(file_contents)
    
    logger.info(f"Saved uploaded file to {temp_file_path}")

    # Define an explicit output directory
    output_directory = Path("output_3d_models")
    output_directory.mkdir(exist_ok=True)
    output_file_path = output_directory / (file.filename + ".obj")

    # Execute the Blender script externally
    blender_script_path = "Blender/floorplan_to_3dObject_in_blender.py"
    command = [
        "/Applications/Blender.app/Contents/MacOS/blender",
        "--background", 
        "--python", blender_script_path, 
        "--",  
        str(temp_file_path),
        str(output_file_path)
    ]
    result = subprocess.run(command, capture_output=True, text=True)

    # Log Blender's output and error messages
    logger.info("Blender STDOUT: " + result.stdout)
    logger.error("Blender STDERR: " + result.stderr)

    # Check the result for any errors or output
    if result.returncode != 0:
        logger.error(f"Blender execution failed with return code: {result.returncode}")
        return {"status": "error", "message": result.stderr}
    
    # Check if the 3D model was generated and return it
    if output_file_path.exists():
        logger.info(f"3D model generated successfully at {output_file_path}")
        return FileResponse(output_file_path, media_type="application/octet-stream", filename=f"{file.filename}.obj")
    else:
        logger.error("Failed to generate 3D model.")
        raise HTTPException(status_code=500, detail="Failed to generate 3D model.")

@app.get("/download/{filename}")
async def download_file(filename: str):
    logger.info(f"Received request to download file: {filename}")
    return FileResponse(f"output_3d_models/{filename}", media_type="application/octet-stream", filename=filename)
