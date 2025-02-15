from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)


# ✅ Chargement des bases de données
df_fournisseurs = pd.read_excel("bd_fournisseurs_fictif.xlsx")
df_tva = pd.read_excel("bd_tva.xlsx", dtype=str, keep_default_na=False)
df_tva["Taux TVA"] = df_tva["Taux TVA"].astype(str)  # S'assurer que les valeurs sont bien des chaînes
df_delai_paiement = pd.read_excel("bd_delai_de_paiement.xlsx", dtype=str, keep_default_na=False)
df_plan_comptable_crediter = pd.read_excel("plan_comptable_crediter.xlsx", dtype=str, keep_default_na=False)
df_plan_comptable_debiter = pd.read_excel("plan_comptable_debiter.xlsx", dtype=str, keep_default_na=False)

# ✅ Extraction des données pour les menus déroulants
tva_options = df_tva["Taux TVA"].dropna().tolist()
delai_paiement_options = df_delai_paiement["Délai de paiement"].dropna().tolist()
comptes_crediter = df_plan_comptable_crediter["Numéro de compte"].dropna().tolist()

# ✅ Construction de la liste complète pour le menu déroulant "Compte à débiter"
comptes_debiter = df_plan_comptable_debiter.apply(
    lambda row: f"{row['Numéro de compte']} - {row['Libellé']} - {row['Catégorie']}",
    axis=1
).dropna().tolist()

# 🔹 Vérification des chargements
print("🔹 Options TVA chargées :", tva_options)
print("🔹 Délai de paiement chargés :", delai_paiement_options)
print("🔹 Comptes à créditer chargés :", comptes_crediter)
print("🔹 Comptes à débiter chargés :", comptes_debiter)

@app.route("/", methods=["GET"])
def index():
    return render_template(
        "recherche_fournisseurs.html",
        tva_options=tva_options,
        comptes_crediter=comptes_crediter,
        comptes_debiter=comptes_debiter,
        delai_paiement_options=delai_paiement_options
    )
@app.route("/creer", methods=["POST"])
def creerfournisseur():
    try:
        data = request.form.to_dict()
        print("🔹 Données reçues :", data)  # Debugging

        # Vérifier que toutes les zones obligatoires sont remplies
        required_fields = [
            "Code fournisseur", "Nom du fournisseur", "NPA/Ville", "No téléphone 1",
            "Compte à créditer", "Compte à débiter", "Délai de paiement"
        ]
        missing_fields = [field for field in required_fields if not data.get(field)]

        if missing_fields:
            print(f"❌ Champs obligatoires manquants : {missing_fields}")
            return jsonify({"message": f"Veuillez remplir : {', '.join(missing_fields)}"}), 400 

         # ✅ Ajout des données dans le fichier Excel
        global df_fournisseurs  # Nécessaire pour modifier la variable globale
        df_fournisseurs = df_fournisseurs.append(data, ignore_index=True)
        df_fournisseurs.to_excel("bd_fournisseurs_fictif.xlsx", index=False)

        return jsonify({"message": "Fournisseur ajouté avec succès !"}), 200

    except Exception as e:
        print(f"❌ Erreur : {e}")
        return jsonify({"message": f"Une erreur s'est produite : {e}"}), 500

if __name__ == "__main__":
     app.run(debug=True, port=5000)
