from pinotdb import connect
import streamlit as st
import pandas as pd
from openai import OpenAI
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
            ToDateTime(ts, 'M/d HH') as hr, 
            count(frame) as "count"
        from video
        where 
            person <> 'none' 
            --and person <> 'hubert' 
        group by hr, person
        order by hr desc
        """
        curs.execute(sql)
        rows = [row for row in curs]
        return pd.DataFrame(rows, columns=[item[0] for item in curs.description])
    
    def total_booth_activity(self):
        curs = self.conn.cursor()
        sql = f"""
            select 
                person, 
                count(frame) as "count"
            from video
            where 
                person <> 'none' 
                --and person <> 'hubert' 
            group by person
            order by "count" desc
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
                and person <> 'hubert'
                -- and where VECTOR_SIMILARITY(embedding, ARRAY{search_embedding}, 10)
            order by ts desc
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
query_text = 'Summarize what has been happening at the booths in one sentence'
##############

st.set_page_config(
    page_title="Real-Time Booth Duty Dashboard",
    layout="wide",
)
placeholder = st.empty()

########

while True:
    df = db.booth_activity()
    totals = db.total_booth_activity()
    ai, frames = db.booth_activity_genai(query_text=query_text)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    with placeholder.container():
        timeline, genai = st.columns(2)
        with timeline:
            st.markdown(f'### Video Frames {current_time}')
            st.bar_chart(df, x="hr", y='count', color='person')
            st.markdown(f'### Video Frames Total {current_time}')
            st.dataframe(totals)

        with genai:
            st.markdown(f'### Real-Time GenAI Evaluation of what is happening at the booth for the last 15 mins: {current_time}')
            frame_str = ' '.join([str(f) for f in frames])
            st.write(f'{ai.content}\n\n**Source Frames**\n\n{frame_str}')
        
        time.sleep(15)

