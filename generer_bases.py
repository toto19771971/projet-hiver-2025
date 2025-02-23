import pandas as pd
from datetime import datetime, timedelta

# Génération de bd_clients.xlsx
data_clients = {
    "Code client": [f"CLI-{i:03}" for i in range(1, 21)],
    "Nom du client": [f"Client {i}" for i in range(1, 21)],
    "Personne responsable": [f"Responsable {i}" for i in range(1, 21)],
    "Adresse": [f"Rue {i}, {i*10}" for i in range(1, 21)],
    "NPA/Ville": [f"{i*1000} Ville {i}" for i in range(1, 21)],
    "No téléphone 1": [f"+41 {i*1000000}" for i in range(1, 21)],
    "No téléphone 2": [f"+41 {i*1000001}" for i in range(1, 21)],
    "Site internet": [f"www.client{i}.com" for i in range(1, 21)],
    "E-mail": [f"contact@client{i}.com" for i in range(1, 21)],
    "Compte à créditer": [f"CC-{i}" for i in range(1, 21)],
    "Compte à débiter": [f"CD-{i}" for i in range(1, 21)],
    "Taux TVA 1": [7.7 for _ in range(20)],
    "Taux TVA 2": [2.5 for _ in range(20)],
    "Délai de paiement": [30 for _ in range(20)],
    "Nom de la banque": [f"Banque {i}" for i in range(1, 21)],
    "NPA/Ville banque": [f"{i*1000} Ville Banque {i}" for i in range(1, 21)],
    "No de compte": [f"CH{i}123456789" for i in range(1, 21)],
    "IBAN": [f"CH{i}1234567890123456789" for i in range(1, 21)],
    "Commentaire": [f"Commentaire client {i}" for i in range(1, 21)]
}

df_clients = pd.DataFrame(data_clients)
df_clients.to_excel('bd_clients.xlsx', index=False)

# Génération de bd_factures_clients.xlsx
data_factures = {
    "N° de facture": [f"FACT-CLI-{i:03}" for i in range(1, 21)],
    "Client": [f"Client {i}" for i in range(1, 21)],
    "N° de commande": [f"CMD-{i:04}" for i in range(1001, 1021)],
    "Payé": ["Oui" if i % 2 == 0 else "Non" for i in range(20)],
    "N° de compte client": [f"CC-{i}" for i in range(1, 21)],
    "Annuler": ["Non" for _ in range(20)],
    "Date de facture De": [datetime(2023, 1, 1) + timedelta(days=i) for i in range(20)],
    "Date de facture Vers": [datetime(2023, 1, 5) + timedelta(days=i) for i in range(20)],
    "Date d'échéance De": [datetime(2023, 2, 1) + timedelta(days=i) for i in range(20)],
    "Date d'échéance Vers": [datetime(2023, 2, 5) + timedelta(days=i) for i in range(20)],
    "Date échéance remise De": [datetime(2023, 3, 1) + timedelta(days=i) for i in range(20)],
    "Date échéance remise Vers": [datetime(2023, 3, 5) + timedelta(days=i) for i in range(20)],
    "Date paiement prévu De": [datetime(2023, 4, 1) + timedelta(days=i) for i in range(20)],
    "Date paiement prévu Vers": [datetime(2023, 4, 5) + timedelta(days=i) for i in range(20)],
    "Ancien code client": [f"OLD-CLI-{i:03}" for i in range(1, 21)],
    "Trier selon": ["Date" for _ in range(20)],
    "Statut": ["En attente" if i % 2 == 0 else "Validé" for i in range(20)],
    "Devise": ["CHF" for _ in range(20)]
}

df_factures = pd.DataFrame(data_factures)
df_factures.to_excel('bd_factures_clients.xlsx', index=False)

print("Fichiers Excel générés avec succès : bd_clients.xlsx et bd_factures_clients.xlsx")









body {
  font-family: Arial, sans-serif;
  margin: 20px;
}

/* Conteneur centré avec largeur limitée */
.container {
  max-width: 600px;
  margin: 0 auto;
}

h1 {
  color: #333;
}

.buttons button {
  background-color: #007BFF;
  color: white;
  border: none;
  padding: 10px 15px;
  cursor: pointer;
  font-size: 16px;
  border-radius: 5px;
  margin-right: 10px;
}

.buttons button:hover {
  background-color: #0056b3;
}

.suggestions {
  border: 1px solid #ccc;
  background: white;
  max-height: 150px;
  overflow-y: auto;
  position: absolute;
  width: 250px;
  z-index: 10;
}

.suggestions div {
  padding: 5px;
  cursor: pointer;
}

.suggestions div:hover {
  background-color: #e9e9e9;
}

.mandatory::after {
  content: " *";
  color: red;
}

.form-group {
  margin-bottom: 10px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input, select, textarea {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}







