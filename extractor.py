import requests
import pandas as pd
import json
from io import StringIO

# URL directa de Los Lagos
URL = "http://www.chileindica.cl/loslagos/modulos/transparencia/listado_iniciativas.php"

def extraer_datos():
    # Simulamos ser un navegador muy común para evitar bloqueos
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/119.0.0.0 Safari/537.36'
    }

    try:
        print("Conectando con el servidor de ChileIndica...")
        # Desactivamos la verificación SSL por si el sitio tiene certificados vencidos
        response = requests.get(URL, headers=headers, timeout=30, verify=False)
        response.encoding = 'utf-8'
        
        print("Analizando el contenido de la tabla...")
        # Usamos un lector de HTML más básico pero compatible
        tablas = pd.read_html(StringIO(response.text))
        
        if tablas:
            # Seleccionamos la tabla con más datos
            df = max(tablas, key=len)
            
            # Limpiamos los nombres de las columnas para el JSON
            df.columns = [str(c).replace('.', '').strip() for c in df.columns]
            
            # Convertimos a JSON
            datos_finales = df.to_dict(orient='records')
            
            with open('datos.json', 'w', encoding='utf-8') as f:
                json.dump(datos_finales, f, ensure_ascii=False, indent=4)
            
            print(f"✅ ¡Éxito total! Se han guardado {len(df)} registros.")
        else:
            print("❌ No se encontró ninguna tabla en la página.")

    except Exception as e:
        print(f"❌ Error detectado: {str(e)}")
        # Forzamos que el error sea visible en GitHub Actions
        exit(1)

if __name__ == "__main__":
    extraer_datos()
