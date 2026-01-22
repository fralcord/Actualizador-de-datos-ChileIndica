import requests
from bs4 import BeautifulSoup
import json
import re

# Ruta principal basada en tus capturas
URL_BASE = "http://www.chileindica.cl/loslagos/"
URL_TRANSPARENCIA = URL_BASE + "modulos/transparencia/listado_iniciativas.php"

def extraer_datos():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        print("Iniciando ruta de Transparencia ChileIndica...")
        response = requests.get(URL_TRANSPARENCIA, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Buscamos la tabla principal de iniciativas
        tabla = soup.find('table')
        if not tabla:
            print("No se encontró la tabla en la ruta de Transparencia.")
            exit(1)

        filas = tabla.find_all('tr')
        datos_finales = []

        print(f"Analizando {len(filas)} filas encontradas...")

        for fila in filas:
            celdas = fila.find_all('td')
            # Filtramos celdas que tengan la estructura de la tabla de seguimiento
            if len(celdas) >= 5:
                texto_celdas = [c.get_text(strip=True) for c in celdas]
                
                # Evitamos los encabezados
                if "Código" not in texto_celdas[0] and texto_celdas[0].isdigit():
                    datos_finales.append({
                        "Codigo": texto_celdas[0],
                        "Iniciativa": texto_celdas[1],
                        "Etapa": texto_celdas[4] if len(texto_celdas) > 4 else "N/A",
                        "Institucion": texto_celdas[2],
                        "Monto": texto_celdas[3]
                    })

        if datos_finales:
            with open('datos.json', 'w', encoding='utf-8') as f:
                json.dump(datos_finales, f, ensure_ascii=False, indent=4)
            print(f"✅ ¡Automatización completa! {len(datos_finales)} iniciativas procesadas.")
        else:
            print("❌ No se pudieron procesar las iniciativas. Verificando estructura...")
            exit(1)

    except Exception as e:
        print(f"❌ Error en la ruta: {str(e)}")
        exit(1)

if __name__ == "__main__":
    extraer_datos()
