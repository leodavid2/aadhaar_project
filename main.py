from fastapi import FastAPI, File, UploadFile, Request,Form,HTTPException,Depends
from fastapi.templating import Jinja2Templates
from PIL import Image
import pytesseract
from io import BytesIO
import re
from typing import List
# from sqlalchemy.orm import Session
#users modules to created
# from database1 import SessionLocal, User
from pattern import find_pattern
import os


app = FastAPI()
  

@app.get("/")
def read_form(request: Request):
    return  {"request": request}

@app.post("/upload/")
async def upload_images(request: Request, files: List[UploadFile] = File(...)):
    data=""

    for file in files:
        # Read the image
        
        img = Image.open(BytesIO(await file.read()))

        # Perform OCR using pytesseract
        sampledata = pytesseract.image_to_string(img)

        data += sampledata

    print(data)
    # print(type(data))

    # find all kind of aadhaar numbers
    result_aahaar_number=find_pattern.find_aadhaar_numbers(data)
    print(result_aahaar_number)

    #find all kind of dob pattern 
    result_dob=find_pattern.find_dob(data)
    print(result_dob)

    #addresses getting 
    result_address =find_pattern.find_addresses(data)
    print(result_address)

    # name pattern 2 this is completly great
    result_name = find_pattern.extract_name_from_data(data)
    print(result_name)

    #find gender pattern
    result_gender = find_pattern.find_gender_patterns(data)
    print("getting the last value :",result_gender)
        
    
    return  {"request": request, "name": result_name ,
                                                       'dob': result_dob ,"gender":result_gender,'aadhar_number':result_aahaar_number,
                                                       'address':result_address,}


