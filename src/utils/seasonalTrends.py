import plotly.graph_objects as go
import pandas as pd

legend = {
    True: 'Blue',
    False: 'Red'
    }

def seasonalBar(data, monoTrends_label):
    '''
        Seasonal Bars, color coded and labeled based on if implying good or bad
    
    '''

    label = data > 0

    bars = []
    # Display Trends
    for monoTrends in range(0,len(data)):
        bars +=  [go.Bar( x=[ monoTrends_label[monoTrends] ], y=[ data[monoTrends] ], marker={'color': legend[label[monoTrends]]}, name="") ]
    fig = go.FigureWidget(data=bars)
    fig.update(layout_showlegend=False)

    return fig