import os        # Para trabajar con carpetas y archivos en la computadora
import re        # Para buscar texto dentro de los PDFs con patrones
import fitz      # Librería PyMuPDF, sirve para abrir y leer PDFs
import pandas as pd  # Librería para organizar datos como una tabla

# 🔧 1. Define la carpeta donde están los PDFs
carpeta_pdfs = r"C:\Users\pinguinosos\Documents\Boletas"
datos_extraidos = []  # Aquí se guardarán los datos de cada boleta

# 📌 2. Lista de conceptos a buscar y su formato en el PDF
conceptos = {
    "ISR": r"ISR\s+\$ ?(-?\d+\.\d+)",  # Busca la línea con "ISR $123.45"
    "ISSS": r"ISSS\s+\$ ?(-?\d+\.\d+)",
    "AFP CONFIA": r"AFP CONFIA\s+\$ ?(-?\d+\.\d+)",
    "BANCO": r"BANCO\s+\$ ?(-?\d+\.\d+)",
    "FUNTER": r"FUNTER\s+\$ ?(-?\d+\.\d+)",
    "Liquido a recibir": r"Liquido\s+a\s+recibir\s*:\s*\$ ?(-?\d+\.\d+)",
    
}

# 🗂️ 3. Busca cada archivo PDF en la carpeta
print(f"📁 Buscando PDFs en: {carpeta_pdfs}")
for archivo in os.listdir(carpeta_pdfs):
    if archivo.lower().endswith(".pdf"):
        ruta_pdf = os.path.join(carpeta_pdfs, archivo)
        print(f"🔍 Procesando: {archivo}")
        try:
            # 📖 Abre y extrae el texto de cada página del PDF
            doc = fitz.open(ruta_pdf)
            texto = ""
            for pagina in doc:
                texto += pagina.get_text()  # Une todo el texto del PDF
            doc.close()

            if not texto.strip():
                print(f"⚠️ No se pudo extraer texto de: {archivo}")
                continue

            # 📊 Extrae los valores definidos en los conceptos
            fila = {"Archivo": archivo}  # Guarda el nombre del archivo
            for clave, patron in conceptos.items():
                match = re.search(patron, texto, re.IGNORECASE | re.MULTILINE)
                fila[clave] = float(match.group(1)) if match else None
                print(f"   ➤ {clave}: {fila[clave]}")

            datos_extraidos.append(fila)  # Agrega los datos al resumen
        except Exception as e:
            print(f"❌ Error al procesar {archivo}: {e}")

# 📤 4. Guarda todo en un archivo Excel
if datos_extraidos:
    df = pd.DataFrame(datos_extraidos)  # Convierte los datos a tabla
    salida_excel = os.path.join(carpeta_pdfs, "resumen_boletas.xlsx")
    df.to_excel(salida_excel, index=False)
    print(f"\n✅ Archivo Excel guardado en: {salida_excel}")
else:
    print("⚠️ No se extrajo información de ningún PDF.")
    
    
    
    
    # Samael Bautista 2025* https://www.linkedin.com/in/sambautistam/
    # El conocimiento se usa para la mejora continua, inluso de la calidad de vida, no para dañar.