#!/bin/bash

# Définition de l'URL de la crypto
ETHEREUM_URL="https://crypto.com/price/ethereum"

# Extraction du prix avec grep et Regex
PRICE=$(curl -s "$ETHEREUM_URL" | grep -oP '(?<=<span class="chakra-text css-13hqrwd">).*?(?=</span>)')

# Récupération de la date et de l'heure
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# Nettoyage du format du prix pour éviter les erreurs de parsing
CLEAN_PRICE=$(echo "$PRICE" | sed 's/[^0-9.]//g')

# Stockage des données dans un fichier CSV propre
echo "$TIMESTAMP,$CLEAN_PRICE" >> /home/streich/crypto_git/data/data.csv

# Affichage pour debug
echo "[$TIMESTAMP] ETH Price: $CLEAN_PRICE"
