import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

row1 = dcc.Markdown(
    '''
    # **Insights**
    ---
    ''',
    style={'textAlign':'center'}
)


row2 = dbc.Col(
    [
        dcc.Markdown(
            """
            ## Looking at _Feature Importances_ and _Permutation Importances_
            """
        ),
        dcc.Markdown(
            '''
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Due to the nature of the app, I wanted to only include "front facing" 
            features i.e. features that a potential investor would be able to see on the Lending Club site before investing. 
            This led me to begin looking into the feature importances on training the data and on predicting the data (the graph 
            labeled Feature Importances are on the training data, while I used permutation importance, a method of scrambling each 
            feature and checking the loss of accuracy to gather its importance, on the test data) of both models. Below are the 
            feature importances and permutation importances of the Random Forest Regression model I fit with over 25 features. 
            I did this to get a gauge of which of my 'front facing' features would have the most impact on my final model.
            '''
        ),    
    ],
)

row3 = dbc.Row([
    dbc.Col(
        html.Img(src='assets/FeatureImportRFR.png', className='img-fluid')
    ),
    dbc.Col(
        html.Img(src='assets/MyRFR_Perm.png', className='img-fluid'),
        md=6,
    ),
])
row4 = dcc.Markdown(
    '''
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; With these graphs I was able to determine which features have an impact on both fitting 
    the model to my data, and on the importance of a feature in the actual prediction. The front facing features that have the biggest 
    impact on training the model (left graph) are: Interest Rate, Sub Grade (A grade given to each loan by Lending Club based on 'back end' 
    information not available to the potential investor such as fico score of applicant, number of satisfactory accounts open, debt to income, 
    and many other features which are included in this model as well), Installment, and Loan Amount, while the Term of the loan is 
    not as important. However, many of the front facing features are strong predictors of how much a loan will Return. Also notice that 
    while Term was not as strong for training the model, it bumped up quite a bit in importance of predicting the ROI. (A quick note: 
    Annual income was included in the app even though it is not a feature available to the user, more on this later.)\n
    Below, we will look at feature importances of my final model using only the front facing features, and LightGBM Regression.
    '''
)
row5 = dbc.Col([
    dbc.Row([
        dbc.Col(
            html.Img(src='assets/FeatureImportLGBM.png', className='img-fluid')
        ),
        dbc.Col(
            html.Img(src='assets/MyLGBM_Perm.png', className='img-fluid')
        ),
    ]),
    dcc.Markdown(
        '''
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Here we can see that while a feature may be important for training the model, 
        it may not be quite as important for predicting the target. In the case of Annual Income, we can see that it does help 
        fit the model but has only slight importance for our predictions, and this is why I decided to keep it in the app as a 
        fun feature even though it is not available information to the user.\n
        '''

    )
])

row6 = dcc.Markdown(
    '''
    ## Issues With Dropping 'Back End' Features
    ---
    ''',
    style={'textAlign': 'center'}
)

row7 = dbc.Row([
    dbc.Col(
        dcc.Markdown(
            '''
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; In the original dataset there were over 140 features that included a multitude of
            information about the loan applicant. In dropping almost all of these features I was worried that the model would lose too much
            accuracy and be basically useles. After testing I was able to still improve on the baseline predictions by a decent amount.
            One impact this had, however, was that my model with less features was not as good at predicting the loans that had almost no
            amount paid back from the applicant. In the graphs to the right I took 200 random samples from each model and plotted their predictions, 
            actual values, and the baseline prediction for that model. In the first graph, which came from the Random Forrest Regression model that 
            included 31 features, we can see that while the majority of the predictions are very similar to the baseline there are quite a few predictions well 
            below the baseline. When we look at the bottom graph, which came from the Light Gradient Boosting regression model that included only 6 features, we
            can see that while the predictions seem a lot closer to the reality, it has a VERY hard time predicting the low end values representing the times
            when an investor would lose the most money! While this is only a random sample of 200 individual loans, it is quite indicative of the nature of the 
            two different models, and of their strengths and weaknesses. When looking at the features chosen it makes sense that it would have a hard time predicting
            negative ROI as none of them innately stand out as derogetory marks of a loan applicant except for the Sub-Grade, which is a very broad feature
            that the front end user really can't piece together themselves. If you as an investor could look at all 140 features of a loan applicant this model
            would most likely become much more accurate, and not only that, be better at predicting the 'lose all' scenarios. In the end though, it is
            extremely difficult to predict human nature, and thus, is almost impossible to truly forsee how the investment will turn out.  
            '''
        ),
    ),
    dbc.Col([
        dbc.Row(html.Img(src='assets/SampleRFR.png', className='img-fluid')),
        dbc.Row(html.Img(src='assets/SampleLGBM.png', className='img-fluid'))
    ], md=8)
])

layout = dbc.Col([row1, row2, row3, row4, row5, row6, row7])
