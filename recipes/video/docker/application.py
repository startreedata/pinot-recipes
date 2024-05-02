from pinotdb import connect
import streamlit as st
import pandas as pd
from openai import OpenAI
from langchain_community.document_loaders import DataFrameLoader
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

class PinotVector():
    def __init__(self, host, port=8099, path='/query/sql', scheme='http', model='text-embedding-ada-002') -> None:
        self.conn = connect(host=host, port=port, path=path, scheme=scheme)
        self.client = OpenAI()
        self.model = model

    def get_embedding(self, text):
        text = text.replace("\n", " ")
        return self.client.embeddings.create(input = [text], model=self.model).data[0].embedding
    
    def booth_activity(self):
        curs = self.conn.cursor()
        sql = f"""
        select 
            person, 
            ToDateTime(ts,'h', 'America/Los_Angeles') as hr, 
            count(frame) as "count"
        from video
        where person <> 'none' and
            ts > ago('PT12H') 
        group by person, hr
        order by hr
        """
        curs.execute(sql)
        return pd.DataFrame(curs, columns=[item[0] for item in curs.description])

    def similarity_search(self, query_text:str):

        search_embedding = self.get_embedding(query_text)
        
        curs = self.conn.cursor()
        sql = f"""
            SELECT 
                frame,
                person,
                description
            from video
            where 
                ts > ago('PT15M') 
                -- and where VECTOR_SIMILARITY(embedding, ARRAY{search_embedding}, 10)
            order by frame desc
            limit 50
            """
        
        curs.execute(sql)
        return [row for row in curs]
        

db = PinotVector(host="localhost")

df = db.booth_activity()
st.write("Video Frames")
# st.write(df)
st.line_chart(df, x="hr", y='count', color='person')

df

PROMPT_TEMPLATE = """
Below are video logs for the last 15 minutes. They contain descriptions 
of video frames and the name of a person that was found in the frame if
one was identified.

No logs indicates the video stream has just started.

Answer the question based on this log:
----

{context}

----
Based on the above video frame descriptions, answer this question:

{question}
"""

query_text = 'Summarize what has been happening at the booths?'

results = db.similarity_search(query_text)
logs = [f'frame: [{log[0]}] - person [{log[1]}]: {log[2]}' for log in results]
context_text = "\n\n---\n\n".join(logs)
prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
prompt = prompt_template.format(context=context_text, question=query_text)

print(prompt)

model = ChatOpenAI()
response_text = model.invoke(prompt)

frames = [row[0] for row in results]


st.markdown("""
    ***Real-Time GenAI Evaluation of what is happening at the booth for the last 15mins:***
""")

response_text.content

st.markdown("**Frames:**")
frames


# select
# 	person, 
# 	hr,
# 	count (frame) over (PARTITION BY person ORDER BY hr ) as c
# from (select frame, ToDateTime(ts,'h', 'America/Los_Angeles') as hr, person from video)