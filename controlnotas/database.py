import mysql.connector
import pandas as pd

def conectar():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="cositop"
    )
    return conexion


def obtenerusuarios(username):
    #cpnectar a la base de datos
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    #busca4r el usuario el la bd
    query = "SELECT * FROM usuarios WHERE Username = %s"
    cursor.execute(query, (username,))
    usuario = cursor.fetchone()
    conn.close()
    return usuario

# obtener los estudiantes
def obtenerestudiantes():

    conn = conectar()
    query = "SELECT * FROM estudiantes"
    df = pd.read_sql(query, conn)
    conn.close()

    print("=== COLUMNAS ===", df.columns.tolist())  # ← agrega esto
    print("=== DATOS ===")
    print(df.head())   

    return df

#registrar estudiantes
def insertar_estudiante(nombre, edad, carrera, nota1, nota2, nota3, promedio, desempeno ):
    conn = conectar()
    cursor = conn.cursor()
    query = """
        INSERT INTO estudiantes (Nombre_estudiante, Edad_estudiante, Carrera_estudiante, Nota1, Nota2, Nota3, Promedio, Desempeño)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (nombre, edad, carrera, nota1, nota2, nota3, promedio, desempeno))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Prueba de conexión 
    coon=conectar()
    print("conexion exitosa mi pez")
    coon.close()