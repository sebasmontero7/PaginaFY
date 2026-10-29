import os
import re
import smtplib
from email.message import EmailMessage

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

MAX_NOMBRE = 80
MAX_EMAIL = 254
MAX_MENSAJE = 350
PATRON_EMAIL = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/contacto", methods=["POST"])
def contacto():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(success=False, message="La solicitud no tiene un formato válido."), 400

    nombre = data.get("nombre", "")
    email = data.get("email", "")
    mensaje = data.get("mensaje", "")
    if not all(isinstance(value, str) for value in (nombre, email, mensaje)):
        return jsonify(success=False, message="Revisa los datos del formulario."), 400

    nombre, email, mensaje = nombre.strip(), email.strip(), mensaje.strip()
    if not nombre or not email or not mensaje:
        return jsonify(success=False, message="Por favor completa todos los campos del formulario."), 400
    if len(nombre) > MAX_NOMBRE:
        return jsonify(success=False, message=f"El nombre no puede superar {MAX_NOMBRE} caracteres."), 400
    if "\r" in nombre or "\n" in nombre:
        return jsonify(success=False, message="El nombre contiene caracteres no válidos."), 400
    if len(email) > MAX_EMAIL or not PATRON_EMAIL.fullmatch(email):
        return jsonify(success=False, message="Por favor ingresa un correo electrónico válido."), 400
    if len(mensaje) > MAX_MENSAJE:
        return jsonify(success=False, message=f"El mensaje no puede superar {MAX_MENSAJE} caracteres."), 400

    remitente = os.getenv("SMTP_USER")
    contrasena = os.getenv("SMTP_PASSWORD")
    destinatario = os.getenv("CONTACT_EMAIL")
    if not all((remitente, contrasena, destinatario)):
        app.logger.error("Falta configurar SMTP_USER, SMTP_PASSWORD o CONTACT_EMAIL.")
        return jsonify(success=False, message="El formulario no está disponible por el momento."), 503

    correo = EmailMessage()
    correo["From"] = remitente
    correo["To"] = destinatario
    correo["Reply-To"] = email
    correo["Subject"] = f"Nuevo mensaje de contacto de {nombre}"
    correo.set_content(f"Nombre: {nombre}\nCorreo: {email}\n\nMensaje:\n{mensaje}")

    try:
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=15) as servidor:
            servidor.starttls()
            servidor.login(remitente, contrasena)
            servidor.send_message(correo)
    except (OSError, smtplib.SMTPException):
        app.logger.exception("No se pudo enviar el mensaje del formulario.")
        return jsonify(success=False, message="Hubo un problema al enviar el correo. Inténtalo más tarde."), 500

    return jsonify(success=True, message=f"¡Gracias, {nombre}! Tu mensaje fue recibido. Te contactaremos pronto.")


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG") == "1")
