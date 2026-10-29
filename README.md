# F&Y Solutions

Sitio web de F&Y Solutions hecho con Flask, HTML y CSS. La página incluye información de servicios y un formulario que envía consultas por correo.

## Requisitos

- Python 3.10 o posterior
- Una cuenta de correo configurada para enviar por SMTP. Si usas Gmail, utiliza una contraseña de aplicación nueva.

## Instalación

Desde esta carpeta, crea un entorno e instala las dependencias:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Configura estas variables de entorno antes de iniciar la aplicación:

```powershell
$env:SMTP_USER = "tu_correo_de_envio@gmail.com"
$env:SMTP_PASSWORD = "tu_nueva_contrasena_de_aplicacion"
$env:CONTACT_EMAIL = "correo_que_recibira_los_mensajes@example.com"
```

Luego inicia el servidor:

```powershell
python app.py
```

Abre `http://127.0.0.1:5000` en el navegador. El formulario necesita que las variables SMTP estén configuradas; sin ellas, la página sigue cargando, pero el envío de mensajes queda desactivado.

## Seguridad

- Nunca guardes contraseñas, tokens ni claves dentro del código o del repositorio.
- Si una contraseña se compartió o se publicó, revócala y crea una nueva.
- `FLASK_DEBUG` debe permanecer desactivado fuera del entorno local.
- El formulario valida los datos en el servidor y limita el mensaje a 350 caracteres.
