# modulo_db.py
import sqlite3
import json
from datetime import datetime

DB_PATH = "comandas.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS comandas (
            id TEXT PRIMARY KEY,
            created_at TEXT,
            customer TEXT,
            items TEXT,
            total REAL,
            notes TEXT,
            status TEXT,
            image_path TEXT,
            remote_id TEXT
        )
    """)
    conn.commit()
    conn.close()

def agregar_comanda(cid, customer, items, total, notes, image_path):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO comandas VALUES (?,?,?,?,?,?,?,?,?)
    """, (
        cid,
        datetime.utcnow().isoformat(),
        customer,
        json.dumps(items) if isinstance(items, list) else items,
        total,
        notes,
        "NEW",
        image_path,
        None
    ))
    conn.commit()
    conn.close()

def obtener_comandas():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM comandas ORDER BY created_at DESC")
    data = cur.fetchall()
    conn.close()
    return data

def obtener_comanda(cid):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM comandas WHERE id=?", (cid,))
    data = cur.fetchone()
    conn.close()
    return data

def actualizar_comanda(cid, customer, items, total, notes):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        UPDATE comandas
        SET customer=?, items=?, total=?, notes=?, status='EDITED'
        WHERE id=?
    """, (customer, items, total, notes, cid))
    conn.commit()
    conn.close()

def marcar_subida(cid, remote_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        UPDATE comandas SET status='UPLOADED', remote_id=? WHERE id=?
    """, (remote_id, cid))
    conn.commit()
    conn.close()
