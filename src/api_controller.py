"""Patient API Controller"""

from flask import Flask, request, jsonify
from patient_db import PatientDB


class PatientAPIController:
    def __init__(self):
        self.app = Flask(__name__)
        self.patient_db = PatientDB()
        self.setup_routes()
        self.run()

    def setup_routes(self):
        """
        Sets up the routes for the API endpoints.
        """
        self.app.route("/patients", methods=["GET"])(self.get_patients)
        self.app.route("/patients/<patient_id>", methods=["GET"])(self.get_patient)
        self.app.route("/patients", methods=["POST"])(self.create_patient)
        self.app.route("/patient/<patient_id>", methods=["PUT"])(self.update_patient)
        self.app.route("/patient/<patient_id>", methods=["DELETE"])(self.delete_patient)


    """
    TODO:
    Implement the following methods,
    use the self.patient_db object to interact with the database.

    Every method in this class should return a JSON response with status code
    Status code should be 200 if the operation was successful,
    Status code should be 400 if there was a client error,
    """

    def create_patient(self):
        data = request.json

        patient = self.patient_db.insert_patient(data)
        if patient is not None:
            return jsonify(data), 200
        else:
            return jsonify({"error": "failed to create patient"}), 400
        
    def get_patients(self):
        patients = self.patient_db.select_all_patients()
        if patients is not None:
            return jsonify(patients), 200
        else:
            return jsonify({"error": "failed to get patients"}), 400

    def get_patient(self, patient_id):
        patient = self.patient_db.select_patient(patient_id)
        if patient:
            return jsonify(patient), 200
        else:
            return jsonify({"error": "patient not found"}), 400

    def update_patient(self, patient_id):
        data = request.json
        number = self.patient_db.update_patient(patient_id, data)
        if number:
            return jsonify({"message": f"{number} rows updated"}), 200
        else:
            return jsonify({"error": "failed to update patient"}), 400

    def delete_patient(self, patient_id):
        number = self.patient_db.delete_patient(patient_id)
        if number:
            return jsonify({"message": f"{number} rows deleted"}), 200
        else:
            return jsonify({"error": "failed to delete patient"}), 400

    def run(self):
        """
        Runs the Flask application.
        """
        self.app.run()


PatientAPIController()
