import requests
import json
from bs4 import BeautifulSoup

# URL que genera el acceso transparente
URL_ACCESO = "http://www.chileindica.cl/loslagos/modulos/transparencia/listado_iniciativas.php"
# URL de la tabla detallada que vimos en tus fotos
URL_TABLA = "http://www.chileindica.cl/loslagos/inversiones/menu_principal_ejecucion.php"

def extraer_datos():
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        print("Solicitando Acceso Ciudadano (Inversión Transparente)...")
        # 1. Entramos a la página de transparencia para activar la sesión
        acceso_res = session.get(URL_ACCESO, headers=headers, verify=False)
        
        # 2. Con la sesión activa, vamos directamente a la tabla regional
        print("Accediendo al Módulo de Seguimiento con sesión activa...")
        response = session.get(URL_TABLA, headers=headers, verify=False)
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        # Buscamos la tabla grande (la que tiene los 6,032 registros en tus capturas)
        tablas = soup.find_all('table')
        
        datos_finales = []
        for tabla in tablas:
            filas = tabla.find_all('tr')
            for fila in filas:
                celdas = fila.find_all('td')
                # Buscamos la estructura de columnas de tu imagen 668112
                if len(celdas) >= 12:
                    limpio = [c.get_text(strip=True) for c in celdas]
                    # Validamos que la segunda celda sea un código numérico
                    if len(limpio) > 1 and limpio[1].isdigit():
                        datos_finales.append({
                            "Codigo": limpio[1],
                            "Iniciativa": limpio[2],
                            "Etapa": limpio[5],
                            "Unidad_Tecnica": limpio[10],
                            "Costo_Total": limpio[11],
                            "Saldo_Anio_Sig": limpio[16] if len(limpio) > 16 else "0"
                        })

        if datos_finales:
            with open('datos.json', 'w', encoding='utf-8') as f:
                json.dump(datos_finales, f, ensure_ascii=False, indent=4)
            print(f"✅ ¡LOGRADO! Se extrajeron {len(datos_finales)} iniciativas exitosamente.")
        else:
            print("❌ No se encontraron datos. El servidor no entregó la tabla detallada.")
            # Imprimimos los primeros 300 caracteres para ver qué respondió el sitio
            print("Respuesta del servidor:", response.text[:300])
            exit(1)

    except Exception as e:
        print(f"❌ Error técnico: {str(e)}")
        exit(1)

if __name__ == "__main__":
    extraer_datos()
