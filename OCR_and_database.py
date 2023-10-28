from fastapi import FastAPI, File, UploadFile, Request,Form,HTTPException,Depends
from fastapi.templating import Jinja2Templates
from PIL import Image
import pytesseract
from io import BytesIO
from typing import List
from sqlalchemy.orm import Session
#users modules to created
from database1 import SessionLocal, User 
from pattern import find_pattern


app = FastAPI()
templates = Jinja2Templates(directory="templates")  

@app.get("/")
def read_form(request: Request):
    return templates.TemplateResponse("upload_form.html", {"request": request})

@app.post("/upload/")
async def upload_images(request: Request, files: List[UploadFile] = File(...)):
    data=""

    for file in files:
        # Read the image
        img = Image.open(BytesIO(await file.read()))

        # Perform OCR using pytesseract
        sampledata = pytesseract.image_to_string(img)

        data += sampledata


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
        
    success_message = f"Check Your Details!!!"
    return templates.TemplateResponse("result.html", {"request": request, "name": result_name ,
                                                       'dob': result_dob ,"gender":result_gender,'aadhar_number':result_aahaar_number,
                                                       'address':result_address, "message": success_message},)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#get the values in the form page
@app.post("/submit/")
async def submit_form(
    name: str = Form(...),
    dob: str = Form(...),
    gender: str = Form(...),
    aadhar_number: str = Form(...),
    addressPerAadhaar: str = Form(...),
    position: str = Form(...),
    joiningDate: str = Form(...),
    adminName: str = Form(...),
    siteName: str = Form(...),
    presiteName: str = Form(...),
    adminMobile: str = Form(...),
    mobile: str = Form(...),
    fathersName: str = Form(...),
    mothersName: str = Form(...),
    accountHolderName: str = Form(...),
    accountNumber: str = Form(...),
    ifscCode: str = Form(...),
    religion: str = Form(...),
    esicNumber: str = Form(...),
    identificationMark: str = Form(...),
    nationality: str = Form(...),
    referredBy: str = Form(...),
    uanNumber: str = Form(...),
    height: str = Form(...),
    clientName: str = Form(...),
    recruiterName: str = Form(...),
    workLocation: str = Form(...),
    currentState: str = Form(...),
    currentAddress: str = Form(...),
    currentDistrict: str = Form(...),
    pincode: str = Form(...),
    maritalStatus: str = Form(...),
    job_Role: str = Form(...),
    bloodGroup: str = Form(...),
    email: str = Form(...),
    panNumber: str = Form(...),
    drivingLicense: str = Form(...),
    voterId: str = Form(...),
    reportingManager: str = Form(...),
    db: Session = Depends(get_db)
):
    # Insert user data into the database using SQLAlchemy
    user = User(name=name, dob=dob, aadhar_number=aadhar_number, address=addressPerAadhaar,gender=gender,
                Mobile_No=mobile,Position_Applied_For=position,
                Date_of_Joining=joiningDate,Admin_or_HRs_Name=adminName,Site_Name=siteName,Previous_Site_Name=presiteName,
                Admin_or_HRs_Mobile_Number=adminMobile,Fathers_Name=fathersName,Mothers_Name=mothersName,Account_Holder_Name=accountHolderName,
                Account_Number=accountNumber,IFSC_Code=ifscCode,Religion=religion,ESIC_Number=esicNumber,Identification_Mark=identificationMark,
                Nationality=nationality,Referred_By=referredBy,UAN_Number=uanNumber,Height=height,Client_Name=clientName,
                Recruiter_Name=recruiterName,Work_Location=workLocation,Current_State=currentState,Current_Address=currentAddress,
                Current_District=currentDistrict,Pincode=pincode,Marital_Status=maritalStatus,Job_Role=job_Role,Blood_Group=bloodGroup,
                Email=email,PAN_Number=panNumber,Driving_License_Number=drivingLicense,Voter_ID=voterId,Reporting_Manager_Name=reportingManager
                )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "Form data saved successfully!"}

@app.get("/users/{user_id}")
async def read_user(user_id: int, db: Session = Depends(get_db)):
    # Retrieve user data from the database using SQLAlchemy
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.delete("/delecte/{user_id}")
async def delete_user(user_id: int, db: Session =Depends(get_db)):
    db = SessionLocal()
    db_item = db.query(User).filter(User.id == user_id).first()
    if db_item is None:
        db.close()
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    db.close()
    return db_item