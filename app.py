from flask import Flask, render_template, request, jsonify
import datetime
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/contacto", methods=["POST"])
def contacto():
    data = request.get_json()

    nombre = data.get("nombre", "").strip()
    email = data.get("email", "").strip()
    mensaje = data.get("mensaje", "").strip()

    # Validación 1: Campos vacíos
    if not nombre or not email or not mensaje:
        return jsonify({
            "success": False,
            "message": "Por favor completa todos los campos del formulario."
        }), 400

    # Validación 2: Formato de correo electrónico válido
    patron_email = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(patron_email, email):
        return jsonify({
            "success": False,
            "message": "Por favor ingresa un correo electrónico válido (ejemplo: correo@dominio.com)."
        }), 400

    # Validación 3: Límite de 120 caracteres para el mensaje
    if len(mensaje) > 120:
        return jsonify({
            "success": False,
            "message": f"El mensaje es muy largo ({len(mensaje)}/120 caracteres permitidos)."
        }), 400

    # ====================================================
    # Enviar correos
    # ====================================================
    remitente_correo = "sebas13montero@gmail.com"  
    contrasena_app = "wmwslqtqzsdqrgnv"   
    destinatario_correo = "fysolutionsas@gmail.com" 

    try:
        msg = MIMEMultipart()
        msg['From'] = remitente_correo
        msg['To'] = destinatario_correo
        msg['Subject'] = f"Nuevo mensaje de contacto de: {nombre}"

        cuerpo_mensaje = f"Nombre: {nombre}\nCorreo del cliente: {email}\nMensaje:\n{mensaje}"
        msg.attach(MIMEText(cuerpo_mensaje, 'plain'))

        # Nos conectamos al servidor de Google para enviarlo
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(remitente_correo, contrasena_app)
        server.sendmail(remitente_correo, destinatario_correo, msg.as_string())
        server.quit()
        
        print("¡Correo enviado con éxito!")

    except Exception as e:
        print(f"Error al enviar el correo: {e}")
        return jsonify({
            "success": False,
            "message": "Hubo un problema al enviar el correo. Inténtalo más tarde."
        }), 500
    # ====================================================

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("\n" + "="*50)
    print(f"  NUEVO MENSAJE DE CONTACTO — {timestamp}")
    print("="*50)
    print(f"  Nombre:  {nombre}")
    print(f"  Email:   {email}")
    print(f"  Mensaje: {mensaje}")
    print("="*50 + "\n")

    return jsonify({
        "success": True,
        "message": f"¡Gracias, {nombre}! Tu mensaje fue recibido. Te contactaremos pronto."
    })


if __name__ == "__main__":
    app.run(debug=True)