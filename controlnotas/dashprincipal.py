import pandas as pd
import plotly.express as px
import dash
from dash import html, Input, Output, dcc, dash_table
from database import obtenerestudiantes
from flask import session
import dash.exceptions


def creartablero(server):

    appnotas = dash.Dash(
        __name__,
        server=server,
        url_base_pathname="/dashprincipal/",
        suppress_callback_exceptions=True
    )

    _init = obtenerestudiantes()

    if _init.empty:
        _init = pd.DataFrame(columns=[
            "Id_estudiante",
            "Nombre_estudiante",
            "Edad_estudiante",
            "Carrera_estudiante",
            "Nota1",
            "Nota2",
            "Nota3",
            "Promedio",
            "Desempeño"
        ])

    carreras = _init["Carrera_estudiante"].unique()
    valor_default = carreras[0] if len(carreras) > 0 else None

    edad_min = int(_init["Edad_estudiante"].min()) if not _init.empty else 0
    edad_max = int(_init["Edad_estudiante"].max()) if not _init.empty else 100


    # ===================== Layout =====================
    appnotas.layout = html.Div([

        dcc.Location(id="url", refresh=False),

        # ── Header ──
        html.Div([
            html.Div([
                html.H3("Dashboard", style={"marginRight": "20px", "color": "white"}),
                html.Span(id="usuario_header", style={"fontWeight": "bold", "color": "white"})
            ], style={"display": "flex", "alignItems": "center", "gap": "15px"}),

            html.Div([
                html.A("Registrar Estudiante", href="/registro_estudiante",
                    style={"backgroundColor": "#3498db", "color": "white",
                           "padding": "8px 16px", "textDecoration": "none",
                           "borderRadius": "5px", "marginRight": "10px", "fontWeight": "bold"}),
                html.A("Carga Masiva", href="/carga_masiva",
                    style={"backgroundColor": "orange", "color": "white",
                           "padding": "8px 16px", "textDecoration": "none",
                           "borderRadius": "5px", "marginRight": "10px", "fontWeight": "bold"}),
                html.A("Cerrar Sesión", href="/logout",
                    style={"backgroundColor": "red", "color": "white",
                           "padding": "8px 16px", "textDecoration": "none",
                           "borderRadius": "5px", "fontWeight": "bold"})
            ])
        ], style={
            "display": "flex", "justifyContent": "space-between",
            "alignItems": "center", "padding": "15px 30px",
            "backgroundColor": "#1E1BD2"
        }),

        dcc.Input(
            id="busqueda", type="text", placeholder="Buscar estudiante...",
            style={"marginBottom": "20px", "marginTop": "10px",
                   "padding": "8px", "width": "300px"}
        ),

        

        # ── Filtros ──
        html.Div([
            html.Label("Seleccionar carrera:", style={"fontWeight": "bold"}),
            dcc.Dropdown(
                id="filtro_carrera",
                options=[{"label": ca, "value": ca} for ca in sorted(carreras)],
                value=valor_default
            ),
            html.Br(),
            html.Label("Rango de edad:", style={"fontWeight": "bold"}),
            dcc.RangeSlider(
                id="slider_edad", min=edad_min, max=edad_max, step=1,
                value=[edad_min, edad_max],
                marks={i: str(i) for i in range(edad_min, edad_max + 1, 5)},
                tooltip={"placement": "bottom", "always_visible": True}
            ),
            html.Br(),
            html.Label("Rango promedio:", style={"fontWeight": "bold"}),
            dcc.RangeSlider(
                id="slider_promedio", min=0, max=5, step=0.5, value=[0, 5],
                tooltip={"placement": "bottom", "always_visible": True}
            )
        ], style={
            "width": "80%", "margin": "auto", "padding": "20px",
            "border": "1px solid #ccc", "borderRadius": "10px"
        }),

        html.Br(),

        html.Div(id="kpis", style={"display": "flex", "justifyContent": "space-around"}),

       html.H1("TABLERO AVANZADO", style={
            "textAlign": "center", "backgroundColor": "#73AECAFF",
            "color": "white", "padding": "20px", "borderRadius": "10px"
        }),

        html.Br(),

        dcc.Interval(id="intervalo", interval=10000, n_intervals=0),

        dcc.Loading(
            dash_table.DataTable(
                id="tabla", page_size=8,
                filter_action="native", sort_action="native",
                row_selectable="multi", selected_rows=[],
                style_table={"overflowX": "auto"},
                style_cell={"textAlign": "center", "padding": "10px"},
                style_header={"backgroundColor": "#f2f2f2", "fontWeight": "bold"}
            ),
            type="circle"
        ),

        html.Br(),

        dcc.Loading(dcc.Graph(id="gra_detallado"), type="default"),

        html.Br(),

        dcc.Tabs([
            dcc.Tab(label="Histograma",          children=[dcc.Graph(id="histograma")]),
            dcc.Tab(label="Dispersión",           children=[dcc.Graph(id="dispersion")]),
            dcc.Tab(label="Desempeño",            children=[dcc.Graph(id="pie")]),
            dcc.Tab(label="Promedio por Carrera", children=[dcc.Graph(id="barras")])
        ]),

        html.Br(),

         html.Br(),

          html.Div([
            html.H2("Ranking Académico Top 10", style={
                "textAlign": "center", "color": "#1B7AD2"
            }),
            html.Div(id="ranking_tabla")
        ], style={
            "width": "90%", "margin": "auto", "padding": "20px",
             "borderRadius": "10px",
            "marginBottom": "30px"
        }),

        # ── Punto 6: Alerta de estudiantes en riesgo ──
        html.Div(id="alerta_riesgo", style={"width": "90%", "margin": "auto"}),

        html.Br(),
    ], style={"fontFamily": "Arial"})


    # ===================== RESET FILTROS =====================
    @appnotas.callback(
        Output("filtro_carrera", "value"),
        Output("slider_edad", "value"),
        Output("slider_promedio", "value"),
        Input("url", "search")
    )
    def reset_filtros(search):
        if search and "reset=1" in search:
            dataf = obtenerestudiantes()
            if dataf.empty:
                raise dash.exceptions.PreventUpdate
            edad_min = int(dataf["Edad_estudiante"].min())
            edad_max = int(dataf["Edad_estudiante"].max())
            return None, [edad_min, edad_max], [0, 5]
        raise dash.exceptions.PreventUpdate


    # ===================== USUARIO HEADER =====================
    @appnotas.callback(
        Output("usuario_header", "children"),
        Input("intervalo", "n_intervals")
    )
    def mostrar_usuario(n):
        if "username" in session:
            return f"Usuario: {session['username']}"
        return "Invitado"


    # ===================== CALLBACK PRINCIPAL =====================
    @appnotas.callback(
        Output("tabla", "data"),
        Output("tabla", "columns"),
        Output("kpis", "children"),
        Output("histograma", "figure"),
        Output("dispersion", "figure"),
        Output("pie", "figure"),
        Output("barras", "figure"),
        Input("filtro_carrera", "value"),
        Input("slider_edad", "value"),
        Input("slider_promedio", "value"),
        Input("busqueda", "value"),
        Input("intervalo", "n_intervals")
    )
    def actualizar_comp(carrera, rangoedad, rangoprome, busqueda, n_intervals):

        dataf = obtenerestudiantes()

        if carrera:
            filtro = dataf[
                (dataf["Carrera_estudiante"].str.strip() == carrera) &
                (dataf["Edad_estudiante"] >= rangoedad[0]) &
                (dataf["Edad_estudiante"] <= rangoedad[1]) &
                (dataf["Promedio"] >= rangoprome[0]) &
                (dataf["Promedio"] <= rangoprome[1])
            ]
        else:
            # Sin carrera seleccionada - mostrar todos 
            filtro = dataf[
                (dataf["Edad_estudiante"] >= rangoedad[0]) &
                (dataf["Edad_estudiante"] <= rangoedad[1]) &
                (dataf["Promedio"] >= rangoprome[0]) &
                (dataf["Promedio"] <= rangoprome[1])
            ]

        if busqueda:
            filtro = filtro[
                filtro.apply(lambda row: busqueda.lower() in str(row).lower(), axis=1)
            ]

        promedio = round(filtro["Promedio"].mean(), 2) if not filtro.empty else 0
        total    = len(filtro)
        maximo   = round(filtro["Promedio"].max(), 2) if not filtro.empty else 0

        kpis = [
            html.Div([html.H4("Promedio"),          html.H2(promedio)],
                style={"backgroundColor": "#3498db", "color": "white",
                       "padding": "15px", "borderRadius": "10px"}),
            html.Div([html.H4("Total Estudiantes"), html.H2(total)],
                style={"backgroundColor": "#2ecc71", "color": "white",
                       "padding": "15px", "borderRadius": "10px"}),
            html.Div([html.H4("Nota Máxima"),       html.H2(maximo)],
                style={"backgroundColor": "#e67e22", "color": "white",
                       "padding": "15px", "borderRadius": "10px"})
        ]

        histo = px.histogram(filtro, x="Promedio", nbins=10,
                             title="Distribución de Promedios")
        dispersion = px.scatter(filtro, x="Edad_estudiante", y="Promedio",
                                color="Desempeño", title="Edad vs Promedio")
        pie = px.pie(filtro, names="Desempeño", title="Distribución por Desempeño")

        promedios = dataf.groupby("Carrera_estudiante")["Promedio"].mean().reset_index()
        barras = px.bar(promedios, x="Carrera_estudiante", y="Promedio",
                        color="Carrera_estudiante",
                        title="Promedio General por Carrera")

        return (
            filtro.to_dict("records"),
            [{"name": i, "id": i} for i in filtro.columns],
            kpis, histo, dispersion, pie, barras
        )


    # ===================== GRÁFICO DETALLADO =====================
    @appnotas.callback(
        Output("gra_detallado", "figure"),
        Input("tabla", "derived_virtual_data"),
        Input("tabla", "derived_virtual_selected_rows"),
        Input("intervalo", "n_intervals")
    )
    def actualizartab(rows, selected_rows, n_intervals):
        if rows is None:
            return px.scatter(title="Sin datos")

        dff = pd.DataFrame(rows)

        if selected_rows:
            dff = dff.iloc[selected_rows]

        fig = px.scatter(dff, x="Edad_estudiante", y="Promedio",
                         color="Desempeño", size="Promedio",
                         title="Análisis Detallado")
        return fig


    # =====================  RANKING TOP 10 =====================
    @appnotas.callback(
        Output("ranking_tabla", "children"),
        Input("intervalo", "n_intervals")
    )
    def mostrar_ranking(n):
        dataf = obtenerestudiantes()

        if dataf.empty:
            return html.P("No hay datos aún.", style={"textAlign": "center"})

        top10 = (
            dataf[["Nombre_estudiante", "Carrera_estudiante", "Promedio"]]
            .sort_values("Promedio", ascending=False)
            .head(10)
            .reset_index(drop=True)
        )
        top10.index += 1  # posición desde 1

        medallas = {1: "1", 2: "2", 3: "3"}

        filas = []
        for pos, row in top10.iterrows():
            icono = medallas.get(pos, f"#{pos}")
            bg = "#fff9c4" if pos == 1 else ("#f0f0f0" if pos % 2 == 0 else "white")
            filas.append(html.Tr([
                html.Td(icono,               style={"padding": "10px 20px", "textAlign": "center", "fontWeight": "bold"}),
                html.Td(row["Nombre_estudiante"],   style={"padding": "10px 20px"}),
                html.Td(row["Carrera_estudiante"],  style={"padding": "10px 20px"}),
                html.Td(row["Promedio"],            style={"padding": "10px 20px", "textAlign": "center", "fontWeight": "bold"})
            ], style={"backgroundColor": bg}))

        tabla = html.Table([
            html.Thead(html.Tr([
                html.Th("Pos",      style={"padding": "10px 20px", "backgroundColor": "#1E1BD2", "color": "white"}),
                html.Th("Nombre",   style={"padding": "10px 20px", "backgroundColor": "#1E1BD2", "color": "white"}),
                html.Th("Carrera",  style={"padding": "10px 20px", "backgroundColor": "#1E1BD2", "color": "white"}),
                html.Th("Promedio", style={"padding": "10px 20px", "backgroundColor": "#1E1BD2", "color": "white"})
            ])),
            html.Tbody(filas)
        ], style={"width": "100%", "borderCollapse": "collapse", "marginTop": "10px"})

        return tabla


    # =====================  ALERTA ESTUDIANTES EN RIESGO =====================
    @appnotas.callback(
        Output("alerta_riesgo", "children"),
        Input("intervalo", "n_intervals")
    )
    def alerta_riesgo(n):
        dataf = obtenerestudiantes()

        en_riesgo = dataf[dataf["Promedio"] < 3.0][
            ["Nombre_estudiante", "Carrera_estudiante", "Promedio"]
        ].sort_values("Promedio")

        if en_riesgo.empty:
            return html.Div(
                " No hay estudiantes en riesgo actualmente.",
                style={
                    "backgroundColor": "#d4edda", "color": "#155724",
                    "padding": "12px 20px", "borderRadius": "8px",
                    "border": "1px solid #c3e6cb", "fontWeight": "bold"
                }
            )

        filas = [
            html.Tr([
                html.Td(row["Nombre_estudiante"],  style={"padding": "8px 16px"}),
                html.Td(row["Carrera_estudiante"], style={"padding": "8px 16px"}),
                html.Td(row["Promedio"],           style={"padding": "8px 16px",
                                                          "color": "red", "fontWeight": "bold"})
            ])
            for _, row in en_riesgo.iterrows()
        ]

        tabla_riesgo = html.Table([
            html.Thead(html.Tr([
                html.Th("Nombre",   style={"padding": "8px 16px", "backgroundColor": "#e74c3c", "color": "white"}),
                html.Th("Carrera",  style={"padding": "8px 16px", "backgroundColor": "#e74c3c", "color": "white"}),
                html.Th("Promedio", style={"padding": "8px 16px", "backgroundColor": "#e74c3c", "color": "white"})
            ])),
            html.Tbody(filas)
        ], style={"width": "100%", "borderCollapse": "collapse"})

        return html.Div([
            html.H3(f" Estudiantes en Riesgo Académico ({len(en_riesgo)})",
                    style={"color": "#e74c3c", "marginBottom": "10px"}),
            tabla_riesgo
        ], style={
            "backgroundColor": "#fdecea", "padding": "20px",
            "borderRadius": "10px", 
        })

    return appnotas