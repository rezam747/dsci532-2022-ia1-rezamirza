from dash import Dash, html, dcc, Input, Output
import altair as alt
import pandas as pd

# alt.data_transformers.enable('data_server')


# Read in global data
path = 'https://raw.githubusercontent.com/UofTCoders/workshops-dc-py/master/data/processed/world-data-gapminder.csv'
gapminder = pd.read_csv(path, parse_dates=['year'])


# Setup app and layout/frontend
app = Dash(__name__,  external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server
app.layout = html.Div([
    html.Iframe(
        id='linechart',
        style={'border-width': '0', 'width': '100%', 'height': '400px'}),
    dcc.Dropdown(
        id='xcol-widget',
        value='life_expectancy',  # REQUIRED to show the plot on the first page load
        options=[{'label': col, 'value': col} for col in gapminder.select_dtypes('number').columns]),
    dcc.Dropdown(
        id='country-widget',
        value='Canada',  # REQUIRED to show the plot on the first page load
        options=[{'label': country, 'value': country} for country in gapminder['country'].unique()])])

# Set up callbacks/backend
@app.callback(
    Output('linechart', 'srcDoc'),
    Input('xcol-widget', 'value'),
    Input('country-widget', 'value'))
def plot_altair(xcol, country):
    gapminder_country = gapminder[gapminder['country'] == country]
    chart = alt.Chart(gapminder_country, title=f'{xcol} of {country} during the time').mark_line().encode(
      alt.X('year', title='Time'),
      alt.Y(xcol, title=f'{xcol}'),
      tooltip = xcol).interactive()
    return chart.to_html()

if __name__ == '__main__':
    app.run_server(debug=True)