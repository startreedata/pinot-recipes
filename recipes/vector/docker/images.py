#!/usr/bin/env python3

import pandas as pd
from pinotdb import connect
from sentence_transformers import SentenceTransformer
from PIL import Image
from matplotlib import pyplot as plt
from matplotlib import image as mpimg
import os, sys

model = SentenceTransformer('clip-ViT-B-32')

def seed():
    print("creating embeddings from images")
    rows = []
    images = os.listdir("./images")
    for i, f in enumerate(images):
        file = f'./images/{f}'
        print(file)
        img_emb = model.encode(Image.open(file))
        rows.append({"id":i, "path":file, "embedding":img_emb.tolist()})

    print("exporting to parquet")
    df = pd.DataFrame(rows)
    df.to_parquet('out/image.embeddings.parquet.gzip', compression='gzip')


def search(query_string:str):    
    search_embedding = model.encode(query_string)
    print(len(search_embedding.tolist()))

    conn = connect(host='pinot-broker', port=8099, path='/query/sql', scheme='http')
    curs = conn.cursor()
    sql = f"""
    SELECT 
        id,
        path,
        l2_distance(embedding, ARRAY{search_embedding.tolist()}) AS l2_dist
    from images
    order by l2_dist asc
    limit 2
    """
    curs.execute(sql)

    for row in curs:
        print(row)
        show(row[1], row[2])
    
def show(path, distance):
    plt.title(f'{path} {distance}')
    image = mpimg.imread(path)
    plt.imshow(image)
    plt.show()

if __name__ == '__main__':

    args = sys.argv

    if len(args) > 1 and args[1] == '--seed':
        seed()
    elif len(args) > 1 and args[1] == '--search':
        search(args[2])

