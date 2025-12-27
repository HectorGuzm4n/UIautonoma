# modulo_api.py
from flask import Flask, request, jsonify
import uuid
import modulo_db as db
import json
import os

app = Flask(__name__)

UPLOADS = "uploads"
os.makedirs(UPLOADS, exist_ok=True)

@app.route("/scan", methods=["POST"])
def recibir_comanda():
    data = request.get_json()
    cid = str(uuid.uuid4())

    image_path = None
    if "image_base64" in data:
        import base64
        img_bytes = base64.b64decode(data["image_base64"])
        image_path = f"{UPLOADS}/{cid}.jpg"
        with open(image_path, "wb") as f:
            f.write(img_bytes)

    db.agregar_comanda(
        cid=cid,
        customer=data.get("customer"),
        items=data.get("items"),
        total=data.get("total"),
        notes=data.get("notes"),
        image_path=image_path
    )

    return jsonify({"ok": True, "id": cid})

def iniciar_servidor():
    db.init_db()
    app.run(host="0.0.0.0", port=6000)
