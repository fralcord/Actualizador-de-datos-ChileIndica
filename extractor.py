import requests
import json
from bs4 import BeautifulSoup

# URL del formulario que procesa el acceso ciudadano
URL_PROCESA = "http://www.chileindica.cl/loslagos/index.php"
# URL final donde está la tabla de seguimiento
URL_TABLA = "http://www.chileindica.cl/loslagos/inversiones/menu_principal_ejecucion.php"

def extraer_datos():
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    try:
        print("Enviando credenciales de Acceso Ciudadano...")
        # Estos son los datos capturados del código fuente de la página
        payload = {
            'usuario': 'ACCESO CIUDADANO',
            'id_usuario': '498',
            'nregion': '10'  # Región de Los Lagos
        }
        
        # 1. Activamos la sesión enviando el formulario
        session.post(URL_PROCESA, data=payload, headers=headers, verify=False)
        
        # 2. Consultamos la tabla de seguimiento detallada
        print("Accediendo al Módulo de Seguimiento Regional...")
        response = session.get(URL_TABLA, headers=headers, verify=False)
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        tablas = soup.find_all('table')
        
        datos_finales = []
        for tabla in tablas:
            filas = tabla.find_all('tr')
            for fila in filas:
                celdas = fila.find_all('td')
                # Buscamos la estructura de la tabla de seguimiento
                if len(celdas) >= 12:
                    limpio = [c.get_text(strip=True) for c in celdas]
                    # Validamos que el segundo campo sea el código de iniciativa
                    if len(limpio) > 1 and limpio[1].isdigit():
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
            print(f"✅ ¡ÉXITO! Se capturaron {len(datos_finales)} iniciativas.")
        else:
            print("❌ El servidor no entregó los datos. Verificando respuesta...")
            exit(1)

    except Exception as e:
        print(f"❌ Error técnico: {str(e)}")
        exit(1)

if __name__ == "__main__":
    extraer_datos()
