import zipfile
from matplotlib import pyplot as plt
from matplotlib import image as mpimg
from PIL import Image
from sentence_transformers import SentenceTransformer
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, wait
from tqdm import tqdm
import typer
from io import BytesIO 
import multiprocessing
import cv2
import os
from imgbeddings import imgbeddings

app = typer.Typer()
model = SentenceTransformer('clip-ViT-B-32')
ibed = imgbeddings()
face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def has_face(img):
    face = face_classifier.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))
    return len(face) != 0

# def get_file_images(img):
#         img = cv2.imread(img)
#         return has_face(img)

# def to_emb(entry, func, pbar):
#     try:
#         name, data = func(entry)
#         img = Image.open(data)
#         emb = model.encode(img)
#         face = has_face(img)
#     except Exception as e:
#         raise e

#     row = {
#         "name":name,
#         "embedding":emb,
#         "has_face": face
#     }
#     pbar.update()
#     return row

# def zip_entry(entry):
#     zi = entry[0]
#     zip = entry[1]
#     name = zi.filename
#     bytes = zip.read(zi)
#     return name, BytesIO(bytes)

# def to_parquet(enteries, func, start):
#     pbar = tqdm(total=len(enteries), desc=str(start))
#     rows = [to_emb(entry, func, pbar) for entry in enteries]
#     filtered = list(filter(lambda x: x['has_face'], rows))
#     col_removed = [{"name": f['name'], "embedding": f['embedding']} for f in filtered]

#     df = pd.DataFrame(col_removed, columns=['name','embedding'])
#     df.to_parquet(f'out/data_{pbar.desc}.parquet')
#     pbar.close()

def zip_worker(entries, name, zipfile):
    filtered = list(filter(lambda x: x.filename.endswith('.jpg'), entries))
    pbar = tqdm(total=len(files), desc=f'{name}-filter-jpg')
    filtered = list(filter(lambda x: {
        x.filename.endswith('.jpg'),
        pbar.update()
    }, entries))
    pbar.close()

    pbar = tqdm(total=len(filtered), desc='finding faces')
    faces = list(filter(lambda zi: {
        has_face(BytesIO(zip.read(zi))),
        pbar.update()
    }, filtered))
    pbar.close()

    def to_emb(entry, pbar):
        try:
            img = Image.open(entry)
            emb = model.encode(img)
        except Exception as e:
            raise e

        row = {
            "name":entry,
            "embedding":emb
        }
        pbar.update()
        return row

    rows = [to_emb(face, pbar) for face in faces]
    df = pd.DataFrame(rows, columns=['name','embedding'])
    df.to_parquet(f'out3/data_{pbar.desc}.parquet')
    pbar.close()


@app.command()
def zip(zip:str, limit:int=-1):
    z = zipfile.ZipFile(zip)
    filtered = list(filter(lambda x: x.filename.endswith('.jpg'), z.filelist))
    split(enteries=filtered[0:limit], worker=zip_worker, name="zip", zipfile=z)

def file_worker(files, name, directory):
    pbar = tqdm(total=len(files), desc=f'{name}-filter-jpg')
    def filter_jpg(img, pbar):
        pbar.update()
        return img.endswith('.jpg')
    filtered = list(filter(lambda x:filter_jpg(x, pbar), files))
    pbar.close()

    def get_faces(img, pbar):
        pbar.update()
        return has_face(cv2.imread(f'{directory}/{img}'))
    
    pbar = tqdm(total=len(filtered), desc=f'{name}-get-faces')
    faces = list(filter(lambda img: get_faces(img, pbar), filtered))
    pbar.close()

    pbar = tqdm(total=len(faces), desc=f'{name}-to-embedding')
    def to_emb(entry, pbar):
        try:
            img = Image.open(f'{directory}/{entry}')
            # emb = model.encode(img)
            emb = ibed.to_embeddings(img)[0]
        except Exception as e:
            print(e)
            raise e

        row = {
            "name":entry,
            "embedding":emb
        }
        pbar.update()
        return row

    rows = [to_emb(face, pbar) for face in faces]
    df = pd.DataFrame(rows, columns=['name','embedding'])
    df.to_parquet(f'out4/data_{pbar.desc}.parquet')
    pbar.close()

@app.command()
def files(directory:str, limit:int=None):
    images = os.listdir(directory)
    split(enteries=images[0:limit], worker=file_worker, name="file", directory=directory)
    

def split(enteries, worker, name, **kwargs):
    futures = []
    threads = int(multiprocessing.cpu_count() / 2)
    step = 100
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for i in range(0, len(enteries), step):
            start = i
            end = i + step
            futures.append(executor.submit(worker, enteries[start:end], f'{str(start)}-{name}', **kwargs))

        wait(futures)

    for f in futures:
        f.result()

if __name__ == "__main__":
    app()
