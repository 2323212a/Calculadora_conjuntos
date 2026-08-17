import tkinter as tk
from tkinter import ttk, messagebox

from utils.entrada import crear_conjunto_desde_entrada


class DialogoConjunto(tk.Toplevel):

    def __init__(
        self,
        parent,
        titulo="Crear conjunto",
        nombre_inicial="",
        elementos_iniciales="",
        modo="crear"
    ):
        super().__init__(parent)

        self.resultado = None

        self.modo = modo

        self.title(titulo)

        self.geometry("560x420")
        self.minsize(
            500,
            380
        )

        self.transient(parent)
        self.grab_set()

        self.crear_interfaz(
            nombre_inicial,
            elementos_iniciales
        )

        self.protocol(
            "WM_DELETE_WINDOW",
            self.cancelar
        )

    # ==========================================================
    # INTERFAZ
    # ==========================================================

    def crear_interfaz(
        self,
        nombre_inicial,
        elementos_iniciales
    ):

        self.columnconfigure(
            0,
            weight=1
        )

        self.rowconfigure(
            0,
            weight=1
        )

        contenedor = ttk.Frame(
            self,
            padding=25
        )

        contenedor.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        contenedor.columnconfigure(
            0,
            weight=1
        )

        # ======================================================
        # TÍTULO
        # ======================================================

        if self.modo == "editar":

            titulo = "Agregar elementos"

        else:

            titulo = "Crear conjunto"

        ttk.Label(
            contenedor,
            text=titulo,
            font=("Segoe UI", 17, "bold")
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 20)
        )

        # ======================================================
        # NOMBRE
        # ======================================================

        ttk.Label(
            contenedor,
            text="Nombre del conjunto"
        ).grid(
            row=1,
            column=0,
            sticky="w"
        )

        self.entrada_nombre = ttk.Entry(
            contenedor
        )

        self.entrada_nombre.grid(
            row=2,
            column=0,
            sticky="ew",
            pady=(5, 15)
        )

        self.entrada_nombre.insert(
            0,
            nombre_inicial
        )

        # ------------------------------------------------------
        # EN EDICIÓN NO SE PUEDE CAMBIAR EL NOMBRE
        # ------------------------------------------------------

        if self.modo == "editar":

            self.entrada_nombre.config(
                state="disabled"
            )

        # ======================================================
        # CREAR
        # ======================================================

        if self.modo == "crear":

            self.crear_interfaz_crear(
                contenedor
            )

        # ======================================================
        # EDITAR
        # ======================================================

        else:

            self.crear_interfaz_editar(
                contenedor,
                elementos_iniciales
            )

        # ======================================================
        # BOTONES
        # ======================================================

        botones = ttk.Frame(
            contenedor
        )

        botones.grid(
            row=9,
            column=0,
            sticky="e",
            pady=(20, 0)
        )

        ttk.Button(
            botones,
            text="Cancelar",
            command=self.cancelar
        ).pack(
            side="left",
            padx=5
        )

        texto_boton = (
            "Crear conjunto"
            if self.modo == "crear"
            else "Agregar elementos"
        )

        ttk.Button(
            botones,
            text=texto_boton,
            style="Principal.TButton",
            command=self.aceptar
        ).pack(
            side="left",
            padx=5
        )

        # ======================================================
        # ENFOQUE
        # ======================================================

        if self.modo == "crear":

            self.entrada_nombre.focus_set()

        else:

            self.entrada_elementos_nuevos.focus_set()

    # ==========================================================
    # INTERFAZ CREAR
    # ==========================================================

    def crear_interfaz_crear(
        self,
        contenedor
    ):

        ttk.Label(
            contenedor,
            text="Elementos separados por comas"
        ).grid(
            row=3,
            column=0,
            sticky="w"
        )

        self.entrada_elementos = ttk.Entry(
            contenedor
        )

        self.entrada_elementos.grid(
            row=4,
            column=0,
            sticky="ew",
            pady=(5, 5)
        )

        ttk.Label(
            contenedor,
            text=(
                "Ejemplo: 1, 2, rojo, azul, α\n"
                "También puedes dejarlo vacío para crear ∅."
            ),
            foreground="#6B7280"
        ).grid(
            row=5,
            column=0,
            sticky="w",
            pady=(5, 20)
        )

    # ==========================================================
    # INTERFAZ EDITAR
    # ==========================================================

    def crear_interfaz_editar(
        self,
        contenedor,
        elementos_iniciales
    ):

        # ------------------------------------------------------
        # ELEMENTOS ACTUALES
        # ------------------------------------------------------

        ttk.Label(
            contenedor,
            text="Elementos actuales"
        ).grid(
            row=3,
            column=0,
            sticky="w"
        )

        self.entrada_elementos_actuales = tk.Text(
            contenedor,
            height=4,
            font=("Consolas", 10),
            state="disabled",
            wrap="word"
        )

        self.entrada_elementos_actuales.grid(
            row=4,
            column=0,
            sticky="ew",
            pady=(5, 10)
        )

        self.entrada_elementos_actuales.config(
            state="normal"
        )

        self.entrada_elementos_actuales.insert(
            "1.0",
            elementos_iniciales
        )

        self.entrada_elementos_actuales.config(
            state="disabled"
        )

        # ------------------------------------------------------
        # AVISO
        # ------------------------------------------------------

        ttk.Label(
            contenedor,
            text=(
                "Los elementos existentes no se pueden eliminar."
            ),
            foreground="#6B7280"
        ).grid(
            row=5,
            column=0,
            sticky="w",
            pady=(0, 15)
        )

        # ------------------------------------------------------
        # NUEVOS ELEMENTOS
        # ------------------------------------------------------

        ttk.Label(
            contenedor,
            text="Agregar elementos"
        ).grid(
            row=6,
            column=0,
            sticky="w"
        )

        self.entrada_elementos_nuevos = ttk.Entry(
            contenedor
        )

        self.entrada_elementos_nuevos.grid(
            row=7,
            column=0,
            sticky="ew",
            pady=(5, 5)
        )

        ttk.Label(
            contenedor,
            text="Ejemplo: 6, 7, 8, amarillo",
            foreground="#6B7280"
        ).grid(
            row=8,
            column=0,
            sticky="w"
        )

    # ==========================================================
    # ACEPTAR
    # ==========================================================

    def aceptar(self):

        if self.modo == "crear":

            self.aceptar_crear()

            return

        self.aceptar_editar()

    # ==========================================================
    # ACEPTAR CREAR
    # ==========================================================

    def aceptar_crear(self):

        nombre = (
            self.entrada_nombre
            .get()
            .strip()
            .upper()
        )

        entrada = (
            self.entrada_elementos
            .get()
        )

        # ------------------------------------------------------
        # VALIDAR NOMBRE
        # ------------------------------------------------------

        if (
            len(nombre) != 1
            or not nombre.isalpha()
        ):

            messagebox.showerror(
                "Nombre inválido",
                "El nombre debe ser una sola letra.",
                parent=self
            )

            return

        # ------------------------------------------------------
        # U RESERVADO
        # ------------------------------------------------------

        if nombre == "U":

            messagebox.showerror(
                "Nombre reservado",
                (
                    "La letra U está reservada para "
                    "el conjunto universo."
                ),
                parent=self
            )

            return

        # ------------------------------------------------------
        # CREAR
        # ------------------------------------------------------

        try:

            conjunto = crear_conjunto_desde_entrada(
                nombre,
                entrada
            )

        except ValueError as error:

            messagebox.showerror(
                "Error",
                str(error),
                parent=self
            )

            return

        self.resultado = conjunto

        self.destroy()

    # ==========================================================
    # ACEPTAR EDITAR
    # ==========================================================

    def aceptar_editar(self):

        entrada = (
            self.entrada_elementos_nuevos
            .get()
            .strip()
        )

        # ------------------------------------------------------
        # VALIDAR
        # ------------------------------------------------------

        if not entrada:

            messagebox.showwarning(
                "Sin elementos",
                "Escribe al menos un elemento para agregar.",
                parent=self
            )

            return

        nombre = (
            self.entrada_nombre
            .get()
            .strip()
            .upper()
        )

        # ------------------------------------------------------
        # CREAR CONJUNTO TEMPORAL
        # ------------------------------------------------------

        try:

            conjunto = crear_conjunto_desde_entrada(
                nombre,
                entrada
            )

        except ValueError as error:

            messagebox.showerror(
                "Error",
                str(error),
                parent=self
            )

            return

        self.resultado = conjunto

        self.destroy()

    # ==========================================================
    # CANCELAR
    # ==========================================================

    def cancelar(self):

        self.resultado = None

        self.destroy()