from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "sqlite:///./sample.db"

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


    
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    dob = Column(String)
    gender = Column(String)
    aadhar_number = Column(String, unique=True, index=True)
    address = Column(String)
    Mobile_No=Column(String)
    Position_Applied_For=Column(String)
    Date_of_Joining=Column(String)
    Admin_or_HRs_Name=Column(String)
    Site_Name=Column(String)
    Previous_Site_Name=Column(String)
    Admin_or_HRs_Mobile_Number=Column(String)
    Fathers_Name=Column(String)
    Mothers_Name=Column(String)
    Account_Holder_Name=Column(String)
    Account_Number=Column(String, unique=True, index=True)
    IFSC_Code=Column(String)
    Religion=Column(String)
    ESIC_Number=Column(String)
    Identification_Mark=Column(String)
    Nationality=Column(String)
    Referred_By=Column(String)
    UAN_Number=Column(String)
    Height=Column(String)
    Client_Name=Column(String)
    Recruiter_Name=Column(String)
    Work_Location=Column(String)
    Current_State=Column(String)
    Current_Address=Column(String)
    Current_District=Column(String)
    Pincode=Column(String)
    Marital_Status=Column(String)
    Job_Role=Column(String)
    Blood_Group=Column(String)
    Email=Column(String)
    PAN_Number=Column(String, unique=True, index=True)
    Driving_License_Number=Column(String, unique=True, index=True)
    Voter_ID=Column(String)
    Reporting_Manager_Name=Column(String)
    
# Create the table in the database
Base.metadata.create_all(bind=engine)
