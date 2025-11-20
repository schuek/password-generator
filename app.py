import tkinter as tk
from tkinter import messagebox
import json
import os

# ---------------------------
# Clase Contacto
# ---------------------------
class Contacto:
    def __init__(self, nombre, telefono, email):
        self.nombre = nombre
        self.telefono = telefono
        self.email = email

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "telefono": self.telefono,
            "email": self.email
        }

# ---------------------------
# Clase GestorContactos (lógica)
# ---------------------------
class GestorContactos:
    def __init__(self, archivo="contactos.json"):
        self.archivo = archivo
        self.contactos = []

    def agregar(self, contacto):
        self.contactos.append(contacto)

    def guardar(self):
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump([c.to_dict() for c in self.contactos], f, indent=4)

    def cargar(self):
        if os.path.exists(self.archivo):
            with open(self.archivo, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.contactos = [Contacto(**c) for c in data]

# ---------------------------
# Clase Interfaz (Tkinter)
# ---------------------------
class Interfaz:
    def __init__(self, root, gestor):
        self.root = root
        self.gestor = gestor

        root.title("📇 Contact Manager")
        root.geometry("400x400")

        # Entradas
        tk.Label(root, text="Name:").pack()
        self.entry_nombre = tk.Entry(root)
        self.entry_nombre.pack()

        tk.Label(root, text="Phone:").pack()
        self.entry_telefono = tk.Entry(root)
        self.entry_telefono.pack()

        tk.Label(root, text="Email:").pack()
        self.entry_email = tk.Entry(root)
        self.entry_email.pack()

        # Botones
        tk.Button(root, text="Add Contact", command=self.agregar_contacto).pack(pady=5)
        tk.Button(root, text="Load Contacts", command=self.cargar_contactos).pack(pady=5)

        # Lista de contactos
        self.lista = tk.Listbox(root, width=50)
        self.lista.pack(pady=10, fill="both", expand=True)

        # Al cerrar la ventana → guardar
        root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def agregar_contacto(self):
        nombre = self.entry_nombre.get()
        telefono = self.entry_telefono.get()
        email = self.entry_email.get()

        if not nombre or not telefono or not email:
            messagebox.showwarning("Warning", "All fields are required.")
            return

        contacto = Contacto(nombre, telefono, email)
        self.gestor.agregar(contacto)
        self.lista.insert(tk.END, f"{nombre} | {telefono} | {email}")

        # Limpiar entradas
        self.entry_nombre.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)

    def cargar_contactos(self):
        self.gestor.cargar()
        self.lista.delete(0, tk.END)
        for c in self.gestor.contactos:
            self.lista.insert(tk.END, f"{c.nombre} | {c.telefono} | {c.email}")

    def on_closing(self):
        self.gestor.guardar()
        self.root.destroy()

# ---------------------------
# Programa principal
# ---------------------------
if __name__ == "__main__":
    gestor = GestorContactos()
    root = tk.Tk()
    app = Interfaz(root, gestor)
    root.mainloop()
