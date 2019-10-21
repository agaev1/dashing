import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from pandas.api.types import is_numeric_dtype
from kobra import Date_custom
from dash.dependencies import Input, Output
from app import app


def deal_simul_dataframe():

    default_start = Date_custom('2019-01-01').date
    default_end = Date_custom('2019-03-03').date
    default_amt = 2500
    default_type = 'DEPO'

    df = pd.DataFrame(
        {
            'START': [default_start],
            'END': [default_end],
            'AMT_MIO': [default_amt],
            'DEAL_TYPE': [default_type],
        }
    )

    return df


def deal_simulation_table():
    df_init = deal_simul_dataframe()
    table = dash_table.DataTable(
        id='deal-table',
        columns=[
            {'id': 'START', 'name': 'START', 'type': 'datetime'},
            {'id': 'END', 'name': 'END', 'type': 'datetime'},
            {
                'id': 'AMT_MIO',
                'name': 'AMT_MIO',
                'type': 'numeric',
                'format': {

                    'specifier': ',.0f'
                }
            },
            {'id': 'DEAL_TYPE', 'name': 'DEAL_TYPE', 'presentation': 'dropdown'},

        ],
        data=df_init.to_dict('records'),
        style_data_conditional=[
            {
                'if': {
                    'column_id': str(x),
                    'filter_query': '{{{}}} < 0'.format(x)
                },
                'color': 'red',
            } for x in df_init.columns if is_numeric_dtype(df_init[x])
        ],
        editable=True,
        dropdown={
            'DEAL_TYPE': {
                'options': [
                    {'label': i, 'value': i}
                    for i in ['DEPO', 'FX', 'LOAN']
                ]
            }
        }
    )
    return table


layout = html.Div(
    [
        html.H3('TABLES!'),
        html.P('Using the new datatables module.'),
        dcc.Link('Go to Main Page', href='/apps/'),
        deal_simulation_table(),
        html.Div(id='deal-description')
    ]
)

# Callbacks


@app.callback(
    Output('deal-description', 'children'),
    [Input('deal-table', 'data'),
     Input('deal-table', 'columns')])
def display_output(rows, columns):
    # Describe the deal, just for testing
    df = pd.DataFrame(rows, columns=[c['name'] for c in columns])
    amt = '{:,.0f}'.format(df['AMT_MIO'][0])
    deal_type = df['DEAL_TYPE'][0]
    start = Date_custom(df['START'][0]).date.strftime('%B %d')
    end = Date_custom(df['END'][0]).date.strftime('%B %d')
    return_string = 'This is a {} starting {}, ending {}, for {} million!'.format(
        deal_type,
        start,
        end,
        amt
    )
    return return_string
