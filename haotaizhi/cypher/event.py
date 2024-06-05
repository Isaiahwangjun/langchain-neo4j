# import_event = """
# LOAD CSV WITH HEADERS FROM $source_file_name AS row
#     FOREACH(ignoreMe IN CASE WHEN row.source IS NOT NULL THEN [1] ELSE [] END |
#         FOREACH (name IN split(row.name, '\n') |
#             MERGE (n:Person {id: name})
#             MERGE (document:Document {text: coalesce(row.name + ',' + row.source, "Unknown"), source: $source_file_name})
#             MERGE (n)<-[r:MENTION]-(document)
#             SET r.source = $source_file_name
#             SET r.srcID = row.srcID
#         )
#     );
# """

import_event = """
LOAD CSV WITH HEADERS FROM $source_file_name AS row
    FOREACH(ignoreMe IN CASE WHEN row.source IS NOT NULL THEN [1] ELSE [] END |
        FOREACH (name IN split(row.name, '\n') |
            MERGE (n:Person {id: name})
            MERGE (document:Document {text: coalesce(row.name + ',' + row.source, "Unknown")})
            MERGE (n)<-[r:MENTION]-(document)
            SET r.srcID = row.srcID
        )
    );
"""
