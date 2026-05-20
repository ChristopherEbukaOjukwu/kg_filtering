import duckdb

con = duckdb.connect()

# Human only, count distinct PMIDs per gene
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

con.sql("SELECT COUNT(*) AS n_genes FROM pub_counts").show()
con.sql("SELECT * FROM pub_counts ORDER BY n_publications DESC LIMIT 10").show()
