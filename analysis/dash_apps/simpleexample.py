import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
from django_plotly_dash import DjangoDash
from plotly.subplots import make_subplots

from dashboard.models import Weather

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('SimpleExample', external_stylesheets=external_stylesheets)

# TODO: cover in try catch and put the original sql call back
df = pd.DataFrame(
    [{'timestamp': datetime.datetime(2020, 7, 16, 0, 1, 39, 488000), 'temperature': 12.18, 'humidity': 62.88},
     {'timestamp': datetime.datetime(2020, 7, 16, 0, 2, 39, 520000), 'temperature': 12.14, 'humidity': 62.75},
     {'timestamp': datetime.datetime(2020, 7, 16, 0, 3, 39, 550000), 'temperature': 12.08, 'humidity': 63.16},
     {'timestamp': datetime.datetime(2020, 7, 16, 0, 4, 39, 580000), 'temperature': 12.04, 'humidity': 63.1},
     {'timestamp': datetime.datetime(2020, 7, 16, 0, 5, 39, 610000), 'temperature': 11.94, 'humidity': 63.02},
     {'timestamp': datetime.datetime(2020, 7, 16, 0, 6, 39, 640000), 'temperature': 11.98, 'humidity': 63.24},
     {'timestamp': datetime.datetime(2020, 7, 16, 0, 7, 39, 670000), 'temperature': 11.95, 'humidity': 63.15},
     {'timestamp': datetime.datetime(2020, 7, 16, 0, 8, 39, 700000), 'temperature': 11.92, 'humidity': 63.22},
     {'timestamp': datetime.datetime(2020, 7, 16, 0, 9, 39, 731000), 'temperature': 11.9, 'humidity': 63.35}])

# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig.add_trace(
    go.Scatter(x=df['timestamp'], y=df['temperature'], name="Temperature"),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=df['timestamp'], y=df['humidity'], name="Humidity"),
    secondary_y=True,
)
# Add figure title
fig.update_layout(
    title_text="Hourly Temperature vs Humidity"
)

# Set y-axes titles
fig.update_yaxes(title_text="Temperature Axis", secondary_y=False)
fig.update_yaxes(title_text="Humidity Axis", secondary_y=True)

fig.update_xaxes(
    title_text="Hour",
    tickformat="%I %p")

app.layout = html.Div([
    dcc.DatePickerSingle(
        id='my-date-picker-single',
        min_date_allowed=datetime.date(1995, 8, 5),
        max_date_allowed=datetime.date(2022, 9, 19),
        with_portal=True,
        date=datetime.date(2020, 8, 25)
    ),
    dcc.Graph(id="scatter-plot", figure=fig)
])


@app.callback(
    dash.dependencies.Output('scatter-plot', 'figure'),
    dash.dependencies.Input('my-date-picker-single', 'date'))
def update_figure(date_value):
    if date_value is not None:
        date_object = datetime.date.fromisoformat(date_value)
        df = pd.DataFrame(list(
            Weather.objects.filter(timestamp__date=date_object).values('timestamp', 'temperature',
                                                                       'humidity')))
        fig.data = []

        fig.add_trace(
            go.Scatter(x=df['timestamp'], y=df['temperature'], name="Temperature"),
            secondary_y=False,
        )

        fig.add_trace(
            go.Scatter(x=df['timestamp'], y=df['humidity'], name="Humidity"),
            secondary_y=True,
        )

        fig.update_layout(transition_duration=500)

        return fig
