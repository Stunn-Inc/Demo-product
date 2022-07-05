# Draw a title and some text to the app:
'''
# This is the document title

This is some _markdown_.
'''
from re import X
import streamlit as st
import pandas as pd
import numpy as np
from  business_models import profit_timeSeries
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from prophet import Prophet

from utils.seasonalTrends import seasonalBar

st.set_page_config(
    page_title="RealTime Time Series P/L Forcasting",
    layout="wide",
)


date_rng = pd.date_range(start='1/6/2018', end='6/24/2022', freq='D')


data = pd.DataFrame(columns=['profit'], index=date_rng)
data['profit'] = np.random.normal(size=len(date_rng))


profit_timeSeries.add_trends(data, monthly_coff=[], weekly_coff=[1,1,-1,2,0,0,0,0])
profit_timeSeries.add_anomalys(data)

# run prediction
df = pd.DataFrame(columns=['ds','y'])

df['y'] = data['profit'].cumsum()
df['ds'] = data.index

dt = 18

m = Prophet()
m.fit(df.iloc[:-dt])

# produce prediction
future = m.make_future_dataframe(periods=365)
forecast = m.predict(future)
forecast.index = forecast['ds']

#produce anomalys
# forecast['y'] = df['y']
# forecast['uncertainty'] = forecast['yhat_upper'] - forecast['yhat_lower']
# forecast['anomaly'] = forecast.apply(lambda x: 'Yes' if(np.abs(x['y']) > forecast['yhat_upper'] or ) else 'No', axis = 1)

#display
fig =go.Figure(data=[
    # go.Scatter(
    #         x = data.index,
    #         y = data['profit'].cumsum(),
    #         mode='markers',
    #         showlegend=False,
    #         marker = {'color': 'black' }
    #     ),
    go.Scatter(
        x=forecast["ds"], 
        y=forecast['trend'], 
        name="Profit Trend", 
        showlegend=False
       ),
    go.Scatter(
            x=forecast["ds"].to_list()+forecast["ds"].to_list()[::-1], # x, then x reversed
            y=forecast["yhat_lower"].to_list()+forecast["yhat_upper"].to_list()[::-1], # upper, then lower reversed
            fill='toself',
            fillcolor='rgba(0,100,80,0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            hoverinfo="skip",
            showlegend=False
        ),
    ])

# add anomolies
# for anomaly in forecast[forecast['anomaly'] == 'Yes'].iloc:
#     fig.add_vline(x=anomaly['ds'], line_width=3, line_dash="dash", line_color="red")


fig.update_layout(xaxis={"rangeslider":{"visible":True},"type":"date"})
# fig.update_xaxes(
#     rangeslider_visible=True,
#     rangeselector=dict(
#         buttons=list([
#             dict(count=1, label="1m", step="month", stepmode="backward"),
#             dict(count=6, label="6m", step="month", stepmode="backward"),
#             dict(count=1, label="YTD", step="year", stepmode="todate"),
#             dict(count=1, label="1y", step="year", stepmode="backward"),
#             dict(step="all")
#         ])
#     )
# )
st.header("Profit Forecast")
st.plotly_chart(fig, config = {'displayModeBar': False})


# Trends part
col1, col2 = st.columns([1, 1])

weekly_trends = forecast['weekly'].iloc[0:8]
day_names = weekly_trends.index.day_name()
pattern = weekly_trends.diff().iloc[1:8]


fig = seasonalBar(pattern, day_names)
col1.header("Weekly Trends")
col1.plotly_chart(fig, config = {'displayModeBar': False})
# print(forecast['weekly'][:7])


yearly_trends = forecast[['yearly', 'yearly_lower', 'yearly_upper']]
yearly_trends = yearly_trends.loc[yearly_trends.index.year == yearly_trends.index.year[1]]
fig = go.Figure(data=[
    go.Scatter(x=yearly_trends.index, y=yearly_trends['yearly'], showlegend=False, name="Yearly Trend"),
    go.Scatter(
            x=yearly_trends.index.to_list()+yearly_trends.index.to_list()[::-1], # x, then x reversed
            y=yearly_trends["yearly_lower"].to_list()+yearly_trends["yearly_upper"].to_list()[::-1], # upper, then lower reversed
            fill='toself',
            fillcolor='rgba(0,100,80,0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            hoverinfo="skip",
            showlegend=False
        ),
    ])
fig.update_xaxes(
    dtick="M1",
    tickformat="%b\n",
    showspikes = True,
    )
fig.update_layout(hovermode="x")
col2.header("Yearly Trends")
col2.plotly_chart(fig, use_container_width=True, config = {'displayModeBar': False})