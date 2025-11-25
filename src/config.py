# src/config.py
import os

# 讀取 api.txt
API_KEY_PATH = os.path.join(os.path.dirname(__file__), "../API.txt")

with open(API_KEY_PATH, "r") as f:
    API_KEY = f.read().strip()

BASE_URL = "https://api-gateway.netdb.csie.ncku.edu.tw"
MODEL_NAME = "gpt-oss:120b"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}