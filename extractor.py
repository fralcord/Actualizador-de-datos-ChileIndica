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

        # Usamos una técnica de "búsqueda de texto" (Regex) para encontrar las filas 
        # Esto es más seguro cuando las tablas HTML son complejas
        print("Buscando datos en el contenido...")
        
        # Este patrón busca el contenido entre las etiquetas <td> de la tabla
        filas = re.findall(r'<tr>(.*?)</tr>', html, re.DOTALL)
        
        if len(filas) > 1:
            datos_finales = []
            # Saltamos la primera fila porque suele ser el encabezado
            for fila in filas[1:]:
                celdas = re.findall(r'<td.*?>(.*?)</td>', fila, re.DOTALL)
                if len(celdas) >= 5:
                    # Limpiamos el texto de etiquetas HTML
                    celdas_limpias = [re.sub(r'<.*?>', '', c).strip() for c in celdas]
                    
                    datos_finales.append({
                        "Codigo": celdas_limpias[0],
                        "Iniciativa": celdas_limpias[1],
                        "Institucion": celdas_limpias[2],
                        "Monto": celdas_limpias[3],
                        "Estado": celdas_limpias[4]
                    })
            
            with open('datos.json', 'w', encoding='utf-8') as f:
                json.dump(datos_finales, f, ensure_ascii=False, indent=4)
            
            print(f"✅ ¡LO LOGRAMOS! Se guardaron {len(datos_finales)} iniciativas.")
        else:
            print("❌ No se detectaron filas de datos.")
            exit(1)

    except Exception as e:
        print(f"❌ Error técnico: {str(e)}")
        exit(1)

if __name__ == "__main__":
    extraer_datos()
