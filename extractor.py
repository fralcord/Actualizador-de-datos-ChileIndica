import requests
import json
from bs4 import BeautifulSoup

# URLs clave identificadas
URL_RAIZ = "http://www.chileindica.cl/loslagos/index.php"
URL_TABLA = "http://www.chileindica.cl/loslagos/inversiones/menu_principal_ejecucion.php"

def extraer_datos():
    # Creamos una sesión para mantener las cookies de validación entre pasos
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Referer': URL_RAIZ
    }

    try:
        print("Paso 1: Obteniendo cookies de sesión iniciales...")
        session.get(URL_RAIZ, headers=headers, timeout=20, verify=False)

        print("Paso 2: Activando Acceso Ciudadano (Inversión Transparente)...")
        # Datos del formulario oculto
        payload = {
            'usuario': 'ACCESO CIUDADANO',
            'id_usuario': '498',
            'nregion': '' 
        }
        # Enviamos el POST a la raíz como lo hace el formulario
        session.post(URL_RAIZ, data=payload, headers=headers, verify=False)

        print("Paso 3: Extrayendo tabla regional...")
        # Navegamos al módulo de seguimiento
        response = session.get(URL_TABLA, headers=headers, timeout=30, verify=False)
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        tablas = soup.find_all('table')
        
        datos_finales = []
        for tabla in tablas:
            filas = tabla.find_all('tr')
            for fila in filas:
                celdas = fila.find_all('td')
                # La tabla regional tiene una estructura amplia
                if len(celdas) >= 12:
                    limpio = [c.get_text(strip=True) for c in celdas]
                    # Validamos por el Código de iniciativa
                    if len(limpio) > 1 and limpio[1].isdigit():
                        datos_finales.append({
                            "Codigo": limpio[1],
                            "Iniciativa": limpio[2],
                            "Etapa": limpio[5],
                            "Costo_Total": limpio[11],
                            "Solicitado_2025": limpio[15] if len(limpio) > 15 else "0"
                        })

        if datos_finales:
            with open('datos.json', 'w', encoding='utf-8') as f:
                json.dump(datos_finales, f, ensure_ascii=False, indent=4)
            print(f"✅ ¡ÉXITO! Se capturaron {len(datos_finales)} iniciativas.")
        else:
            print("❌ El servidor no entregó la tabla de datos.")
            # Si falla, revisamos si el HTML contiene el error de sesión
            if "sesion ha caducado" in response.text:
                 print("Diagnóstico: El servidor sigue pidiendo re-ingreso.")
            exit(1)

    except Exception as e:
        print(f"❌ Error técnico: {str(e)}")
        exit(1)

if __name__ == "__main__":
    extraer_datos()
