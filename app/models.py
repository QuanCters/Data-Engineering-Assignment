# models.py
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import Column, DateTime, Integer, SmallInteger, String, ForeignKey, Float
from app import get_engine

Base = declarative_base()

# Create a Session factory bound to the Engine
engine = get_engine()
Session = sessionmaker(bind=engine)

class Caregiver(Base):
    __tablename__ = "caregiver"
    caregiver_id = Column(String, primary_key=True)

    def to_dict(self):
        return {"caregiver_id": self.caregiver_id}

class Admissions(Base):
    __tablename__ = "admissions"
   
    subject_id = Column(Integer, nullable=True)
    hadm_id = Column(Integer, primary_key=True)
    admittime = Column(DateTime, nullable=True)
    dischtime = Column(DateTime, nullable=True)
    deathtime = Column(DateTime, nullable=True)
    admission_type = Column(String(40), nullable=True)
    admit_provider_id = Column(String(10), nullable=True)
    admission_location = Column(String(60), nullable=True)
    discharge_location = Column(String(60), nullable=True)
    insurance = Column(String(255), nullable=True)
    language = Column(String(10), nullable=True)
    marital_status = Column(String(30), nullable=True)
    race = Column(String(80), nullable=True)
    edregtime = Column(DateTime, nullable=True)
    edouttime = Column(DateTime, nullable=True)
    hospital_expire_flag = Column(SmallInteger, nullable=True) 

    def to_dict(self):
        return {
            "subject_id": self.subject_id,
            "hadm_id": self.hadm_id,
            "admittime": self.admittime.isoformat() if self.admittime else None,
            "dischtime": self.dischtime.isoformat() if self.dischtime else None,
            "deathtime": self.deathtime.isoformat() if self.deathtime else None,
            "admission_type": self.admission_type,
            "admit_provider_id": self.admit_provider_id,
            "admission_location": self.admission_location,
            "discharge_location": self.discharge_location,
            "insurance": self.insurance,
            "language": self.language,
            "marital_status": self.marital_status,
            "race": self.race,
            "edregtime": self.edregtime.isoformat() if self.edregtime else None,
            "edouttime": self.edouttime.isoformat() if self.edouttime else None,
            "hospital_expire_flag": self.hospital_expire_flag,
        }

class Patients(Base):
    __tablename__="patients"

    subject_id = Column(Integer, primary_key=True)
    gender = Column(String(1), nullable=False)
    anchor_age = Column(Integer, nullable=False)
    anchor_year = Column(Integer, nullable=False)
    anchor_year_group  = Column(String(255), nullable=False)
    dod = Column(DateTime, nullable=True)

    def to_dict(self):
        return {
            "subject_id": self.subject_id,
            "gender": self.gender,
            "anchor_age": self.anchor_age,
            "anchor_year": self.anchor_year,
            "anchor_year_group": self.anchor_year_group,
            "dod": self.dod.strftime('%Y-%m-%d %H:%M:%S') if self.dod else None,
        }

class Prescriptions(Base):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    subject_id = Column(Integer, nullable=True)
    hadm_id = Column(Integer, nullable=True)
    pharmacy_id = Column(Integer, nullable=True)
    poe_id = Column(String(25), nullable=True)
    poe_seq = Column(Integer, nullable=True)
    order_provider_id = Column(String(10), nullable=True)
    starttime = Column(DateTime, nullable=True)
    stoptime = Column(DateTime, nullable=True)
    drug_type = Column(String(20), nullable=True)
    drug = Column(String(255), nullable=True)
    formulary_drug_cd = Column(String(50), nullable=True)
    gsn = Column(String(255), nullable=True)
    ndc = Column(String(25), nullable=True)
    prod_strength = Column(String(255), nullable=True)
    form_rx = Column(String(25), nullable=True)
    dose_val_rx = Column(String(100), nullable=True)
    dose_unit_rx = Column(String(50), nullable=True)
    form_val_disp = Column(String(50), nullable=True)
    form_unit_disp = Column(String(50), nullable=True)
    doses_per_24_hrs = Column(Float, nullable=True)
    route = Column(String(50), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "subject_id": self.subject_id,
            "hadm_id": self.hadm_id,
            "pharmacy_id": self.pharmacy_id,
            "poe_id": self.poe_id,
            "poe_seq": self.poe_seq,
            "order_provider_id": self.order_provider_id,
            "starttime": self.starttime.isoformat() if self.starttime else None,
            "stoptime": self.stoptime.isoformat() if self.stoptime else None,
            "drug_type": self.drug_type,
            "drug": self.drug,
            "formulary_drug_cd": self.formulary_drug_cd,
            "gsn": self.gsn,
            "ndc": self.ndc,
            "prod_strength": self.prod_strength,
            "form_rx": self.form_rx,
            "dose_val_rx": self.dose_val_rx,
            "dose_unit_rx": self.dose_unit_rx,
            "form_val_disp": self.form_val_disp,
            "form_unit_disp": self.form_unit_disp,
            "doses_per_24_hrs": self.doses_per_24_hrs,
            "route": self.route,
        }