#!/bin/sh
# Usage : sh deploy.sh https://TON-NOM:TON-TOKEN@github.com/TON-NOM/NOM-DU-DEPOT.git
[ -z "$1" ] && { echo "Il manque l'adresse du depot GitHub."; exit 1; }
git init -q
git config user.email "club@cahier.local"
git config user.name "Cahier d'appel"
git branch -M main
git add -A
git commit -q -m "Cahier d'appel" || echo "(rien de nouveau a enregistrer)"
git remote remove origin 2>/dev/null
git remote add origin "$1"
git push -u origin main --force && echo "OK : envoye. Va dans l'onglet Actions de ton depot GitHub."
echo "--- Fichiers envoyes :"
git ls-files
