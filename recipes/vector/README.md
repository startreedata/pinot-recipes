# Similarity Search with Apache Pinot Vector Index


## Build a Pre-released version of Apache Pinot

```bash
# Clone a repo
git clone https://github.com/apache/pinot.git
cd pinot

# Build Pinot
mvn clean install -DskipTests -Pbin-dist

# Run the Quick Demo
cd build/
bin/quick-start-batch.sh
```

## Fine Food Reviews Example

Apache Pinot comes with a built-in table with embeddings of reviews of fine foods. The embeddings were created using the `text-embedding-ada-002` from [OpenAI](https://platform.openai.com/docs/guides/embeddings/embedding-models).

To perform a similarity search, we will need to use the same model to generate an embedding from our search query.

Search queries using embeddings aren't convenient to author in a SQL editor. Embeddings are high dimensional vectors (arrays) that aren't easy to type. We want to use a model to convert unstructured data into an embedding. Then, set that embedding into the SQL statement.

Run the example using Python below. The application will prompt you for a search query of the reviews. We suggest this query: `tomato soup`. 

```bash
$ python fine_food_reviews.py
what do you want to eat? tomato soup
['B0046H30M8', 'great soup', 4, 0.5498560408357057]
['B000LKTTTW', 'Best tomato soup', 5, 0.5560827995927847]
['B0042WXFJU', 'Tasty, but....', 4, 0.5712535523938602]
['B001NGAT9W', 'A Hit!', 5, 0.5916323445185989]
['B0058CGLH6', "If you like Campbells Pepper pot soup then don't buy this!", 1, 0.5929770105173966]
['B0005Z7GMA', 'Mrs. Dash Tomato Basil Garlic', 5, 0.5954086280399798]
```

```python
from pinotdb import connect
from openai import OpenAI

model = 'text-embedding-ada-002'
search = input("what do you want to eat? ")

client = OpenAI()

def get_embedding(text, model=model):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

search_embedding = get_embedding(search)

conn = connect(host='localhost', port=8000, path='/query/sql', scheme='http')
curs = conn.cursor()
curs.execute(f"""
SELECT 
  ProductId, 
  Summary, 
  Score,
  l2_distance(embedding, ARRAY{search_embedding}) AS l2_dist
from fineFoodReviews
where VECTOR_SIMILARITY(embedding, ARRAY{search_embedding}, 5)
order by l2_dist asc
""")

for row in curs:
    print(row)



```

# Image Search Example

WIP

## Build Segments


## Load Segments


## Search For Images

