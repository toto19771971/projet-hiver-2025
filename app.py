from flask import Flask, render_template, request, jsonify
import pandas as pd


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu_principal')
def menu_principal():
    return render_template('menu_principal.html')

@app.route('/menu_comptabilite')
def menu_comptabilite():
    return render_template('menu_comptabilite.html')

@app.route('/comptabilite_fournisseurs')
def comptabilite_fournisseurs():
    return render_template('templates_fournisseurs/comptabilite_fournisseurs.html')

@app.route('/recherche_factures_fournisseurs')
def recherche_factures_fournisseurs():
    return render_template('templates_fournisseurs/recherche_factures_fournisseurs.html')

# Chargement des bases de données
df_fournisseurs = pd.read_excel("bd_fournisseurs_fictif.xlsx", dtype=str, keep_default_na=False)
df_tva = pd.read_excel("bd_tva.xlsx", dtype=str, keep_default_na=False)
df_delai = pd.read_excel("bd_delai_de_paiement.xlsx", dtype=str, keep_default_na=False)

# Pour les comptes, on charge chacun depuis son fichier
df_crediter = pd.read_excel("plan_comptable_crediter.xlsx", dtype=str, keep_default_na=False)
df_debiter = pd.read_excel("plan_comptable_debiter.xlsx", dtype=str, keep_default_na=False)

@app.route('/recherche_fournisseurs')
def recherche_fournisseurs():
    print("==> Page recherche_fournisseurs rechargée <==")
    # Conversion des DataFrames en listes de dictionnaires
    tva_options = df_tva.to_dict(orient="records")
    delai_options = df_delai.to_dict(orient="records")
    crediter_options = df_crediter.to_dict(orient="records")
    debiter_options = df_debiter.to_dict(orient="records")

    print("✅ Options envoyées :", {
        "tva": tva_options[:5],  # Montre les 5 premiers éléments pour vérifier
        "delai": delai_options[:5],
        "crediter": crediter_options[:5],
        "debiter": debiter_options[:5]
})

    print("🔎 Vérification : TVA options envoyées :", tva_options)

    return render_template('templates_fournisseurs/recherche_fournisseurs.html',
    tva_options=tva_options,
    delai_options=delai_options,
    crediter_options=crediter_options,
    debiter_options=debiter_options
)

@app.route("/autocomplete", methods=["GET"])
def autocomplete():
    query = request.args.get("query", "").strip().lower()
    if not query:
        return jsonify([])

    results = df_fournisseurs[
        df_fournisseurs["Code fournisseur"].str.lower().str.startswith(query) |
        df_fournisseurs["Nom du fournisseur"].str.lower().str.startswith(query)
        ].to_dict(orient="records")
    return jsonify(results)

@app.route("/modifier", methods=["POST"])
def modifier():
    try:
        data = request.form.to_dict()
        code = data.get("Code fournisseur")
        if not code:
            return jsonify({"message": "Code fournisseur manquant !"}), 400

        idx = df_fournisseurs[df_fournisseurs["Code fournisseur"] == code].index
        if idx.empty:
            return jsonify({"message": "Fournisseur non trouvé !"}), 404

        for key, value in data.items():
            df_fournisseurs.at[idx[0], key] = value

        df_fournisseurs.to_excel("bd_fournisseurs_fictif.xlsx", index=False)
        return jsonify({"message": "Fournisseur modifié avec succès !"}), 200

    except Exception as e:
        return jsonify({"message": f"Erreur : {str(e)}"}), 500

@app.route("/creer", methods=["POST"])
def creer_fournisseur():
    global df_fournisseurs
    try:
        data = request.form.to_dict()
        print("📌 Données reçues pour création :", data)  # Debug

        mandatory_fields = [
            "Code fournisseur", "Nom du fournisseur", "No téléphone 1",
            "Compte à créditer", "Compte à débiter", "Taux TVA 1", "Délai de paiement"
        ]
        for field in mandatory_fields:
            if not data.get(field) or not data[field].strip():
                return jsonify({"message": f"Champ obligatoire manquant: {field}"}), 400
        if not df_fournisseurs[df_fournisseurs["Code fournisseur"] == data.get("Code fournisseur")].empty:
            return jsonify({"message": "Fournisseur existe déjà !"}), 400

        new_row_df = pd.DataFrame([data])
        df_fournisseurs = pd.concat([df_fournisseurs, new_row_df], ignore_index=True)
        df_fournisseurs.to_excel("bd_fournisseurs_fictif.xlsx", index=False)
        return jsonify({"message": "Fournisseur créé avec succès !"}), 200
    except Exception as e:
        return jsonify({"message": f"Erreur lors de la création du fournisseur: {str(e)}"}), 500


@app.route("/supprimer", methods=["POST"])
def supprimer_fournisseur():
    global df_fournisseurs
    try:
        data = request.form.to_dict()
        code = data.get("Code fournisseur")
        if not code or not code.strip():
            return jsonify({"message": "Champ obligatoire manquant: Code fournisseur (pour supprimer)"}), 400
        index = df_fournisseurs[df_fournisseurs["Code fournisseur"] == code].index
        if index.empty:
            return jsonify({"message": "Fournisseur non trouvé !"}), 404
        df_fournisseurs = df_fournisseurs.drop(index)
        df_fournisseurs.to_excel("bd_fournisseurs_fictif.xlsx", index=False)
        return jsonify({"message": "Fournisseur supprimé avec succès !"}), 200
    except Exception as e:
        return jsonify({"message": f"Erreur lors de la suppression du fournisseur: {str(e)}"}), 500
    

@app.route('/comptabilite_clients')
def comptabilite_clients():
        return render_template('templates_clients/comptabilite_clients.html')

@app.route('/recherche_clients')
def recherche_clients():
    return render_template('templates_clients/recherche_clients.html')

@app.route('/recherche_factures_clients')
def recherche_factures_clients():
    return render_template('templates_clients/recherche_factures_clients.html')

@app.route('/salaires_rh_menu')
def salaires_rh_menu():
    return render_template('templates_rh/salaires_rh_menu.html')

@app.route('/gestion_employes')
def gestion_employes():
    return render_template('templates_rh/gestion_employes.html')

@app.route('/traitement_salaires')
def traitement_salaires():
    return render_template('templates_rh/traitement_salaires.html')



if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))  # Utilise le port donné par Render, sinon 5000 par défaut
    app.run(host='0.0.0.0', port=port, debug=True)
