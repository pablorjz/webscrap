import pandas as pd
import plotly.express as px
from dash import Dash ,dcc , html , input , output
##importar datos
df = pd.read_csv("Datasets/cyberpuerta_limpio.csv")

aplicacion = Dash(__name__)

aplicacion.layout = html.Div([
    html.H1("Analisis de computadoras - cyberpuerta"),

    dcc.dropdown(
        id="desplegable-componente",
        options=[
            {"label":"GPU", "value":"GPU"},
            {"label":"RAM", "value":"RAM"},
            {"label":"CPU", "value":"CPU"},
        ],
        value="GPU",
        placeholder="Selecciona una componente para comparar precios",
    ),
    dcc.Graph(id="comparacion-precios"),

    html.Hr(),

    #PRECIOVSSTOCK
    dcc.Graph(id="precio-stock",figure=px.scatter(
        df,x="stock",y="precio",color="nombre",
        title="relacion precio vs stock",
        template="plotly_dark",
        labels={"stock":"Stock dsiponible","precio":"precio en MXN"}
    )),

    html.Hr(),

    #filtros interactivos
    html.Div([
        html.Label("sistema operativo"),
        dcc.Dropdown(id="filtro-so",options=[{"label":so,"value":so}for so in df["SO"].unique()],multi=True),

        html.Label("GPU"),
        dcc.Dropdown(id="filtro-gpu",options=[{"label":gpu,"value":gpu}for gpu in df["GPU"].unique()],multi=True),


        html.Label("RAM"),
        dcc.Dropdown(id="filtro-ram",options=[{"label":ram,"value":ram}for ram in df["RAM"].unique()],multi=True),
    ]),
    dcc.Graph(id="resultados-filtrados"),
])

@plicacion.callback(
    Output("comparacion-precios", "figure"),
    input("desplegable-componente","value")
)

def actualizar_comparacion_precios(componente_seleccionado):
    if componente_seleccionado:
        figura = px.bar(df,x=componente_seleccionado,y="precio",color="nombre",
                        title=f"comparacion precio por {componente_seleccionado}",
                        template="plotly_dark",)
        return figura


@plicacion.callback(
    Output("resultados-filtrados", "figure"),
    [input("filtro-so","value"),
     input("filtro-gpu","value"),
     input("filtro-ram","value")]
)

def filtrar_computadoras(so_seleccionado,gpu_seleccionado,ram_seleccionado):
    df_filtrado = df.copy()
    if so_seleccionado:
        df_filtrado = df_filtrado[df_filtrado["SO"].isin(so_seleccionado)]
        if gpu_seleccionado:
            df_filtrado = df_filtrado[df_filtrado["GPU"].isin(gpu_seleccionado)]
            if ram_seleccionado:
                df_filtrado = df_filtrado[df_filtrado["RAM"].isin(ram_seleccionado)]


    figura = px.scatter(df_filtrado,x="Nombre",y="Precio",color="SO",
                        title="Computadoras Filtradas por Especificaciones",
                        template="plotly_dark",)
    return figura
if __name__ == '__main__':
    aplicacion.run_server(debug=True)