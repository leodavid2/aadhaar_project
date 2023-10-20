import logging
# Configure logging
logging.basicConfig(level=logging.INFO)  # Set the desired logging level
from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel
from PIL import Image
import pytesseract
from io import BytesIO
from pattern import find_pattern

app = FastAPI(max_upload_size=10000000)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ImageData(BaseModel):
    filename: str
    content_type: str
    content: bytes

class ResponseModel(BaseModel):
    name: str
    dob: str
    gender: str
    aadhar_number: str
    address: str

# This is our API endpoint
@app.post("/upload/")
async def upload_images(files: List[UploadFile] = File(...), request: Request = None):
    data = ""

    for file in files:
        try:
            img = Image.open(BytesIO(await file.read()))

            # Perform OCR using pytesseract
            sampledata = pytesseract.image_to_string(img)

            data += sampledata
        except Exception as e:
            logging.error(f"Error processing image: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    # Find all kinds of Aadhaar numbers
    result_aadhar_number = find_pattern.find_aadhaar_numbers(data)

    # Find all kinds of DOB patterns
    result_dob = find_pattern.find_dob(data)

    # Extract addresses
    result_address = find_pattern.find_addresses(data)

    # Extract names
    result_name = find_pattern.extract_name_from_data(data)

    # Find gender patterns
    result_gender = find_pattern.find_gender_patterns(data)

    response_data = ResponseModel(
        name=result_name,
        dob=result_dob,
        gender=result_gender,
        aadhar_number=result_aadhar_number,
        address=result_address,
    )

    return response_data
