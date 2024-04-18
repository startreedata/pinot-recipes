import pandas as pd
from sentence_transformers import SentenceTransformer
from PIL import Image
import os

model = SentenceTransformer('clip-ViT-B-32')
    
if __name__ == '__main__':
    rows = []
    images = os.listdir("./images")
    for i, f in enumerate(images):
        file = f'./images/{f}'
        name = f.split('.')[0]
        print(file)
        img_emb = model.encode(Image.open(file))
        rows.append({"name":name, "path":file, "embedding":img_emb.tolist()})

    print("exporting to parquet")
    df = pd.DataFrame(rows)
    df.to_parquet('out/image.embeddings.parquet.gzip', compression='gzip')
