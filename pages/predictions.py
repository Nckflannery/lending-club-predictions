import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output
from joblib import load

from app import app

pipeline = load('assets/lgbm_pipeline.joblib')

column1 = dbc.Col(
    [
        dcc.Markdown(
            """
            ## Select the features of the potential loan
            ---
            """
        ),
        dcc.Markdown('''##### **Interest Rate**'''),
        dcc.Slider(
            id = 'interest',
            min=5,
            max=35,
            step=.25,
            value=20,
            updatemode='drag',
            marks={n: str(n) for n in range(5, 36, 5)},
            className='mb-5',
        ),
        html.Div(id='interest-rate-slider', style={'textAlign':'center'}),
        dcc.Markdown('''##### **Loan Amount**'''),
        dcc.Slider(
            id = 'loan',
            min=500,
            max=40000,
            step=50,
            value=20000,
            updatemode='drag',
            marks={
                500 : '$500',
                5000: '$5,000',
                10000: '$10,000',
                15000: '$15,000',
                20000: '$20,000',
                25000: '$25,000',
                30000: '$30,000',
                35000: '$35,000',
                40000: '$40,000'
            },
            className='mb-5',
        ),
        html.Div(id='loan-amount-slider', style={'textAlign':'center'}),
        dcc.Markdown('''##### **Sub Grade**'''),
        dcc.Slider(
            id = 'subgrade',
            min=1,
            max=35,
            step=1,
            value=35,
            updatemode='drag',
            marks={
                1:'A1', 
                2:'A2', 
                3:'A3', 
                4:'A4', 
                5:'A5',
                6:'B1', 
                7:'B2', 
                8:'B3', 
                9:'B4', 
                10:'B5',
                11:'C1', 
                12:'C2', 
                13:'C3', 
                14:'C4', 
                15:'C5',
                16:'D1', 
                17:'D2', 
                18:'D3', 
                19:'D4', 
                20:'D5',
                21:'E1', 
                22:'E2', 
                23:'E3', 
                24:'E4', 
                25:'E5',
                26:'F1', 
                27:'F2', 
                28:'F3', 
                29:'F4', 
                30:'F5',
                31:'G1', 
                32:'G2', 
                33:'G3', 
                34:'G4', 
                35:'G5',
            },
            className='mb-5',
        ),
        dcc.Markdown('''##### **Monthly Installment Payment**'''),
        dcc.Slider(
            id='installment',
            min=5,
            max=1800,
            step=5,
            value=900,
            marks={
                5:'$5',
                500:'$500',
                1000:'$1,000',
                1500:'$1,500',
                1800:'$1,800'
            },
            className='mb-5',
        ),
        html.Div(id='installment-slider', style={'textAlign':'center'}),
        dcc.Markdown('''##### **Annual Income of Loan Applicant**'''),
        dcc.Slider(
            id='income',
            min=10000,
            max=500000,
            step=500,
            value=250000,
            updatemode='drag',
            marks={
                10000 :'$10,000',
                50000 :'$50,000',
                100000:'$100,000',
                150000:'$150,000',
                200000:'$200,000',
                250000:'$250,000',
                300000:'$300,000',
                350000:'$350,000',
                400000:'$400,000',
                450000:'$450,000',
                500000:'$500,000'
            },
            # tooltip={'always_visible':True, 'placement':'bottomLeft'}, THIS LOOKS BAD!
            className='mb-5',
        ),
        html.Div(id='annual-income-slider', style={'textAlign':'center'}),
        dcc.Markdown('''##### **Term of Loan**'''),
        dcc.RadioItems(
            id = 'term',
            options = [
                {'label': ' 36 Months', 'value': 1},
                {'label': ' 60 Months', 'value': 2}
            ],
            value=2,
            labelStyle = {'margin-right': '20px'},
            className='mb-5'
        ),   
    ],
    md=6,
)

column2 = dbc.Col(
    [
        dcc.Markdown(
            '''
            ## Predicted Return on Investment
            ---
            '''
        ),  
        daq.Gauge(
            id='ROI_Gauge',
            color={'gradient':True, 'ranges':{'red':[-100,20],'orange':[20,40],"yellow":[40,60],"green":[60,100]}},
            showCurrentValue=True,
            units='Percent Return',
            value=0,
            min=-100,
            max=100,
            size=500
        ),
    ]
)

layout = dbc.Row([column1, column2])

@app.callback(
    Output('loan-amount-slider', 'children'),
    [Input('loan', 'value')]
)
def loan_output(x):
    return f'Loan Amount: ${x:,}'

@app.callback(
    Output('interest-rate-slider', 'children'),
    [Input('interest', 'value')]
)
def interest_output(x):
    return f'Interest Rate: {x}%'

@app.callback(
    Output('annual-income-slider', 'children'),
    [Input('income', 'value')]
)
def income_output(x):
    return f'Annual Income: ${x:,}'

@app.callback(
    Output('installment-slider', 'children'),
    [Input('installment', 'value')]
)
def installment_output(x):
    return f'Monthly Installment: ${x:,}'

@app.callback(
    Output('ROI_Gauge', 'value'),
    [Input('interest', 'value'),
    Input('term', 'value'),
    Input('subgrade', 'value'),
    Input('loan', 'value'),
    Input('income', 'value'),
    Input('installment', 'value')]
)
def roi_output(a, b, c, d, e, f):
    x = pd.DataFrame(
        columns=['int_rate', 'term', 'sub_grade', 'loan_amnt', 'annual_inc', 'installment'],
        data=[[a, b, c, d, e, f]]
    )
    y_pred = pipeline.predict(x)[0].round(2)
    return y_pred
