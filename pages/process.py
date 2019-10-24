import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## Process


            """
        ),
        html.Img(src='assets/RFR_MAE.png', className='img-fluid'),
        html.Img(src='assets/LGBM_MAE.png', className='img-fluid'),
    ],
)

layout = dbc.Row([column1])