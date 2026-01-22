import requests
import pandas as pd
import json
from io import StringIO

# URL de Inversión Transparente Los Lagos
URL = "http://www.chileindica.cl/loslagos/modulos/transparencia/listado_iniciativas.php"

def extraer_datos():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
    }

    try:
        print("Intentando conectar con ChileIndica...")
        # verify=False ayuda si el sitio tiene problemas de certificados SSL
        response = requests.get(URL, headers=headers, timeout=60, verify=False)
        response.encoding = 'utf-8'
        
        print("Pagina recibida. Buscando tablas...")
        html_content = StringIO(response.text)
        
        # Leemos las tablas. Usamos 'html5lib' que es más tolerante a errores de diseño web
        tablas = pd.read_html(html_content, flavor='html5lib')
        
        if len(tablas) > 0:
            # Seleccionamos la tabla que contiene los datos (usualmente la que tiene más filas)
            df = max(tablas, key=len)
            
            # Limpiamos los nombres de las columnas
            df.columns = [str(c).strip() for c in df.columns]
            
            # Convertimos a formato JSON
            resultado = df.to_dict(orient='records')
            
            with open('datos.json', 'w', encoding='utf-8') as f:
                json.dump(resultado, f, ensure_ascii=False, indent=4)
            
            print(f"¡LOGRADO! Se extrajeron {len(df)} iniciativas.")
        else:
            print("No se encontraron tablas de datos en el sitio.")
            
    except Exception as e:
        print(f"Error encontrado: {str(e)}")
        raise e 

if __name__ == "__main__":
    extraer_datos()
