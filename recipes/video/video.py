import cv2
from transformers import pipeline
from sentence_transformers import SentenceTransformer
from PIL import Image
from multiprocessing.pool import ThreadPool
from confluent_kafka import Producer
import time, json
from pinotdb import connect

model = SentenceTransformer('clip-ViT-B-32')
captioner = pipeline("image-to-text",model="Salesforce/blip-image-captioning-base")

class Kafka():
    def __init__(self, topic:str, bootstrap='localhost:29092') -> None:
        self.p = Producer({'bootstrap.servers': bootstrap})
        self.topic = topic

    def send(self, key, data):
        try:
            self.p.produce(
                key=str(key),
                topic=self.topic, 
                value=data, 
                on_delivery=None)
            self.p.flush()
        except Exception as e:
            print(e)

def find_people(embedding:list[float], distance=.25, host='localhost', port=8099, scheme='http'):
    conn = connect(host=host, port=port, path='/query/sql', scheme=scheme)
    curs = conn.cursor()
    sql = f"""
        with DIST as (
            SELECT 
                name,
                cosine_distance(embedding, ARRAY{embedding}) AS distance
            from people
            where VECTOR_SIMILARITY(embedding, ARRAY{embedding}, 10)
        )
        select * from DIST
        where distance < {distance}
        order by distance asc
    """
    try:
        curs.execute(sql, queryOptions="useMultistageEngine=true")
        return [row[0] for row in curs]
    except Exception as e:
        print(e)
    finally:
        curs.close()

def capture_frames(kafka:Kafka, threshold, iframe, frame_number, ts):
    img_emb = model.encode(iframe).tolist()
    found = find_people(img_emb, distance=threshold)
    if len(found) != 0:
        for person in found:
            print(f'found {person} in frame [{frame_number}]')
            video = {
                "frame": frame_number,
                "person": person,
                "description": captioner(iframe)[0]['generated_text'],
                "embedding":img_emb,
                "ts": ts
            }
            kafka.send(frame_number, json.dumps(video))
    else:
        video = {
            "frame": frame_number,
            "person": 'none',
            "description": captioner(iframe)[0]['generated_text'],
            "embedding":img_emb,
            "ts": ts
        }
        kafka.send(frame_number, json.dumps(video))

def video(threshold=.3):
    video = cv2.VideoCapture(0)
    pool = ThreadPool(processes=10)
    kafka =  Kafka('video')
    try:
        frame_number = 0
        while True:
            success, frame = video.read()
            iframe = Image.fromarray(frame)

            if frame_number % 100 == 0 and success:
                pool.apply_async(capture_frames, (
                    kafka, 
                    threshold,
                    iframe, 
                    frame_number, 
                    round(time.time() * 1000)
                ))

            frame_number += 1
        
            cv2.imshow("frame", frame)
            cv2.waitKey(1)

    except Exception as e:
        print(e)
    finally:
        video.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
   video()

