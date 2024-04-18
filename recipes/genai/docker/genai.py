#!/usr/bin/env python3

from langchain_community.embeddings import OpenAIEmbeddings
# from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import DataFrameLoader
from langchain.prompts import ChatPromptTemplate
import pandas as pd
from pinotdb import connect
from openai import OpenAI
import sys

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

class PinotVector():

    def __init__(self, host, port=8099, path='/query/sql', scheme='http', model='text-embedding-ada-002') -> None:
        self.conn = connect(host=host, port=port, path=path, scheme=scheme)
        self.client = OpenAI()
        self.model = model

    def get_embedding(self, text):
        text = text.replace("\n", " ")
        return self.client.embeddings.create(input = [text], model=self.model).data[0].embedding
    
    def similarity_search(self, query_text:str, dist:int=1, limit:int=10):

        search_embedding = self.get_embedding(query_text)

        curs = self.conn.cursor()
        sql = f"""
            SELECT 
                source, 
                content, 
                metadata,
                cosine_distance(embedding, ARRAY{search_embedding}) AS cosine
            from documentation
            having cosine < {dist}
            """
        
        curs.execute(sql)
        df = pd.DataFrame(curs, columns=[item[0] for item in curs.description])
        loader = DataFrameLoader(df, page_content_column="content")
        return loader.load()


if __name__ == "__main__":

    query_text = sys.argv[1]
    # Prepare the DB.
    db = PinotVector(host="pinot-broker")

    # Search the DB.
    results = db.similarity_search(query_text, dist=.5)
    if len(results) == 0:
        print(f"Unable to find matching results.")
    else:
        context_text = "\n\n---\n\n".join([doc.page_content for doc in results])
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text, question=query_text)

        model = ChatOpenAI()
        response_text = model.invoke(prompt)

        sources = [doc.metadata.get("source", None) for doc in results]
        print("response:                                                                     ")
        print(f'{response_text.content} \n')
        [print(f' - {source}') for source in sources]


