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
            # **Process**
            ---
            """,
            style={'textAlign':'center'}
        ),
        dbc.Row(
            dcc.Markdown(
                '''
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The Dataset that I chose (from https://www.kaggle.com/wendykan/lending-club-loan-data#loan.csv) 
                has data on over 2.2 million individual loan applications and 145 unique features. After some initial data exploration I decided to only 
                look at loans that had been finalized (either payed off, charged off, or defaulted). For this project I could have included open loans as 
                the target is return on investment and it is possible (and probable) to have made your money back while the loan is still open, however, 
                when doing so the return is often extremely low due to brand new loans that have not had time to generate any income. 
                So my first step was to seperate out all finalized loans.
                ```
                df = pd.read_csv(datapath + '\\loan.csv', low_memory=False)
                df.shape  
                (2260668, 145)
                

                loans_usable = ['Fully Paid', 'Charged Off', 'Default']
                df1 = df[df['loan_status'].isin(loans_usable)]
                df1.shape
                (1303638, 145)

                ```
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Next I noticed that there were around 58 columns that had over 500,000+ null values. Considering 
                that none of these features would end up in my final model I decided to drop them. I then exported a new .csv file with 1,303,638 loans and 
                87 features as working with multiple large dataframes slows the whole process down. Next I engineered the ROI feature:

                ```
                # First we'll drop the rows where funded_amnt_inv == 0 (1. There will be no return if there is no investment 2. Can't divide by 0 later!)
                df = df[df['funded_amnt_inv'] != 0]
                df['Return'] = df['total_pymnt_inv'] - df['funded_amnt_inv']
                df['ROI'] = ((df['Return']/df['funded_amnt_inv'])*100).round(4)
                ```
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; I did this by creating a `Return` feature which was the difference between amount invested and 
                total amount paid back to investors. Next, create the `ROI` feature by dividing `Return` by total amount invested and multiplying by 100 to 
                get a percent.\n\n

                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Next, I took a look at which features would be valid for use in the model. Many of the features 
                included are generated well AFTER the loan has been accepted, and are thus unuseable in the model (Time travel is still science fiction!). 
                After narrowing it down I defined a function to filter features, fill NaN values, convert date time features, and ordinally encode categorical 
                features (this also included my earlier `Return` and `ROI` creation).
                ```
                def wrangle(dataframe):
                feats = ['loan_amnt', 'term', 'int_rate', 'installment', 'sub_grade', 'emp_title', 'emp_length', 'home_ownership', 
                'annual_inc', 'verification_status', 'issue_d', 'purpose', 'title', 'zip_code', 'addr_state', 'dti', 'delinq_2yrs', 
                'earliest_cr_line', 'inq_last_6mths', 'open_acc', 'pub_rec', 'revol_bal', 'revol_util', 'total_acc', 'total_bal_ex_mort',
                'total_bc_limit', 'mo_sin_old_il_acct','mo_sin_old_rev_tl_op', 'num_accts_ever_120_pd', 'num_sats', 'total_pymnt_inv', 'funded_amnt_inv']

                # Features to fillna with 0
                na_fill = ['emp_length', 'mo_sin_old_il_acct', 'mo_sin_old_rev_tl_op', 'num_accts_ever_120_pd', 'num_sats', 
                'revol_util', 'dti', 'inq_last_6mths', 'total_bal_ex_mort', 'total_bc_limit']
                
                # DF to work with
                x = dataframe[feats].copy()
                
                # Remove loans that had no investments
                x = x[x['funded_amnt_inv'] != 0]
                
                # Create ROI and Return features
                x['Return'] = x['total_pymnt_inv'] - x['funded_amnt_inv']
                x['ROI'] = (x['Return']/x['funded_amnt_inv']*100)   

                # Drop income outliers
                x = x[(x['annual_inc'] > 10000) & (x['annual_inc'] < 500000)]

                # Fix date time 
                x['days_since_earliest_cr_line'] = (pd.to_datetime(x['issue_d']) - pd.to_datetime(x['earliest_cr_line'])).dt.days
                
                # Fill nans
                x[na_fill] = x[na_fill].fillna(0)
            
                # Cat encode categorical features and remove other columns
                encoder = ce.OrdinalEncoder()
                x = encoder.fit_transform(x.drop(columns=['issue_d', 'earliest_cr_line', 'total_pymnt_inv', 'funded_amnt_inv']))
                
                return x
                ```
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Unfortunately for me, I ended up using only 6 of these features in my final model, however, 
                many of these features were necessary to do much of the data exploration discussed in the [Insights](insights) section.

                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Next I made a pipeline including sklearn's `StandardScaler` and `RandomForestRegressor` and 
                used a `RandomizedSearchCV` to fit an initial model that I would use to get feature importances for 28 of the features. The results 
                were...a little disappointing to say the least.
                ```
                RFR Val MAE: 19.46089566971158
                Baseline MAE: 20.001037505776097
                Improvement over Baseline for Random Forest Regression: 0.5401418360645174
                ```
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; My Mean Absolute Error had only improved by .54 over the baseline but I was able to gather many 
                [insights](insights) from the outcome.\n
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; At this point I had decided to only use 'front facing' features so I created a new pipeline again 
                using `StandardScaler` but this time with `LGBMRegressor` from lightgbm and using a very large GridSearchCV. Even with the feature reduction 
                this change gave me a much better result:
                ```
                LGBM Test MAE: 16.685289066414494
                Baseline MAE for Test data: 20.223643467120777
                Improvement over Baseline for Light GBM Regression: 3.5383544007062824
                ```
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; As I stated before, this is in no way perfect, or necessarily even THAT good, but for only considering 
                a few features it is a great improvement over the baseline. I believe that including many of the hidden or backend features included in the data 
                set would allow someone to much more accurately predict the Return on Investment.
                '''
            )
        )
    ],
)

layout = dbc.Row([column1])