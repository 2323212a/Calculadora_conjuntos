import tkinter as tk
from tkinter import ttk, messagebox
import re

from app.sesion import SesionCalculadora
from interfaz.estilos import Estilos
from interfaz.dialogo_conjunto import DialogoConjunto


class VentanaPrincipal:

    def __init__(self):

        self.root = tk.Tk()

        self.root.title(
            "Calculadora de Conjuntos"
        )

        self.root.geometry(
            "1300x800"
        )

        self.root.minsize(
            1000,
            650
        )

        self.sesion = SesionCalculadora()

        Estilos.configurar()

        self.datos_diagrama = None

        self.crear_interfaz()

        self.root.bind(
            "<Control-Return>",
            self.resolver_operacion
        )

    # ==========================================================
    # INTERFAZ
    # ==========================================================

    def crear_interfaz(self):

        self.root.columnconfigure(
            0,
            weight=1
        )

        self.root.rowconfigure(
            0,
            weight=1
        )

        principal = ttk.Frame(
            self.root,
            padding=20
        )

        principal.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        principal.columnconfigure(
            0,
            weight=1
        )

        principal.rowconfigure(
            1,
            weight=1
        )

        # ======================================================
        # ENCABEZADO
        # ======================================================

        encabezado = ttk.Frame(
            principal
        )

        encabezado.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 15)
        )

        ttk.Label(
            encabezado,
            text="Calculadora de Conjuntos",
            style="Titulo.TLabel"
        ).pack(
            anchor="w"
        )

        ttk.Label(
            encabezado,
            text=(
                "Crea conjuntos y resuelve operaciones "
                "con representación matemática y gráfica."
            ),
            style="Subtitulo.TLabel"
        ).pack(
            anchor="w"
        )

        # ======================================================
        # CONTENIDO
        # ======================================================

        contenido = ttk.Frame(
            principal
        )

        contenido.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        contenido.columnconfigure(
            0,
            weight=1,
            minsize=230
        )

        contenido.columnconfigure(
            1,
            weight=2,
            minsize=400
        )

        contenido.columnconfigure(
            2,
            weight=2,
            minsize=350
        )

        contenido.rowconfigure(
            0,
            weight=1
        )

        self.crear_panel_conjuntos(
            contenido
        )

        self.crear_panel_operacion(
            contenido
        )

        self.crear_panel_grafico(
            contenido
        )

    # ==========================================================
    # PANEL CONJUNTOS
    # ==========================================================

    def crear_panel_conjuntos(
        self,
        padre
    ):

        panel = ttk.Frame(
            padre,
            style="Panel.TFrame",
            padding=15
        )

        panel.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 8)
        )

        panel.columnconfigure(
            0,
            weight=1
        )

        panel.rowconfigure(
            1,
            weight=1
        )

        ttk.Label(
            panel,
            text="Conjuntos",
            style="PanelTitulo.TLabel"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 3)
        )

        ttk.Label(
            panel,
            text=(
                "Los conjuntos pueden crecer, pero sus "
                "elementos existentes no se eliminan."
            ),
            style="Subtitulo.TLabel"
        ).grid(
            row=0,
            column=0,
            sticky="e",
            pady=(0, 3)
        )

        # ======================================================
        # LISTA
        # ======================================================

        marco_lista = ttk.Frame(
            panel
        )

        marco_lista.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        marco_lista.columnconfigure(
            0,
            weight=1
        )

        marco_lista.rowconfigure(
            0,
            weight=1
        )

        self.lista_conjuntos = tk.Listbox(
            marco_lista,
            font=("Consolas", 10),
            activestyle="none",
            selectmode=tk.SINGLE,
            exportselection=False
        )

        self.lista_conjuntos.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        scroll = ttk.Scrollbar(
            marco_lista,
            orient="vertical",
            command=self.lista_conjuntos.yview
        )

        scroll.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        self.lista_conjuntos.configure(
            yscrollcommand=scroll.set
        )

        self.lista_conjuntos.bind(
            "<Double-Button-1>",
            lambda event:
            self.editar_conjunto()
        )

        # ======================================================
        # BOTONES
        # ======================================================

        botones = ttk.Frame(
            panel
        )

        botones.grid(
            row=2,
            column=0,
            sticky="ew",
            pady=(10, 0)
        )

        botones.columnconfigure(
            0,
            weight=1
        )

        botones.columnconfigure(
            1,
            weight=1
        )

        ttk.Button(
            botones,
            text="+ Crear conjunto",
            style="Principal.TButton",
            command=self.crear_conjunto
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(0, 5)
        )

        ttk.Button(
            botones,
            text="Editar",
            command=self.editar_conjunto
        ).grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(0, 3)
        )

        ttk.Button(
            botones,
            text="Eliminar",
            command=self.eliminar_conjunto
        ).grid(
            row=1,
            column=1,
            sticky="ew",
            padx=(3, 0)
        )

        # ======================================================
        # INFORMACIÓN DEL UNIVERSO
        # ======================================================

        marco_universo = ttk.Frame(
            panel,
            style="Panel.TFrame",
            padding=8
        )

        marco_universo.grid(
            row=3,
            column=0,
            sticky="ew",
            pady=(10, 0)
        )

        ttk.Label(
            marco_universo,
            text="U — Conjunto universo",
            style="PanelTitulo.TLabel"
        ).pack(
            anchor="w"
        )

        ttk.Label(
            marco_universo,
            text=(
                "Se genera automáticamente con todos los "
                "elementos existentes en los conjuntos."
            ),
            style="Subtitulo.TLabel",
            wraplength=250
        ).pack(
            anchor="w",
            pady=(3, 0)
        )

    # ==========================================================
    # PANEL OPERACIÓN
    # ==========================================================

    def crear_panel_operacion(
        self,
        padre
    ):

        panel = ttk.Frame(
            padre,
            style="Panel.TFrame",
            padding=15
        )

        panel.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=8
        )

        panel.columnconfigure(
            0,
            weight=1
        )

        panel.rowconfigure(
            5,
            weight=1
        )

        ttk.Label(
            panel,
            text="Operación",
            style="PanelTitulo.TLabel"
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        ttk.Label(
            panel,
            text=(
                "Puedes escribir la expresión directamente."
            ),
            style="Subtitulo.TLabel"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=(3, 8)
        )

        self.entrada_expresion = ttk.Entry(
            panel,
            font=("Segoe UI", 13)
        )

        self.entrada_expresion.grid(
            row=2,
            column=0,
            sticky="ew"
        )

        self.entrada_expresion.bind(
            "<Return>",
            self.resolver_operacion
        )

        # ======================================================
        # OPERADORES
        # ======================================================

        operadores_frame = ttk.Frame(
            panel
        )

        operadores_frame.grid(
            row=3,
            column=0,
            sticky="ew",
            pady=10
        )

        operadores = [
            "∪",
            "∩",
            "-",
            "△",
            "ᶜ",
            "(",
            ")"
        ]

        for i, operador in enumerate(
            operadores
        ):

            operadores_frame.columnconfigure(
                i,
                weight=1
            )

            ttk.Button(
                operadores_frame,
                text=operador,
                command=lambda op=operador:
                self.insertar_operador(op)
            ).grid(
                row=0,
                column=i,
                sticky="ew",
                padx=2
            )

        ttk.Button(
            panel,
            text="RESOLVER OPERACIÓN",
            style="Principal.TButton",
            command=self.resolver_operacion
        ).grid(
            row=4,
            column=0,
            sticky="ew",
            pady=(0, 10)
        )

        # ======================================================
        # RESULTADO
        # ======================================================

        zona = ttk.Frame(
            panel
        )

        zona.grid(
            row=5,
            column=0,
            sticky="nsew"
        )

        zona.columnconfigure(
            0,
            weight=1
        )

        zona.rowconfigure(
            3,
            weight=1
        )

        ttk.Label(
            zona,
            text="Resultado",
            style="PanelTitulo.TLabel"
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.resultado = tk.Text(
            zona,
            height=3,
            font=("Consolas", 11),
            state="disabled",
            wrap="word"
        )

        self.resultado.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(5, 12)
        )

        ttk.Label(
            zona,
            text="Procedimiento",
            style="PanelTitulo.TLabel"
        ).grid(
            row=2,
            column=0,
            sticky="w"
        )

        marco_pasos = ttk.Frame(
            zona
        )

        marco_pasos.grid(
            row=3,
            column=0,
            sticky="nsew",
            pady=(5, 0)
        )

        marco_pasos.columnconfigure(
            0,
            weight=1
        )

        marco_pasos.rowconfigure(
            0,
            weight=1
        )

        self.pasos = tk.Text(
            marco_pasos,
            font=("Consolas", 10),
            state="disabled",
            wrap="word"
        )

        self.pasos.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        scroll = ttk.Scrollbar(
            marco_pasos,
            orient="vertical",
            command=self.pasos.yview
        )

        scroll.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        self.pasos.configure(
            yscrollcommand=scroll.set
        )

    # ==========================================================
    # PANEL GRÁFICO
    # ==========================================================

    def crear_panel_grafico(
        self,
        padre
    ):

        panel = ttk.Frame(
            padre,
            style="Panel.TFrame",
            padding=15
        )

        panel.grid(
            row=0,
            column=2,
            sticky="nsew",
            padx=(8, 0)
        )

        panel.columnconfigure(
            0,
            weight=1
        )

        panel.rowconfigure(
            2,
            weight=1
        )

        ttk.Label(
            panel,
            text="Representación gráfica",
            style="PanelTitulo.TLabel"
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.etiqueta_grafico = ttk.Label(
            panel,
            text="Sin operación",
            style="Subtitulo.TLabel"
        )

        self.etiqueta_grafico.grid(
            row=1,
            column=0,
            sticky="w",
            pady=(3, 8)
        )

        self.canvas = tk.Canvas(
            panel,
            background="white",
            highlightthickness=1,
            highlightbackground="#D1D5DB"
        )

        self.canvas.grid(
            row=2,
            column=0,
            sticky="nsew"
        )

        self.canvas.bind(
            "<Configure>",
            lambda event:
            self.redibujar_diagrama()
        )

    # ==========================================================
    # ACTUALIZAR LISTA
    # ==========================================================

    def actualizar_lista_conjuntos(self):

        self.lista_conjuntos.delete(
            0,
            tk.END
        )

        conjuntos = (
            self.sesion.gestor.obtener_todos()
        )

        for nombre, conjunto in conjuntos.items():

            self.lista_conjuntos.insert(
                tk.END,
                str(conjunto)
            )

    # ==========================================================
    # OBTENER SELECCIONADO
    # ==========================================================

    def obtener_nombre_seleccionado(self):

        seleccion = (
            self.lista_conjuntos.curselection()
        )

        if not seleccion:

            return None

        nombres = list(
            self.sesion.gestor
            .obtener_todos()
            .keys()
        )

        indice = seleccion[0]

        if indice >= len(nombres):

            return None

        return nombres[indice]

    # ==========================================================
    # CREAR
    # ==========================================================

    def crear_conjunto(self):

        dialogo = DialogoConjunto(
            self.root,
            titulo="Crear conjunto",
            modo="crear"
        )

        self.root.wait_window(
            dialogo
        )

        if dialogo.resultado is None:

            return

        try:

            self.sesion.gestor.agregar(
                dialogo.resultado
            )

        except ValueError as error:

            messagebox.showerror(
                "No se pudo crear",
                str(error),
                parent=self.root
            )

            return

        self.actualizar_lista_conjuntos()

    # ==========================================================
    # EDITAR / AGREGAR ELEMENTOS
    # ==========================================================

    def editar_conjunto(self):

        nombre = (
            self.obtener_nombre_seleccionado()
        )

        if nombre is None:

            messagebox.showwarning(
                "Selecciona un conjunto",
                "Selecciona primero un conjunto.",
                parent=self.root
            )

            return

        # ======================================================
        # U SOLO LECTURA
        # ======================================================

        if nombre == "U":

            messagebox.showinfo(
                "Conjunto universo",
                (
                    "U es un conjunto automático.\n\n"
                    "No puede editarse directamente.\n\n"
                    "Su contenido se obtiene automáticamente "
                    "de los elementos de los demás conjuntos."
                ),
                parent=self.root
            )

            return

        # ======================================================
        # OBTENER CONJUNTO
        # ======================================================

        conjunto = (
            self.sesion.gestor.obtener(
                nombre
            )
        )

        elementos_actuales = ", ".join(
            map(
                str,
                sorted(
                    conjunto.elementos,
                    key=lambda elemento: str(elemento)
                )
            )
        )

        # ======================================================
        # ABRIR DIÁLOGO
        # ======================================================

        dialogo = DialogoConjunto(
            self.root,
            titulo=f"Agregar elementos a {nombre}",
            nombre_inicial=nombre,
            elementos_iniciales=elementos_actuales,
            modo="editar"
        )

        self.root.wait_window(
            dialogo
        )

        if dialogo.resultado is None:

            return

        # ======================================================
        # OBTENER NUEVOS ELEMENTOS
        # ======================================================

        nuevos_elementos = set(
            dialogo.resultado.elementos
        )

        # ======================================================
        # CONSERVAR LOS EXISTENTES
        # ======================================================

        elementos_finales = (
            conjunto.elementos
            | nuevos_elementos
        )

        # ======================================================
        # GUARDAR
        # ======================================================

        try:

            self.sesion.gestor.modificar(
                nombre,
                elementos_finales
            )

        except ValueError as error:

            messagebox.showerror(
                "No se pudo modificar",
                str(error),
                parent=self.root
            )

            return

        self.actualizar_lista_conjuntos()

    # ==========================================================
    # ELIMINAR
    # ==========================================================

    def eliminar_conjunto(self):

        nombre = (
            self.obtener_nombre_seleccionado()
        )

        if nombre is None:

            messagebox.showwarning(
                "Selecciona un conjunto",
                "Selecciona primero un conjunto.",
                parent=self.root
            )

            return

        # ======================================================
        # U NO PUEDE ELIMINARSE
        # ======================================================

        if nombre == "U":

            messagebox.showinfo(
                "Conjunto universo",
                (
                    "U es generado automáticamente y "
                    "no puede eliminarse."
                ),
                parent=self.root
            )

            return

        # ======================================================
        # CONFIRMAR
        # ======================================================

        confirmar = messagebox.askyesno(
            "Eliminar conjunto",
            (
                f"¿Deseas eliminar el conjunto {nombre}?\n\n"
                "Sus elementos dejarán de pertenecer a U "
                "si ningún otro conjunto los contiene."
            ),
            parent=self.root
        )

        if not confirmar:

            return

        # ======================================================
        # ELIMINAR
        # ======================================================

        try:

            self.sesion.gestor.eliminar(
                nombre
            )

        except ValueError as error:

            messagebox.showerror(
                "No se pudo eliminar",
                str(error),
                parent=self.root
            )

            return

        self.actualizar_lista_conjuntos()

    # ==========================================================
    # INSERTAR OPERADOR
    # ==========================================================

    def insertar_operador(
        self,
        operador
    ):

        self.entrada_expresion.insert(
            tk.INSERT,
            operador
        )

        self.entrada_expresion.focus_set()

    # ==========================================================
    # RESOLVER
    # ==========================================================

    def resolver_operacion(
        self,
        event=None
    ):

        expresion = (
            self.entrada_expresion
            .get()
            .strip()
        )

        if not expresion:

            messagebox.showwarning(
                "Expresión vacía",
                "Escribe una expresión.",
                parent=self.root
            )

            return

        try:

            resultado, pasos = (
                self.sesion.resolver(
                    expresion
                )
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error),
                parent=self.root
            )

            return

        self.mostrar_resultado(
            resultado
        )

        self.mostrar_pasos(
            pasos
        )

        self.preparar_diagrama(
            expresion,
            resultado
        )

    # ==========================================================
    # RESULTADO
    # ==========================================================

    def mostrar_resultado(
        self,
        resultado
    ):

        self.resultado.config(
            state="normal"
        )

        self.resultado.delete(
            "1.0",
            tk.END
        )

        self.resultado.insert(
            tk.END,
            str(resultado)
        )

        self.resultado.config(
            state="disabled"
        )

    # ==========================================================
    # PROCEDIMIENTO
    # ==========================================================

    def mostrar_pasos(
        self,
        pasos
    ):

        self.pasos.config(
            state="normal"
        )

        self.pasos.delete(
            "1.0",
            tk.END
        )

        for numero, paso in enumerate(
            pasos,
            start=1
        ):

            self.pasos.insert(
                tk.END,
                f"{numero}. {paso}\n\n"
            )

        self.pasos.config(
            state="disabled"
        )

    # ==========================================================
    # PREPARAR DIAGRAMA
    # ==========================================================

    def preparar_diagrama(
        self,
        expresion,
        resultado
    ):

        expresion_limpia = (
            expresion
            .replace(" ", "")
        )

        # ======================================================
        # OPERACIÓN BINARIA SIMPLE
        # ======================================================

        patron = re.fullmatch(
            r"([A-Za-z])([∪∩△-])([A-Za-z])",
            expresion_limpia
        )

        if patron:

            A = patron.group(1).upper()
            operador = patron.group(2)
            B = patron.group(3).upper()

            try:

                conjunto_a = (
                    self.sesion.gestor.obtener(A)
                )

                conjunto_b = (
                    self.sesion.gestor.obtener(B)
                )

            except ValueError:

                return

            self.datos_diagrama = {
                "tipo": "binario",
                "A": A,
                "B": B,
                "operador": operador,
                "conjunto_a": conjunto_a,
                "conjunto_b": conjunto_b,
                "resultado": resultado
            }

            self.etiqueta_grafico.config(
                text=(
                    f"{A} {operador} {B}   →   "
                    f"{resultado}"
                )
            )

            self.redibujar_diagrama()

            return

        # ======================================================
        # COMPLEMENTO
        # ======================================================

        patron = re.fullmatch(
            r"([A-Za-z])ᶜ",
            expresion_limpia
        )

        if patron:

            A = patron.group(1).upper()

            try:

                conjunto_a = (
                    self.sesion.gestor.obtener(A)
                )

                universo = (
                    self.sesion.gestor.obtener_universo()
                )

            except ValueError:

                return

            self.datos_diagrama = {
                "tipo": "complemento",
                "A": A,
                "conjunto_a": conjunto_a,
                "universo": universo,
                "resultado": resultado
            }

            self.etiqueta_grafico.config(
                text=f"{A}ᶜ → {resultado}"
            )

            self.redibujar_diagrama()

            return

        # ======================================================
        # OPERACIÓN COMPLEJA
        # ======================================================

        nombres = []

        for letra in re.findall(
            r"[A-Za-z]",
            expresion_limpia
        ):

            letra = letra.upper()

            if letra not in nombres:

                nombres.append(
                    letra
                )

        conjuntos = {}

        for nombre in nombres:

            try:

                conjuntos[nombre] = (
                    self.sesion.gestor.obtener(
                        nombre
                    )
                )

            except ValueError:

                pass

        self.datos_diagrama = {
            "tipo": "complejo",
            "expresion": expresion,
            "conjuntos": conjuntos,
            "resultado": resultado
        }

        self.etiqueta_grafico.config(
            text=(
                f"{expresion}   →   "
                f"{resultado}"
            )
        )

        self.redibujar_diagrama()

    # ==========================================================
    # REDIBUJAR DIAGRAMA
    # ==========================================================

    def redibujar_diagrama(self):

        self.canvas.delete(
            "all"
        )

        if not self.datos_diagrama:

            self.canvas.create_text(
                self.canvas.winfo_width() / 2,
                self.canvas.winfo_height() / 2,
                text="Sin operación",
                font=("Segoe UI", 12),
                fill="#6B7280"
            )

            return

        tipo = (
            self.datos_diagrama["tipo"]
        )

        if tipo == "binario":

            self.dibujar_binario()

        elif tipo == "complemento":

            self.dibujar_complemento()

        else:

            self.dibujar_complejo()

    # ==========================================================
    # DIAGRAMA BINARIO
    # ==========================================================

    def dibujar_binario(self):

        datos = self.datos_diagrama

        A = datos["A"]
        B = datos["B"]

        conjunto_a = datos["conjunto_a"]
        conjunto_b = datos["conjunto_b"]

        operador = datos["operador"]

        resultado = datos["resultado"]

        ancho = self.canvas.winfo_width()
        alto = self.canvas.winfo_height()

        if ancho < 100 or alto < 100:

            return

        # ======================================================
        # UNIVERSO
        # ======================================================

        margen = 30

        self.canvas.create_rectangle(
            margen,
            margen,
            ancho - margen,
            alto - margen,
            outline="#94A3B8",
            width=2
        )

        self.canvas.create_text(
            margen + 15,
            margen + 12,
            text="U",
            font=("Segoe UI", 11, "bold"),
            fill="#475569"
        )

        # ======================================================
        # CÍRCULOS
        # ======================================================

        cy = alto * 0.52

        radio = min(
            ancho * 0.24,
            alto * 0.30
        )

        cx1 = ancho * 0.40
        cx2 = ancho * 0.60

        self.canvas.create_oval(
            cx1 - radio,
            cy - radio,
            cx1 + radio,
            cy + radio,
            outline="#2563EB",
            width=3
        )

        self.canvas.create_oval(
            cx2 - radio,
            cy - radio,
            cx2 + radio,
            cy + radio,
            outline="#DC2626",
            width=3
        )

        # ======================================================
        # ETIQUETAS
        # ======================================================

        self.canvas.create_text(
            cx1 - radio * 0.65,
            cy - radio * 0.75,
            text=A,
            font=("Segoe UI", 14, "bold"),
            fill="#2563EB"
        )

        self.canvas.create_text(
            cx2 + radio * 0.65,
            cy - radio * 0.75,
            text=B,
            font=("Segoe UI", 14, "bold"),
            fill="#DC2626"
        )

        # ======================================================
        # REGIONES
        # ======================================================

        solo_a = (
            conjunto_a.elementos
            - conjunto_b.elementos
        )

        interseccion = (
            conjunto_a.elementos
            & conjunto_b.elementos
        )

        solo_b = (
            conjunto_b.elementos
            - conjunto_a.elementos
        )

        # ======================================================
        # ELEMENTOS
        # ======================================================

        self.dibujar_elementos_region(
            list(solo_a),
            cx1 - radio * 0.45,
            cy,
            resultado,
            operador,
            "A"
        )

        self.dibujar_elementos_region(
            list(interseccion),
            (cx1 + cx2) / 2,
            cy,
            resultado,
            operador,
            "INTER"
        )

        self.dibujar_elementos_region(
            list(solo_b),
            cx2 + radio * 0.45,
            cy,
            resultado,
            operador,
            "B"
        )

        # ======================================================
        # ELEMENTOS FUERA
        # ======================================================

        try:

            universo = (
                self.sesion.gestor
                .obtener_universo()
            )

            fuera = (
                universo.elementos
                - conjunto_a.elementos
                - conjunto_b.elementos
            )

        except Exception:

            fuera = set()

        self.dibujar_elementos_region(
            list(fuera),
            ancho * 0.83,
            alto * 0.78,
            resultado,
            operador,
            "FUERA"
        )

        # ======================================================
        # LEYENDA
        # ======================================================

        self.canvas.create_text(
            ancho / 2,
            alto - 12,
            text=(
                f"{A} {operador} {B} = "
                f"{resultado}"
            ),
            font=("Segoe UI", 10, "bold"),
            fill="#334155"
        )

    # ==========================================================
    # ELEMENTOS
    # ==========================================================

    def dibujar_elementos_region(
        self,
        elementos,
        x,
        y,
        resultado,
        operador,
        region
    ):

        elementos = sorted(
            elementos,
            key=lambda elemento: str(elemento)
        )

        if not elementos:

            return

        resultado_elementos = set(
            resultado.elementos
        )

        columnas = 3

        separacion_x = 48
        separacion_y = 28

        inicio_x = (
            x
            - (
                min(
                    len(elementos),
                    columnas
                )
                - 1
            )
            * separacion_x
            / 2
        )

        for indice, elemento in enumerate(
            elementos
        ):

            fila = indice // columnas
            columna = indice % columnas

            x_actual = (
                inicio_x
                + columna * separacion_x
            )

            y_actual = (
                y
                + fila * separacion_y
            )

            pertenece = (
                elemento
                in resultado_elementos
            )

            if pertenece:

                self.canvas.create_oval(
                    x_actual - 18,
                    y_actual - 14,
                    x_actual + 18,
                    y_actual + 14,
                    fill="#DCFCE7",
                    outline="#16A34A",
                    width=2
                )

                color = "#166534"

            else:

                color = "#64748B"

            self.canvas.create_text(
                x_actual,
                y_actual,
                text=str(elemento),
                font=("Segoe UI", 10, "bold"),
                fill=color
            )

    # ==========================================================
    # COMPLEMENTO
    # ==========================================================

    def dibujar_complemento(self):

        datos = self.datos_diagrama

        A = datos["A"]

        conjunto = datos["conjunto_a"]
        universo = datos["universo"]

        resultado = datos["resultado"]

        ancho = self.canvas.winfo_width()
        alto = self.canvas.winfo_height()

        if ancho < 100 or alto < 100:

            return

        margen = 30

        # ======================================================
        # UNIVERSO
        # ======================================================

        self.canvas.create_rectangle(
            margen,
            margen,
            ancho - margen,
            alto - margen,
            outline="#475569",
            width=2
        )

        self.canvas.create_text(
            margen + 15,
            margen + 12,
            text="U",
            font=("Segoe UI", 11, "bold")
        )

        # ======================================================
        # CONJUNTO A
        # ======================================================

        radio = min(
            ancho * 0.27,
            alto * 0.32
        )

        cx = ancho / 2
        cy = alto / 2

        self.canvas.create_oval(
            cx - radio,
            cy - radio,
            cx + radio,
            cy + radio,
            outline="#2563EB",
            width=3
        )

        self.canvas.create_text(
            cx,
            cy - radio - 15,
            text=A,
            font=("Segoe UI", 14, "bold"),
            fill="#2563EB"
        )

        # ======================================================
        # ELEMENTOS DENTRO DE A
        # ======================================================

        elementos_a = sorted(
            conjunto.elementos,
            key=lambda elemento: str(elemento)
        )

        for indice, elemento in enumerate(
            elementos_a
        ):

            x = (
                cx - radio * 0.45
                + (indice % 3) * 45
            )

            y = (
                cy - 20
                + (indice // 3) * 28
            )

            color = (
                "#64748B"
                if elemento not in resultado.elementos
                else "#166534"
            )

            self.canvas.create_text(
                x,
                y,
                text=str(elemento),
                font=("Segoe UI", 10, "bold"),
                fill=color
            )

        # ======================================================
        # ELEMENTOS FUERA DE A
        # ======================================================

        fuera = (
            universo.elementos
            - conjunto.elementos
        )

        for indice, elemento in enumerate(
            sorted(
                fuera,
                key=lambda elemento: str(elemento)
            )
        ):

            x = (
                margen + 70
                + (indice % 3) * 45
            )

            y = (
                alto - 90
                + (indice // 3) * 25
            )

            self.canvas.create_text(
                x,
                y,
                text=str(elemento),
                font=("Segoe UI", 10, "bold"),
                fill="#166534"
            )

        # ======================================================
        # LEYENDA
        # ======================================================

        self.canvas.create_text(
            ancho / 2,
            alto - 12,
            text=f"{A}ᶜ = {resultado}",
            font=("Segoe UI", 10, "bold"),
            fill="#334155"
        )

    # ==========================================================
    # DIAGRAMA COMPLEJO
    # ==========================================================

    def dibujar_complejo(self):

        datos = self.datos_diagrama

        expresion = datos["expresion"]
        resultado = datos["resultado"]

        ancho = self.canvas.winfo_width()
        alto = self.canvas.winfo_height()

        if ancho < 100 or alto < 100:

            return

        # ======================================================
        # EXPRESIÓN
        # ======================================================

        self.canvas.create_text(
            ancho / 2,
            35,
            text=expresion,
            font=("Consolas", 15, "bold"),
            fill="#2563EB"
        )

        self.canvas.create_text(
            ancho / 2,
            65,
            text=f"Resultado: {resultado}",
            font=("Consolas", 11),
            fill="#334155"
        )

        # ======================================================
        # CONJUNTOS
        # ======================================================

        conjuntos = datos["conjuntos"]

        nombres = list(
            conjuntos.keys()
        )

        posiciones = [
            (ancho * 0.35, alto * 0.55),
            (ancho * 0.65, alto * 0.55),
            (ancho * 0.50, alto * 0.68)
        ]

        for indice, nombre in enumerate(
            nombres[:3]
        ):

            conjunto = conjuntos[nombre]

            x, y = posiciones[indice]

            radio = min(
                ancho * 0.22,
                alto * 0.25
            )

            self.canvas.create_oval(
                x - radio,
                y - radio,
                x + radio,
                y + radio,
                outline="#64748B",
                width=2
            )

            self.canvas.create_text(
                x,
                y - radio + 15,
                text=nombre,
                font=("Segoe UI", 13, "bold"),
                fill="#334155"
            )

            elementos = sorted(
                conjunto.elementos,
                key=lambda elemento: str(elemento)
            )

            for i, elemento in enumerate(
                elementos[:12]
            ):

                ex = (
                    x - 35
                    + (i % 3) * 35
                )

                ey = (
                    y - 10
                    + (i // 3) * 25
                )

                color = (
                    "#166534"
                    if elemento in resultado.elementos
                    else "#64748B"
                )

                self.canvas.create_text(
                    ex,
                    ey,
                    text=str(elemento),
                    font=("Segoe UI", 9, "bold"),
                    fill=color
                )

        # ======================================================
        # LEYENDA
        # ======================================================

        self.canvas.create_text(
            ancho / 2,
            alto - 15,
            text=(
                "Verde = elementos pertenecientes "
                "al resultado"
            ),
            font=("Segoe UI", 9),
            fill="#166534"
        )

    # ==========================================================
    # EJECUCIÓN
    # ==========================================================

    def ejecutar(self):

        self.actualizar_lista_conjuntos()

        self.root.mainloop()