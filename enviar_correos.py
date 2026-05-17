import os
import re
import pandas as pd
import smtplib
from email.message import EmailMessage

# ==================== CONFIGURACIÓN ====================
GMAIL_USER = 'comsoc.pucp@ieee.org'  
GMAIL_PASS = 'AQUI_TU_CLAVE_DE_16_LETRAS_SIN_ESPACIOS'  # Reemplaza con la clave generada
ARCHIVO_EXCEL = 'lista_completa_ponentes_teleweek.xlsx'
CARPETA_PDFS = 'Certificados_TeleWeek'
PREFIJO_PDF = "Certificado de Reconocimiento Ponente - "
# =======================================================

def enviar_correos():
    try:
        # Leer el archivo Excel
        df = pd.read_excel(ARCHIVO_EXCEL)
        
        # Verificar que la columna de correos exista (ignorando mayúsculas/minúsculas)
        columna_correo = next((col for col in df.columns if col.lower().strip() == 'correos' or col.lower().strip() == 'correo'), None)
        if not columna_correo:
            print("❌ ERROR: No se encontró una columna llamada 'correos' en el Excel.")
            return

        # Buscar la columna de nombres (como en el script anterior)
        posibles_nombres = ['Nombres', 'Nombre', 'Ponente', 'Nombre y Apellidos']
        columna_nombre = next((col for col in df.columns if str(col).strip() in posibles_nombres), df.columns[0])

    except Exception as e:
        print(f"❌ Error al leer el Excel: {e}")
        return

    try:
        # Conexión a Gmail
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(GMAIL_USER, GMAIL_PASS)
        print("\n✅ Conexión exitosa al servidor de Gmail. Iniciando envíos...\n")

        for index, row in df.iterrows():
            email_destinatario = str(row[columna_correo]).strip()
            nombre_completo = str(row[columna_nombre]).strip()
            
            # Validar que haya un correo (ignorar filas vacías o con "nan")
            if email_destinatario.lower() == 'nan' or not email_destinatario:
                print(f"⚠️ Omitiendo a {nombre_completo} (No tiene correo registrado)")
                continue
            
            # Extraer primer nombre para el saludo
            primer_nombre = nombre_completo.split()[0]
            
            # Limpiar el nombre exactamente como lo hicimos al crear los PDFs
            nombre_limpio = re.sub(r'[\\/*?:"<>|]', "", nombre_completo)
            
            # Nombre del PDF esperado
            nombre_archivo = f"{PREFIJO_PDF}{nombre_limpio}.pdf"
            ruta_archivo = os.path.join(CARPETA_PDFS, nombre_archivo)

            # VERIFICACIÓN: Comprobar que exista el PDF
            if os.path.exists(ruta_archivo):
                # Crear el correo
                msg = EmailMessage()
                msg['Subject'] = 'Certificado de Ponente - TeleWeek 2026'
                msg['From'] = GMAIL_USER
                msg['To'] = email_destinatario
                
                # Cuerpo del correo actualizado para la TeleWeek
                cuerpo = f"""Hola {primer_nombre},

Muchas gracias por tu valiosa participación como ponente en la TeleWeek 2026. Ha sido un honor contar con tu experiencia para enriquecer los conocimientos de nuestra comunidad.

Adjuntamos a este correo tu certificado de reconocimiento oficial.

Te invitamos a seguir atentos a nuestras redes sociales y canales de difusión para futuras iniciativas.

¡Sigue a la Familia ComSoc PUCP🩵!"""
                msg.set_content(cuerpo)

                # Adjuntar el PDF
                with open(ruta_archivo, 'rb') as f:
                    file_data = f.read()
                    msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=nombre_archivo)

                # Enviar el mensaje
                server.send_message(msg)
                print(f"📨 Enviado correctamente a: {nombre_completo} ({email_destinatario})")
            else:
                print(f"❌ ERROR: Se omitió a {nombre_completo}. No se encontró su PDF: '{nombre_archivo}'")

        server.quit()
        print("\n🚀 ¡Todos los correos han sido procesados y enviados exitosamente!")

    except smtplib.SMTPAuthenticationError:
        print("❌ Error de autenticación: Verifica que la Contraseña de Aplicación sea correcta.")
    except Exception as e:
        print(f"❌ Ocurrió un error general: {e}")

# Ejecutar el script
if __name__ == "__main__":
    enviar_correos()
