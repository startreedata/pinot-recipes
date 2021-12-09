import streamlit as st
from pinotdb import connect
import pandas as pd
import plotly.express as px
from streamlit_tags import st_tags

st.set_page_config(layout="wide")
st.title("Chicago Crimes")

conn = connect(host='localhost', port=8099, path='/query/sql', scheme='http')
curs = conn.cursor()

curs.execute("""
select ToDateTime(min(DateEpoch), 'YYYY-MM-dd') AS min, 
       ToDateTime(max(DateEpoch), 'YYYY-MM-dd') as max
from crimes
""")

df = pd.DataFrame(curs, columns=[item[0] for item in curs.description])

st.markdown(f"""
This app is based on the [Chicago Crimes dataset](https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2) and covers crimes committed between {df["min"].values[0]} to {df["max"].values[0]}.
""")

conn = connect(host='localhost', port=8099, path='/query/sql', scheme='http')
curs = conn.cursor()

curs.execute("""
select Beat, count(*)
from crimes
GROUP BY Beat
ORDER BY count(*) DESC
LIMIT 30
""")

df = pd.DataFrame(curs, columns=[item[0] for item in curs.description])

figure = px.bar(df, 
    x='Beat', 
    y="count(*)",
    color_discrete_sequence=["#1d242d"],
)
figure.update_layout(
    margin=dict(l=0, r=0, t=0, b=0)
)

st.header("Crimes by beat")
st.plotly_chart(figure, use_container_width=True)


curs.execute("""
select DISTINCT Beat
from crimes
LIMIT 500
""")

df = pd.DataFrame(curs, columns=[item[0] for item in curs.description])

beats = st_tags(
    label='## Enter beats:',
    text='Press enter to add more',
    value=['0421'],
    suggestions=list(df["Beat"].values),
    maxtags = 10,
    key='1')

st.write(f"Selected beats: {', '.join(beats) if len(beats) > 0 else 'All'}")
if len(beats) == 0:
    beats = list(df["Beat"].values)

curs.execute("""
select count(*)
from crimes
WHERE Beat IN (%(beats)s)
""", {"beats": beats})
df_crimes = pd.DataFrame(curs, columns=[item[0] for item in curs.description])

curs.execute("""
select count(*)
from crimes
WHERE Beat IN (%(beats)s) AND Arrest = True
""", {"beats": beats})
df_arrests = pd.DataFrame(curs, columns=[item[0] for item in curs.description])

curs.execute("""
select count(*)
from crimes
WHERE Beat IN (%(beats)s) AND Domestic = True
""", {"beats": beats})
df_domestic = pd.DataFrame(curs, columns=[item[0] for item in curs.description])

df = pd.DataFrame([
    {
    "Type": "Crimes", 
    "Value": df_crimes['count(*)'].values[0]
    },
    {
    "Type": "Arrests", 
    "Value": df_arrests['count(*)'].values[0]
    },
        {
    "Type": "Domestic", 
    "Value": df_domestic['count(*)'].values[0]
    },
])

left1, right1 = st.columns(2)
with left1:
    figure = px.bar(df, 
        x='Value', 
        y="Type",
        color_discrete_sequence=["#1d242d"],
        orientation='h'
    )
    figure.update_layout(
        margin=dict(l=0, r=0, t=0, b=0)
    )
    st.subheader("Overall")
    st.plotly_chart(figure)

with right1:
    curs.execute("""
    select PrimaryType, count(*)
    from crimes
    WHERE Beat IN (%(beats)s) 
    GROUP BY PrimaryType
    ORDER BY count(*) DESC
    LIMIT 10
    """, {"beats": beats})

    df_types = pd.DataFrame(curs, columns=[item[0] for item in curs.description])

    figure = px.bar(df_types, 
        x='PrimaryType', 
        y="count(*)",
        color_discrete_sequence=["#1d242d"],
    )
    figure.update_layout(
        margin=dict(l=0, r=0, t=0, b=0)
    )
    st.subheader("Most popular crime types")
    st.plotly_chart(figure)


left2, right2 = st.columns(2)

with left2:
    curs.execute("""
    select HOUR(DateEpoch) AS hour, count(*)
    from crimes
    WHERE Beat IN (%(beats)s) 
    GROUP BY hour
    ORDER BY hour
    LIMIT 1000
    """, {"beats": beats})

    df_dates = pd.DataFrame(curs, columns=[item[0] for item in curs.description])

    figure = px.line(df_dates, 
        x='hour', 
        y="count(*)",
        color_discrete_sequence=["#00A3DE"],
    )
    figure.update_layout(
        margin=dict(l=0, r=0, t=0, b=0)
    )
    st.subheader("Crimes by hour")
    st.plotly_chart(figure)
with right2:
    curs.execute("""
    select ToDateTime(DATETRUNC('month',DateEpoch), 'yyyy-MM-dd') AS month, count(*)
    from crimes
    WHERE Beat IN (%(beats)s) 
    GROUP BY month
    ORDER BY month
    LIMIT 1000
    """, {"beats": beats})

    df_dates = pd.DataFrame(curs, columns=[item[0] for item in curs.description])

    figure = px.line(df_dates, 
        x='month', 
        y="count(*)",
        color_discrete_sequence=["#00A3DE"],
    )
    figure.update_layout(
        margin=dict(l=0, r=0, t=0, b=0)
    )
    st.subheader("Crimes over time")
    st.plotly_chart(figure)