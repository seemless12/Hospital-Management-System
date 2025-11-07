from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional, List,  Annotated 

class Patient (BaseModel):
    # Validation schema for patient data
    name: Annotated[str,
                    Field(max_length=50 ,
                           pattern="^[a-zA-Z\s]+$",
                          description="The name of the patient (in letters Only), max 50 characters",
                          examples=["Huzaifa khan","Aarish Arif"]
                          )]
    age: int = Field(..., gt=0, lt=100,
                     description="The age of the patient, must be between 1 and 100",
                     examples=[25, 40])
    gender: Annotated[str,
                      Field(max_length=10 ,description="The gender of the patient, max 10 characters",
                            examples=["Male","Female"])]
    blood_type: Annotated[str,
                          Field(max_length=3 ,description="The blood type of the patient, max 3 characters",
                                examples=["A+","O-"])]
    contact_phone: Annotated[str,
                             Field(pattern=r"^\d{4,15}$",
                                   description="The contact phone number of the patient",
                                   examples=["0312-3456789","03123456789"])]   
    contact_email: Annotated[Optional[EmailStr],
                             Field(default=None, description="The contact email of the patient")] 
    Medical_History: Annotated[Optional[List[str]], 
                               Field(default=None,max_length=5,
                                     description="The medical history of the patient")]
    doctor_assigned: Annotated[str,
                               Field(max_length=50 ,
                                     description="The name of the doctor assigned to the patient, max 50 characters",
                                     examples=["Dr. Hamza","Dr. Wajahat"])]
    @validator("doctor_assigned")
    def add_prefix(cls, v):
        if not v.lower().startswith("dr"):
            return f"Dr {v.strip()}"
        return v.strip()


def Check_schema(patient : Patient):
    print("✅ Schema validation successful.")
    
        





patient_data = {
    "name": "Huzaifa Khan",
    "age": 27,
    "gender": "Male",
    "blood_type": "A+",
    "contact_phone": "0312-3456789",
    "contact_email": "huzaifa.khan@example.com",
    "Medical_History": ["Asthma", "Allergy"],
    "doctor_assigned": "Dr. Hamza"
}

patient_1 = Patient(**patient_data)
       
Check_schema(patient_1)