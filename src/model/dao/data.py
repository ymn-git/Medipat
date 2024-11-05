from src.model.entities import Patient, MedicinesLog, SymptomsLog

class DataStore:
    def __init__(self):
       self.patients_list = []
       self.medicines_log_list = []
       self.symptoms_log_list = []

    def add_patient(self, patient):
        self.patients_list.append(patient)

    def add_symptom(self, symptom):
        self.symptoms_log_list.append(symptom)

    def add_medicine(self, medicine):
        self.medicines_log_list.append(medicine)

    def get_patient(self, patient_name):
        for patient in self.patients_list:
            if patient.name == patient_name:
                return patient

    def get_all_patients(self):
        return self.patients_list

    def get_sym_by_pat(self, patient_name):
        for symp in self.symptoms_log_list:
            if symp.patient == patient_name:
                return symp

    def get_med_by_pat(self, patient_name):
        med_by_pat_list = []
        for medi in self.symptoms_log_list:
            if medi.patient == patient_name:
                med_by_pat_list.append(medi)
        return med_by_pat_list