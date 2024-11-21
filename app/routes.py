# routes.py
from flask import request
from flask_restx import Namespace, Resource, fields
from sqlalchemy import desc, func
from sqlalchemy.exc import SQLAlchemyError
from .models import Caregiver,Admissions, Patients, Session, Prescriptions
from app.utils import format_response

# name space
caregiver_ns = Namespace('caregivers', description='Caregiver APIs')
admissions_ns = Namespace('admissions', description='Admissions APIs')
patients_ns = Namespace('patients', description='Patients APIs')
prescriptions_ns = Namespace('prescriptions', description='Descriptions APIs')

# models for documentation
caregiver_model = caregiver_ns.model('Caregivers', {
    'caregiver_id': fields.String(readonly=True, description="The unique identifier of caregiver")
})

admissions_model = admissions_ns.model('Admissions', {
    'subject_id': fields.Integer(description="The subject ID associated with the admission"),
    'hadm_id': fields.Integer(readonly=True, description="The unique identifier of the hospital admission"),
    'admittime': fields.DateTime(description="The time of admission"),
    'dischtime': fields.DateTime(description="The time of discharge"),
    'deathtime': fields.DateTime(description="The time of death (if applicable)"),
    'admission_type': fields.String(description="The type of admission"),
    'admit_provider_id': fields.String(description="The provider ID associated with the admission"),
    'admission_location': fields.String(description="The location of the patient before admission"),
    'discharge_location': fields.String(description="The location the patient was discharged to"),
    'insurance': fields.String(description="The insurance information for the admission"),
    'language': fields.String(description="The preferred language of the patient"),
    'marital_status': fields.String(description="The marital status of the patient"),
    'race': fields.String(description="The race of the patient"),
    'edregtime': fields.DateTime(description="The time the patient registered in the emergency department"),
    'edouttime': fields.DateTime(description="The time the patient was discharged from the emergency department"),
    'hospital_expire_flag': fields.Integer(description="Flag indicating if the patient expired in the hospital")
})

patients_model = patients_ns.model('Patients', {
    'subject_id': fields.Integer(description="The unique identifier of the patient"),
    'gender': fields.String(description="The gender of the patient"),
    'anchor_age': fields.Integer(description="The age of the patient at the time of admission"),
    'anchor_year': fields.Integer(description="The year of admission"),
    'anchor_year_group': fields.String(description="The age group of the patient"),
    'dod': fields.String(description="The date of death (if applicable)")
})

prescriptions_model = prescriptions_ns.model('Prescriptions', {
    'subject_id': fields.Integer(description="The unique identifier of the subject"),
    'hadm_id': fields.Integer(description="The unique identifier of the hospital admission"),
    'pharmacy_id': fields.Integer(description="The unique identifier of the pharmacy"),
    'poe_id': fields.String(description="The provider order entry identifier"),
    'poe_seq': fields.Integer(description="The sequence number of the provider order entry"),
    'order_provider_id': fields.String(description="The identifier of the order provider"),
    'starttime': fields.DateTime(description="The start time of the prescription"),
    'stoptime': fields.DateTime(description="The stop time of the prescription"),
    'drug_type': fields.String(description="The type of drug prescribed"),
    'drug': fields.String(description="The name of the drug prescribed"),
    'formulary_drug_cd': fields.String(description="The formulary drug code"),
    'gsn': fields.String(description="The generic sequence number"),
    'ndc': fields.String(description="The National Drug Code"),
    'prod_strength': fields.String(description="The strength of the product"),
    'form_rx': fields.String(description="The form of the prescription"),
    'dose_val_rx': fields.String(description="The dose value of the prescription"),
    'dose_unit_rx': fields.String(description="The unit of the dose"),
    'form_val_disp': fields.String(description="The form value for dispensing"),
    'form_unit_disp': fields.String(description="The unit for dispensing"),
    'doses_per_24_hrs': fields.Float(description="The number of doses per 24 hours"),
    'route': fields.String(description="The route of administration"),
})

# routes
@caregiver_ns.route('/')
class CaregiverList(Resource):
    # @caregiver_ns.marshal_list_with(caregiver_model)
    def get(self):
        """List all caregivers"""
        session = Session()
        try:
            caregivers = session.query(Caregiver).all()
            return [caregiver.to_dict() for caregiver in caregivers]
        except SQLAlchemyError as e:
            return format_response(str(e), message="Error fetching caregivers", status=500)
        finally:
            session.close()

@caregiver_ns.route('/<string:caregiver_id>')
@caregiver_ns.response(404, 'Caregiver not found')
@caregiver_ns.param('caregiver_id', 'The caregiver identifier')
class CaregiverResource(Resource):
    # @caregiver_ns.marshal_with(caregiver_model)
    def get(self, caregiver_id):
        """Get a caregiver by ID"""
        session = Session()
        try:
            caregiver = session.query(Caregiver).filter(Caregiver.caregiver_id == caregiver_id).first()
            if caregiver:
                return caregiver.to_dict()
            caregiver_ns.abort(404, "Caregiver not found")
        except SQLAlchemyError as e:
            return format_response(str(e), message="Error fetching caregiver", status=500)
        finally:
            session.close()

@admissions_ns.route('/')
class AdmissionsList(Resource):
    @admissions_ns.doc(params={
        'page': 'Page number for pagination (default is 1)'
    })
    def get(self):
        """List all admissions with pagination"""
        session = Session()
        try:
            # Get query parameters with default values
            page = request.args.get('page', 1, type=int)
            per_page = 9

            # Ensure page and per_page are valid
            if page < 1:
                return format_response(
                    "Invalid pagination parameters",
                    message="Page must be 1 or greater",
                    status=400
                )

            # Query total count and fetch paginated results
            total_admissions = session.query(Admissions).count()
            admissions = (
                session.query(Admissions)
                .order_by(Admissions.hadm_id)  # Ensure consistent ordering
                .offset((page - 1) * per_page)
                .limit(per_page)
                .all()
            )

            # Prepare response with metadata
            return {
                "admissions": [admission.to_dict() for admission in admissions],
                "meta": {
                    "page": page,
                    "total_admissions": total_admissions,
                    "total_pages": (total_admissions + per_page - 1) // per_page,  # Ceiling division
                }
            }
        except SQLAlchemyError as e:
            return format_response(str(e), message="Error fetching admissions", status=500)
        finally:
            session.close()

@admissions_ns.route('/<int:hadm_id>')
@admissions_ns.response(404, 'Admission not found')
@admissions_ns.param('hadm_id', 'The admission identifier')
class AdmissionResource(Resource):
    def get(self, hadm_id):
        """Get a admission by ID"""
        session = Session()
        try:
            admission = session.query(Admissions).filter(Admissions.hadm_id == hadm_id).first()
            if admission:
                return admission.to_dict()
            admissions_ns.abort(404, "Admission not found")
        except SQLAlchemyError as e:
            return format_response(str(e), message="Error fetching admission", status=500)
        finally:
            session.close()
            
@patients_ns.route('/')
class PatientsList(Resource):
    @patients_ns.doc(params={'page': 'Page number for pagination'})
    def get(self):
        """List all patients with pagination"""
        session = Session()
        try:
            # Pagination parameters
            page = request.args.get('page', 1, type=int)
            per_page = 9  # Items per page (can be configured)

            if page < 1:
                return format_response("Invalid page number", message="Page must be 1 or greater", status=400)

            # Query total count and fetch paginated results
            total_patients = session.query(Patients).count()
            patients = (
                session.query(Patients)
                .order_by(Patients.subject_id) 
                .offset((page - 1) * 9)
                .limit(9)
                .all()
             )

            # Prepare response
            return {
                "patients": [patient.to_dict() for patient in patients],
                "meta": {
                    "page": page,
                    "per_page": per_page,
                    "total_patients": total_patients,
                    "total_pages": (total_patients + per_page - 1) // per_page,  # Ceiling division
                }
            }
        except SQLAlchemyError as e:
            return format_response(str(e), message="Error fetching patients", status=500)
        finally:
            session.close()

@patients_ns.route('/<int:subject_id>')
@patients_ns.response(404, 'Patient not found')
@patients_ns.param('subject_id', 'The patient identifier')
class PatientResource(Resource):
    def get(self, subject_id):
        """Get a patient by ID"""
        session = Session()
        try:
            patient = session.query(Patients).filter(Patients.subject_id == subject_id).first()
            if patient:
                return patient.to_dict()
            patients_ns.abort(404, "Patient not found")
        except SQLAlchemyError as e:
            return format_response(str(e), message="Error fetching patient", status=500)
        finally:
            session.close()

@prescriptions_ns.route('/most_used')
class MostUsedDrugs(Resource):
    @prescriptions_ns.doc(params={
        'limit': 'Number of top drugs to return (default is 10)'
    })
    def get(self):
        """List the most used drugs"""
        session = Session()
        try:
            limit = request.args.get('limit', 10, type=int)

            # Query to get the most used drugs
            most_used_drugs = (
                session.query(Prescriptions.drug, func.count(Prescriptions.drug).label('count'))
                .group_by(Prescriptions.drug)
                .order_by(desc('count'))
                .limit(limit)
                .all()
            )

            return {
                "most_used_drugs": [{"drug": drug, "count": count} for drug, count in most_used_drugs]
            }
        except SQLAlchemyError as e:
            return format_response(str(e), message="Error fetching most used drugs", status=500)
        finally:
            session.close()