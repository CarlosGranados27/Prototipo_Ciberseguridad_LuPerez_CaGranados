import tkinter as tk
from tkinter import messagebox
import sqlite3
from openpyxl import Workbook
from openpyxl.styles import PatternFill
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from tkinter import ttk


# ===================================
# TEMA CIBERSEGURIDAD / SOC
# ===================================

COLOR_FONDO = "#0A192F"
COLOR_PANEL = "#112240"
COLOR_BOTON = "#233554"
COLOR_TEXTO = "#CCD6F6"
COLOR_TITULO = "#64FFDA"

FUENTE_TITULO = ("Consolas", 20, "bold")
FUENTE_NORMAL = ("Consolas", 10)
FUENTE_BOTON = ("Consolas", 10, "bold")


# ===================================
# CREAR BASE DE DATOS
# ===================================

conexion = sqlite3.connect("riesgos.db")
cursor = conexion.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS activos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    tipo TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS riesgos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    activo TEXT,
    amenaza TEXT,
    probabilidad INTEGER,
    impacto INTEGER,
    nivel_riesgo INTEGER
)
""")


conexion.commit()
conexion.close()


# ===================================
# REGISTRAR ACTIVOS
# ===================================

def registrar_activo():

    ventana_activos = tk.Toplevel()
    ventana_activos.title("Registro de Activos")
    ventana_activos.geometry("700x500")
    ventana_activos.configure(bg=COLOR_FONDO)

    titulo = tk.Label(
        ventana_activos,
        text="REGISTRO DE ACTIVOS ISO 27002",
        bg=COLOR_FONDO,
        fg=COLOR_TITULO,
        font=("Consolas", 16, "bold")
    )

    titulo.pack(pady=20)

    tk.Label(
        ventana_activos,
        text="Nombre del Activo",
        bg=COLOR_FONDO,
        fg=COLOR_TEXTO,
        font=FUENTE_NORMAL
    ).pack(pady=10)

    entrada_nombre = tk.Entry(
        ventana_activos,
        width=40,
        bg=COLOR_PANEL,
        fg="white",
        insertbackground="white",
        font=FUENTE_NORMAL
    )

    entrada_nombre.pack()

    tk.Label(
        ventana_activos,
        text="Tipo de Activo",
        bg=COLOR_FONDO,
        fg=COLOR_TEXTO,
        font=FUENTE_NORMAL
    ).pack(pady=10)

    combo_tipo = ttk.Combobox(
        ventana_activos,
        width=37,
        state="readonly",
        values=[
            "Hardware",
            "Software",
            "Información",
            "Red",
            "Recurso Humano",
            "Infraestructura Física"
        ]
    )

    combo_tipo.pack()

    def guardar_activo():

        nombre = entrada_nombre.get()
        tipo = combo_tipo.get()

        if nombre == "" or tipo == "":

            messagebox.showwarning(
                "Advertencia",
                "Debe completar todos los campos"
            )

            return

        conexion = sqlite3.connect("riesgos.db")
        cursor = conexion.cursor()

        cursor.execute(
            """
            INSERT INTO activos
            (
                nombre,
                tipo
            )
            VALUES (?, ?)
            """,
            (
                nombre,
                tipo
            )
        )

        conexion.commit()
        conexion.close()

        messagebox.showinfo(
            "Éxito",
            "Activo guardado correctamente"
        )

        entrada_nombre.delete(
            0,
            tk.END
        )

        combo_tipo.set("")

    btn_guardar = tk.Button(
        ventana_activos,
        text="💾 GUARDAR ACTIVO",
        width=25,
        command=guardar_activo
    )

    btn_guardar.pack(pady=30)

    estilo_boton(btn_guardar)


# ===================================
# VER ACTIVOS
# ===================================

def ver_activos():

    ventana_ver = tk.Toplevel()
    ventana_ver.title("Inventario de Activos")
    ventana_ver.geometry("1000x550")
    ventana_ver.configure(bg="white")

    titulo = tk.Label(
        ventana_ver,
        text="INVENTARIO DE ACTIVOS ISO 27002",
        bg="white",
        fg="#0A192F",
        font=("Segoe UI", 14, "bold")
    )

    titulo.pack(pady=10)

    estilo = ttk.Style()

    estilo.theme_use("clam")

    estilo.configure(
        "Treeview.Heading",
        background="#0A192F",
        foreground="white",
        font=("Segoe UI", 10, "bold")
    )

    estilo.configure(
        "Treeview",
        font=("Segoe UI", 10),
        rowheight=28
    )

    frame = tk.Frame(
        ventana_ver,
        bg="white"
    )

    frame.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    columnas = (
        "ID",
        "NOMBRE",
        "TIPO"
    )

    tabla = ttk.Treeview(
        frame,
        columns=columnas,
        show="headings"
    )

    tabla.heading("ID", text="ID")
    tabla.heading("NOMBRE", text="NOMBRE DEL ACTIVO")
    tabla.heading("TIPO", text="TIPO DE ACTIVO")

    tabla.column(
        "ID",
        width=80,
        anchor="center"
    )

    tabla.column(
        "NOMBRE",
        width=550
    )

    tabla.column(
        "TIPO",
        width=250,
        anchor="center"
    )

    scrollbar = ttk.Scrollbar(
        frame,
        orient="vertical",
        command=tabla.yview
    )

    tabla.configure(
        yscrollcommand=scrollbar.set
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    tabla.pack(
        fill="both",
        expand=True
    )

    # ===== COLORES POR TIPO =====

    tabla.tag_configure(
        "Hardware",
        background="#D6EAF8"
    )

    tabla.tag_configure(
        "Software",
        background="#D5F5E3"
    )

    tabla.tag_configure(
        "Información",
        background="#FCF3CF"
    )

    tabla.tag_configure(
        "Red",
        background="#FADBD8"
    )

    tabla.tag_configure(
        "Recurso Humano",
        background="#E8DAEF"
    )

    tabla.tag_configure(
        "Infraestructura Física",
        background="#FDEBD0"
    )

    conexion = sqlite3.connect("riesgos.db")
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT *
        FROM activos
    """)

    registros = cursor.fetchall()

    total_activos = len(registros)

    lbl_total = tk.Label(
        ventana_ver,
        text=f"Total de Activos Registrados: {total_activos}",
        bg="white",
        fg="#0A192F",
        font=("Segoe UI", 10, "bold")
    )

    lbl_total.pack(pady=(0,10))

    for fila in registros:

        tipo = fila[2]

        tabla.insert(
            "",
            tk.END,
            values=(
                fila[0],
                fila[1],
                fila[2]
            ),
            tags=(tipo,)
        )

    conexion.close()


# ===================================
# EVALUAR RIESGOS
# ===================================

def evaluar_riesgo():

    ventana_riesgo = tk.Toplevel()
    ventana_riesgo.title("Evaluación de Riesgos")
    ventana_riesgo.geometry("700x650")
    ventana_riesgo.configure(bg=COLOR_FONDO)

    titulo = tk.Label(
        ventana_riesgo,
        text="EVALUACIÓN DE RIESGOS ISO 27002",
        bg=COLOR_FONDO,
        fg=COLOR_TITULO,
        font=("Consolas", 16, "bold")
    )

    titulo.pack(pady=20)

    # ==========================
    # CARGAR ACTIVOS
    # ==========================

    conexion = sqlite3.connect("riesgos.db")
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT nombre
        FROM activos
        ORDER BY nombre
    """)

    lista_activos = []

    for fila in cursor.fetchall():
        lista_activos.append(fila[0])

    conexion.close()

    # ==========================
    # ACTIVO
    # ==========================

    tk.Label(
        ventana_riesgo,
        text="Activo",
        bg=COLOR_FONDO,
        fg=COLOR_TEXTO,
        font=("Consolas", 10, "bold")
    ).pack(pady=5)

    combo_activo = ttk.Combobox(
        ventana_riesgo,
        width=37,
        state="readonly",
        values=lista_activos
    )

    combo_activo.pack()

    # ==========================
    # AMENAZA
    # ==========================

    tk.Label(
        ventana_riesgo,
        text="Amenaza",
        bg=COLOR_FONDO,
        fg=COLOR_TEXTO,
        font=("Consolas", 10, "bold")
    ).pack(pady=5)

    combo_amenaza = ttk.Combobox(
        ventana_riesgo,
        width=37,
        state="readonly",
        values=[
            "Phishing",
            "Malware",
            "Ransomware",
            "Acceso no autorizado",
            "Robo físico",
            "Pérdida de información",
            "Error humano",
            "Ataque DDoS",
            "Corrupción de datos",
            "Intrusión",
            "Denegación de Servicio"
        ]
    )

    combo_amenaza.pack()

    # ==========================
    # PROBABILIDAD
    # ==========================

    tk.Label(
        ventana_riesgo,
        text="Probabilidad (1 - 5)",
        bg=COLOR_FONDO,
        fg=COLOR_TEXTO,
        font=("Consolas", 10, "bold")
    ).pack(pady=5)

    combo_probabilidad = ttk.Combobox(
        ventana_riesgo,
        width=10,
        state="readonly",
        values=["1", "2", "3", "4", "5"]
    )

    combo_probabilidad.pack()

    # ==========================
    # IMPACTO
    # ==========================

    tk.Label(
        ventana_riesgo,
        text="Impacto (1 - 5)",
        bg=COLOR_FONDO,
        fg=COLOR_TEXTO,
        font=("Consolas", 10, "bold")
    ).pack(pady=5)

    combo_impacto = ttk.Combobox(
        ventana_riesgo,
        width=10,
        state="readonly",
        values=["1", "2", "3", "4", "5"]
    )

    combo_impacto.pack()

    # ==========================
    # RESULTADO
    # ==========================

    resultado = tk.Label(
        ventana_riesgo,
        text="",
        bg=COLOR_FONDO,
        fg=COLOR_TITULO,
        font=("Consolas", 14, "bold")
    )

    resultado.pack(pady=20)

    # ==========================
    # CALCULAR RIESGO
    # ==========================

    def calcular_riesgo():

        try:

            activo = combo_activo.get()
            amenaza = combo_amenaza.get()

            if activo == "":
                messagebox.showerror(
                    "Error",
                    "Seleccione un activo"
                )
                return

            if amenaza == "":
                messagebox.showerror(
                    "Error",
                    "Seleccione una amenaza"
                )
                return

            probabilidad = int(
                combo_probabilidad.get()
            )

            impacto = int(
                combo_impacto.get()
            )

            riesgo = probabilidad * impacto

            if riesgo <= 5:

                clasificacion = "BAJO"
                color = "#00FF00"
                icono = "🟢"

            elif riesgo <= 10:

                clasificacion = "MEDIO"
                color = "#FFD700"
                icono = "🟡"

            elif riesgo <= 15:

                clasificacion = "ALTO"
                color = "#FFA500"
                icono = "🟠"

            else:

                clasificacion = "CRÍTICO"
                color = "#FF4444"
                icono = "🔴"

            conexion = sqlite3.connect(
                "riesgos.db"
            )

            cursor = conexion.cursor()

            cursor.execute(
                """
                INSERT INTO riesgos
                (
                    activo,
                    amenaza,
                    probabilidad,
                    impacto,
                    nivel_riesgo
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    activo,
                    amenaza,
                    probabilidad,
                    impacto,
                    riesgo
                )
            )

            conexion.commit()
            conexion.close()

            resultado.config(
                text=f"{icono} RIESGO: {riesgo} - {clasificacion}",
                fg=color
            )

            messagebox.showinfo(
                "Resultado",
                f"""
Activo: {activo}

Amenaza: {amenaza}

Probabilidad: {probabilidad}

Impacto: {impacto}

Nivel de Riesgo: {riesgo}

Clasificación: {clasificacion}
"""
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Debe seleccionar Probabilidad e Impacto"
            )

    btn_calcular = tk.Button(
        ventana_riesgo,
        text="🛡️ CALCULAR RIESGO",
        width=25,
        command=calcular_riesgo
    )

    btn_calcular.pack(pady=20)

    estilo_boton(btn_calcular)



# ===================================
# VER RIESGOS
# ===================================

def ver_riesgos():

    ventana_ver = tk.Toplevel()
    ventana_ver.title("Matriz de Riesgos")
    ventana_ver.geometry("1200x550")
    ventana_ver.configure(bg="white")

    titulo = tk.Label(
        ventana_ver,
        text="MATRIZ DE RIESGOS ISO 27002",
        bg="white",
        fg="#0A192F",
        font=("Segoe UI", 14, "bold")
    )

    titulo.pack(pady=10)

    # ===== ESTILO TABLA =====

    estilo = ttk.Style()

    estilo.theme_use("clam")

    estilo.configure(
        "Treeview.Heading",
        background="#0A192F",
        foreground="white",
        font=("Segoe UI", 10, "bold")
    )

    estilo.configure(
        "Treeview",
        font=("Segoe UI", 10),
        rowheight=28
    )

    frame = tk.Frame(
        ventana_ver,
        bg="white"
    )

    frame.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    columnas = (
        "ID",
        "ACTIVO",
        "AMENAZA",
        "PROBABILIDAD",
        "IMPACTO",
        "RIESGO",
        "CLASIFICACION"
    )

    tabla = ttk.Treeview(
        frame,
        columns=columnas,
        show="headings"
    )

    tabla.heading("ID", text="ID")
    tabla.heading("ACTIVO", text="ACTIVO")
    tabla.heading("AMENAZA", text="AMENAZA")
    tabla.heading("PROBABILIDAD", text="PROB")
    tabla.heading("IMPACTO", text="IMP")
    tabla.heading("RIESGO", text="RIESGO")
    tabla.heading("CLASIFICACION", text="CLASIFICACIÓN")

    tabla.column("ID", width=50, anchor="center")

    tabla.column(
        "ACTIVO",
        width=220
    )

    tabla.column(
        "AMENAZA",
        width=250
    )

    tabla.column(
        "PROBABILIDAD",
        width=90,
        anchor="center"
    )

    tabla.column(
        "IMPACTO",
        width=90,
        anchor="center"
    )

    tabla.column(
        "RIESGO",
        width=90,
        anchor="center"
    )

    tabla.column(
        "CLASIFICACION",
        width=140,
        anchor="center"
    )

    scrollbar = ttk.Scrollbar(
        frame,
        orient="vertical",
        command=tabla.yview
    )

    tabla.configure(
        yscrollcommand=scrollbar.set
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    tabla.pack(
        fill="both",
        expand=True
    )

    # ===== COLORES =====

    tabla.tag_configure(
        "BAJO",
        background="#D9EAD3"
    )

    tabla.tag_configure(
        "MEDIO",
        background="#FFF3CD"
    )

    tabla.tag_configure(
        "ALTO",
        background="#FCE5CD"
    )

    tabla.tag_configure(
        "CRITICO",
        background="#FF6B6B",
        foreground="white"
    )

    # ===== CONSULTA =====

    conexion = sqlite3.connect("riesgos.db")
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT *
        FROM riesgos
    """)

    registros = cursor.fetchall()

    for fila in registros:

        riesgo = fila[5]

        if riesgo <= 5:

            clasificacion = "BAJO"
            color = "BAJO"

        elif riesgo <= 10:

            clasificacion = "MEDIO"
            color = "MEDIO"

        elif riesgo <= 15:

            clasificacion = "ALTO"
            color = "ALTO"

        else:

            clasificacion = "CRÍTICO"
            color = "CRITICO"

        tabla.insert(
            "",
            tk.END,
            values=(
                fila[0],
                fila[1],
                fila[2],
                fila[3],
                fila[4],
                fila[5],
                clasificacion
            ),
            tags=(color,)
        )

    conexion.close()



# ===================================
# EXPORTAR A EXCEL
# ===================================

def exportar_excel():

    conexion = sqlite3.connect("riesgos.db")
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT *
        FROM riesgos
    """)

    registros = cursor.fetchall()

    libro = Workbook()
    hoja = libro.active

    hoja.title = "Riesgos"

    hoja.append([
        "ID",
	"Activo",
        "Amenaza",
        "Probabilidad",
        "Impacto",
        "Nivel Riesgo",
        "Clasificación"
    ])

    for fila in registros:

        riesgo = fila[5]

        if riesgo <= 5:
            clasificacion = "BAJO"

        elif riesgo <= 10:
            clasificacion = "MEDIO"

        elif riesgo <= 15:
            clasificacion = "ALTO"

        else:
            clasificacion = "CRÍTICO"

        hoja.append([
            fila[0], #  ID
            fila[1], #  ACTIVO
            fila[2], #  AMENAZA
            fila[3], #  PROBABILIDAD
            fila[4], #  IMPACTO
	    fila[5],  # RIESGO
            clasificacion
        ])

    verde = PatternFill(
        start_color="92D050",
        end_color="92D050",
        fill_type="solid"
    )

    amarillo = PatternFill(
        start_color="FFFF00",
        end_color="FFFF00",
        fill_type="solid"
    )

    naranja = PatternFill(
        start_color="FFC000",
        end_color="FFC000",
        fill_type="solid"
    )

    rojo = PatternFill(
        start_color="FF0000",
        end_color="FF0000",
        fill_type="solid"
    )

    for fila in hoja.iter_rows(min_row=2):

        clasificacion = fila[6].value

        if clasificacion == "BAJO":
            fila[6].fill = verde

        elif clasificacion == "MEDIO":
            fila[6].fill = amarillo

        elif clasificacion == "ALTO":
            fila[6].fill = naranja

        elif clasificacion == "CRÍTICO":
            fila[6].fill = rojo

    libro.save("Reporte_Riesgos.xlsx")

    conexion.close()

    messagebox.showinfo(
        "Éxito",
        "Reporte_Riesgos.xlsx generado correctamente"
    )




# ===================================
# GENERAR PDF ISO 27002
# ===================================

def generar_pdf():

    conexion = sqlite3.connect("riesgos.db")
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT *
    FROM riesgos
    """)

    registros = cursor.fetchall()

    conexion.close()

    pdf = canvas.Canvas(
        "Informe_ISO27002_Granados_Arismendi.pdf",
        pagesize=letter
    )

    ancho = 550
    y = 750

    # ---------------------------------------------------
    # PORTADA
    # ---------------------------------------------------

    pdf.setFont("Helvetica-Bold", 16)

    pdf.drawCentredString(
        300,
        y,
        "INFORME DE DIAGNOSTICO"
    )

    y -= 25

    pdf.drawCentredString(
        300,
        y,
        "ISO/IEC 27002:2022"
    )

    y -= 50

    pdf.setFont("Helvetica", 12)

    pdf.drawString(
        50,
        y,
        "Empresa Evaluada:"
    )

    pdf.drawString(
        180,
        y,
        "Granados y Arismendi S.A.S."
    )

    y -= 20

    pdf.drawString(
        50,
        y,
        "Tipo de Evaluacion:"
    )

    pdf.drawString(
        180,
        y,
        "Diagnostico de Riesgos de Seguridad"
    )

    y -= 20

    pdf.drawString(
        50,
        y,
        "Norma de Referencia:"
    )

    pdf.drawString(
        180,
        y,
        "ISO/IEC 27002:2022"
    )

    y -= 40

    # ---------------------------------------------------
    # OBJETIVO
    # ---------------------------------------------------

    pdf.setFont("Helvetica-Bold", 12)

    pdf.drawString(
        50,
        y,
        "1. OBJETIVO DEL DIAGNOSTICO"
    )

    y -= 20

    pdf.setFont("Helvetica", 10)

    pdf.drawString(
        50,
        y,
        "Evaluar los riesgos que afectan los activos"
    )

    y -= 15

    pdf.drawString(
        50,
        y,
        "de informacion de Granados y Arismendi S.A.S."
    )

    y -= 15

    pdf.drawString(
        50,
        y,
        "con base en las buenas practicas de ISO 27002."
    )

    y -= 35

    # ---------------------------------------------------
    # ALCANCE
    # ---------------------------------------------------

    pdf.setFont("Helvetica-Bold", 12)

    pdf.drawString(
        50,
        y,
        "2. ALCANCE"
    )

    y -= 20

    pdf.setFont("Helvetica", 10)

    pdf.drawString(
        60,
        y,
        "- Equipos de computo"
    )

    y -= 15

    pdf.drawString(
        60,
        y,
        "- Correo corporativo"
    )

    y -= 15

    pdf.drawString(
        60,
        y,
        "- Recursos tecnologicos"
    )

    y -= 15

    pdf.drawString(
        60,
        y,
        "- Informacion administrativa y financiera"
    )

    y -= 30

    # ---------------------------------------------------
    # RESUMEN EJECUTIVO
    # ---------------------------------------------------

    pdf.setFont("Helvetica-Bold", 12)

    pdf.drawString(
        50,
        y,
        "3. RESUMEN EJECUTIVO"
    )

    y -= 20

    pdf.setFont("Helvetica", 10)

    pdf.drawString(
        50,
        y,
        f"Se analizaron {len(registros)} riesgos registrados."
    )

    y -= 30

    pdf.showPage()

    y = 750

    # ---------------------------------------------------
    # ANALISIS DE RIESGOS
    # ---------------------------------------------------

    pdf.setFont("Helvetica-Bold", 14)

    pdf.drawString(
        50,
        y,
        "4. ANALISIS DE RIESGOS"
    )

    y -= 30

    criticos = 0

    for fila in registros:

        activo = fila[1]
        amenaza = fila[2]
        riesgo = fila[5]

        if riesgo <= 5:
            clasificacion = "BAJO"

        elif riesgo <= 10:
            clasificacion = "MEDIO"

        elif riesgo <= 15:
            clasificacion = "ALTO"

        else:
            clasificacion = "CRITICO"
            criticos += 1

        if "ransomware" in amenaza.lower():

            control = (
                "8.7 Proteccion contra Malware, "
                "8.13 Copias de Seguridad, "
                "5.24 Gestion de Incidentes"
            )

            recomendacion = (
                "Implementar EDR, backups offline "
                "y monitoreo continuo."
            )

        elif "phishing" in amenaza.lower():

            control = (
                "6.3 Concienciacion del Personal, "
                "5.15 Gestion de Accesos."
            )

            recomendacion = (
                "Capacitacion y MFA."
            )

        elif "malware" in amenaza.lower():

            control = (
                "8.7 Proteccion contra Malware y "
                "8.8 Gestion de Vulnerabilidades."
            )

            recomendacion = (
                "Actualizar sistemas y antivirus."
            )

        else:

            control = "Pendiente de determinar"

            recomendacion = (
                "Realizar analisis especifico."
            )

        pdf.setFont("Helvetica-Bold", 11)

        pdf.drawString(
            50,
            y,
            f"Activo: {activo}"
        )

        y -= 15

        pdf.setFont("Helvetica", 10)

        pdf.drawString(
            60,
            y,
            f"Amenaza: {amenaza}"
        )

        y -= 15

        pdf.drawString(
            60,
            y,
            f"Nivel Riesgo: {riesgo}"
        )

        y -= 15

        pdf.drawString(
            60,
            y,
            f"Clasificacion: {clasificacion}"
        )

        y -= 15

        pdf.drawString(
            60,
            y,
            f"Control ISO: {control}"
        )

        y -= 15

        pdf.drawString(
            60,
            y,
            f"Recomendacion: {recomendacion}"
        )

        y -= 30

        if y < 120:

            pdf.showPage()
            y = 750

    # ---------------------------------------------------
    # CONCLUSIONES
    # ---------------------------------------------------

    pdf.showPage()

    y = 750

    pdf.setFont("Helvetica-Bold", 14)

    pdf.drawString(
        50,
        y,
        "5. CONCLUSIONES"
    )

    y -= 30

    pdf.setFont("Helvetica", 10)

    pdf.drawString(
        50,
        y,
        f"Total de riesgos evaluados: {len(registros)}"
    )

    y -= 20

    pdf.drawString(
        50,
        y,
        f"Riesgos criticos detectados: {criticos}"
    )

    y -= 30

    pdf.drawString(
        50,
        y,
        "La organizacion presenta amenazas asociadas"
    )

    y -= 15

    pdf.drawString(
        50,
        y,
        "a malware, phishing y ransomware que pueden"
    )

    y -= 15

    pdf.drawString(
        50,
        y,
        "afectar la confidencialidad, integridad y"
    )

    y -= 15

    pdf.drawString(
        50,
        y,
        "disponibilidad de la informacion."
    )

    y -= 30

    pdf.setFont("Helvetica-Bold", 12)

    pdf.drawString(
        50,
        y,
        "RECOMENDACIONES GENERALES"
    )

    y -= 25

    pdf.setFont("Helvetica", 10)

    recomendaciones = [
        "Implementar autenticacion multifactor.",
        "Mantener antivirus actualizado.",
        "Aplicar gestion de vulnerabilidades.",
        "Implementar backups fuera de linea.",
        "Capacitar al personal en phishing.",
        "Documentar procedimientos de incidentes.",
        "Realizar auditorias periodicas."
    ]

    for r in recomendaciones:

        pdf.drawString(
            60,
            y,
            f"- {r}"
        )

        y -= 15

    pdf.save()

    messagebox.showinfo(
        "PDF Generado",
        "Informe_ISO27002_Granados_Arismendi.pdf generado correctamente."
    )







# ===================================
# INFORME ISO 27002
# ===================================

def informe_amenazas():

    ventana = tk.Toplevel()
    ventana.title("Informe Diagnóstico ISO 27002")
    ventana.geometry("1100x800")
    ventana.configure(bg="white")

    titulo = tk.Label(
        ventana,
        text="INFORME DIAGNÓSTICO DE SEGURIDAD DE LA INFORMACIÓN\nISO/IEC 27002:2022",
        bg="white",
        fg="#0A192F",
        font=("Segoe UI", 14, "bold")
    )

    # Área del informe
    texto = tk.Text(
        ventana,
        width=90,
        height=45,
        bg="white",
        fg="black",
        font=("Consolas", 10),
        wrap="word",
        padx=80
)

    texto.pack(
        padx=80,
        pady=10
)

    conexion = sqlite3.connect("riesgos.db")
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT *
        FROM riesgos
    """)

    registros = cursor.fetchall()

    total_riesgos = len(registros)

    criticos = 0
    altos = 0
    medios = 0
    bajos = 0

    for fila in registros:

        riesgo = fila[5]

        if riesgo <= 5:
            bajos += 1

        elif riesgo <= 10:
            medios += 1

        elif riesgo <= 15:
            altos += 1

        else:
            criticos += 1

    if criticos > 0:
        estado_general = "ALTO RIESGO"

    elif altos > 0:
        estado_general = "RIESGO MODERADO"

    else:
        estado_general = "RIESGO CONTROLADO"

    texto.insert(
        tk.END,
        f"""
=====================================================================
INFORME DE DIAGNÓSTICO DE SEGURIDAD DE LA INFORMACIÓN
ISO/IEC 27002:2022
=====================================================================

EMPRESA:
Granados y Arismendi S.A.S.

TIPO DE EVALUACIÓN:
Diagnóstico de Riesgos de Seguridad de la Información

NORMA DE REFERENCIA:
ISO/IEC 27002:2022

OBJETIVO

Evaluar los riesgos de seguridad de la información
identificados en los activos tecnológicos de la empresa,
utilizando las buenas prácticas establecidas por la
norma ISO/IEC 27002:2022.

---------------------------------------------------------------------
ALCANCE
---------------------------------------------------------------------

La evaluación comprende:

• Equipos de cómputo
• Correo corporativo
• Sistemas de información
• Infraestructura tecnológica
• Información administrativa y financiera

---------------------------------------------------------------------
METODOLOGÍA UTILIZADA
---------------------------------------------------------------------

La evaluación fue realizada mediante una metodología
de análisis de riesgos basada en:

• Identificación de activos
• Identificación de amenazas
• Valoración de probabilidad
• Valoración de impacto
• Determinación del nivel de riesgo

Fórmula utilizada:

RIESGO = PROBABILIDAD x IMPACTO

---------------------------------------------------------------------
RESUMEN EJECUTIVO
---------------------------------------------------------------------

Total de Riesgos Evaluados : {total_riesgos}

Riesgos Críticos : {criticos}
Riesgos Altos    : {altos}
Riesgos Medios   : {medios}
Riesgos Bajos    : {bajos}

Estado General:
{estado_general}

=====================================================================
ANÁLISIS DETALLADO DE RIESGOS
=====================================================================

"""
    )

    for fila in registros:

        activo = fila[1]
        amenaza = fila[2]
        riesgo = fila[5]

        if riesgo <= 5:
            clasificacion = "BAJO"

        elif riesgo <= 10:
            clasificacion = "MEDIO"

        elif riesgo <= 15:
            clasificacion = "ALTO"

        else:
            clasificacion = "CRÍTICO"

        if "ransomware" in amenaza.lower():

            control_iso = """
8.7 Protección contra Malware
8.13 Copias de Seguridad
5.24 Gestión de Incidentes
8.15 Registro de Eventos
"""

            recomendacion = """
Implementar backups fuera de línea,
solución EDR corporativa,
plan de respuesta a incidentes
y monitoreo continuo.
"""

        elif "phishing" in amenaza.lower():

            control_iso = """
6.3 Concienciación del Personal
5.15 Gestión de Accesos
8.5 Autenticación Segura
"""

            recomendacion = """
Capacitación periódica,
autenticación multifactor,
filtrado de correo electrónico
y simulaciones de phishing.
"""

        elif "malware" in amenaza.lower():

            control_iso = """
8.7 Protección contra Malware
8.8 Gestión de Vulnerabilidades
8.9 Gestión de Configuración
"""

            recomendacion = """
Actualizar sistemas,
fortalecer antivirus,
realizar escaneos periódicos
y endurecimiento de equipos.
"""

        else:

            control_iso = """
Controles ISO por determinar.
"""

            recomendacion = """
Realizar análisis específico del riesgo.
"""

        texto.insert(
            tk.END,
            f"""

=====================================================================
ACTIVO EVALUADO
=====================================================================

Activo: {activo}

Amenaza: {amenaza}

Nivel de Riesgo: {riesgo}

Clasificación: {clasificacion}

---------------------------------------------------------------------
CONTROLES ISO 27002 APLICABLES
---------------------------------------------------------------------

{control_iso}

---------------------------------------------------------------------
RECOMENDACIONES
---------------------------------------------------------------------

{recomendacion}

"""
        )

    texto.insert(
        tk.END,
        f"""

=====================================================================
OBSERVACIONES
=====================================================================

• Se identifican riesgos relacionados con malware,
  phishing y ransomware.

• Se requiere fortalecer la gestión de accesos.

• Es recomendable implementar autenticación multifactor.

• Se recomienda fortalecer la estrategia de copias
  de seguridad y recuperación.

• Es necesario incrementar la concienciación del personal
  frente a amenazas de ingeniería social.

=====================================================================
CONCLUSIONES
=====================================================================

Total de Riesgos Analizados : {total_riesgos}

Riesgos Críticos Detectados : {criticos}

Estado General de Seguridad :

{estado_general}

La evaluación realizada evidencia riesgos que pueden
afectar la confidencialidad, integridad y disponibilidad
de la información de la organización.

Se recomienda implementar controles alineados con
la norma ISO/IEC 27002:2022 para reducir la exposición
a incidentes de seguridad y mejorar la madurez del
sistema de gestión de seguridad de la información.

=====================================================================
RECOMENDACIONES GENERALES
=====================================================================

• Implementar autenticación multifactor (MFA).
• Mantener antivirus actualizado.
• Ejecutar gestión periódica de vulnerabilidades.
• Aplicar políticas de control de acceso.
• Implementar copias de seguridad fuera de línea.
• Capacitar al personal en seguridad informática.
• Realizar auditorías periódicas.
• Mantener monitoreo continuo de eventos.

=====================================================================
MÉTRICAS DE PRUEBA DEL PROTOTIPO
=====================================================================

Pruebas Ejecutadas : 5

Pruebas Exitosas : 5

Porcentaje de Éxito : 100%

Casos Evaluados:

✓ Registro de Activos
✓ Evaluación de Riesgos
✓ Visualización de Matriz
✓ Exportación a Excel
✓ Generación de Informe PDF

=====================================================================
FIN DEL INFORME
=====================================================================

"""
    )

    conexion.close()



# ===================================
# REPORTES / DASHBOARD
# ===================================

def reportes():

    conexion = sqlite3.connect("riesgos.db")
    cursor = conexion.cursor()

    # Total activos
    cursor.execute(
        "SELECT COUNT(*) FROM activos"
    )

    total_activos = cursor.fetchone()[0]

    # Total riesgos
    cursor.execute(
        "SELECT COUNT(*) FROM riesgos"
    )

    total_riesgos = cursor.fetchone()[0]

    # Riesgos críticos

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM riesgos
        WHERE nivel_riesgo >= 16
        """
    )

    criticos = cursor.fetchone()[0]

    # Riesgos altos

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM riesgos
        WHERE nivel_riesgo BETWEEN 11 AND 15
        """
    )

    altos = cursor.fetchone()[0]

    # Riesgos medios

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM riesgos
        WHERE nivel_riesgo BETWEEN 6 AND 10
        """
    )

    medios = cursor.fetchone()[0]

    # Riesgos bajos

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM riesgos
        WHERE nivel_riesgo <= 5
        """
    )

    bajos = cursor.fetchone()[0]

    conexion.close()

    # ===================================
    # DASHBOARD
    # ===================================

    ventana_dashboard = tk.Toplevel()
    ventana_dashboard.title("Indicadores de Riesgo")
    ventana_dashboard.geometry("850x600")
    ventana_dashboard.configure(bg=COLOR_FONDO)

    titulo = tk.Label(
        ventana_dashboard,
        text="DASHBOARD DE INDICADORES ISO 27002",
        bg=COLOR_FONDO,
        fg=COLOR_TITULO,
        font=("Consolas", 16, "bold")
    )

    titulo.pack(pady=20)

    # ===================================
    # TARJETAS SUPERIORES
    # ===================================

    frame_superior = tk.Frame(
        ventana_dashboard,
        bg=COLOR_FONDO
    )

    frame_superior.pack(pady=10)

    # Activos

    frame_activos = tk.Frame(
        frame_superior,
        bg="#1E3A5F",
        width=180,
        height=100
    )

    frame_activos.grid(
        row=0,
        column=0,
        padx=15
    )

    frame_activos.pack_propagate(False)

    tk.Label(
        frame_activos,
        text="📦 ACTIVOS",
        bg="#1E3A5F",
        fg="white",
        font=("Consolas", 10, "bold")
    ).pack(pady=10)

    tk.Label(
        frame_activos,
        text=total_activos,
        bg="#1E3A5F",
        fg="white",
        font=("Consolas", 18, "bold")
    ).pack()

    # Riesgos

    frame_riesgos = tk.Frame(
        frame_superior,
        bg="#34495E",
        width=180,
        height=100
    )

    frame_riesgos.grid(
        row=0,
        column=1,
        padx=15
    )

    frame_riesgos.pack_propagate(False)

    tk.Label(
        frame_riesgos,
        text="📊 RIESGOS",
        bg="#34495E",
        fg="white",
        font=("Consolas", 10, "bold")
    ).pack(pady=10)

    tk.Label(
        frame_riesgos,
        text=total_riesgos,
        bg="#34495E",
        fg="white",
        font=("Consolas", 18, "bold")
    ).pack()

    # ===================================
    # MATRIZ DE INDICADORES
    # ===================================

    frame_indicadores = tk.Frame(
        ventana_dashboard,
        bg=COLOR_FONDO
    )

    frame_indicadores.pack(
        pady=25
    )

    # Criticos

    frame_criticos = tk.Frame(
        frame_indicadores,
        bg="#FF4444",
        width=180,
        height=120
    )

    frame_criticos.grid(
        row=0,
        column=0,
        padx=15,
        pady=15
    )

    frame_criticos.pack_propagate(False)

    tk.Label(
        frame_criticos,
        text="🔴 CRÍTICOS",
        bg="#FF4444",
        fg="white",
        font=("Consolas", 11, "bold")
    ).pack(pady=15)

    tk.Label(
        frame_criticos,
        text=criticos,
        bg="#FF4444",
        fg="white",
        font=("Consolas", 24, "bold")
    ).pack()

    # Altos

    frame_altos = tk.Frame(
        frame_indicadores,
        bg="#FFA500",
        width=180,
        height=120
    )

    frame_altos.grid(
        row=0,
        column=1,
        padx=15,
        pady=15
    )

    frame_altos.pack_propagate(False)

    tk.Label(
        frame_altos,
        text="🟠 ALTOS",
        bg="#FFA500",
        fg="white",
        font=("Consolas", 11, "bold")
    ).pack(pady=15)

    tk.Label(
        frame_altos,
        text=altos,
        bg="#FFA500",
        fg="white",
        font=("Consolas", 24, "bold")
    ).pack()

    # Medios

    frame_medios = tk.Frame(
        frame_indicadores,
        bg="#FFD700",
        width=180,
        height=120
    )

    frame_medios.grid(
        row=1,
        column=0,
        padx=15,
        pady=15
    )

    frame_medios.pack_propagate(False)

    tk.Label(
        frame_medios,
        text="🟡 MEDIOS",
        bg="#FFD700",
        fg="black",
        font=("Consolas", 11, "bold")
    ).pack(pady=15)

    tk.Label(
        frame_medios,
        text=medios,
        bg="#FFD700",
        fg="black",
        font=("Consolas", 24, "bold")
    ).pack()

    # Bajos

    frame_bajos = tk.Frame(
        frame_indicadores,
        bg="#00AA55",
        width=180,
        height=120
    )

    frame_bajos.grid(
        row=1,
        column=1,
        padx=15,
        pady=15
    )

    frame_bajos.pack_propagate(False)

    tk.Label(
        frame_bajos,
        text="🟢 BAJOS",
        bg="#00AA55",
        fg="white",
        font=("Consolas", 11, "bold")
    ).pack(pady=15)

    tk.Label(
        frame_bajos,
        text=bajos,
        bg="#00AA55",
        fg="white",
        font=("Consolas", 24, "bold")
    ).pack()

    # ===================================
    # ESTADO GENERAL
    # ===================================

    if criticos > 0:
        estado = "🔴 ALTO RIESGO"
        color_estado = "#FF4444"

    elif altos > 0:
        estado = "🟠 RIESGO MODERADO"
        color_estado = "#FFA500"

    else:
        estado = "🟢 RIESGO CONTROLADO"

    tk.Label(
        ventana_dashboard,
        text=f"Estado General del Sistema: {estado}",
        bg=COLOR_FONDO,
        fg=COLOR_TITULO,
        font=("Consolas", 12, "bold")
    ).pack(pady=20)



# ===================================
# VENTANA PRINCIPAL
# ===================================

ventana = tk.Tk()
ventana.title("SOC - Sistema de Gestión de Riesgos ISO 27002")
ventana.geometry("1000x700")
ventana.configure(bg=COLOR_FONDO)

titulo = tk.Label(
    ventana,
    text="SOC - Sistema de Gestión de Riesgos ISO 27002",
    bg=COLOR_FONDO,
    fg=COLOR_TITULO,
    font=FUENTE_TITULO
)

titulo.pack(pady=20)

lbl_estado = tk.Label(
    ventana,
    text="● MONITOREO ACTIVO",
    bg=COLOR_FONDO,
    fg="#00FF00",
    font=("Consolas", 11, "bold")
)

lbl_estado.pack(pady=5)

def estilo_boton(boton):
    boton.config(
        bg=COLOR_BOTON,
        fg=COLOR_TEXTO,
        activebackground="#1E90FF",
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2",
        font=FUENTE_BOTON
    )

btn_activos = tk.Button(
    ventana,
    text="Gestión de Activos",
    width=30,
    height=2,
    command=registrar_activo
)

btn_activos.pack(pady=10)

btn_ver = tk.Button(
    ventana,
    text="Ver Activos",
    width=30,
    height=2,
    command=ver_activos
)

btn_ver.pack(pady=10)

btn_riesgos = tk.Button(
    ventana,
    text="Evaluación de Riesgos",
    width=30,
    height=2,
    command=evaluar_riesgo
)

btn_riesgos.pack(pady=10)

btn_ver_riesgos = tk.Button(
    ventana,
    text="Matriz de Riesgos",
    width=30,
    height=2,
    command=ver_riesgos
)

btn_ver_riesgos.pack(pady=10)


btn_excel = tk.Button(
    ventana,
    text="Exportar Matriz a Excel",
    width=30,
    height=2,
    command=exportar_excel
)

btn_excel.pack(pady=10)

btn_informe = tk.Button(
    ventana,
    text="Generar Diagnóstico ISO 27002",
    width=30,
    height=2,
    command=informe_amenazas
)

btn_informe.pack(pady=10)


btn_pdf = tk.Button(
    ventana,
    text="Exportar Diagnóstico a PDF",
    width=30,
    height=2,
    command=generar_pdf
)

btn_pdf.pack(pady=10)


btn_reportes = tk.Button(
    ventana,
    text="Indicadores de Riesgo",
    width=30,
    height=2,
    command=reportes
)

btn_reportes.pack(pady=10)

btn_salir = tk.Button(
    ventana,
    text="Cerrar Sistema",
    width=30,
    height=2,
    command=ventana.destroy
)

btn_salir.pack(pady=10)

estilo_boton(btn_activos)
estilo_boton(btn_ver)
estilo_boton(btn_riesgos)
estilo_boton(btn_ver_riesgos)
estilo_boton(btn_excel)
estilo_boton(btn_informe)
estilo_boton(btn_pdf)
estilo_boton(btn_reportes)
estilo_boton(btn_salir)

ventana.mainloop()