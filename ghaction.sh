#!/usr/bin/env bash
set -e

export NOW="$(date '+%Y-%m-%d')"

cd "$(dirname "$(readlink -f "$0")")"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting data generation"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Running dump.py"
.venv/bin/python dump.py

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Running leaderboard.py"
.venv/bin/python leaderboard.py

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Running legendaries.py"
.venv/bin/python legendaries.py

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Running update_csv.py"
.venv/bin/python update_csv.py

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Running make_plots.py"
.venv/bin/python make_plots.py

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Data generation complete"

git config --local user.email "actions@github.com"
git config --local user.name "Actions"

git add -A -- "files/Legendaries"*.json
git add -A -- "files/leaderboard.txt"
git add -A -- "data/"*.json
git add -A -- "data/"*.xml
git add -A -- "files/trades.csv"
git add -A -- "files/"*.html

git commit -m "($NOW) Update"
git push

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Data generation complete"
