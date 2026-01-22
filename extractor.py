import requests
import pandas as pd
import json
from io import StringIO

URL = "http://www.chileindica.cl/loslagos/modulos/transparencia/listado_iniciativas.php"

def extraer_datos():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        print("Solicitando datos a ChileIndica...")
        response = requests.get(URL, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        
        # Usamos StringIO para que pandas no dé advertencias de formato
        html_content = StringIO(response.text)
        
        # Intentamos leer las tablas
        tablas = pd.read_html(html_content)
        
        if len(tablas) > 0:
            # Buscamos la tabla que tenga más filas (esa suele ser la de datos)
            df = max(tablas, key=len)
            
            # Limpiamos nombres de columnas (quitar espacios o caracteres raros)
            df.columns = [str(c).strip() for c in df.columns]
            
            resultado = df.to_dict(orient='records')
            
            with open('datos.json', 'w', encoding='utf-8') as f:
                json.dump(resultado, f, ensure_ascii=False, indent=4)
            
            print(f"¡Éxito! Se guardaron {len(df)} iniciativas.")
        else:
            print("No se encontraron tablas en la página.")
            
    except Exception as e:
        print(f"Error técnico encontrado: {str(e)}")
        # Esto hará que el error sea visible en el log de GitHub
        raise e 

if __name__ == "__main__":
    extraer_datos()
