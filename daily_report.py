import pandas as pd
import os
from datetime import datetime

# Charger les données
file_path = "/home/streich/crypto_git/data/data.csv"
report_path = "/home/streich/crypto_git/data/daily_report.csv"

def generate_daily_report():
    if not os.path.exists(file_path):
        print("Fichier de données introuvable.")
        return
    
    df = pd.read_csv(file_path, names=["timestamp", "price"], dtype=str)
    
    # Nettoyer les données
    df["timestamp"] = pd.to_datetime(df["timestamp"].str.strip(), format="%Y-%m-%d %H:%M:%S", errors="coerce")
    df["price"] = df["price"].astype(float)
    
    # Filtrer pour les données du jour
    today = datetime.now().strftime("%Y-%m-%d")
    df_today = df[df["timestamp"].dt.strftime("%Y-%m-%d") == today]
    
    if df_today.empty:
        print("Aucune donnée pour aujourd'hui.")
        return

    # Calcul des statistiques
    open_price = df_today.iloc[0]["price"]
    close_price = df_today.iloc[-1]["price"]
    volatility = df_today["price"].std()
    evolution = ((close_price - open_price) / open_price) * 100

    # Enregistrement du rapport
    report_data = {
        "date": today,
        "open_price": open_price,
        "close_price": close_price,
        "volatility": volatility,
        "evolution": evolution
    }
    
    report_df = pd.DataFrame([report_data])
    report_df.to_csv(report_path, mode="a", header=not os.path.exists(report_path), index=False)

    print(f"Rapport du {today} généré avec succès.")

if __name__ == "__main__":
    generate_daily_report()
