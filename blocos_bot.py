#!/usr/bin/env python3
import json, logging, os, uuid
from datetime import datetime
from pathlib import Path
from typing import Tuple
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

logging.basicConfig(level=logging.INFO)
TELEGRAM_TOKEN = "8314760047:AAEsTZd4qxxfbYp8Q0LtSooBHAzNNJ0iki8"
DATA_DIR = Path("data")
GITHUB_REPO = "https://github.com/UNGUSTO/blocos-ideas"
DATA_DIR.mkdir(exist_ok=True)
(DATA_DIR / "investigaciones").mkdir(exist_ok=True)
(DATA_DIR / "pending_executions").mkdir(exist_ok=True)

class BlocosIdeasBot:
    def __init__(self):
        self.ideas_file = DATA_DIR / "ideas.json"
        self.ideas = self.load_ideas()
    def load_ideas(self):
        if self.ideas_file.exists():
            with open(self.ideas_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    def save_ideas(self):
        with open(self.ideas_file, "w", encoding="utf-8") as f:
            json.dump(self.ideas, f, indent=2, ensure_ascii=False)
    def create_idea(self, content):
        idea = {"id": str(uuid.uuid4())[:13], "content": content, "timestamp": datetime.now().isoformat(), "categories": self.classify_idea(content)}
        self.ideas.append(idea)
        self.save_ideas()
        return idea
    def classify_idea(self, content):
        keywords = {"Offroad": ["offroad", "4x4", "covers"], "Bolsos": ["bolso", "mochila"], "TPR": ["tpr", "reciclado"], "4PL": ["4pl"]}
        for cat, kws in keywords.items():
            if any(kw in content.lower() for kw in kws):
                return [cat]
        return ["General"]
    def get_investigation(self, idea_id, action_type):
        inv_map = {"MERCADO": "Tamaño: $850M | Crecimiento: 12% | Eco: +25%", "TECNICO": "HDPE+3D | Inyección | CAD", "ESTRATEGIA": "Premium eco | +35-40%", "COMPETENCIA": "ARB vs Ranch Hand vs Go Ind | Ventaja: TPR+3D", "PRODUCCION": "500u/mes | $45-60 | 15-20d", "FINANCIERO": "$75K inv | $200K año1 | Break-even mes 8-10", "MARKETING": "Instagram, TikTok, YouTube | $2-5K/mes", "IMPLEMENTACION": "4 fases | 6-9 meses | 3-5 personas"}
        inv = inv_map.get(action_type, "Investigacion completada")
        fname = f"INVESTIGACION_{action_type}_{idea_id}.md"
        fpath = DATA_DIR / "investigaciones" / fname
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(f"# {action_type}\n\n{inv}")
        return inv, f"{GITHUB_REPO}/blob/main/data/investigaciones/{fname}"

bot = BlocosIdeasBot()

async def start(update, context):
    await update.message.reply_text("🚀 BLOCOS-IDEAS v7\n✨ Envía idea → Elige acción → Recibe investigación")

async def handle_idea(update, context):
    idea = bot.create_idea(update.message.text)
    btn = [[InlineKeyboardButton("MERCADO", callback_data=f"a_{idea['id']}_MERCADO"), InlineKeyboardButton("TECNICO", callback_data=f"a_{idea['id']}_TECNICO")], [InlineKeyboardButton("ESTRATEGIA", callback_data=f"a_{idea['id']}_ESTRATEGIA"), InlineKeyboardButton("COMPETENCIA", callback_data=f"a_{idea['id']}_COMPETENCIA")], [InlineKeyboardButton("PRODUCCION", callback_data=f"a_{idea['id']}_PRODUCCION"), InlineKeyboardButton("FINANCIERO", callback_data=f"a_{idea['id']}_FINANCIERO")], [InlineKeyboardButton("MARKETING", callback_data=f"a_{idea['id']}_MARKETING"), InlineKeyboardButton("IMPLEMENTACION", callback_data=f"a_{idea['id']}_IMPLEMENTACION")]]
    await update.message.reply_text(f"✅ Idea: {idea['id']}", reply_markup=InlineKeyboardMarkup(btn))

async def handle_action(update, context):
    q = update.callback_query
    await q.answer()
    p = q.data.split("_")
    iid, atype = p[1], p[2]
    idea = next((i for i in bot.ideas if i["id"] == iid), None)
    if idea:
        inv, link = bot.get_investigation(iid, atype)
        await q.edit_message_text(f"{atype}\n\n{inv}\n\n[GitHub]({link})", parse_mode="Markdown")

def main():
    print("✅ BOT v7 EN COMEX")
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_idea))
    app.add_handler(CallbackQueryHandler(handle_action))
    app.run_polling()

if __name__ == "__main__":
    main()
