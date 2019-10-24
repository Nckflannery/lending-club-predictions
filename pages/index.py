import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

from app import app

"""
https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout

Layout in Bootstrap is controlled using the grid system. The Bootstrap grid has 
twelve columns.

There are three main layout components in dash-bootstrap-components: Container, 
Row, and Col.

The layout of your app should be built as a series of rows of columns.

We set md=4 indicating that on a 'medium' sized or larger screen each column 
should take up a third of the width. Since we don't specify behaviour on 
smaller size screens Bootstrap will allow the rows to wrap so as not to squash 
the content.
"""

row1 = dcc.Markdown(
    '''
    # __Can You Predict the Return on Investment of a Loan?__
    ---
    ''',
    style={'textAlign':'center'}
)

row2 = dbc.Row([
    dbc.Col([
        dcc.Markdown(
            """
            Have you ever thought of investing on Lending Club but worry about how much you might lose?\n
            If only you had some way of predicting which loans would be best to invest in, maybe you'd give it a shot!\n
            Well, using this app you can predict what your Return on Investment percentage (percent return for every dollar invested) would be!
            """
        ),
        dcc.Link(dbc.Button('PREDICT', color='secondary', outline=True, block=True), href='/predictions'),
        dcc.Markdown(
            '''
            - - -
            '''
        ),
        html.Div(html.Sup('WARNING: INVEST AT YOUR OWN RISK! THIS IS NOT PERFECT!'))
    ]),
    dbc.Col(html.Img(src='assets/investment.jpg', className='img-fluid'), md=8)
])


layout = dbc.Col([row1, row2])