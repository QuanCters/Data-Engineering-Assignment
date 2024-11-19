# routes.py
from flask_restx import Namespace, Resource, fields
from sqlalchemy.exc import SQLAlchemyError
from .models import Caregiver, Session
from app.utils import format_response

caregiver_ns = Namespace('caregivers', description='Caregiver APIs')

caregiver_model = caregiver_ns.model('Caregivers', {
    'caregiver_id': fields.String(readonly=True, description="The unique identifier of caregiver")
})

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
