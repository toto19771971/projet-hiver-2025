import pandas as pd 

# Création d'un plan comptable suisse fictif
plan_comptable_data = {
    "Numéro de compte": ["2000", "2001", "2002", "2003", "2004"],
    "Libellé": ["Caisse", "Banque", "Créances clients", "Dettes fournisseurs", "Stocks"]
}

# Création du DataFrame
df_plan_comptable = pd.DataFrame(plan_comptable_data)

# Sauvegarde du fichier Excel
df_plan_comptable.to_excel("plan_comptable.xlsx", index=False, engine='openpyxl')

print("✅ Fichier 'plan_comptable.xlsx' créé avec succès !")
