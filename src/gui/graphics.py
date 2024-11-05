import customtkinter as ctk
from datetime import datetime
from tkcalendar import DateEntry
from src.model.dao import DataStore
from src.model.entities import Patient, SymptomsLog, MedicinesLog

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class Graphics(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MediPat")
        self.geometry("800x800")
        self.data = DataStore()
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.logo_label = ctk.CTkLabel(self, text="Medipat", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=1, padx=20, pady=(20, 10), sticky="n")

        # acá creo 3 frames(contenedores) donde meto los widgets
        self.left_frame = ctk.CTkFrame(self, width=200, height=200)
        self.left_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        self.center_frame = ctk.CTkFrame(self, width=200, height=400)
        self.center_frame.grid(row=0, column=1, padx=20, pady=20, sticky="ew")

        self.right_frame = ctk.CTkFrame(self, width=200, height=200)
        self.right_frame.grid(row=0, column=2, padx=20, pady=20, sticky="ew")

        # configuracion de los frames
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Campo de entrada donde se escribe el nombre del paciente
        self.entry_patient = ctk.CTkEntry(self.left_frame, placeholder_text="Nombre del paciente")
        self.entry_patient.grid(row=0, column=2, padx=2, pady=5)

        #creacion boton que agrega el paciente en forma de objeto a la lista al usar el command add_patient
        self.patient_button = ctk.CTkButton(self.left_frame, text="Agregar paciente", command=self.add_patient)
        #ubicacion del boton
        self.patient_button.grid(row=1, column=2, padx=2, pady=5)
        #creacion del combobox
        self.patient_combo = ctk.CTkComboBox(self.center_frame)
        #texto que aparece por defecto en el combobox hasta elegir un paciente
        self.patient_combo.set("Paciente")
        self.patient_combo.grid(row=0, column=0, padx=1, pady=1)
        self.actualizar_patient_combo()
        self.date_entry_label = ctk.CTkLabel(self.center_frame, text="Fecha", font=ctk.CTkFont(size=13, weight="bold"))
        self.date_entry_label.grid(row=5, column=1, padx=50, columnspan=1, sticky="w")

        #todos los entry de medicina
        self.entry_medicine_date = DateEntry(self.center_frame, date_pattern='dd-mm-yyyy')
        self.entry_medicine_date.grid(row=5, column=2, padx=25, pady=(10, 10), sticky="w")
        self.entry_medicine_time = ctk.CTkEntry(self.center_frame, placeholder_text="Hora")
        self.entry_medicine_time.grid(row=6, column=2, padx=20, pady=(10, 10))
        self.entry_medicine_taken = ctk.CTkEntry(self.center_frame, placeholder_text="Medicina ingerida")
        self.entry_medicine_taken.grid(row=7, column=2, padx=20, pady=(10, 10))
        self.entry_medicine_description = ctk.CTkEntry(self.center_frame, placeholder_text="Descripción")
        self.entry_medicine_description.grid(row=8, column=2, padx=20, pady=(10, 10))

        #todos los entry de symptom
        self.entry_symptom_date = DateEntry(self.center_frame, date_pattern='dd-mm-yy')
        self.entry_symptom_date.grid(row=5, column=0, padx=0, pady=(10, 10), sticky="e")
        self.entry_symptom_time = ctk.CTkEntry(self.center_frame, placeholder_text="Hora")
        self.entry_symptom_time.grid(row=6, column=0, padx=0, pady=(10, 10),sticky="ew")
        self.entry_symptom = ctk.CTkEntry(self.center_frame, placeholder_text="Síntoma")
        self.entry_symptom.grid(row=7, column=0, padx=0, pady=(10, 10),sticky="ew")
        self.entry_symptom_description = ctk.CTkEntry(self.center_frame, placeholder_text="Descripción")
        self.entry_symptom_description.grid(row=8, column=0, padx=0, pady=(10, 10),sticky="ew")

        # botones
        self.medicine_button_log = ctk.CTkButton(self.center_frame, text="Cargar registro\nde medicación",command=self.add_medicine_log)
        self.medicine_button_log.grid(row=9, column=2, padx=20, pady=20, sticky="ew")
        self.symptom_button_log = ctk.CTkButton(self.center_frame, text="Cargar registro\nde síntoma", command=self.add_symptom_log)
        self.symptom_button_log.grid(row=9, column=0, padx=0, pady=20, sticky="ew")
        self.show_medicines_button = ctk.CTkButton(self.right_frame, text="Mostrar historial\nde medicaciones", command=self.show_medicine_log)
        self.show_medicines_button.grid(row=1, column=4, padx=20, pady=20, sticky="ew")
        self.show_symptoms_button = ctk.CTkButton(self.right_frame, text="Mostrar historial\nde sintomas", command=self.show_symptom_log)
        self.show_symptoms_button.grid(row=1, column=3, padx=20, pady=20, sticky="ew")

        #lugar donde se muestran los historiales
        self.show_logs_text = ctk.CTkTextbox(self.right_frame)
        self.show_logs_text.grid(row=0, column=3, columnspan=2, padx=20, pady=20, sticky="nsew")

    def add_patient(self):
        patient_name = self.entry_patient.get()
        if patient_name:
            new_patient = Patient(patient_name)
            self.data.add_patient(new_patient)
            self.entry_patient.delete(0, ctk.END)
            self.entry_patient.insert(0, "Nombre del paciente")
            self.actualizar_patient_combo()

    def actualizar_patient_combo(self):
        patient_names = [patient.name for patient in self.data.get_all_patients()]
        self.patient_combo.configure(values=patient_names)

    def add_medicine_log(self):
        medicine_date = self.entry_medicine_date.get()
        medicine_time = self.entry_medicine_time.get()
        medicine_taken = self.entry_medicine_taken.get()
        medicine_description = self.entry_medicine_description.get()
        selected_patient = self.patient_combo.get()
        #a diferencia de los 4 argumentos de medicine, el selected_patient recibe el paciente elegido en el combobox
        # luego verifico con los if que todos los parametros esten completos recuperando con get lo almacenado en ellos previamente
        if medicine_date and medicine_time and medicine_taken and medicine_description and selected_patient:
            patient = next(patient for patient in self.data.get_all_patients() if patient.name == selected_patient)
            new_medicine_log = MedicinesLog(medicine_date, medicine_time, medicine_taken, medicine_description, patient)
            self.data.add_medicine(new_medicine_log)
            self.entry_medicine_date.delete(0, ctk.END)
            self.entry_medicine_time.delete(0, ctk.END)
            self.entry_medicine_taken.delete(0, ctk.END)
            self.entry_medicine_description.delete(0, ctk.END)

    def add_symptom_log(self):
        symptom_date = self.entry_symptom_date.get()
        symptom_time = self.entry_symptom_time.get()
        symptom = self.entry_symptom.get()
        symptom_description = self.entry_symptom_description.get()
        selected_patient = self.patient_combo.get()
        if symptom_date and symptom_time and symptom and symptom_description:
            patient = next(patient for patient in self.data.get_all_patients() if patient.name == selected_patient)
            new_symptom_log = SymptomsLog(symptom_date, symptom_time, symptom, symptom_description, patient)
            self.data.add_symptom(new_symptom_log)
            self.entry_symptom_date.delete(0, ctk.END)
            self.entry_symptom_time.delete(0, ctk.END)
            self.entry_symptom.delete(0, ctk.END)
            self.entry_symptom_description.delete(0, ctk.END)

    def show_medicine_log(self):
        log_found = []
        selected_patient = self.patient_combo.get()
        for i in self.data.medicines_log_list:
            if i.patient.name == selected_patient:
                log_found.append(i)
        self.show_logs_text.delete("1.0", ctk.END)  # Limpiar el contenido anterior
        for log in log_found:
            self.show_logs_text.insert(ctk.END, f"Paciente {selected_patient} {log.date} - {log.time} - {log.medicine}\n")  # Mostrar registros

    def show_symptom_log(self):
        log_found = []
        selected_patient = self.patient_combo.get()
        for i in self.data.symptoms_log_list:
            if i.patient.name == selected_patient:
                log_found.append(i)
        # esto limpia el textbox primero y luego le inserta todas las iteraciones de la lista log_found
        # ya que ahi fui guardando todos los registros que coinciden con el paciente seleccionado del combo
        self.show_logs_text.delete("1.0", ctk.END)  # Limpiar el contenido anterior
        for log in log_found:
            self.show_logs_text.insert(ctk.END, f"Paciente {selected_patient} {log.date} - {log.time} - {log.symptom}\n")  # Mostrar registros
