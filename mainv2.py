import tkinter as tk
from tkinter import messagebox
import sqlite3

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
    ventana_riesgo.geometry("500x400")

    tk.Label(
        ventana_riesgo,
        text="Amenaza"
    ).pack(pady=5)

    entrada_amenaza = tk.Entry(
        ventana_riesgo,
        width=40
    )
    entrada_amenaza.pack()

    tk.Label(
        ventana_riesgo,
        text="Probabilidad (1-5)"
    ).pack(pady=5)

    entrada_probabilidad = tk.Entry(
        ventana_riesgo,
        width=10
    )
    entrada_probabilidad.pack()

    tk.Label(
        ventana_riesgo,
        text="Impacto (1-5)"
    ).pack(pady=5)

    entrada_impacto = tk.Entry(
        ventana_riesgo,
        width=10
    )
    entrada_impacto.pack()

    
def calcular_riesgo():

        try:

            amenaza = entrada_amenaza.get()
            probabilidad = int(entrada_probabilidad.get())
            impacto = int(entrada_impacto.get())

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

            elif riesgo <= 10:
                clasificacion = "MEDIO"

            elif riesgo <= 15:
                clasificacion = "ALTO"

            else:
                clasificacion = "CRÍTICO"

            conexion = sqlite3.connect("riesgos.db")
            cursor = conexion.cursor()

            cursor.execute(
                """
                INSERT INTO riesgos
                (amenaza, probabilidad, impacto, nivel_riesgo)
                VALUES (?, ?, ?, ?)
                """,
                (
                    amenaza,
                    probabilidad,
                    impacto,
                    riesgo
                )
            )

            conexion.commit()
            conexion.close()

            messagebox.showinfo(
                "Resultado",
                f"Nivel de riesgo: {riesgo}\nClasificación: {clasificacion}"
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Probabilidad e Impacto deben ser números entre 1 y 5"
            )

    tk.Button(
        ventana_riesgo,
        text="Calcular Riesgo",
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

        riesgo = fila[4]

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
            f"{fila[0]} | {fila[1]} | {fila[2]} | {fila[3]} | {fila[4]} | {clasificacion}\n"
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
    text="Registrar Activos",
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
    text="Evaluar Riesgos",
    width=25,
    height=2,
    command=evaluar_riesgo
)

btn_riesgos.pack(pady=10)

btn_ver_riesgos = tk.Button(
    ventana,
    text="Ver Riesgos",
    width=25,
    height=2,
    command=ver_riesgos
)

btn_ver_riesgos.pack(pady=10)


btn_reportes = tk.Button(
    ventana,
    text="Reportes",
    width=25,
    height=2,
    command=reportes
)

btn_reportes.pack(pady=10)

btn_salir = tk.Button(
    ventana,
    text="Salir",
    width=25,
    height=2,
    command=ventana.destroy
)

btn_salir.pack(pady=10)

ventana.mainloop()