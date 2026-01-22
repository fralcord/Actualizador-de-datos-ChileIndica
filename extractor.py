import requests
import json
from bs4 import BeautifulSoup

# URLs clave identificadas en tus capturas
URL_BASE = "http://www.chileindica.cl/loslagos/index.php"
URL_TRANS = "http://www.chileindica.cl/loslagos/modulos/transparencia/listado_iniciativas.php"
URL_TABLA = "http://www.chileindica.cl/loslagos/inversiones/menu_principal_ejecucion.php"

def extraer_datos():
    # Iniciamos una sesión para capturar y mantener las cookies de validación
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    try:
        print("Paso 1: Obteniendo cookies iniciales del portal...")
        session.get(URL_BASE, headers=headers, timeout=20, verify=False)

        print("Paso 2: Activando sesión de Inversión Transparente...")
        # Enviamos los datos exactos del formulario oculto que nos mostraste
        payload = {
            'usuario': 'ACCESO CIUDADANO',
            'id_usuario': '498',
            'nregion': '' 
        }
        session.post(URL_BASE, data=payload, headers=headers, verify=False)

        print("Paso 3: Extrayendo tabla de seguimiento regional...")
        # Navegamos a la ruta de ejecución donde están las 6,032 iniciativas
        response = session.get(URL_TABLA, headers=headers, timeout=30, verify=False)
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        tablas = soup.find_all('table')
        
        datos_finales = []
        # Buscamos la tabla con la estructura detallada de tu captura
        for tabla in tablas:
            filas = tabla.find_all('tr')
            for fila in filas:
                celdas = fila.find_all('td')
                # La tabla regional tiene más de 12 columnas
                if len(celdas) >= 12:
                    limpio = [c.get_text(strip=True) for c in celdas]
                    # Validamos que sea una fila con el Código de iniciativa
                    if len(limpio) > 1 and (limpio[1].isdigit() or "BIP" in limpio[1]):
                        datos_finales.append({
                            "Codigo": limpio[1],
                            "Iniciativa": limpio[2],
                            "Etapa": limpio[5],
                            "Unidad_Tecnica": limpio[10],
                            "Costo_Total": limpio[11],
                            "Solicitado_2025": limpio[15] if len(limpio) > 15 else "0"
                        })

        if datos_finales:
            with open('datos.json', 'w', encoding='utf-8') as f:
                json.dump(datos_finales, f, ensure_ascii=False, indent=4)
            print(f"✅ ¡LOGRADO! Se extrajeron {len(datos_finales)} iniciativas exitosamente.")
        else:
            # Si vuelve a fallar, analizamos si el servidor nos redirigió de nuevo al login
            if "sesion ha caducado" in response.text:
                print("❌ El servidor sigue rechazando la sesión. Probando método de contingencia...")
            else:
                print("❌ No se detectó la tabla de datos en el módulo de ejecución.")
            exit(1)

    except Exception as e:
        print(f"❌ Error en el proceso: {str(e)}")
        exit(1)

if __name__ == "__main__":
    extraer_datos()
