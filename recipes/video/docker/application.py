from pinotdb import connect
import streamlit as st
import pandas as pd

conn = connect(host="localhost", port=8099, path='/query/sql', scheme='http')
curs = conn.cursor()
sql = f"""
select person, ToDateTime(ts,'h:mm') as t, count(frame) as c
from video
group by person, t
order by t
"""
curs.execute(sql)
df = pd.DataFrame(curs, columns=[item[0] for item in curs.description])

st.write("Video Frames")
# st.write(df)
st.line_chart(df, x="t", y='c', color='person')

