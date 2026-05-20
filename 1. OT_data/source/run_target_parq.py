import duckdb

con = duckdb.connect()
path = "/mnt/c/Users/chieb/Downloads/OT_data/target/*.parquet"

# 1. Schema sanity check
con.sql(f"DESCRIBE SELECT * FROM '{path}'").show()

# 2. Row count — should be ~63k (Open Targets includes more than just the
#    ~31k targets that appear in associations)
con.sql(f"SELECT COUNT(*) AS n_rows FROM '{path}'").show()

# 3. Biotype distribution — your F4 lives here
con.sql(f"""
    SELECT biotype, COUNT(*) AS n
    FROM '{path}'
    GROUP BY biotype
    ORDER BY n DESC
""").show()

# 4. Chromosome distribution (struct field access uses dot notation)
con.sql(f"""
    SELECT genomicLocation.chromosome AS chrom, COUNT(*) AS n
    FROM '{path}'
    GROUP BY chrom
    ORDER BY n DESC
""").show()

# 5. Sample a few rows of the scalar columns only (nested structs/arrays
#    are unreadable in a wide print)
con.sql(f"""
    SELECT id, approvedSymbol, approvedName, biotype,
           genomicLocation.chromosome AS chrom,
           genomicLocation.start AS start_pos
    FROM '{path}'
    LIMIT 10
""").show()

# 6. Coverage of optional fields you might want as H3 features
con.sql(f"""
    SELECT
        COUNT(*) AS total,
        COUNT("constraint") AS has_constraint,
        COUNT(targetClass) AS has_target_class,
        COUNT(tractability) AS has_tractability,
        COUNT(tep) AS has_tep
    FROM '{path}'
""").show()

# 7. How many targets have a non-empty GO annotation list?
#    (Arrays are NULL-or-non-empty; len() gives length)
con.sql(f"""
    SELECT
        COUNT(*) AS total,
        SUM(CASE WHEN len(go) > 0 THEN 1 ELSE 0 END) AS has_any_go,
        AVG(len(go)) AS mean_n_go_terms,
        AVG(len(pathways)) AS mean_n_pathways
    FROM '{path}'
""").show()

