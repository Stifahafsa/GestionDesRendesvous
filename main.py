import json
from datetime import datetime
from patient import Patient
from medecin import Medecin
from rendezvous import RendezVous

patients = []
medecins = []
rendez_vous = []

def inscrire_patient():
    nom = input("Entrez votre nom : ")
    prenom = input("Entrez votre prénom : ")
    age = int(input("Entrez votre âge : "))
    email = input("Entrez votre email : ")
    patients.append(Patient(nom, prenom, age, email))
    print("Inscription réussie.")

def inscrire_medecin():
    nom = input("Entrez votre nom : ")
    prenom = input("Entrez votre prénom : ")
    specialite = input("Entrez votre spécialité : ")
    caractere_specifique = input("Entrez le caractère spécifique : ")
    if caractere_specifique == "Medecin":
        medecins.append(Medecin(nom, prenom, specialite))
        print("Inscription réussie.")
    else:
        print("Caractère spécifique incorrect, inscription échouée.")

def inscrire():
    print("Choisissez le type d'inscription :")
    print("1. Patient")
    print("2. Médecin")
    choix = input("Entrez votre choix : ")
    if choix == "1":
        inscrire_patient()
    elif choix == "2":
        inscrire_medecin()
    else:
        print("Choix invalide. Veuillez réessayer.")

def prendre_rendez_vous(patient):
    specialite = input("Entrez la spécialité du médecin : ")
    medecin_disponible = None
    for medecin in medecins:
        if medecin.specialite == specialite and len(medecin.rendez_vous) < 5:
            medecin_disponible = medecin
            break
    if medecin_disponible:
        print("Heures disponibles pour rendez-vous (9h à 16h) :")
        heures_prises = [rdv.heure for rdv in medecin_disponible.rendez_vous if rdv.date == datetime.now().strftime("%d/%m/%Y")]
        heures_disponibles = [f"{heure}:00" for heure in range(9, 17) if f"{heure}:00" not in heures_prises]
        if heures_disponibles:
            print("\n".join(heures_disponibles))
            heure = input("Choisissez une heure disponible pour le rendez-vous (hh:mm) : ")
            rendez_vous.append(RendezVous(patient, medecin_disponible, datetime.now().strftime("%d/%m/%Y"), heure))
            medecin_disponible.rendez_vous.append(RendezVous(patient, medecin_disponible, datetime.now().strftime("%d/%m/%Y"), heure))
            enregistrer_rendez_vous()
            print("Rendez-vous pris avec succès.")
        else:
            print("Aucune heure disponible pour aujourd'hui. Veuillez choisir un autre jour.")
    else:
        print("Aucun médecin disponible pour cette spécialité ou plus de rendez-vous pour ce médecin.")

def enregistrer_rendez_vous():
    rendez_vous_data = []
    for rdv in rendez_vous:
        rendez_vous_data.append({
            "patient": {"nom": rdv.patient.nom, "prenom": rdv.patient.prenom},
            "medecin": {"nom": rdv.medecin.nom, "prenom": rdv.medecin.prenom},
            "date": rdv.date,
            "heure": rdv.heure,
            "statut": rdv.statut
        })
    with open("rendez_vous.json", "w") as f:
        json.dump(rendez_vous_data, f, indent=4)


def afficher_rendez_vous(patient):
    with open("rendez_vous.json", "r") as f:
        rendez_vous_data = json.load(f)
        print("Vos rendez-vous :")
        for rdv in rendez_vous_data:
            if rdv["patient"]["nom"] == patient.nom and rdv["patient"]["prenom"] == patient.prenom:
                print(f"Date : {rdv['date']}, Heure : {rdv['heure']}")

def afficher_rendez_vous_medecin(medecin):
    with open("rendez_vous.json", "r") as f:
        rendez_vous_data = json.load(f)
        print(f"Rendez-vous du Dr {medecin.nom} {medecin.prenom} :")
        for rdv in rendez_vous_data:
            if rdv["medecin"]["nom"] == medecin.nom and rdv["medecin"]["prenom"] == medecin.prenom:
                print(f"{rdv['date']} à {rdv['heure']} avec {rdv['patient']['nom']} {rdv['patient']['prenom']} - {rdv['statut']}")
        choix = input("Entrez l'heure du rendez-vous à terminer (hh:mm) ou 'q' pour quitter : ")
        if choix != 'q':
            terminer_rendez_vous(medecin, choix)

def terminer_rendez_vous(medecin, heure):
    for rdv in rendez_vous:
        if rdv.medecin == medecin and rdv.heure == heure and rdv.date == datetime.now().strftime("%d/%m/%Y"):
            rdv.statut = "Terminé"
            print("Rendez-vous marqué comme terminé avec succès.")
            enregistrer_rendez_vous()
            return
    print("Aucun rendez-vous trouvé avec cette heure.")

def afficher_menu_principal():
    print("\nMenu Principal :")
    print("1. Inscrire")
    print("2. Connecter")
    print("3. Quitter")

def afficher_menu_patient():
    print("\nMenu Patient :")
    print("1. Prendre un rendez-vous")
    print("2. Voir mes rendez-vous")
    print("3. Se déconnecter")

def afficher_menu_medecin():
    print("\nMenu Médecin :")
    print("1. Voir mes rendez-vous de la journée")
    print("2. Se déconnecter")

def main():
    while True:
        afficher_menu_principal()
        choix = input("Entrez votre choix : ")
        if choix == "1":
            inscrire()
        elif choix == "2":
            username = input("Entrez votre nom d'utilisateur : ")
            password = input("Entrez votre mot de passe : ")
            if any(patient.nom == username for patient in patients):
                patient_connecte = next(patient for patient in patients if patient.nom == username)
                print("Connecté en tant que patient.")
                while True:
                    afficher_menu_patient()
                    choix_patient = input("Entrez votre choix : ")
                    if choix_patient == "1":
                        prendre_rendez_vous(patient_connecte)
                    elif choix_patient == "2":
                        afficher_rendez_vous(patient_connecte)
                    elif choix_patient == "3":
                        break
                    else:
                        print("Choix invalide. Veuillez réessayer.")
            elif any(medecin.nom == username for medecin in medecins):
                medecin_connecte = next(medecin for medecin in medecins if medecin.nom == username)
                print("Connecté en tant que médecin.")
                while True:
                    afficher_menu_medecin()
                    choix_medecin = input("Entrez votre choix : ")
                    if choix_medecin == "1":
                        afficher_rendez_vous_medecin(medecin_connecte)
                    elif choix_medecin == "2":
                        break
                    else:
                        print("Choix invalide. Veuillez réessayer.")
            else:
                print("Nom d'utilisateur ou mot de passe incorrect.")
        elif choix == "3":
            print("Au Revoir! Merci de nous faire confiance")
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main()
