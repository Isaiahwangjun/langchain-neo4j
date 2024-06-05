# import_award = """
# LOAD CSV WITH HEADERS FROM $source_file_name AS row
#         MERGE (award:Award {srcID: row.srcID})
#         ON CREATE SET award.id = coalesce(row.Award, "Unknown")
#         FOREACH(ignoreMe IN CASE WHEN row.name IS NOT NULL THEN [1] ELSE [] END |
#             FOREACH (name IN split(row.name, '\n') |
#                 MERGE (person:Person {id: name})
#                 MERGE (person)-[r:hasAward]->(award)
#                 SET r.source = $source_file_name
#             )
#         );
# """
import_award = """
LOAD CSV WITH HEADERS FROM $source_file_name AS row
        MERGE (award:Award {srcID: row.srcID})
        ON CREATE SET award.id = coalesce(row.Award, "Unknown")
        FOREACH(ignoreMe IN CASE WHEN row.name IS NOT NULL THEN [1] ELSE [] END |
            FOREACH (name IN split(row.name, '\n') |
                MERGE (person:Person {id: name})
                MERGE (person)-[r:hasAward]->(award)
            )
        );
"""
