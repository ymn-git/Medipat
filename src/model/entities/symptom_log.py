class SymptomsLog:
    def __init__(self, date, time, symptom, description, patient):
        self.date = date
        self.time = time
        self.symptom = symptom
        self.description = description
        self.patient = patient


    def __str__(self):
        return f"{self.patient}: {self.date}, {self.time}, {self.symptom}, {self.description}"

