import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/nz_weather.csv')
df["Dunedin"] = pd.to_numeric(df["Dunedin"], errors='coerce')
df["Hamilton"] = pd.to_numeric(df["Hamilton"], errors='coerce')
df = df.replace("'-", method='bfill')

col = ["Greens", "YlOrRd", "Bluered", "RdBu", "Reds", "Blues", "Picnic", "Rainbow", "Portland", "Jet", "Hot",
       "Blackbody", "Earth", "Electric", "Viridis", "Cividis"]

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H1("New Zealand Rainfall")

    ], style={
        'textAlign': "center"
    }),
    html.Div([
        html.Div([html.Span("Choose City"),
                  dcc.Dropdown(
                      id="selected-city",
                      options=[{
                          "label": i, "value": i
                      } for i in df.columns.values[1:]],
                      value="Auckland",

                  )], style={'width': '48%', "float": "left"}),
        html.Div([html.Span("Choose Colorscale"),
                  dcc.Dropdown(
                      id="selected-color",
                      options=[{
                          "label": i, "value": i
                      } for i in col],
                      value="Electric",

                  )], style={'width': '48%', "float": "right"})

    ], style={'width': '100%', 'display': 'inline-block'}),
    dcc.Graph(id="my-graph")

], className="container")


@app.callback(
    Output('my-graph', 'figure'),
    [Input('selected-city', 'value'),
     Input('selected-color', 'value')])
def update_figure(selected, selected_color):
    trace = (go.Scatter(
        x=df["DATE"],
        y=df[selected],
        name=selected,
        mode='markers',
        marker={'size': 8,
                'cmax': 250,
                'cmin': 0,
                'color': df[selected].values.tolist(),
                'colorscale': selected_color,
                "colorbar": {
                    "title": 'Rainfall',
                    "titleside": 'top',
                    "tickmode": 'array',
                    "tickvals": [0, 125, 250],
                    "ticktext": ['Light', 'Moderate', 'Heavy'],
                    "ticks": 'outside'
                }
                },

        line={'width': 4}

    )
    )

    return {
        "data": [trace],

        "layout": go.Layout(
            title=f'Rainfall for {selected} Over Time',
            xaxis={
                "title": "Date"

            },
            yaxis={
                "title": "Rainfall (mm)",
                "range": [0, 350],
                "showline": True
            },
            font={"color": "#ffffff"},
            paper_bgcolor="#000000",
            plot_bgcolor="#000000"
        )

    }


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
