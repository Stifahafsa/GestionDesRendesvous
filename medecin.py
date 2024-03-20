from datetime import datetime

class Medecin:
    def __init__(self, nom, prenom, specialite):
        self.nom = nom
        self.prenom = prenom
        self.specialite = specialite
        self.rendez_vous = []

    def ajouter_rendez_vous(self, rendez_vous):
        self.rendez_vous.append(rendez_vous)

    def afficher_rendez_vous_journee(self):
        now = datetime.now()
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        for rendez_vous in self.rendez_vous:
            if rendez_vous.date == today:
                print(f"Rendez-vous à {rendez_vous.heure} avec {rendez_vous.patient.nom} {rendez_vous.patient.prenom}")

