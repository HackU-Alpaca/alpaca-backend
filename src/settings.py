import json
import os

import dotenv
import firebase_admin
from firebase_admin import credentials, firestore
from linebot import LineBotApi, WebhookHandler

# =========================
# LINEBOT の設定
# =========================
dotenv.load_dotenv()
CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]
LIFFID = os.environ["LIFFID"]

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# =========================
# Firebase の設定
# =========================
cred = credentials.Certificate(json.loads(str(os.environ.get("FIREBASE_KEY"))))
firebase_admin.initialize_app(cred)

db = firestore.client()
