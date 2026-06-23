import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Extraemos las credenciales de forma segura desde las variables de entorno de GitHub
USUARIO = os.environ.get("CHILEINDICA_USER")
CLAVE = os.environ.get("CHILEINDICA_PASS")
URL_LOGIN = "http://www.chileindica.cl" 

def descargar_reporte():
    print("Iniciando proceso de descarga en los servidores de GitHub...")
    
    # Configuraciones obligatorias para que Selenium corra en la nube sin interfaz gráfica
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') 
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # Decimosle a Chrome que descargue el archivo en la misma carpeta del proyecto
    directorio_actual = os.getcwd()
    prefs = {"download.default_directory": directorio_actual}
    options.add_experimental_option("prefs", prefs)
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(10)
    
    try:
        driver.get(URL_LOGIN)
        
        # Login (Recuerda ajustar los selectores By.NAME o By.ID según la página real)
        campo_usuario = driver.find_element(By.NAME, "input_user_id")
        campo_usuario.send_keys(USUARIO)
        
        campo_clave = driver.find_element(By.NAME, "input_password_id")
        campo_clave.send_keys(CLAVE)
        
        boton_login = driver.find_element(By.ID, "boton_ingresar_id")
        boton_login.click()
        
        print("Inicio de sesión exitoso.")
        time.sleep(5) 
        
        # Clic en el reporte
        boton_reporte = driver.find_element(By.LINK_TEXT, "Descargar Reporte Ejecución")
        boton_reporte.click()
        
        print("Descargando archivo en el repositorio...")
        time.sleep(20) # Damos tiempo para que se complete la descarga en la nube
        print("¡Descarga finalizada con éxito!")
        
    except Exception as e:
        print(f"Error en la automatización: {e}")
        raise e # Forzamos el error para que GitHub nos avise si algo falla
    finally:
        driver.quit()

if __name__ == "__main__":
    descargar_reporte()
