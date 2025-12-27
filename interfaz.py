# interfaz.py
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import modulo_db as db
import requests

db.init_db()

# ----------- Lanzar API en background -----------
def iniciar_api():
    subprocess.Popen(["python3", "modulo_api.py"])

threading.Thread(target=iniciar_api, daemon=True).start()

# ----------- Funciones -----------

def refrescar():
    tabla.delete(*tabla.get_children())
    data = db.obtener_comandas()
    for row in data:
        cid = row[0]
        tabla.insert("", "end", iid=cid, values=(cid[:8], row[2], row[6], row[3]))

def editar():
    seleccion = tabla.selection()
    if not seleccion:
        return
    cid = seleccion[0]
    datos = db.obtener_comanda(cid)

    win = tk.Toplevel(root)
    win.title("Editar comanda")

    tk.Label(win, text="Cliente").pack()
    e1 = tk.Entry(win)
    e1.insert(0, datos[2] or "")
    e1.pack()

    tk.Label(win, text="Items").pack()
    e2 = tk.Text(win, height=5)
    e2.insert("1.0", datos[3] or "")
    e2.pack()

    tk.Label(win, text="Total").pack()
    e3 = tk.Entry(win)
    e3.insert(0, datos[4] or "")
    e3.pack()

    tk.Label(win, text="Notas").pack()
    e4 = tk.Text(win, height=4)
    e4.insert("1.0", datos[5] or "")
    e4.pack()

    def guardar():
        db.actualizar_comanda(
            cid,
            e1.get(),
            e2.get("1.0", "end"),
            float(e3.get() or 0),
            e4.get("1.0", "end")
        )
        win.destroy()
        refrescar()

    tk.Button(win, text="Guardar", command=guardar).pack()

def subir():
    seleccion = tabla.selection()
    if not seleccion:
        return
    cid = seleccion[0]
    datos = db.obtener_comanda(cid)

    payload = {
        "customer": datos[2],
        "items": datos[3],
        "total": datos[4],
        "notes": datos[5]
    }

    try:
        r = requests.post("https://API_REMOTA_AQUÍ", json=payload)
        if r.status_code in (200, 201):
            remote_id = r.json().get("id")
            db.marcar_subida(cid, remote_id)
            messagebox.showinfo("OK", "Comanda subida.")
            refrescar()
        else:
            messagebox.showerror("Error", f"Respuesta remota: {r.text}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# ----------- UI -----------

root = tk.Tk()
root.title("Comandas Local - Infinity")

tabla = ttk.Treeview(root, columns=("id","cliente","estado","items"), show="headings")
tabla.heading("id", text="ID")
tabla.heading("cliente", text="Cliente")
tabla.heading("estado", text="Estado")
tabla.heading("items", text="Items")
tabla.pack(fill="both", expand=True)

btn_frame = tk.Frame(root)
btn_frame.pack()

tk.Button(btn_frame, text="Refrescar", command=refrescar).pack(side="left")
tk.Button(btn_frame, text="Editar", command=editar).pack(side="left")
tk.Button(btn_frame, text="Subir", command=subir).pack(side="left")

refrescar()
root.mainloop()
