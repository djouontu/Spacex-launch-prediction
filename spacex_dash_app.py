# Import required libraries
import pandas as pd
import more_itertools
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
launch_site= spacex_df['Launch Site'].unique()
all_df = spacex_df.groupby('Launch Site')['class'].sum().reset_index()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[{'label': 'All Sites', 'value': 'ALL'},
                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                     ],
                                    value='ALL',
                                    placeholder="Select a Launch Site here",
                                    searchable=True
                               ),
 # TASK 2: Add a pie chart to show the total successful launches count for all sites
 # If a specific launch site was selected, show the Success vs. Failed counts for the site
                             html.Div(dcc.Graph(id='success-pie-chart',
                             figure=px.pie(
                                        all_df,
                                        values='class',
                                        names='Launch Site',
                                        title="Number of Successes by Site"))),
                            
                            html.Br(),
                            html.P("Payload range (Kg):"),
# TASK 3: Add a slider to select payload range
                           dcc.RangeSlider(id='payload-slider',
                                min=min_payload, max=max_payload, step=1000,
                                marks={0: '0',
                                        100: '100'},
                                value=[min_payload, max_payload]),

# TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(
                                    id='success-payload-scatter-chart',
                                    figure = px.scatter(
                                                spacex_df,
                                                x="Payload Mass (kg)",
                                                y="class"))),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
    )
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(all_df, values='class', 
        names='Launch Site', 
        title='total success by launch site')
        return fig
    else:
        # return the outcomes piechart for a selected site
        filtered_df=spacex_df[spacex_df['Launch Site']==entered_site]
        entered_df= filtered_df.groupby('class')['Launch Site'].count().reset_index()
        fig = px.pie(entered_df, values='Launch Site', 
        names='class', 
        title='total success launch for site {}'.format(entered_site))
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value')]
    )

def get_scatter(value1,value2):
    filtered_df1 =spacex_df[(spacex_df['Payload Mass (kg)'] > value2[0]) & (spacex_df['Payload Mass (kg)'] < value2[1])]

    if value1=='ALL':
        fig= px.scatter(filtered_df1,
        x="Payload Mass (kg)",
        y="class",color="Booster Version Category",
        title="Correlation between Payload and Success for All sites")
        return fig
    else :
        filtered_df2=filtered_df1[filtered_df1['Launch Site']==value1]
        fig= px.scatter(filtered_df2,
        x="Payload Mass (kg)",
        y="class",
        color="Booster Version Category",
        title="Correlation between Payload and Success for site {value1}")
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
