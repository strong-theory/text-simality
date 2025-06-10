CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS plpgsql;

CREATE TABLE IF NOT EXISTS openapi (
    id SERIAL PRIMARY KEY,
    file_name TEXT NOT NULL,
    conteudo TEXT NOT NULL,
    embedding VECTOR(384) NOT NULL
);

CREATE TABLE IF NOT EXISTS openapi_similarity (
    id SERIAL PRIMARY KEY,
    openapi_id_1 INTEGER NOT NULL REFERENCES openapi(id),
    openapi_id_2 INTEGER NOT NULL REFERENCES openapi(id),
    similarity FLOAT NOT NULL
);
