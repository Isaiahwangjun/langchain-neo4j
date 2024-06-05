# import_replaceOrg = """
# LOAD CSV WITH HEADERS FROM $source_file_name AS row
#     FOREACH (org1 IN split(row.hasReplaced, '\n') |
#         MERGE (n1:Organization {id: org1})

#         FOREACH (org2 IN split(row.isReplacedBy, '\n') |
#             MERGE (n2:Organization {id: org2})
#             MERGE (n1)-[r:isReplacedBy]->(n2)
#             SET r.srcID = coalesce(row.srcID, "Unknown")
#             SET r.source = $source_file_name
#         )
#     );
# """

import_replaceOrg = """
LOAD CSV WITH HEADERS FROM $source_file_name AS row
    FOREACH (org1 IN split(row.hasReplaced, '\n') |
        MERGE (n1:Organization {id: org1})

        FOREACH (org2 IN split(row.isReplacedBy, '\n') |
            MERGE (n2:Organization {id: org2})
            MERGE (n1)-[r:isReplacedBy]->(n2)
            SET r.srcID = coalesce(row.srcID, "Unknown")
        )
    );
"""
