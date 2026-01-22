import requests
from bs4 import BeautifulSoup
import json
import re

# Ruta que detectamos en tus capturas de pantalla
URL_INICIO = "http://www.chileindica.cl/loslagos/inversiones/menu_principal_ejecucion.php"

def extraer_datos():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        print("Accediendo directamente al Módulo de Seguimiento...")
        # Usamos una sesión para mantener la conexión activa
        session = requests.Session()
        response = session.get(URL_INICIO, headers=headers, timeout=30, verify=False)
        response.encoding = 'utf-8'
        
        # El sitio usa un sistema de frames o tablas dinámicas
        # Buscamos todas las tablas en el contenido recibido
        soup = BeautifulSoup(response.text, 'html.parser')
        tablas = soup.find_all('table')
        
        print(f"Se encontraron {len(tablas)} tablas. Analizando contenido...")
        
        datos_finales = []
        
        # Buscamos la tabla que tenga la palabra 'Iniciativa' o más de 10 columnas
        for tabla in tablas:
            filas = tabla.find_all('tr')
            for fila in filas:
                celdas = fila.find_all('td')
                # Según tu captura image_668112.png, la tabla es muy ancha (muchas columnas)
                if len(celdas) >= 10:
                    limpio = [c.get_text(strip=True) for c in celdas]
                    
                    # Validamos que sea una fila de datos (el código suele ser el segundo campo)
                    if limpio[1].isdigit():
                        datos_finales.append({
                            "Codigo": limpio[1],
                            "Iniciativa": limpio[2],
                            "Etapa": limpio[5],
                            "Unidad_Tecnica": limpio[10],
                            "Costo_Total": limpio[11],
                            "Saldo_Anio_Siguiente": limpio[16] if len(limpio) > 16 else "0"
                        })

        if datos_finales:
            with open('datos.json', 'w', encoding='utf-8') as f:
                json.dump(datos_finales, f, ensure_ascii=False, indent=4)
            print(f"✅ ¡ÉXITO! Se capturaron {len(datos_finales)} iniciativas del panel regional.")
        else:
            print("❌ No se pudieron validar los datos en las tablas encontradas.")
            # Si falla, imprimimos un trozo del código para diagnosticar
            print("Muestra del HTML recibido:", response.text[:500])
            exit(1)

    except Exception as e:
        print(f"❌ Error técnico: {str(e)}")
        exit(1)

if __name__ == "__main__":
    extraer_datos()
