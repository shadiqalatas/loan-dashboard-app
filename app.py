import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Load and prepare the data
df = pd.read_csv("./data/LuxuryLoanPortfolio.csv")

# Convert data types
df['funded_date'] = pd.to_datetime(df['funded_date'])
df['funded_amount'] = pd.to_numeric(df['funded_amount'])
df['loan_balance'] = pd.to_numeric(df['loan balance'])
df['interest_rate'] = pd.to_numeric(df['interest rate percent'])
df['payments'] = pd.to_numeric(df['payments'])
df['total_past_payments'] = pd.to_numeric(df['total past payments'])
df['property_value'] = pd.to_numeric(df['property value'])
df['duration_months'] = pd.to_numeric(df['duration months'])

# Data Preparation for Loan Performance Trends
df['year'] = df['funded_date'].dt.year
df['year_month'] = df['funded_date'].dt.to_period('M').astype(str)

funding_trend = df.groupby('year_month').agg({
    'funded_amount': 'sum',
    'loan_id': 'count'
}).reset_index()
funding_trend.columns = ['year_month', 'funded_amount', 'borrower_count']
funding_trend['year_month'] = pd.to_datetime(funding_trend['year_month'])

rate_trend = df.groupby('year_month')['interest rate'].mean().reset_index()
rate_trend['year_month'] = pd.to_datetime(rate_trend['year_month'])

# Data Preparation for Loan-to-Value Ratio Distribution
df['LTV'] = df['funded_amount'] / df['property_value']


# Data Preparation for Purpose Analysis on Interest Rate and Duration
purpose_analysis = df.groupby('purpose').agg({
    'interest_rate': 'mean',
    'duration_months': 'mean',
    'funded_amount': 'sum',
    'loan_id': 'count'
}).reset_index()

purpose_analysis.columns = ['purpose', 'avg_interest_rate', 'avg_duration_months', 'total_funded', 'loan_count']
purpose_analysis['avg_duration_years'] = purpose_analysis['avg_duration_months'] / 12

# Configure the App
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Luxury Loan Portfolio Dashboard", style={'textAlign': 'center', 'fontFamily':'sans-serif'}),
    
    html.Div([
        html.Div([
        dcc.Graph(id='purpose-analysis')
    ], style={'width': '48%', 'display': 'inline-block'}
    ),

        html.Div([
            dcc.Graph(id='ltv-distribution')
        ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
    ]),

    html.Div([
        dcc.Graph(id='loan-performance-trend')
    ]),
    
    
])


# Callback for purpose analysis
@app.callback(
    Output('purpose-analysis', 'figure'),
    Input('purpose-analysis', 'value')
)
def update_purpose_analysis(value):
    fig = px.scatter(purpose_analysis,
                     x='avg_interest_rate',
                     y='avg_duration_years',
                     size='total_funded',
                     color='purpose',
                     hover_name='purpose',
                     title='Loan Purpose Analysis on Interest Rate and Duration',
                     labels={'avg_interest_rate': 'Average Interest Rate (%)',
                            'avg_duration_years': 'Average Duration (Years)',
                            'total_funded': 'Total Funded Amount ($)'},
                     hover_data=['loan_count'])
    
    fig.update_layout(
        xaxis_title='Average Interest Rate (%)',
        yaxis_title='Average Duration (Years)',
        plot_bgcolor='white',
        height=500
    )

    for i in range(len(purpose_analysis)):
        fig.add_annotation(
            x=purpose_analysis['avg_interest_rate'].iloc[i],
            y=purpose_analysis['avg_duration_years'].iloc[i],
            text=purpose_analysis['purpose'].iloc[i],
            showarrow=False,
            font=dict(size=10),
            yshift=10
        )
    
    return fig

# Callback for LTV distribution
@app.callback(
    Output('ltv-distribution', 'figure'),
    Input('ltv-distribution', 'value')
)
def update_ltv_distribution(value):
    fig = px.histogram(df, x='LTV',
                       title='Loan-to-Value (LTV) Ratio Distribution',
                       labels={'LTV': 'LTV Ratio', 'count': 'Number of Loans'},
                       nbins=30,
                       color="purpose",
                       barmode='stack',
                       color_discrete_sequence=px.colors.sequential.Reds)

    fig.add_vline(x=0.8, line_dash="dash", line_color="orange",
                  annotation_text="80% LTV Threshold", annotation_position="top left")
    fig.add_vline(x=0.9, line_dash="dash", line_color="red",
                  annotation_text="90% LTV Threshold", annotation_position="top right")

    avg_ltv = df['LTV'].mean()
    fig.add_vline(x=avg_ltv, line_dash="dot", line_color="green",
                  annotation_text=f"Average: {avg_ltv:.2f}", annotation_position="bottom right")

    fig.update_layout(
        xaxis_title='Loan-to-Value Ratio',
        yaxis_title='Number of Loans',
        plot_bgcolor='white',
        height=500
    )
    
    return fig

# Callback for loan performance trend
@app.callback(
    Output('loan-performance-trend', 'figure'),
    Input('loan-performance-trend', 'value')
)
def update_loan_performance_trend(value):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=funding_trend['year_month'],
        y=funding_trend['funded_amount'],
        mode='lines+markers',
        name='Total Funding Amount',
        line=dict(color='#1f77b4'),
        yaxis='y'
    ))

    fig.add_trace(go.Scatter(
        x=funding_trend['year_month'],
        y=funding_trend['borrower_count'],
        mode='lines+markers',
        name='Number of Borrowers',
        line=dict(color='#ff7f0e'),
        yaxis='y2'
    ))

    fig.update_layout(
        title='Loan Performance Trends Over Time',
        xaxis=dict(title='Date'),
        yaxis=dict(
            title='Total Funding Amount ($)',
            side='left'
        ),
        yaxis2=dict(
            title='Number of Borrowers',
            side='right',
            overlaying='y'
        ),
        plot_bgcolor='white',
        hovermode='x unified',
        height=500,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    # Add range selector buttons
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1M", step="month", stepmode="backward"),
                    dict(count=6, label="6M", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1Y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(visible=True),
            type="date"
        )
    )
    
    return fig


# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050)