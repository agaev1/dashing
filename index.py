import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from app_charts import app_charts
from app_tables import app_tables

app_urls = {
    '/apps/charts': app_charts.layout,
    '/apps/tables': app_tables.layout
}

main_layout = html.Div(
    [
        html.H1('A multipage app!'),
        html.P('Click on an app below!'),
        html.Div(
            [
                dcc.Link('Charts', href='/apps/charts'),
            ]
        ),
        html.Div(
            [
                dcc.Link('Tables', href='/apps/tables'),
            ]
        )
    ]
)


app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=False),
        html.Div(
            id='page-content'
        )
    ]
)


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):

    layout = app_urls.get(pathname, main_layout)
    return layout


if __name__ == '__main__':
    app.run_server(debug=True)
