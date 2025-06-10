import os
import json
import dao
from sentence_transformers import SentenceTransformer


OPENAPI_DIR = 'openapis'

model = SentenceTransformer('all-MiniLM-L6-v2')


def save_open_apis():

    for file_name in os.listdir(OPENAPI_DIR):
        if file_name.endswith('.json'):
            path = os.path.join(OPENAPI_DIR, file_name)

            with open(path, 'r', encoding='utf-8') as f:
                raw_open_api = f.read()
                try:
                    json.loads(raw_open_api)
                except json.JSONDecodeError as e:
                    print(f"Error parsing {file_name}: {e}")
                    continue

                # generating embedding
                embedding = model.encode(raw_open_api, convert_to_tensor=True)

                dao.save_open_api(file_name, raw_open_api, embedding.tolist())
                print(f"File {file_name} successfully saved.")


if __name__ == '__main__':
    save_open_apis()
