import duckdb

con = duckdb.connect()

con.sql("""
    CREATE TABLE ensembl_to_ncbi AS
    SELECT DISTINCT
        Ensembl_gene_identifier AS ensembl_id,
        GeneID                  AS ncbi_gene_id
    FROM read_csv(
        '/mnt/c/Users/chieb/Downloads/OT_data/gene2pubmed/gene2ensembl',
        delim='\t',
        header=true,
        columns={
            'tax_id': 'INTEGER',
            'GeneID': 'INTEGER',
            'Ensembl_gene_identifier': 'VARCHAR',
            'RNA_nucleotide_accession_version': 'VARCHAR',
            'Ensembl_rna_identifier': 'VARCHAR',
            'protein_accession_version': 'VARCHAR',
            'Ensembl_protein_identifier': 'VARCHAR'
        },
        nullstr='-'
    )
    WHERE tax_id = 9606
""")

con.sql("""
    SELECT
        COUNT(*) AS total_rows,
        COUNT(DISTINCT ensembl_id) AS unique_ensembl,
        COUNT(DISTINCT ncbi_gene_id) AS unique_ncbi
    FROM ensembl_to_ncbi
""").show()

target_path = "/mnt/c/Users/chieb/Downloads/OT_data/target/*.parquet"

con.sql(f"""
    SELECT
        t.biotype,
        COUNT(*) AS n_total,
        SUM(CASE WHEN m.ncbi_gene_id IS NOT NULL THEN 1 ELSE 0 END) AS n_mapped,
        ROUND(100.0 * SUM(CASE WHEN m.ncbi_gene_id IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_mapped
    FROM '{target_path}' t
    LEFT JOIN ensembl_to_ncbi m ON t.id = m.ensembl_id
    GROUP BY t.biotype
    ORDER BY n_total DESC
""").show()

# pub_counts built as before from gene2pubmed
# Then join on ncbi_gene_id

# Step A: aggregate gene2pubmed to per-gene publication counts (human only)
con.sql("""
    CREATE TABLE pub_counts AS
    SELECT
        GeneID AS ncbi_gene_id,
        COUNT(DISTINCT PubMed_ID) AS n_publications
    FROM read_csv(
        '/mnt/c/Users/chieb/Downloads/OT_data/gene2pubmed/gene2pubmed',
        delim='\t',
        header=true,
        columns={'tax_id': 'INTEGER', 'GeneID': 'INTEGER', 'PubMed_ID': 'BIGINT'}
    )
    WHERE tax_id = 9606
    GROUP BY GeneID
""")

# Step B: join attention onto Ensembl IDs via the mapping you just built
con.sql("""
    CREATE TABLE gene_attention AS
    SELECT
        m.ensembl_id,
        m.ncbi_gene_id,
        COALESCE(p.n_publications, 0) AS n_publications
    FROM ensembl_to_ncbi m
    LEFT JOIN pub_counts p USING (ncbi_gene_id)
""")

# Sanity checks: top genes should be the famous ones
target_path = "/mnt/c/Users/chieb/Downloads/OT_data/target/*.parquet"

con.sql(f"""
    SELECT t.approvedSymbol, t.biotype, a.n_publications
    FROM gene_attention a
    JOIN '{target_path}' t ON a.ensembl_id = t.id
    ORDER BY a.n_publications DESC
    LIMIT 15
""").show()

# Distribution summary
con.sql("""
    SELECT
        COUNT(*) AS total,
        SUM(CASE WHEN n_publications = 0 THEN 1 ELSE 0 END) AS zero_pubs,
        AVG(n_publications) AS mean_pubs,
        MEDIAN(n_publications) AS median_pubs,
        MAX(n_publications) AS max_pubs
    FROM gene_attention
""").show()

# Persist
con.sql("""
    COPY gene_attention TO
    '/mnt/c/Users/chieb/Downloads/OT_data/gene2pubmed/gene_attention.parquet'
    (FORMAT PARQUET)
""")
