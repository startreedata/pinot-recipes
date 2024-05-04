from pinotdb import connect
from flask import Flask, request, send_from_directory, send_file
from sentence_transformers import SentenceTransformer, util
import zipfile
from PIL import Image
import sys, io, os
import traceback
from imgbeddings import imgbeddings


app = Flask(__name__)
model = SentenceTransformer('clip-ViT-B-32')
ibed = imgbeddings()

cache = {}

def get_zip_entry(pid):
    try:
        path = f'data/startree-celebs/{pid}.jpg'
        if os.path.isfile(path):
            return open(path, "rb").read()
        else:
            z = zipfile.ZipFile('data/celebrities2.zip')
            for zi in z.filelist:
                if pid in zi.filename:
                    return z.read(zi.filename)
    except Exception as e:
        raise Exception(f'{pid} not found in celebrity images: {e}')


@app.route('/')
def home():
   return send_from_directory(
       directory='.',
       path='index.html')

@app.route('/images/<string:pid>.jpg')
# @app.route('/images/100k/100k/<string:pid>.jpg')
def get_image(pid):
    if pid in cache:
        image_binary = cache.get(pid)
    else:
        image_binary = get_zip_entry(pid)
        cache[pid] = image_binary

    return send_file(
        io.BytesIO(image_binary),
        mimetype='JPG',
        as_attachment=True,
        download_name='%s.jpg' % pid)


@app.route('/upload', methods=['POST'])
def upload():
    image_bytes = request.files['image'].read()
    image = Image.frombytes('RGBA', (150,150), image_bytes, 'raw')

    try:
        # embedding = model.encode(image, show_progress_bar=True).tolist()
        embedding = ibed.to_embeddings(image)[0].tolist()
        conn = connect(host="localhost", port=8099, path='/query/sql', scheme='http')
        curs = conn.cursor()
        sql = f"""
                SELECT 
                    name,
                    cosine_distance(embedding, ARRAY{embedding}) AS cosine, 
                    l2_distance(embedding, ARRAY{embedding}) AS l2, 
                    l1_distance(embedding, ARRAY{embedding}) AS l1
                from celebrities_cosine_768
                --where 
                    --VECTOR_SIMILARITY(embedding, ARRAY{embedding}, 10) 
                    --name like 'hubert%'
                order by cosine asc
                limit 20
            """
        curs.execute(sql)
        rows = []
        keys = []
        for row in curs:
            print(f'{row[0]} {row[1]} {row[2]} {row[3]}', file=sys.stderr)
            if row[0] not in keys:
                keys.append(row[0])
                rows.append(row)
        return rows
    
    except Exception as e:
        traceback.print_exc()
        print(e, file=sys.stderr)
        return e

if __name__ == '__main__':
    app.run(port=9100)

