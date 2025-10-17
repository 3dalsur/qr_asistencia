import flet as ft
import cv2
from pyzbar import pyzbar
import mysql.connector

# Configura tu conexión MySQL
db = mysql.connector.connect(
    host="186.64.118.90",
    port=3306,
    user="labsurc2_qr ",
    password="1234.,soporte",
    database="labsurc2_codigo"
)

def guardar_qr(codigo):
    cursor = db.cursor()
    sql = "INSERT INTO codigos_qr (codigo) VALUES (%s)"
    cursor.execute(sql, (codigo,))
    db.commit()
    cursor.close()

def main(page: ft.Page):
    result = ft.Text(value="Esperando QR...", size=18)
    page.add(result)

    cap = cv2.VideoCapture(0)
    running = True

    def scan_qr(ev):
        nonlocal running
        running = True
        while running:
            ret, frame = cap.read()
            if not ret:
                continue
            barcodes = pyzbar.decode(frame)
            for barcode in barcodes:
                qr_value = barcode.data.decode("utf-8")
                result.value = f"QR detectado: {qr_value}"
                guardar_qr(qr_value)
                page.update()
                running = False
                break
            cv2.imshow("Escaneo QR", frame)
            if cv2.waitKey(1) == 27 or not running:
                break
        cap.release()
        cv2.destroyAllWindows()

    btn_iniciar = ft.ElevatedButton("Iniciar escaneo QR", on_click=scan_qr)
    page.add(btn_iniciar)

ft.app(target=main)
