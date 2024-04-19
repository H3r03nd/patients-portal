"""
TODO: Implement the Patient class.
Please import and use the config and db config variables.

The attributes for this class should be the same as the columns in the PATIENTS_TABLE.

The Object Arguments should only be name , gender and age.
Rest of the attributes should be set within the class.

-> for id use uuid4 to generate a unique id for each patient.
-> for checkin and checkout use the current date and time.

There should be a method to update the patient's room and ward. validation should be used.(config is given)

Validation should be done for all of the variables in config and db_config.

There should be a method to commit that patient to the database using the api_controller.
"""
import uuid
import requests
from datetime import datetime
from config import DOCTORS, GENDERS, WARD_NUMBERS, ROOM_NUMBERS, API_CONTROLLER_URL
from patient_db_config import PATIENTS_TABLE, ENGINE
from patient_db import PatientDB
class Patient:
    def __init__(self, name, gender, age):
        self.patient_id = str(uuid.uuid4())
        self.name = name
        self.age = age
        self.gender = gender
        self.checkin = datetime.now().isoformat()
        self.checkout = datetime.now().isoformat()
        self.ward = None
        self.room = None
        self.validate_initial_arguments()

    def validate_initial_arguments(self):
        if self.name is None or type(self.name) != str:
            raise ValueError("Invalid name")
        if self.gender not in GENDERS:
            raise ValueError("Invalid gender")
        if not isinstance(self.age, int) or self.age <= 0:
            raise ValueError("Invalid age")

    def update_room_and_ward(self, ward, room):
        if ward in WARD_NUMBERS and room in ROOM_NUMBERS[ward]:
            self.ward = ward
            self.room = room
        else:
            raise ValueError("Invalid ward or room number")
        data = {
            "ward": self.ward,
            "room": self.room
        }
        response = requests.put(f"{API_CONTROLLER_URL}/patient/{self.patient_id}", json=data)

    def commit_to_db(self):
        data = {
            "patient_id": self.patient_id,
            "patient_name": self.name,
            "patient_age": self.age,
            "patient_gender": self.gender,
            "patient_checkin": self.checkin,
            "patient_checkout": self.checkout,
            "patient_ward": self.ward,
            "patient_room": self.room,
        }
        response = requests.post(f"{API_CONTROLLER_URL}/patients", json=data)
        if response.status_code != 201:
            raise Exception("Failed to commit patient to database")
        return response.json()
