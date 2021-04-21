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

df = pd.DataFrame(list(
    Weather.objects.filter(timestamp__date=datetime.date(2020, 7, 16)).values('timestamp', 'temperature',
                                                                              'humidity')))
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
