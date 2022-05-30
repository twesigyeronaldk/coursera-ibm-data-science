# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Get list options
def get_list_options(df):
    list_options = []
    list_options.append(
        {
            "label": "All Sites",
            "value": "All"
        }
    )
    for value in df["Launch Site"].unique():
        opt = {
            "label": value,
            "value": value
        }
        list_options.append(opt)
    return list_options

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites

                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=get_list_options(spacex_df),
                                    value="All",
                                    placeholder="Select a Launch Site",
                                    searchable=True
                                ),
                                
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0,
                                    max=10000,
                                    step=1000,
                                    # marks={
                                    #     0: '0',
                                    #     100: '100'
                                    # },
                                    value=[
                                        spacex_df.sort_values("Payload Mass (kg)", ascending=True).head(1)["Payload Mass (kg)"].values[0],
                                        spacex_df.sort_values("Payload Mass (kg)", ascending=False).head(1)["Payload Mass (kg)"].values[0]
                                    ]
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(
        component_id='success-pie-chart',
        component_property='figure'
    ),
    Input(
        component_id='site-dropdown',
        component_property='value'
    )
)
def get_pie_chart(selected_site):
    if selected_site == "All":
        fig = px.pie(
            spacex_df[spacex_df["class"] == 1],
            values="class",
            names="Launch Site",
            title="Successful Launches by Site"
        )
    else:
        graph_values = []
        graph_names = []

        for index, row in spacex_df[spacex_df["Launch Site"] == selected_site].iterrows():
            if row["class"] == 0:
                graph_names.append("Fail")
            else:
                graph_names.append("Success")
            
            graph_values.append(1)  # this is simply a counter
        
        fig = px.pie(
            values=graph_values,
            names=graph_names,
            title="Successful Lauches for " + selected_site
        )
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(
        component_id='success-payload-scatter-chart',
        component_property='figure'
    ),
    [
        Input(
            component_id='site-dropdown',
            component_property='value'
        ),
        Input(
            component_id='payload-slider',
            component_property='value'
        )
    ]
)
def get_scatter_plot(selected_site, selected_payload):
    if selected_site == "All":
        fig = px.scatter(
            spacex_df,
            x="Payload Mass (kg)",
            y="class",
            color="Booster Version"
        )
    else:
        fig = px.scatter(
            spacex_df[spacex_df["Launch Site"] == selected_site],
            x="Payload Mass (kg)",
            y="class",
            color="Booster Version"
        )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
