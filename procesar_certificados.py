import os
import re
import pandas as pd
from pypdf import PdfReader, PdfWriter

# ==================== CONFIGURACIÓN ====================
# 1. Coloca aquí el nombre exacto de tu archivo PDF de 29 páginas
ARCHIVO_PDF_ORIGINAL = "TU_ARCHIVO_DE_CERTIFICADOS.pdf" 

# 2. Nombre exacto del archivo de Excel
ARCHIVO_EXCEL = "lista_completa_ponentes_teleweek.xlsx" 

# 3. Prefijo para el nombre de los nuevos archivos individuales
PREFIJO = "Certificado de Reconocimiento Ponente - "

# 4. Nombre de la nueva carpeta donde se guardarán los PDFs
CARPETA_SALIDA = "Certificados_TeleWeek"
# =======================================================

def separar_y_renombrar_pdfs():
    # Crear la carpeta de salida si no existe
    if not os.path.exists(CARPETA_SALIDA):
        os.makedirs(CARPETA_SALIDA)
        print(f"📁 Se creó la carpeta: '{CARPETA_SALIDA}'")

    # 1. Leer el archivo de Excel
    try:
        df = pd.read_excel(ARCHIVO_EXCEL)
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo de Excel: {ARCHIVO_EXCEL}")
        return
    except Exception as e:
        print(f"❌ Error al leer el archivo Excel: {e}")
        return

    # Buscar automáticamente la columna de nombres
    columna_nombre = None
    posibles_nombres_columna = ['Nombres', 'Nombre', 'Ponente', 'Nombre y Apellidos', 'Completo']
    for col in df.columns:
        if str(col).strip() in posibles_nombres_columna:
            columna_nombre = col
            break
    
    if not columna_nombre:
        columna_nombre = df.columns[0]

    lista_nombres = df[columna_nombre].dropna().astype(str).str.strip().tolist()

    # 2. Leer el PDF completo
    try:
        reader = PdfReader(ARCHIVO_PDF_ORIGINAL)
        total_paginas = len(reader.pages)
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo PDF: {ARCHIVO_PDF_ORIGINAL}")
        return
    except Exception as e:
        print(f"❌ Error al abrir el archivo PDF: {e}")
        return

    print(f"📊 Filas con datos encontradas en Excel: {len(lista_nombres)}")
    print(f"📄 Páginas detectadas en el PDF original: {total_paginas}\n")

    if total_paginas != len(lista_nombres):
        print("⚠️ ¡Alerta! La cantidad de páginas del PDF no coincide con los registros del Excel.")
        continuar = input("¿Deseas continuar con el proceso usando el límite menor? (s/n): ")
        if continuar.lower() != 's':
            print("Proceso cancelado.")
            return

    # 3. Extraer página por página y guardar en la NUEVA CARPETA
    limite_procesamiento = min(total_paginas, len(lista_nombres))
    certificados_creados = 0

    for i in range(limite_procesamiento):
        nombre_ponente = lista_nombres[i]
        nombre_ponente_limpio = re.sub(r'[\\/*?:"<>|]', "", nombre_ponente)
        
        # Construir el nombre del nuevo PDF y su ruta dentro de la carpeta
        nombre_salida_pdf = f"{PREFIJO}{nombre_ponente_limpio}.pdf"
        ruta_completa_salida = os.path.join(CARPETA_SALIDA, nombre_salida_pdf)
        
        try:
            writer = PdfWriter()
            writer.add_page(reader.pages[i])
            
            # Guardar el archivo en la ruta especificada
            with open(ruta_completa_salida, "wb") as archivo_salida:
                writer.write(archivo_salida)
                
            print(f"✅ Guardado: '{nombre_salida_pdf}'")
            certificados_creados += 1
            
        except Exception as e:
            print(f"❌ Error al dividir la página {i+1} ({nombre_ponente}): {e}")

    print(f"\n🚀 ¡Operación terminada! {certificados_creados} PDFs guardados en la carpeta '{CARPETA_SALIDA}'.")

if __name__ == "__main__":
    separar_y_renombrar_pdfs()
