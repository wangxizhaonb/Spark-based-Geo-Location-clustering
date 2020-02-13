import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

##### step 1

# df = pd.read_csv('test1000.csv') #lat ,lon, date ,manufacturer, model, deviceId
# df = pd.read_csv('test.csv')
# df['text'] = df['date'] + ' ' + df['manufacturer'] + ' ' + df['model'] + ' ' + df['deviceId'].astype(str)

##### step 2
# df = pd.read_csv('geo.csv')
# df['text'] = df['ID']

##### step 3
# df = pd.read_csv('geoLarge.csv')
# df['text'] = df['URL']

##### data1
df = pd.read_csv('data1.csv') #lat ,lon, cluster
# df['text'] = 'cluster ' + df['cluster'].astype(str)
# df = pd.read_csv('data1Boundry.csv') #lat ,lon, cluster
df['text'] = 'cluster ' + df['cluster'].astype(str)

cdf = pd.read_csv('centerData.csv')



fig = go.Figure(
        data=go.Scattergeo(
        lon = df['long'],
        lat = df['lat'],
        # text = df['text'],
        mode = 'markers',
        # name= "a",
        marker = dict(
                size = 2,
                opacity = 0.5,
                color = df["cluster"],
                ),
        )
    )
fig.add_trace(go.Scattergeo(
        lon = cdf['long'],
        lat = cdf['lat'],
        # text = cdf['text'],
        mode = 'markers',
        # name= "a",
        marker = dict(
                size = 10,
                opacity = 1,
                color = 'Gray',
                ),
        )
)

fig.update_layout(
        title = 'CSE427 Final ',
        # geo_scope='usa',
    )
fig.show()