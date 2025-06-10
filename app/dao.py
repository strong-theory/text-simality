import psycopg2


DB_CONFIG = {
    'dbname': 'openapi_db',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': 5432
}


def connect_db():
    return psycopg2.connect(**DB_CONFIG)


def list_open_apis():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT id, embedding FROM openapi")
    records = cur.fetchall()

    conn.commit()
    conn.close()
    cur.close()

    return records

def save_similarity(id1, id2, similarity):

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
                INSERT INTO openapi_similarity (openapi_id_1, openapi_id_2, similarity)
                VALUES (%s, %s, %s)
                """, (id1, id2, similarity))

    conn.commit()
    conn.close()
    cur.close()


def save_open_api(nome_arquivo, conteudo_raw, embedding):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute(
        'INSERT INTO openapi (file_name, conteudo, embedding) VALUES (%s, %s, %s)',
        (nome_arquivo, conteudo_raw, embedding)
    )

    conn.commit()
    conn.close()
    cur.close()
