# 💸 Crypto Dashboard - ETH Tracker en Temps Réel

Suivi du prix de l'Ethereum (ETH) en temps réel via un scraping automatique et un dashboard interactif hébergé 24/24 sur AWS.

---

## 🚀 Fonctionnalités

- 📊 **Dashboard interactif avec Dash** (Python)  
- 📅 **Sélecteur de date dynamique** pour consulter l'évolution quotidienne  
- 🔁 **Scraping toutes les 5 minutes** via un script Bash (`scraper.sh`)  
- 📈 **Rapport quotidien automatique** généré à 20h (`daily_report.py`)  
- 💾 Données stockées en CSV pour persistance et historique  
- 🌍 Déploiement en continu sur une VM AWS Ubuntu  
- 🔐 Projet accessible en ligne via IP publique (ou Elastic IP)

---

## 📂 Architecture du projet

```bash
crypto_dashboard/
│
├── data/
│   ├── data.csv               # Données scrapées (timestamp, prix)
│   └── daily_report.csv       # Rapport quotidien généré à 20h
│
├── scraper.sh                 # Script Bash de scraping (cron toutes les 5min)
├── daily_report.py            # Script Python de génération du rapport journalier
├── dashboard.py               # Dashboard Dash avec visualisation interactive
├── requirements.txt           # Dépendances Python
└── logs/
    ├── scraper.log            # Logs du cron du scraper
    └── report.log             # Logs du rapport journalier
```
---

## ⚙️ Technologies utilisées

- 🐍 Python 3.12
- 📦 Dash (Plotly)
- 📄 Pandas
- 💻 Bash Script
- 🐧 Ubuntu 22.04 LTS (AWS EC2)
- ☁️ AWS EC2 Free Tier

---

## 📅 Automatisation

| Tâche             | Fréquence   | Méthode       |
|------------------|-------------|---------------|
| `scraper.sh`     | Toutes les 5 min | `cron`       |
| `daily_report.py`| Tous les jours à 20h | `cron`  |

---

## 🚦 Lancer le projet en local

```bash
# Cloner le projet
git clone https://github.com/<ton-user>/crypto_dashboard.git
cd crypto_dashboard

# Créer et activer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer le dashboard
python3 dashboard.py

Puis aller sur http://localhost:8050
```
---

## ☁️ Déploiement sur AWS
- Instance EC2 : t2.micro (Free Tier)
- Port 8050 ouvert (custom TCP)
- IP publique ou Elastic IP
- Projet cloné et exécuté avec screen
- Cron configuré pour automatiser le scraping et les rapports

---

## ✍️ Auteurs
- Antoine STREICHENBERGER
- Tancrède TARANTINO
