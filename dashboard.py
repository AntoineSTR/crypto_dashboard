import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import os

# Chemins des fichiers
data_path = "/home/streich/crypto_git/data/data.csv"
report_path = "/home/streich/crypto_git/data/daily_report.csv"

# Charger les données
def load_data():
    if os.path.exists(data_path):
        df = pd.read_csv(data_path, names=["timestamp", "price"], dtype=str)
        df["timestamp"] = pd.to_datetime(df["timestamp"].str.strip(), format="%Y-%m-%d %H:%M:%S", errors="coerce")
        df["price"] = df["price"].astype(float)
        return df.dropna()
    return pd.DataFrame(columns=["timestamp", "price"])

# Charger le dernier rapport journalier
def load_daily_report():
    if os.path.exists(report_path):
        df = pd.read_csv(report_path)
        return df.iloc[-1].to_dict() if not df.empty else None
    return None

# Initialisation de l'application Dash
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1("Prix de l'Ethereum en temps réel", style={'textAlign': 'center'}),
    dcc.Graph(id='live-graph'),
    
    # Section pour afficher le rapport journalier
    html.Div(id='daily-report', style={'marginTop': '20px', 'textAlign': 'center'}),
    
    dcc.Interval(
        id='interval-component',
        interval=300000,  # Mise à jour toutes les 5 minutes
        n_intervals=0
    )
])

@app.callback(
    Output('live-graph', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_graph(n):
    df = load_data()
    if df.empty:
        return {
            'data': [],
            'layout': {'title': 'Aucune donnée disponible', 'xaxis': {'title': 'Temps'}, 'yaxis': {'title': 'Prix (USD)'}}
        }

    return {
        'data': [{'x': df["timestamp"], 'y': df["price"], 'type': 'line', 'name': 'ETH/USD'}],
        'layout': {'title': 'Évolution du prix de l’Ethereum', 'xaxis': {'title': 'Temps'}, 'yaxis': {'title': 'Prix (USD)'}}
    }

@app.callback(
    Output('daily-report', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_report(n):
    report = load_daily_report()
    if not report:
        return html.P("Aucun rapport journalier disponible.")
    
    return html.Div([
        html.H3(f"Rapport du {report['date']}"),
        html.P(f"📌 **Prix d'ouverture** : {report['open_price']} USD"),
        html.P(f"📌 **Prix de clôture** : {report['close_price']} USD"),
        html.P(f"📌 **Volatilité** : {report['volatility']:.2f} USD"),
        html.P(f"📌 **Évolution** : {report['evolution']:.2f} %")
    ])

# Lancer le serveur
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
