import pandas as pd 
import plotly
import plotly.express as px
import dash 
from dash import dcc
from dash import html
import plotly.graph_objects as go
from plotly.subplots import make_subplots

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


crime_df = pd.read_csv('notebooks/covid_data/crime_uk/UK_Police_Street_Crime_2018-10-01_to_2021_09_31.csv')
covid_df = pd.read_csv('notebooks/covid_data/UK_National_Total_COVID_Dataset.csv')
covid_df.date[0] = '2018-10-01'
english_national_lockdowns = ['2020-03-26', '2020-11-05', '2021-01-06']

crimes_per_months = crime_df.groupby('Month')['Month'].count()
crimes_per_months.index = crimes_per_months.index + '-01'

fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.update_layout(title_text = 'How did Covid19 Lockdowns effect UK street crime?')
fig.update_xaxes(title_text = 'Date')
fig.update_yaxes(title_text = 'Reported Street Crime - UK', range=[320000,800000], secondary_y=True)
fig.update_yaxes(title_text = 'New Covid Cases - UK', secondary_y=False)
fig['layout']['yaxis2']['showgrid'] = False

fig.add_trace(
    go.Scatter(x=covid_df['date'], y=covid_df['newCasesByPublishDate'], name="New Covid Cases - UK"),
    secondary_y=False, 
)

fig.add_trace(
    go.Scatter(x=crimes_per_months.index, y=crimes_per_months, name="Reported Street Crimes - UK",line_color = 'orange', opacity = 0.4),
    secondary_y=True,
)

fig.add_trace(
    go.Scatter(x=[english_national_lockdowns[0]], y=[900000], name='English National Lockdowns',line_color = 'red', opacity = 0.4, line_dash = 'dash'),
    secondary_y=True,
)

fig.add_vline(x = english_national_lockdowns[0], line_dash = 'dash', line_color = 'red', opacity = 0.4, name = 'English National Lockdowns')
fig.add_vline(x = english_national_lockdowns[1], line_dash = 'dash', line_color = 'red', opacity = 0.4)
fig.add_vline(x = english_national_lockdowns[2], line_dash = 'dash', line_color = 'red', opacity = 0.4)

app.layout = html.Div([
    dcc.Graph(
        id='',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)