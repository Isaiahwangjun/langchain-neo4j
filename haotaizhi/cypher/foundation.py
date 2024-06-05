# import_foundation = """
# LOAD CSV WITH HEADERS FROM $source_file_name AS row
#     FOREACH (name IN split(row.name, '\n') |
#         MERGE (person:Person {id: name})

#         MERGE (document:Document {text: coalesce(row.name + ',' + row.source, "Unknown"), source: $source_file_name})

#         FOREACH(ignoreMe IN CASE WHEN row.Foundation IS NOT NULL THEN [1] ELSE [] END |
#             FOREACH (Foundation IN split(row.Foundation, '\n') |
#                 MERGE (n:Foundation {id: Foundation})
#                 MERGE (person)-[r:Foundation]->(n)
#                 SET r.FoundationType = coalesce(row.FoundationType, "Unknown")
#                 SET r.srcID = coalesce(row.srcID, "Unknown")
#                 SET r.source = $source_file_name
#                 MERGE (n)<-[rr:MENTION]-(document)
#                 SET rr.source = $source_file_name
#             )
#         )
#     );
# """

import_foundation = """
LOAD CSV WITH HEADERS FROM $source_file_name AS row
    FOREACH (name IN split(row.name, '\n') |
        MERGE (person:Person {id: name})

        MERGE (document:Document {text: coalesce(row.name + ',' + row.source, "Unknown")})

        FOREACH(ignoreMe IN CASE WHEN row.Foundation IS NOT NULL THEN [1] ELSE [] END |
            FOREACH (Foundation IN split(row.Foundation, '\n') |
                MERGE (n:Foundation {id: Foundation})
                MERGE (person)-[r:Foundation]->(n)
                SET r.FoundationType = coalesce(row.FoundationType, "Unknown")
                SET r.srcID = coalesce(row.srcID, "Unknown")
                MERGE (n)<-[rr:MENTION]-(document)
            )
        )
    );
"""
