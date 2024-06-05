# import_relationship = """
# LOAD CSV WITH HEADERS FROM $source_file_name AS row
#     FOREACH (name IN split(row.name, '\n') |
#         MERGE (person:Person {id: name})

#         MERGE (document:Document {text: coalesce(row.name + ',' + row.source, "Unknown"), source: $source_file_name})

#         FOREACH (name2 IN split(row.name2, '\n') |
#             MERGE (person2:Person {id: name2})
#             MERGE (person)-[r:Relationship]->(person2)
#             SET r.relationType = row.relationType
#             SET r.srcID = coalesce(row.srcID, "Unknown")
#             SET r.source = $source_file_name
#             MERGE (n)<-[rr:MENTION]-(document)
#             SET rr.source = $source_file_name
#         )
#     );
# """

import_relationship = """
LOAD CSV WITH HEADERS FROM $source_file_name AS row
    FOREACH (name IN split(row.name, '\n') |
        MERGE (person:Person {id: name})

        MERGE (document:Document {text: coalesce(row.name + ',' + row.source, "Unknown")})

        FOREACH (name2 IN split(row.name2, '\n') |
            MERGE (person2:Person {id: name2})
            MERGE (person)-[r:Relationship]->(person2)
            SET r.relationType = row.relationType
            SET r.srcID = coalesce(row.srcID, "Unknown")
            MERGE (n)<-[rr:MENTION]-(document)
        )
    );
"""
