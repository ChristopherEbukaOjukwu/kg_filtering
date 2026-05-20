import duckdb

con = duckdb.connect()

target_path  = "/mnt/c/Users/chieb/Downloads/OT_data/target/*.parquet"
overall_path = "/mnt/c/Users/chieb/Downloads/OT_data/association_overall_direct/*.parquet"

con.sql(f"""
    SELECT t.biotype, COUNT(DISTINCT a.targetId) AS n_targets_with_associations
    FROM '{overall_path}' a
    LEFT JOIN '{target_path}' t ON a.targetId = t.id
    GROUP BY t.biotype
    ORDER BY n_targets_with_associations DESC
""").show()
