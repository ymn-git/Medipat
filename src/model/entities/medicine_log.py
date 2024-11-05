class MedicinesLog:
    def __init__(self, date, time, medicine, description, patient):
        self.date = date
        self.time = time
        self.medicine = medicine
        self.description = description
        self.patient = patient

    def __str__(self):
        return f"MedicinesLog({self.patient}: {self.date}, {self.time}, {self.medicine} {self.description})"

