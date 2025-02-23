from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Chargement des bases de données
df_fournisseurs = pd.read_excel("bd_fournisseurs_fictif.xlsx", dtype=str, keep_default_na=False)
df_tva = pd.read_excel("bd_tva.xlsx", dtype=str, keep_default_na=False)
df_delai = pd.read_excel("bd_delai_de_paiement.xlsx", dtype=str, keep_default_na=False)

# Pour les comptes, on charge chacun depuis son fichier
df_crediter = pd.read_excel("plan_comptable_crediter.xlsx", dtype=str, keep_default_na=False)
df_debiter = pd.read_excel("plan_comptable_debiter.xlsx", dtype=str, keep_default_na=False)

@app.route("/")
def index():
    # Conversion des DataFrames en listes de dictionnaires
    tva_options = df_tva.to_dict(orient="records")
    delai_options = df_delai.to_dict(orient="records")
    crediter_options = df_crediter.to_dict(orient="records")
    debiter_options = df_debiter.to_dict(orient="records")

    return render_template(
        "recherche_fournisseurs.html",
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

if __name__ == "__main__":
    app.run(debug=True, port=5000)
