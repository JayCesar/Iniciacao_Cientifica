CREATE OR REPLACE FUNCTION create_non_simplified_table(table_name TEXT)
RETURNS VOID AS $$
BEGIN
    EXECUTE FORMAT('
        CREATE TABLE IF NOT EXISTS %I (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(255),
            ponto geometry(Point, 4326)
        );', table_name);
    RAISE NOTICE 'Table % created successfully.', table_name;
END;
$$ LANGUAGE plpgsql;
