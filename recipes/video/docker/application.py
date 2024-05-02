from pinotdb import connect
import streamlit as st
import pandas as pd
from openai import OpenAI
from langchain_community.document_loaders import DataFrameLoader
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import time
from datetime import datetime

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
            ToDateTime(ts,'hh', 'America/Los_Angeles') as hr, 
            count(frame) as "count"
        from video
        where person <> 'none' and
            ts > ago('PT12H') 
        group by person, hr
        order by hr asc
        """
        curs.execute(sql)
        return pd.DataFrame(curs, columns=[item[0] for item in curs.description])

    def booth_activity_genai(self, query_text:str):

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
        results = [row for row in curs]
        frames = [row[0] for row in results]

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

        logs = [f'frame: [{log[0]}] - person [{log[1]}]: {log[2]}' for log in results]
        context_text = "\n\n---\n\n".join(logs)
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text, question=query_text)
        model = ChatOpenAI()
        return model.invoke(prompt), frames
        

##############
db = PinotVector(host="localhost")
df = db.booth_activity()
query_text = 'Summarize what has been happening at the booths in one sentence'
ai, frames = db.booth_activity_genai(query_text=query_text)
##############

st.set_page_config(
    page_title="Real-Time Booth Duty Dashboard",
    layout="wide",
)
placeholder = st.empty()

########

while True:
    df = db.booth_activity()
    ai, frames = db.booth_activity_genai(query_text=query_text)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    with placeholder.container():
        timeline, raw, genai = st.columns(3)
        with timeline:
            st.markdown(f'### Video Frames {current_time}')
            st.line_chart(df, x="hr", y='count', color='person')

        with raw:
            st.markdown(f'### Video Frames Raw {current_time}')
            st.dataframe(df)

        with genai:
            st.markdown(f'### Real-Time GenAI Evaluation of what is happening at the booth for the last 15 mins: {current_time}')
            st.write(f'{ai.content}\n\n**Source Frames**\n\n{' '.join([str(f) for f in frames])}')
        
        time.sleep(10)

    # now = datetime.now()
    # current_time = now.strftime("%H:%M:%S")
    # st.markdown(f'Current Time = {current_time}')
    
    # st.write("Video Frames")
    # # st.write(df)
    # st.line_chart(df, x="hr", y='count', color='person')

    # df

    



# select
# 	person, 
# 	hr,
# 	count (frame) over (PARTITION BY person ORDER BY hr ) as c
# from (select frame, ToDateTime(ts,'h', 'America/Los_Angeles') as hr, person from video)