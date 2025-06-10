import psycopg2
import json
import torch
from sentence_transformers import util


DB_CONFIG = {
    'dbname': 'openapi_db',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': 5432
}

def connect_db():
    return psycopg2.connect(**DB_CONFIG)

def calcular_similaridades():
    conn = connect_db()
    cur = conn.cursor()

    # Lê todos os registros da tabela openapi
    cur.execute("SELECT id, embedding FROM openapi")
    registros = cur.fetchall()


    print(f"Total registros: {len(registros)}")

    for i in range(len(registros)):
        id1, emb1_raw = registros[i]
        for j in range(i + 1, len(registros)):
            id2, emb2_raw = registros[j]

            emb1 = torch.tensor(json.loads(emb1_raw))
            emb2 = torch.tensor(json.loads(emb2_raw))

            similarity = util.cos_sim(emb1, emb2).item()

            print(f"{id1} -> {id2} -> {similarity}")
            cur.execute("""
                        INSERT INTO openapi_similarity (openapi_id_1, openapi_id_2, similarity)
                        VALUES (%s, %s, %s)
                        """, (id1, id2, similarity))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    print("Iniciando calculadora de similaridades")
    calcular_similaridades()
    print("Fim")
