CREATE OR REPLACE FUNCTION create_simplified_table(
    simplified_table_name TEXT,
    non_simplified_table_name TEXT
)
RETURNS VOID AS $$
DECLARE
    combined_table_name TEXT;
    clean_non_simplified_name TEXT;
BEGIN
    clean_non_simplified_name := REPLACE(non_simplified_table_name, 'non_simplified_points_', '');
	
    combined_table_name := simplified_table_name || '_' || clean_non_simplified_name;

    IF NOT EXISTS (
        SELECT 1 FROM information_schema.tables
        WHERE table_name = combined_table_name
    ) THEN
        BEGIN
            EXECUTE FORMAT('
                CREATE TABLE %I (
                    id SERIAL PRIMARY KEY,
                    simplified_nome VARCHAR(255),
                    simplified_ponto GEOMETRY(Point, 4326),
                    non_simplified_id INT REFERENCES %I(id)
                );', combined_table_name, non_simplified_table_name);

            RAISE NOTICE 'Table % created successfully.', combined_table_name;

        EXCEPTION
            WHEN OTHERS THEN
                RAISE NOTICE 'Error creating table: %', SQLERRM;
        END;

    ELSE
        RAISE NOTICE 'Table % already exists.', combined_table_name;
    END IF;

END;
$$ LANGUAGE plpgsql;
