-- Criando uma tabela
CREATE TABLE pontos_xy (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255),
    ponto geometry(Point, 4326)
);

-- Criando extensão (caso não tenha adiconado antes)


CREATE EXTENSION postgis;

-- Inserindo dados
INSERT INTO pontos_xy (nome, ponto) VALUES
    ('Ponto A', ST_SetSRID(ST_MakePoint(-43.12345, -22.98765), 4326)),
    ('Ponto B', ST_SetSRID(ST_MakePoint(-43.23456, -22.87654), 4326)),
    ('Ponto C', ST_SetSRID(ST_MakePoint(-43.34567, -22.76543), 4326));

-- Consultando todos os dados
SELECT * FROM pontos_xy;

-- Consultando apenas as coordenadas
SELECT ST_X(ponto) AS coordenada_x, ST_Y(ponto) AS coordenada_y FROM pontos_xy;