import tkinter as tk
from tkinter import messagebox
import sqlite3
from openpyxl import Workbook
from openpyxl.styles import PatternFill
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


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
    ventana_activos.geometry("500x300")

    tk.Label(
        ventana_activos,
        text="Nombre del Activo"
    ).pack(pady=5)

    entrada_nombre = tk.Entry(
        ventana_activos,
        width=40
    )
    entrada_nombre.pack()

    tk.Label(
        ventana_activos,
        text="Tipo de Activo"
    ).pack(pady=5)

    entrada_tipo = tk.Entry(
        ventana_activos,
        width=40
    )
    entrada_tipo.pack()

    def guardar_activo():

        nombre = entrada_nombre.get()
        tipo = entrada_tipo.get()

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
            INSERT INTO activos (nombre, tipo)
            VALUES (?, ?)
            """,
            (nombre, tipo)
        )

        conexion.commit()
        conexion.close()

        messagebox.showinfo(
            "Éxito",
            "Activo guardado correctamente"
        )

        entrada_nombre.delete(0, tk.END)
        entrada_tipo.delete(0, tk.END)

    tk.Button(
        ventana_activos,
        text="Guardar",
        command=guardar_activo
    ).pack(pady=20)


# ===================================
# VER ACTIVOS
# ===================================

def ver_activos():

    ventana_ver = tk.Toplevel()
    ventana_ver.title("Activos Registrados")
    ventana_ver.geometry("600x400")

    texto = tk.Text(
        ventana_ver,
        width=70,
        height=20
    )

    texto.pack(pady=10)

    conexion = sqlite3.connect("riesgos.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM activos")

    registros = cursor.fetchall()

    texto.insert(
        tk.END,
        "ID | NOMBRE | TIPO\n"
    )

    texto.insert(
        tk.END,
        "-" * 50 + "\n"
    )

    for fila in registros:
        texto.insert(
            tk.END,
            f"{fila[0]} | {fila[1]} | {fila[2]}\n"
        )

    conexion.close()


# ===================================
# EVALUAR RIESGOS
# ===================================

def evaluar_riesgo():

    ventana_riesgo = tk.Toplevel()
    ventana_riesgo.title("Evaluación de Riesgos")
    ventana_riesgo.geometry("500x500")
    ventana_riesgo.configure(bg="#f0f0f0")

    tk.Label(
        ventana_riesgo,
        text="Activo",
        font=("Arial", 10, "bold"),
        bg="#f0f0f0"
    ).pack(pady=5)

    entrada_activo = tk.Entry(
        ventana_riesgo,
        width=40
    )
    entrada_activo.pack()

    tk.Label(
        ventana_riesgo,
        text="Amenaza",
        font=("Arial", 10, "bold"),
        bg="#f0f0f0"
    ).pack(pady=5)

    entrada_amenaza = tk.Entry(
        ventana_riesgo,
        width=40
    )
    entrada_amenaza.pack()

    tk.Label(
        ventana_riesgo,
        text="Probabilidad (1 - 5)",
        font=("Arial", 10, "bold"),
        bg="#f0f0f0"
    ).pack(pady=5)

    entrada_probabilidad = tk.Entry(
        ventana_riesgo,
        width=10
    )
    entrada_probabilidad.pack()

    tk.Label(
        ventana_riesgo,
        text="Impacto (1 - 5)",
        font=("Arial", 10, "bold"),
        bg="#f0f0f0"
    ).pack(pady=5)

    entrada_impacto = tk.Entry(
        ventana_riesgo,
        width=10
    )
    entrada_impacto.pack()

    resultado = tk.Label(
        ventana_riesgo,
        text="",
        font=("Arial", 12, "bold"),
        bg="#f0f0f0"
    )

    resultado.pack(pady=15)

    def calcular_riesgo():

        try:

            activo = entrada_activo.get()
            amenaza = entrada_amenaza.get()

            probabilidad = int(
                entrada_probabilidad.get()
            )

            impacto = int(
                entrada_impacto.get()
            )

            if activo == "":
                messagebox.showerror(
                    "Error",
                    "Debe ingresar un activo"
                )
                return

            if amenaza == "":
                messagebox.showerror(
                    "Error",
                    "Debe ingresar una amenaza"
                )
                return

            if probabilidad < 1 or probabilidad > 5:
                messagebox.showerror(
                    "Error",
                    "La probabilidad debe estar entre 1 y 5"
                )
                return

            if impacto < 1 or impacto > 5:
                messagebox.showerror(
                    "Error",
                    "El impacto debe estar entre 1 y 5"
                )
                return

            riesgo = probabilidad * impacto

            if riesgo <= 5:
                clasificacion = "BAJO"
                color = "green"

            elif riesgo <= 10:
                clasificacion = "MEDIO"
                color = "#d4ac0d"

            elif riesgo <= 15:
                clasificacion = "ALTO"
                color = "#e67e22"

            else:
                clasificacion = "CRÍTICO"
                color = "red"

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
                text=f"RIESGO: {riesgo} - {clasificacion}",
                fg=color
            )

            messagebox.showinfo(
                "Resultado",
                f"""
Activo: {activo}

Amenaza: {amenaza}

Nivel de Riesgo: {riesgo}

Clasificación: {clasificacion}
"""
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Probabilidad e Impacto deben ser números entre 1 y 5"
            )

    tk.Button(
        ventana_riesgo,
        text="Calcular Riesgo",
        bg="#3498db",
        fg="white",
        width=20,
        command=calcular_riesgo
    ).pack(pady=20)



# ===================================
# VER RIESGOS
# ===================================

def ver_riesgos():

    ventana_ver = tk.Toplevel()
    ventana_ver.title("Riesgos Registrados")
    ventana_ver.geometry("800x400")

    texto = tk.Text(
        ventana_ver,
        width=100,
        height=20
    )

    texto.pack(pady=10)

    conexion = sqlite3.connect("riesgos.db")
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT *
        FROM riesgos
        """
    )

    registros = cursor.fetchall()

    texto.insert(
        tk.END,
        "ID | AMENAZA | PROBABILIDAD | IMPACTO | RIESGO | CLASIFICACIÓN\n"
    )

    texto.insert(
        tk.END,
        "-" * 90 + "\n"
    )

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

        texto.insert(
            tk.END,
            f"{fila[0]} | {fila[1]} | {fila[2]} | {fila[3]} | {fila[4]} | {fila[5]} | {clasificacion}\n"
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
    ventana.title("Informe ISO 27002")
    ventana.geometry("1000x800")

    texto = tk.Text(
        ventana,
        width=120,
        height=45
    )

    texto.pack(pady=10)

    conexion = sqlite3.connect("riesgos.db")
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT *
        FROM riesgos
    """)

    registros = cursor.fetchall()

    total_riesgos = len(registros)

    texto.insert(
        tk.END,
        """


=====================================================================
INFORME DE DIAGNÓSTICO DE SEGURIDAD DE LA INFORMACIÓN
ISO/IEC 27002
=====================================================================

EMPRESA:
Granados y Arismendi S.A.S.

OBJETIVO:

Evaluar los riesgos de seguridad de la información
identificados en los activos tecnológicos de la empresa,
utilizando las buenas prácticas establecidas en la
norma ISO/IEC 27002:2022.

---------------------------------------------------------------------
RESUMEN EJECUTIVO
---------------------------------------------------------------------

Durante la evaluación se identificaron riesgos asociados a
amenazas de Phishing, Malware y Ransomware que pueden afectar
la confidencialidad, integridad y disponibilidad de la
información corporativa.

"""
    )

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
            clasificacion = "CRÍTICO"
            criticos += 1

        # CONTROLES ISO SEGÚN AMENAZA

        if "ransomware" in amenaza.lower():

            control_iso = """
8.7 Protección contra Malware
8.13 Copias de Seguridad
5.24 Gestión de Incidentes
8.15 Registro de Eventos
"""

            recomendacion = """
Implementar backups offline,
solución EDR corporativa,
plan de respuesta a incidentes y
monitoreo continuo.
"""

        elif "phishing" in amenaza.lower():

            control_iso = """
6.3 Concienciación del Personal
5.15 Gestión de Accesos
8.5 Autenticación Segura
"""

            recomendacion = """
Capacitación periódica,
autenticación multifactor
y filtrado de correo electrónico.
"""

        elif "malware" in amenaza.lower():

            control_iso = """
8.7 Protección contra Malware
8.8 Gestión de Vulnerabilidades
8.9 Gestión de Configuración
"""

            recomendacion = """
Actualizar sistemas,
fortalecer antivirus
y realizar escaneos periódicos.
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

    # Nivel general

    texto.insert(
        tk.END,
        f"""

=====================================================================
CONCLUSIONES
=====================================================================

Total de Riesgos Analizados: {total_riesgos}

Riesgos Críticos Detectados: {criticos}

La evaluación realizada a Granados y Arismendi S.A.S.
evidencia la existencia de amenazas significativas
relacionadas con ransomware, malware y phishing.

Se recomienda fortalecer los controles técnicos,
organizacionales y operativos establecidos en la
norma ISO/IEC 27002:2022 con el fin de reducir la
exposición a incidentes de seguridad y garantizar
la continuidad de las operaciones.

Estado General de Seguridad:
REQUIERE MEJORA CONTINUA.

=====================================================================
FIN DEL INFORME
=====================================================================
"""
    )

    conexion.close()

# ===================================
# REPORTES
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

    messagebox.showinfo(
        "Reporte General",
        f"""
Total de Activos: {total_activos}

Total de Riesgos: {total_riesgos}

Riesgos Críticos: {criticos}

Riesgos Altos: {altos}

Riesgos Medios: {medios}

Riesgos Bajos: {bajos}
"""
    )



# ===================================
# VENTANA PRINCIPAL
# ===================================

ventana = tk.Tk()
ventana.title("Sistema de Gestión de Riesgos ISO 27002")
ventana.geometry("800x600")

titulo = tk.Label(
    ventana,
    text="Sistema de Gestión de Riesgos ISO 27002",
    font=("Arial", 18, "bold")
)

titulo.pack(pady=20)

btn_activos = tk.Button(
    ventana,
    text="Gestión de Activos",
    width=25,
    height=2,
    command=registrar_activo
)

btn_activos.pack(pady=10)

btn_ver = tk.Button(
    ventana,
    text="Ver Activos",
    width=25,
    height=2,
    command=ver_activos
)

btn_ver.pack(pady=10)

btn_riesgos = tk.Button(
    ventana,
    text="Evaluación de Riesgos",
    width=25,
    height=2,
    command=evaluar_riesgo
)

btn_riesgos.pack(pady=10)

btn_ver_riesgos = tk.Button(
    ventana,
    text="Matriz de Riesgos",
    width=25,
    height=2,
    command=ver_riesgos
)

btn_ver_riesgos.pack(pady=10)


btn_excel = tk.Button(
    ventana,
    text="Exportar Matriz a Excel",
    width=25,
    height=2,
    command=exportar_excel
)

btn_excel.pack(pady=10)

btn_informe = tk.Button(
    ventana,
    text="Generar Diagnóstico ISO 27002",
    width=25,
    height=2,
    command=informe_amenazas
)

btn_informe.pack(pady=10)


btn_pdf = tk.Button(
    ventana,
    text="Exportar Diagnóstico a PDF",
    width=25,
    height=2,
    command=generar_pdf
)

btn_pdf.pack(pady=10)


btn_reportes = tk.Button(
    ventana,
    text="Indicadores de Riesgo",
    width=25,
    height=2,
    command=reportes
)

btn_reportes.pack(pady=10)

btn_salir = tk.Button(
    ventana,
    text="Cerrar Sistema",
    width=25,
    height=2,
    command=ventana.destroy
)

btn_salir.pack(pady=10)

ventana.mainloop()