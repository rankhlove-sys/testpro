# Import des packages requis
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px

# Lire les données spacex depuis le CSV en ligne
spacex_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")

# Obtenir la liste des sites de lancement pour le dropdown
launch_sites = spacex_df['Launch Site'].unique().tolist()
launch_sites.insert(0, 'All Sites')

# Créer l'application Dash
app = dash.Dash(__name__)

# Créer le layout de l'application
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # TASK 1: Add a Launch Site Drop-down Input Component
    # Dropdown pour sélectionner un site de lancement
    dcc.Dropdown(id='site-dropdown',
                 options=[{'label': i, 'value': i} for i in launch_sites],
                 value='All Sites',
                 placeholder="Select a Launch Site here",
                 searchable=True
                 ),
    html.Br(),

    # Graphique Pie Chart
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),
    # TASK 3: Add a Range Slider to Select Payload
    # Slider pour sélectionner la plage de charge utile
    dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=1000,
                    marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
                    value=[0, 10000]),
    
    # Graphique Scatter Chart
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2: Add a callback function to render success-pie-chart based on selected site dropdown
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'All Sites':
        # Affiche le total des succès par site
        fig = px.pie(spacex_df, 
                     values='class', 
                     names='Launch Site', 
                     title='Total Success Launches By Site')
        return fig
    else:
        # Filtre pour le site sélectionné et affiche succès vs échec
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(filtered_df, 
                     names='class', 
                     title=f'Total Success vs Failed Launches for site {entered_site}')
        return fig

# TASK 4: Add a callback function to render the success-payload-scatter-chart scatter plot
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])
def get_scatter_chart(entered_site, payload_range):
    low, high = payload_range
    # Filtre par plage de payload
    mask = (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
    filtered_df = spacex_df
    
    if entered_site == 'All Sites':
        # Affiche pour tous les sites
        fig = px.scatter(filtered_df, 
                         x='Payload Mass (kg)', 
                         y='class', 
                         color="Booster Version Category",
                         title='Correlation between Payload and Success for all Sites')
        return fig
    else:
        # Affiche pour le site sélectionné
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(filtered_df, 
                         x='Payload Mass (kg)', 
                         y='class', 
                         color="Booster Version Category",
                         title=f'Correlation between Payload and Success for site {entered_site}')
        return fig

# Lancer l'application
if __name__ == '__main__':
    app.run(debug=True, port=8050)