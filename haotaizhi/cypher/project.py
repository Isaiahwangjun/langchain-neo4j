import_project = """
LOAD CSV WITH HEADERS FROM $source_file_name AS row
    FOREACH (name IN split(row.name, '\n') |
        MERGE (person:Person {id: name})

        MERGE (document:Document {text: coalesce(row.name + ',' + row.source, "Unknown"), source: $source_file_name})

        FOREACH(ignoreMe IN CASE WHEN row.label_Project IS NOT NULL THEN [1] ELSE [] END |
            FOREACH (label_Project IN split(row.label_Project, '\n') |
                MERGE (n:Project {id: label_Project})
                MERGE (person)-[r:hasProject]->(n)
                SET r.srcID = coalesce(row.srcID, "Unknown")
                SET r.source = $source_file_name
                MERGE (n)<-[rr:MENTION]-(document)
                SET rr.source = $source_file_name
            )
        )
    );
"""
