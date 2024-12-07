import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def conexion(url):
    driver = ChromeDriverManager().install()
    s = Service(driver)
    opc = Options()
    opc.add_argument("--start-maximized")
    navegador = webdriver.Chrome(service=s, options=opc)
    navegador.get(url)
    return navegador


def obtener_informacion_producto(navegador, url):
    navegador.get(url)
    time.sleep(2)

    try:
        mensaje_error = navegador.find_elements(By.XPATH, "//div[contains(text(), 'Al parecer abriste una puerta equivocada')]")
        if mensaje_error:
            print(f"Página con error, saltando URL: {url}")
            return None

        nombre_elemento = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1.detailsInfo_right_title"))
        )
        nombre = nombre_elemento.text.strip()

        precio_elemento = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.priceText"))
        )
        precio = precio_elemento.text.strip()

        stock_elemento = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.stockFlag span"))
        )
        stock = stock_elemento.text.strip()

        return {"Nombre_completo": nombre, "Precio": precio, "Stock": stock}

    except Exception as e:
        print(f"Error al obtener los datos del producto: {e}")
        return None


def obtener_urls_productos(navegador):
    urls = set()
    productos = navegador.find_elements(By.CSS_SELECTOR, "a.emproduct_right_title")
    for producto in productos:
        url = producto.get_attribute("href")
        urls.add(url)
    return list(urls)


class LimpiadorDatos:
    def __init__(self, df):
        self.df = df

    # Función para extraer la GPU
    def extraer_gpu(self, nombre):
        nvidia_match = re.search(r'NVIDIA\s([A-Za-z0-9\s]+)', nombre)
        amd_match = re.search(r'AMD\s(Radeon\s[A-Za-z0-9\s]+)', nombre)

        if nvidia_match:
            return f'NVIDIA {nvidia_match.group(1).strip()}'
        elif amd_match:
            return f'AMD {amd_match.group(1).strip()}'
        return "N/A"

    # Función para extraer la RAM
    def extraer_ram(self, nombre):
        # Buscamos el valor de RAM en GB
        ram_match = re.search(r'(\d+GB)', nombre)

        if ram_match:
            ram_value = int(ram_match.group(1).replace('GB', ''))  # Convertir el valor en GB a entero

            # Solo devolver valores menores a 128GB
            if ram_value < 128:
                return ram_match.group(1)
            else:
                return "N/A"  # O cualquier otro valor que prefieras
        return "N/A"  # Si no se encuentra ninguna RAM, retornar 'N/A'

    def extraer_rom(self, nombre):
        # Buscamos tanto el SSD como HDD y el tamaño
        rom_match = re.search(r'(\d+TB|\d+GB)\s*(SSD|HDD)', nombre)
        if rom_match:
            return rom_match.group(1) + " " + rom_match.group(2)
        return "N/A"

    def extraer_so(self, nombre):
        so_match = re.search(r'(Windows\s[\w\s]+)', nombre)
        if so_match:
            return so_match.group(1).strip()
        return "N/A"

    def extraer_cpu(self, nombre):
        # Buscamos las CPU de tipo Intel o AMD y sus detalles
        cpu_match = re.search(r'(Intel\sCore\s[\w\s-]+|\bAMD\sRyzen\s[\w\s-]+)', nombre)
        if cpu_match:
            return cpu_match.group(0).strip()
        return "N/A"

    def limpiar(self):
        # Crear columnas separadas
        self.df['GPU'] = self.df['Nombre_completo'].apply(self.extraer_gpu)
        self.df['RAM'] = self.df['Nombre_completo'].apply(self.extraer_ram)
        self.df['ROM'] = self.df['Nombre_completo'].apply(self.extraer_rom)
        self.df['SO'] = self.df['Nombre_completo'].apply(self.extraer_so)
        self.df['CPU'] = self.df['Nombre_completo'].apply(self.extraer_cpu)

        self.df['Nombre'] = self.df['Nombre_completo'].str.split(',', n=1).str[0].str.strip()

        self.df['Precio'] = self.df['Precio'].replace({r'\$': '', r',': ''}, regex=True).astype(float)

        # Eliminar columna 'Nombre_completo' ya que ya se separaron las columnas necesarias
        self.df_limpio = self.df.drop(columns=['Nombre_completo'])

        return self.df_limpio
