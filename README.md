# FantaBot Telegram — Starter per Railway

## File inclusi
- `bot.py` — codice del bot (usa variabile d'ambiente `TELEGRAM_TOKEN`)
- `requirements.txt` — dipendenze Python
- `Procfile` — indica a Railway come avviare il bot (processo *worker*)
- **Non dimenticare di aggiungere `giocatori.json`** nella root del repo (stesso livello di `bot.py`).

## Passi rapidi (Railway)
1. Crea un repository su GitHub e carica: `bot.py`, `requirements.txt`, `Procfile` e **il tuo `giocatori.json`**.
2. Vai su https://railway.app → *New Project* → *Deploy from GitHub Repo* → seleziona il repo.
3. Dopo il primo deploy, apri *Project → Variables* e aggiungi:
   - `TELEGRAM_TOKEN` = il token del bot (da @BotFather).
4. Railway avvierà il processo `worker: python bot.py` e il bot sarà online.
5. Controlla i log in *Deployments → Logs* in caso di problemi.

## Comandi del bot
- `/start` — benvenuto + guida
- `/cerca <nome>` — elenco di giocatori simili
- `/stats <nome_giocatore>` — statistiche

## Test locali (opzionale)
```
python -m venv .venv
. .venv/Scripts/activate   # Windows
# oppure: source .venv/bin/activate  # macOS/Linux

pip install -r requirements.txt

# Imposta il token nell'ambiente
set TELEGRAM_TOKEN=IL_TUO_TOKEN      # Windows CMD
# PowerShell:  $env:TELEGRAM_TOKEN="IL_TUO_TOKEN"
export TELEGRAM_TOKEN=IL_TUO_TOKEN   # macOS/Linux

python bot.py
```