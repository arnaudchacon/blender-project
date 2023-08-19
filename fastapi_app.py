from fastapi import FastAPI, UploadFile, File
from pathlib import Path
import subprocess

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/convert-to-3d/")
async def convert_to_3d(file: UploadFile = File(...)):
    # Read the uploaded file
    file_contents = await file.read()
    
    # Save the uploaded file temporarily
    temp_file_path = Path("uploaded_files") / file.filename
    with open(temp_file_path, "wb") as f:
        f.write(file_contents)
    
    # Execute the Blender script externally
    blender_script_path = "Blender/floorplan_to_3dObject_in_blender.py"
    command = [
    "/Applications/Blender.app/Contents/MacOS/blender",
    "--background", 
    "--python", blender_script_path, 
    "--",  
    str(temp_file_path)
]
    result = subprocess.run(command, capture_output=True, text=True)

    # Check the result for any errors or output
    if result.returncode != 0:
        return {"status": "error", "message": result.stderr}
    
    return {"status": "success", "message": "Floor plan successfully converted to 3D!"}
