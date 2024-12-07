from funciones import conexion, obtener_urls_productos, obtener_informacion_producto, LimpiadorDatos
import pandas as pd
import time


def ejecutar():
    productos_lista = []
    url_base = "https://www.cyberpuerta.mx/Computadoras/PC-s-de-Escritorio/"
    navegador = conexion(url_base)

    try:
        for pagina in range(1, 20):
            navegador.get(f"{url_base}?page={pagina}")
            urls_productos = obtener_urls_productos(navegador)
            for url in urls_productos:
                producto_info = obtener_informacion_producto(navegador, url)
                if producto_info:
                    productos_lista.append(producto_info)
            time.sleep(3)

        df = pd.DataFrame(productos_lista)
        df.to_csv("Datasets/cyberpuerta_crudo.csv", index=False, encoding='utf-8')
        print("Archivo crudo guardado en 'Datasets/cyberpuerta_crudo.csv'.")

        # Limpiar datos
        limpiador = LimpiadorDatos(df)
        df_limpio = limpiador.limpiar()

        # Guardar datos limpios
        df_limpio.to_csv("Datasets/cyberpuerta_limpio.csv", index=False, encoding='utf-8')
        print("Archivo limpio guardado en 'Datasets/cyberpuerta_limpio.csv'.")

    except Exception as e:
        print(f"Error en el proceso: {e}")
    finally:
        navegador.quit()


if __name__ == "__main__":
    ejecutar()