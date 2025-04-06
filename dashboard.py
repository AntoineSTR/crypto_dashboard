import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import os
from pytz import timezone
from datetime import datetime

# Chemins des fichiers
data_path = "/home/ubuntu/crypto_dashboard/data/data.csv"
report_path = "/home/ubuntu/crypto_dashboard/data/daily_report.csv"

# Charger les données
def load_data():
    if os.path.exists(data_path):
        df = pd.read_csv(data_path, names=["timestamp", "price"], dtype=str)
        df["timestamp"] = pd.to_datetime(df["timestamp"].str.strip(), errors="coerce")
        df["price"] = pd.to_numeric(df["price"], errors="coerce")
        df = df.dropna(subset=["timestamp", "price"])
        return df
    return pd.DataFrame(columns=["timestamp", "price"])

# Extraire les dates disponibles
def get_available_dates(df):
    if df.empty or "timestamp" not in df.columns:
        return []
    return sorted(df["timestamp"].dt.strftime("%Y-%m-%d").unique(), reverse=True)

# Charger le dernier rapport
def load_daily_report():
    if os.path.exists(report_path):
        df = pd.read_csv(report_path)
        return df.iloc[-1].to_dict() if not df.empty else None
    return None

# Initialisation Dash
app = dash.Dash(__name__)
app.title = "Crypto Dashboard"

app.layout = html.Div(children=[
    html.H1("Prix de l'Ethereum par jour", style={'textAlign': 'center'}),

    html.Div([
        html.Label("Choisis une date :"),
        dcc.Dropdown(id='date-dropdown', options=[], value=None)
    ], style={'width': '300px', 'margin': 'auto'}),

    dcc.Graph(id='daily-graph'),

    html.Div(id='daily-report', style={'marginTop': '20px', 'textAlign': 'center'}),

    # Rafraîchissement automatique
    dcc.Interval(
        id='interval-refresh',
        interval=5 * 60 * 1000,  # toutes les 5 minutes
        n_intervals=0
    )
])

# Callback pour mettre à jour la liste des dates disponibles
@app.callback(
    Output('date-dropdown', 'options'),
    Output('date-dropdown', 'value'),
    Input('interval-refresh', 'n_intervals')
)
def update_available_dates(n):
    df = load_data()
    available_dates = get_available_dates(df)
    options = [{'label': date, 'value': date} for date in available_dates]
    return options, available_dates[0] if available_dates else None

# Callback pour mettre à jour le graphe
@app.callback(
    Output('daily-graph', 'figure'),
    Input('date-dropdown', 'value')
)
def update_graph(selected_date):
    df = load_data()
    if df.empty or not selected_date:
        return {
            'data': [],
            'layout': {'title': 'Aucune donnée disponible', 'xaxis': {'title': 'Temps'}, 'yaxis': {'title': 'Prix (USD)'}}
        }

    df_selected = df[df["timestamp"].dt.strftime("%Y-%m-%d") == selected_date]

    return {
        'data': [{
            'x': df_selected["timestamp"],
            'y': df_selected["price"],
            'type': 'line',
            'name': f'ETH/USD - {selected_date}'
        }],
        'layout': {
            'title': f'Évolution du prix le {selected_date}',
            'xaxis': {'title': 'Heure'},
            'yaxis': {'title': 'Prix (USD)'}
        }
    }

# Callback pour afficher le rapport
@app.callback(
    Output('daily-report', 'children'),
    Input('date-dropdown', 'value')
)
def update_report(selected_date):
    if not selected_date or not os.path.exists(report_path):
        return html.P("Aucun rapport journalier disponible.")

    df_report = pd.read_csv(report_path)
    row = df_report[df_report["date"] == selected_date]

    if row.empty:
        return html.P("Aucun rapport journalier pour cette date.")

    report = row.iloc[0].to_dict()
    return html.Div([
        html.H3(f"Rapport du {report['date']}"),
        html.P(f"📌 Prix d'ouverture : {report['open_price']} USD"),
        html.P(f"📌 Prix de clôture : {report['close_price']} USD"),
        html.P(f"📌 Volatilité : {report['volatility']:.2f} USD"),
        html.P(f"📌 Évolution : {report['evolution']:.2f} %")
    ])

# Lancer le serveur Dash
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8050)
