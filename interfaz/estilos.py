import tkinter as tk
from tkinter import ttk


class Estilos:

    FONDO = "#F4F6F8"
    PANEL = "#FFFFFF"

    PRINCIPAL = "#2563EB"
    PRINCIPAL_HOVER = "#1D4ED8"

    TEXTO = "#1F2937"
    TEXTO_SECUNDARIO = "#6B7280"

    BORDE = "#D1D5DB"

    EXITO = "#16A34A"
    ERROR = "#DC2626"

    @staticmethod
    def configurar():

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "TFrame",
            background=Estilos.FONDO
        )

        style.configure(
            "Panel.TFrame",
            background=Estilos.PANEL
        )

        style.configure(
            "TLabel",
            background=Estilos.FONDO,
            foreground=Estilos.TEXTO,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Titulo.TLabel",
            background=Estilos.FONDO,
            foreground=Estilos.TEXTO,
            font=("Segoe UI", 20, "bold")
        )

        style.configure(
            "Subtitulo.TLabel",
            background=Estilos.FONDO,
            foreground=Estilos.TEXTO_SECUNDARIO,
            font=("Segoe UI", 10)
        )

        style.configure(
            "PanelTitulo.TLabel",
            background=Estilos.PANEL,
            foreground=Estilos.TEXTO,
            font=("Segoe UI", 12, "bold")
        )

        style.configure(
            "TButton",
            font=("Segoe UI", 10),
            padding=(10, 7)
        )

        style.configure(
            "Principal.TButton",
            background=Estilos.PRINCIPAL,
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            padding=(15, 9)
        )

        style.map(
            "Principal.TButton",
            background=[
                ("active", Estilos.PRINCIPAL_HOVER)
            ]
        )

        style.configure(
            "TEntry",
            padding=8,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Treeview",
            font=("Segoe UI", 10),
            rowheight=30
        )

        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold")
        )