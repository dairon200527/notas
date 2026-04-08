from flask import Flask, render_template, request, redirect, session, send_file
from database import conectar, obtenerusuarios, insertar_estudiante, obtenerestudiantes
from dashprincipal import creartablero
import pandas as pd
import unicodedata
import io

app = Flask(__name__)

# Clave necesaria
app.secret_key = "secretico"

creartablero(app)

# Almacenamiento temporal de rechazados en memoria
_rechazados_excel = None


# Evitar cache en páginas protegidas
@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


# Proteger rutas del dashboard
@app.before_request
def proteger_rutas():
    rutas_protegidas = ["/dashprincipal"]
    if any(request.path.startswith(ruta) for ruta in rutas_protegidas):
        if "username" not in session:
            return redirect("/")


# Inicio de sesión
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        usuario = obtenerusuarios(username)

        if not usuario:
            return "Usuario no encontrado"

        if password != usuario["Password"]:
            return "Contraseña incorrecta"

        session["username"] = usuario["Username"]
        session["rol"] = usuario["Rolusuario"]

        return redirect("/dashprincipal")

    return render_template("login.html")


# Cerrar sesión
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ===================== PUNTO 1: Validar duplicado manual =====================
def estudiante_existe(nombre, carrera):
    """Verifica si ya existe un estudiante con ese nombre y carrera en la BD."""
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT COUNT(*) as total FROM estudiantes WHERE Nombre_estudiante = %s AND Carrera_estudiante = %s",
        (nombre, carrera)
    )
    resultado = cursor.fetchone()
    conn.close()
    return resultado["total"] > 0


# Registro de estudiante
@app.route("/registro_estudiante", methods=["GET", "POST"])
def registroestudiante():
    if "username" not in session:
        return redirect("/")

    error = None

    if request.method == "POST":
        nombre = request.form["nombre"].strip().title()
        edad = int(request.form["edad"])
        carrera = request.form["carrera"].strip().title()
        nota1 = float(request.form["nota1"])
        nota2 = float(request.form["nota2"])
        nota3 = float(request.form["nota3"])

        # PUNTO 1: Verificar duplicado
        if estudiante_existe(nombre, carrera):
            error = f"El estudiante '{nombre}' ya está registrado en '{carrera}'."
            return render_template("registro_estudiante.html", error=error)

        # Calcular promedio
        promedio = round((nota1 + nota2 + nota3) / 3, 2)

        # Calcular desempeño
        desempeno = clasificar_desempeno(promedio)

        insertar_estudiante(nombre, edad, carrera, nota1, nota2, nota3, promedio, desempeno)

        return redirect("/dashprincipal")

    return render_template("registro_estudiante.html", error=error)


# Función para quitar acentos
def quitar_acentos(texto):
    if pd.isna(texto):
        return texto

    texto = str(texto)

    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )


# Función para clasificar el desempeño
def clasificar_desempeno(promedio):
    if promedio >= 4.5:
        return "Excelente"
    elif promedio >= 4.0:
        return "Bueno"
    elif promedio >= 3.0:
        return "Regular"
    else:
        return "Bajo"


# =====================  Carga masiva  =====================
@app.route("/carga_masiva", methods=["GET", "POST"])
def carga_masiva():
    global _rechazados_excel

    if request.method == "POST":

        archivo = request.files["archivo"]
        df = pd.read_excel(archivo)

        rechazados = []
        insertados = 0
        duplicados = 0

        # Columnas requeridas
        columnas_requeridas = ["Nombre", "Edad", "Carrera", "Nota1", "Nota2", "Nota3"]

        # ── Detectar datos faltantes ──
        df_nulos = df[df[columnas_requeridas].isnull().any(axis=1)].copy()
        if not df_nulos.empty:
            df_nulos["Motivo_rechazo"] = "Datos faltantes"
            rechazados.append(df_nulos)

        df = df.dropna(subset=columnas_requeridas)

        # Limpiar nombres
        df["Nombre"] = df["Nombre"].astype(str).str.strip()
        df["Nombre"] = df["Nombre"].apply(quitar_acentos)
        df["Nombre"] = df["Nombre"].str.title()

        # Limpiar carrera
        df["Carrera"] = df["Carrera"].astype(str).str.strip()
        df["Carrera"] = df["Carrera"].apply(quitar_acentos)
        df["Carrera"] = df["Carrera"].str.title()

        # ──  Detectar edades negativas ──
        mask_edad = df["Edad"] < 0
        if mask_edad.any():
            rec = df[mask_edad].copy()
            rec["Motivo_rechazo"] = "Edad negativa"
            rechazados.append(rec)
        df = df[~mask_edad]

        # ── Detectar notas inválidas ──
        mask_notas = ~(
            (df["Nota1"] >= 0) & (df["Nota1"] <= 5) &
            (df["Nota2"] >= 0) & (df["Nota2"] <= 5) &
            (df["Nota3"] >= 0) & (df["Nota3"] <= 5)
        )
        if mask_notas.any():
            rec = df[mask_notas].copy()
            rec["Motivo_rechazo"] = "Notas fuera de rango (0-5)"
            rechazados.append(rec)
        df = df[~mask_notas]

        # Calcular promedio y desempeño
        df["Promedio"] = ((df["Nota1"] + df["Nota2"] + df["Nota3"]) / 3).round(2)
        df = df[df["Promedio"] <= 5]
        df["Desempeño"] = df["Promedio"].apply(clasificar_desempeno)

        # ──  Detectar duplicados dentro del mismo archivo ──
        mask_dup_interno = df.duplicated(subset=["Nombre", "Carrera"], keep="first")
        if mask_dup_interno.any():
            rec = df[mask_dup_interno].copy()
            rec["Motivo_rechazo"] = "Duplicado en el archivo"
            rechazados.append(rec)
        df = df[~mask_dup_interno]

        # Insertar en la base de datos
        conn = conectar()
        cursor = conn.cursor()

        for _, row in df.iterrows():
            # ── Punto 1 & 3: Verificar duplicado contra la BD ──
            if estudiante_existe(row["Nombre"], row["Carrera"]):
                rec = row.to_frame().T.copy()
                rec["Motivo_rechazo"] = "Duplicado en base de datos"
                rechazados.append(rec)
                duplicados += 1
                continue

            query = """
            INSERT INTO estudiantes
            (Nombre_estudiante, Edad_estudiante, Carrera_estudiante, Nota1, Nota2, Nota3, Promedio, Desempeño)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                row["Nombre"],
                row["Edad"],
                row["Carrera"],
                row["Nota1"],
                row["Nota2"],
                row["Nota3"],
                row["Promedio"],
                row["Desempeño"]
            ))
            insertados += 1

        conn.commit()
        conn.close()

        total_rechazados = sum(len(r) for r in rechazados)

        # ──  Generar Excel de rechazados ──
        hay_rechazados = total_rechazados > 0
        if hay_rechazados:
            df_rechazados = pd.concat(rechazados, ignore_index=True)
            buf = io.BytesIO()
            with pd.ExcelWriter(buf, engine="openpyxl") as writer:
                df_rechazados.to_excel(writer, index=False, sheet_name="Rechazados")
            _rechazados_excel = buf.getvalue()
        else:
            _rechazados_excel = None

        # ── Resumen estadístico ──
        resumen = [
            {"categoria": " Insertados",  "cantidad": insertados},
            {"categoria": " Rechazados",  "cantidad": total_rechazados},
            {"categoria": " Duplicados",  "cantidad": duplicados},
        ]

        return render_template(
            "carga_masiva.html",
            resumen=resumen,
            hay_rechazados=hay_rechazados
        )

    return render_template("carga_masiva.html", resumen=None, hay_rechazados=False)


# ── Punto 3: Descargar Excel de rechazados ──
@app.route("/descargar_rechazados")
def descargar_rechazados():
    global _rechazados_excel
    if _rechazados_excel is None:
        return "No hay registros rechazados disponibles.", 404

    return send_file(
        io.BytesIO(_rechazados_excel),
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name="rechazados.xlsx"
    )


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)