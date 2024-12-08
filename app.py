
from flask import Flask, render_template, jsonify
import pandas as pd
from trading_bot import get_data

app = Flask(__name__)

@app.route('/')
def index():
    # Récupère les données pour afficher sur le tableau de bord
    df = get_data()
    if df is not None:
        # Préparer les données pour le graphique
        df = df.tail(50)  # Affiche les 50 dernières entrées
        chart_data = {
            "timestamps": df['timestamp'].astype(str).tolist(),
            "close_prices": df['close'].tolist()
        }
    else:
        chart_data = {"timestamps": [], "close_prices": []}

    return render_template('index.html', chart_data=chart_data)

@app.route('/api/data')
def api_data():
    # Récupère les données au format JSON pour des intégrations
    df = get_data()
    if df is not None:
        return jsonify(df.tail(50).to_dict(orient="records"))
    else:
        return jsonify({"error": "Erreur lors de la récupération des données."})

if __name__ == '__main__':
    app.run(debug=True)
