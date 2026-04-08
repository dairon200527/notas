import pandas as pd
import plotly.express as px
import os
import dash
from dash import html,Input,Output,dcc

#cargar los datos
ruta = os.path.join(os.path.dirname(__file__), "notas_limpio.xlsx")
dataf = pd.read_excel(ruta)
#print(dataf)

#iniciar app
appnotas = dash.Dash(__name__)
appnotas.layout = html.Div([
                  html.H1("TABLERO DE NOTAS ESTUDIANTES",style={"textAlign":"center",
                                                  "color":"#0023E7",
                                                  "padding":"20px",
                                                  "fontFamily":"Arial",
                                                  "backgroundColor":"#E9ECEE"
                                                  }),
                  html.Label("SELECCIONA MATERIA",style={"margin":"10px"}),
                  dcc.Dropdown(id="filtro_materia",
                               options=[{"label":Carrera,"value":Carrera} for Carrera in sorted(dataf["Carrera"].unique())],
                               value=dataf["Carrera"].unique()[0],
                               style={"width":"100%","margin":"auto"}
                                ),
                  html.Br(),

                  #crear los tabs de los graficos
                  dcc.Tabs([
                      dcc.Tab(label='Grafico de promedio',children=[dcc.Graph(id='histograma')]),
                      dcc.Tab(label="Edad vs promedios",children=[dcc.Graph(id='dispersion')]),
                      dcc.Tab(label="desempeño",children=[dcc.Graph(id='pie')]),
                      dcc.Tab(label="Promedio notas x carrera",children=[dcc.Graph(id='barras')]),
                      
                  ], style={"fontWeight":"bold","color":"#2c3e50"})
                


                  
                  


                          ])

#actualizar el grafico
@appnotas.callback(
        Output("histograma","figure"),
        Output("dispersion","figure"),
        Output("pie","figure"),
        Output("barras","figure"),
        Input("filtro_materia",'value')
)

#funcon para actualizar el grafico:
def actualizar(filtro_materia):

    filtro = dataf[dataf["Carrera"]==filtro_materia]

    #crear los graficos
    histo = px.histogram(filtro, x="Promedio",nbins=10,title=f"Distribucion de promedios - {filtro_materia}",
                                                                                                        color_discrete_sequence=

                                                                                                        ["#3dbb17"]).update_layout(template="plotly_white",yaxis_title="Cantidad de estudiantes")    
                                                    
    disper = px.scatter(filtro,x="Edad",y="Promedio",color="Desempeño",title=f"Edad vs Promedio - {filtro_materia}",
                                                                                                         color_discrete_sequence=px.colors.qualitative.Set2).update_layout(template="plotly_white")
    pie = px.pie(filtro,names="Desempeño",title=f"Desempeño-{filtro_materia}")
    
    promedios= filtro.groupby("Carrera")["Promedio"].mean().reset_index()                                                
    barra= px.bar(promedios, x="Carrera",y="Promedio",title="Promedio de notas por carrera",color="Carrera",color_discrete_sequence=px.colors.qualitative.Dark2)
    
    return histo, disper, pie, barra                     
    
   

#ejecutar la app
if __name__ == '__main__':
    appnotas.run(debug=True)
    print(dataf)