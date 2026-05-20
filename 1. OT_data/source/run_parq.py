import duckdb

con = duckdb.connect()
path = "/mnt/c/Users/chieb/Downloads/OT_data/association_overall_direct/*.parquet"

# 1. Schema — what columns exist and what are their types?
con.sql(f"DESCRIBE SELECT * FROM '{path}'").show()

# 2. Size and shape
con.sql(f"SELECT COUNT(*) AS n_rows FROM '{path}'").show()

# 3. Look at a few rows
con.sql(f"SELECT * FROM '{path}' LIMIT 5").show()

# 4. Cardinality of the key dimensions
con.sql(f"""
    SELECT
        COUNT(DISTINCT targetId)         AS n_targets,
        COUNT(DISTINCT diseaseId)        AS n_diseases,
        COUNT(DISTINCT aggregationValue) AS n_sources
    FROM '{path}'
""").show()

con.sql(f"""
    SELECT aggregationValue AS source, COUNT(*) AS n_edges
    FROM '{path}'
    GROUP BY aggregationValue
    ORDER BY n_edges DESC
""").show()


