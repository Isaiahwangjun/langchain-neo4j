import_organization = """
LOAD CSV WITH HEADERS FROM $source_file_name AS row
    FOREACH (name IN split(row.name, '\n') |
        MERGE (person:Person {id: name})

        MERGE (document:Document {text: coalesce(row.name + ',' + row.source, "Unknown"), source: $source_file_name})

        FOREACH(ignoreMe IN CASE WHEN row.Founded IS NOT NULL THEN [1] ELSE [] END |
            FOREACH (orgName IN split(row.Founded, '\n') |
                MERGE (founded:Organization {id: orgName})
                MERGE (person)-[r:FOUNDED]->(founded)
                SET r.StartDate = coalesce(row.StartDate, "Unknown")
                SET r.EndDate = coalesce(row.EndDate, "Unknown")
                SET r.Position = coalesce(row.Position, "Unknown")
                SET r.srcID = coalesce(row.srcID, "Unknown")
                SET r.source = $source_file_name
                MERGE (founded)<-[rr:MENTION]-(document)
                SET rr.source = $source_file_name
            )
        )

        FOREACH(ignoreMe IN CASE WHEN row.Participant IS NOT NULL THEN [1] ELSE [] END |
            FOREACH (orgName IN split(row.Participant, '\n') |
                MERGE (participant:Organization {id: orgName}) 
                MERGE (person)-[r:HAS_PARTICIPANT]->(participant)
                SET r.StartDate = coalesce(row.StartDate, "Unknown")
                SET r.EndDate = coalesce(row.EndDate, "Unknown")
                SET r.Position = coalesce(row.Position, "Unknown")
                SET r.srcID = coalesce(row.srcID, "Unknown")
                SET r.source = $source_file_name
                MERGE (participant)<-[rr:MENTION]-(document)
                SET rr.source = $source_file_name
            )
        )
    );
    """
