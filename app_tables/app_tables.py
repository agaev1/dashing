import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from pandas.api.types import is_numeric_dtype

from app import app

df = pd.DataFrame(
    {
        'Names': ['John', 'Paul', 'Ringo'],
        'Numbers': [223442, -33443, 988292]
    }
)


layout = html.Div(
    [
        html.H3('TABLES!'),
        html.P('Using the new datatables module.'),
        dcc.Link('Go to Main Page', href='/apps/'),
        dash_table.DataTable(
            id='table',
            columns=[
                {
                    "name": i,
                    "id": i,
                    'type': 'numeric',
                    'format': {

                        'specifier': ',.0f'
                    }
                } for i in df.columns
            ],
            data=df.to_dict('records'),
            style_data_conditional=[
                {
                    'if': {
                        'column_id': str(x),
                        'filter_query': '{{{}}} < 0'.format(x)
                    },
                    'color': 'red',
                } for x in df.columns if is_numeric_dtype(df[x])
            ]
        )
    ]
)
