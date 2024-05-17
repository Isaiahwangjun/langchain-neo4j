import_organizationInfo = """
LOAD CSV WITH HEADERS FROM $source_file_name AS row
    MERGE (n:Organization {srcID: row.srcID})
    SET n.id = row.org_name
    SET n.source = $source_file_name
"""
