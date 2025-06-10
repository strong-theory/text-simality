import json
import torch
from sentence_transformers import util
import dao


def calculate_similarity():
    records = dao.list_open_apis()

    print(f"Total records: {len(records)}")

    for i in range(len(records)):
        id1, emb1_raw = records[i]
        for j in range(i + 1, len(records)):
            id2, emb2_raw = records[j]

            emb1 = torch.tensor(json.loads(emb1_raw))
            emb2 = torch.tensor(json.loads(emb2_raw))

            similarity = util.cos_sim(emb1, emb2).item()

            print(f"{id1} -> {id2} -> {similarity}")
            dao.save_similarity(id1, id2, similarity)


if __name__ == '__main__':
    print("Init similarity")
    calculate_similarity()
    print("finish similarity")
