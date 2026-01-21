import requests
import pandas as pd
import json

# URL directa del listado de iniciativas de Los Lagos
URL = "http://www.chileindica.cl/loslagos/modulos/transparencia/listado_iniciativas.php"

def extraer_datos():
    print("Conectando a ChileIndica Los Lagos...")
    
    # Configuramos un 'User-Agent' para evitar bloqueos del servidor
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        # 1. Descargamos el contenido de la página
        respuesta = requests.get(URL, headers=headers)
        respuesta.encoding = 'utf-8' # Aseguramos que se lean bien los tildes

        # 2. Buscamos las tablas en el HTML
        # Buscamos tablas que tengan la palabra 'Iniciativa' para no equivocarnos
        tablas = pd.read_html(respuesta.text, header=0)
        
        if not tablas:
            print("No se encontraron tablas en la página.")
            return

        # Generalmente, la tabla de datos es la más grande o la primera
        df = tablas[0]

        # 3. Limpieza básica (Eliminar filas vacías si existen)
        df = df.dropna(how='all')

        # 4. Convertir a JSON
        # 'orient=records' crea una lista de objetos: [{columna: valor}, {columna: valor}]
        resultado = df.to_dict(orient='records')

        with open('datos.json', 'w', encoding='utf-8') as f:
            json.dump(resultado, f, ensure_ascii=False, indent=4)
            
        print(f"¡Éxito! Se han extraído {len(df)} registros y guardado en datos.json.")

    except Exception as e:
        print(f"Error durante la extracción: {e}")

if __name__ == "__main__":
    extraer_datos()
