import requests
import json
import re

URL = "http://www.chileindica.cl/loslagos/modulos/transparencia/listado_iniciativas.php"

def extraer_datos():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        print("Conectando con el servidor de ChileIndica...")
        response = requests.get(URL, headers=headers, timeout=30, verify=False)
        response.encoding = 'utf-8'
        html = response.text

        print("Buscando filas de iniciativas...")
        # Buscamos las filas (tr) que contienen celdas (td)
        # Este nuevo patrón es mucho más potente para detectar la tabla real
        filas_raw = re.findall(r'<tr[^>]*>(.*?)</tr>', html, re.DOTALL)
        
        datos_finales = []
        
        for fila in filas_raw:
            # Extraemos el contenido de cada celda (td)
            celdas = re.findall(r'<td[^>]*>(.*?)</td>', fila, re.DOTALL)
            
            # La tabla de ChileIndica suele tener entre 5 y 8 columnas
            if len(celdas) >= 5:
                # Limpiamos etiquetas HTML y espacios en blanco
                limpio = [re.sub(r'<.*?>', '', c).strip() for c in celdas]
                
                # Evitamos los encabezados comparando con el primer campo
                if "Código" not in limpio[0] and "Iniciativa" not in limpio[0]:
                    datos_finales.append({
                        "Codigo": limpio[0],
                        "Iniciativa": limpio[1],
                        "Institucion": limpio[2],
                        "Monto": limpio[3],
                        "Estado": limpio[4]
                    })
        
        if datos_finales:
            with open('datos.json', 'w', encoding='utf-8') as f:
                json.dump(datos_finales, f, ensure_ascii=False, indent=4)
            print(f"✅ ¡ÉXITO! Se han extraído {len(datos_finales)} iniciativas.")
        else:
            print("❌ No se encontraron datos válidos. El sitio podría estar caído o en mantenimiento.")
            exit(1)

    except Exception as e:
        print(f"❌ Error técnico: {str(e)}")
        exit(1)

if __name__ == "__main__":
    extraer_datos()
