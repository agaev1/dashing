import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

layout = html.Div(
    [
        html.H3('TABLES!'),
        html.P('Using the new datatables module.'),
        dcc.Link('Go to Main Page', href='/apps/')
    ]
)
