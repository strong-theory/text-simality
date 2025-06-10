import os
import json
import psycopg2
from sentence_transformers import SentenceTransformer

# Configurações do banco
DB_CONFIG = {
    'dbname': 'openapi_db',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': 5432
}

# Caminho para os arquivos OpenAPI
OPENAPI_DIR = 'openapis'

# Modelo para gerar embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

def connect_db():
    return psycopg2.connect(**DB_CONFIG)

def salvar_openapis():
    conn = connect_db()
    cur = conn.cursor()

    for nome_arquivo in os.listdir(OPENAPI_DIR):
        if nome_arquivo.endswith('.json'):
            caminho = os.path.join(OPENAPI_DIR, nome_arquivo)

            with open(caminho, 'r', encoding='utf-8') as f:
                conteudo_raw = f.read()
                try:
                    json.loads(conteudo_raw)
                except json.JSONDecodeError as e:
                    print(f"Erro ao parsear {nome_arquivo}: {e}")
                    continue

                # Gerar embedding
                embedding = model.encode(conteudo_raw, convert_to_tensor=True)

                # Salvar no banco com nome do arquivo
                cur.execute(
                    "INSERT INTO openapi (file_name, conteudo, embedding) VALUES (%s, %s, %s)",
                    (nome_arquivo, conteudo_raw, embedding.tolist())
                )
                print(f"Arquivo {nome_arquivo} salvo com sucesso.")

    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    salvar_openapis()
