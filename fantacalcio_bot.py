import json
import unicodedata
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from rapidfuzz import fuzz, process

TELEGRAM_TOKEN = "8416948981:AAFq-NMzcwKC9mLtX-zqR5cl8DUhWc6_Dwg"

# Carica i giocatori dal file JSON
with open("giocatori.json", "r", encoding="utf-8") as f:
    giocatori = json.load(f)

# Funzione di normalizzazione (per gestire maiuscole, accenti, ecc.)
def normalize(s: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", s.lower())
        if unicodedata.category(c) != "Mn"
    )

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "👋 Ciao! Benvenuto nel bot Fantacalcio Serie A 2024/25 ⚽\n\n"
        "Ecco i comandi disponibili:\n"
        "🔹 /start - Mostra questo messaggio\n"
        "🔹 /cerca <nome> - Cerca giocatori simili 🔎\n"
        "🔹 /stats <nome_giocatore> - Statistiche dettagliate 📊\n\n"
        "👉 Prova ad esempio:\n"
        "/cerca lautaro\n"
        "/stats Lautaro Martinez"
    )

# Comando /cerca
async def cerca(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("❌ Per favore scrivi: /cerca <nome>")
        return

    query = normalize(" ".join(context.args))
    nomi = [normalize(player["nome"]) for player in giocatori]

    matches = process.extract(query, nomi, scorer=fuzz.partial_ratio, limit=10)
    valid_matches = [m for m in matches if m[1] >= 60]

    if not valid_matches:
        await update.message.reply_text("❌ Nessun giocatore trovato.")
        return

    elenco = "\n".join(
        [f"- {giocatori[nomi.index(m[0])]['nome']} ({giocatori[nomi.index(m[0])]['squadra']})"
         for m in valid_matches]
    )

    await update.message.reply_text(
        f"🔎 Giocatori trovati simili a '{' '.join(context.args)}':\n\n{elenco}"
    )

# Comando /stats
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("❌ Per favore scrivi: /stats <nome_giocatore>")
        return

    query = normalize(" ".join(context.args))
    nomi = [normalize(player["nome"]) for player in giocatori]

    # 1) Match esatto
    if query in nomi:
        idx = nomi.index(query)
        found = giocatori[idx]

        msg = (
            f"📊 Statistiche Fantacalcio di {found['nome']}\n"
            f"🏆 Squadra: {found['squadra']}\n"
            f"📋 Partite a voto: {found['partite_a_voto']}\n"
            f"⚽ Goal: {found['gol']}\n"
            f"🎯 Assist: {found['assist']}\n"
            f"📈 Media: {found['media']}\n"
            f"⭐ Fantamedia: {found['fantamedia']}"
        )
        await update.message.reply_text(msg)
        return

    # 2) Match simili
    matches = process.extract(query, nomi, scorer=fuzz.partial_ratio, limit=7)
    valid_matches = [m for m in matches if m[1] >= 60]

    if not valid_matches:
        await update.message.reply_text("❌ Nessun giocatore trovato.")
        return

    if len(valid_matches) > 1:
        elenco = "\n".join(
            [f"- {giocatori[nomi.index(m[0])]['nome']} ({giocatori[nomi.index(m[0])]['squadra']})"
             for m in valid_matches]
        )
        await update.message.reply_text(
            f"⚠️ Ho trovato più giocatori simili a '{' '.join(context.args)}':\n\n{elenco}\n\n"
            "👉 Prova a digitare il nome completo per i dettagli."
        )
        return

    # 3) Un match solo → mostra direttamente le statistiche
    best_name = valid_matches[0][0]
    idx = nomi.index(best_name)
    found = giocatori[idx]

    msg = (
        f"📊 Statistiche Fantacalcio di {found['nome']}\n"
        f"🏆 Squadra: {found['squadra']}\n"
        f"📋 Partite a voto: {found['partite_a_voto']}\n"
        f"⚽ Goal: {found['gol']}\n"
        f"🎯 Assist: {found['assist']}\n"
        f"📈 Media: {found['media']}\n"
        f"⭐ Fantamedia: {found['fantamedia']}"
    )
    await update.message.reply_text(msg)

# MAIN
def main() -> None:
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("cerca", cerca))
    app.add_handler(CommandHandler("stats", stats))

    app.run_polling()

if __name__ == "__main__":
    main()
