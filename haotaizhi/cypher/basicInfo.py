# import_basicInfo = """
# LOAD CSV WITH HEADERS FROM $source_file_name AS row
#         MERGE (document:Document {{text: coalesce(row.givenName + ',' + row.source, "Unknown"), source: $source_file_name}})
#         MERGE (person:Person {{srcID: row.srcID}})
#         ON CREATE SET person.id = coalesce(row.label_Person, "Unknown")
#         MERGE (person)<-[r:MENTION]-(document)
#         SET r.source = $source_file_name

#         WITH person, document, row
#         // Conditional creation for {0} directly after WITH to keep row in scope
#             FOREACH(ignoreMe IN CASE WHEN row.{0} IS NOT NULL THEN [1] ELSE [] END |
#                 MERGE (n:{0} {{id: row.{0}}})
#                 MERGE (person)-[r:{0}]->(n)
#                 SET r.source = $source_file_name
#                 MERGE (n)<-[rr:MENTION]-(document)
#                 SET rr.source = $source_file_name
#             )
#     """

import_basicInfo = """
LOAD CSV WITH HEADERS FROM $source_file_name AS row
        MERGE (document:Document {{text: coalesce(row.givenName + ',' + row.source, "Unknown"), url: row.url}})
        MERGE (person:Person {{srcID: row.srcID}})
        ON CREATE SET person.id = coalesce(row.label_Person, "Unknown")
        MERGE (person)<-[r:MENTION]-(document)
        SET r.url = coalesce(row.url, "Unknown")

        WITH person, document, row
        // Conditional creation for {0} directly after WITH to keep row in scope
            FOREACH(ignoreMe IN CASE WHEN row.{0} IS NOT NULL THEN [1] ELSE [] END |
                MERGE (n:{0} {{id: row.{0}}})
                MERGE (person)-[r:{0}]->(n)
                SET r.url = coalesce(row.url, "Unknown")
                MERGE (n)<-[rr:MENTION]-(document)
                SET rr.url = coalesce(row.url, "Unknown")
            )
    """

baseicInfo_list = [
    "BirthDate",
    "DeathDate",
    "courtesyName",
    "artName",
    "birthName",
    "familyName",
    "penName",
    "groupPenName",
    "otherName",
    "EthnicGroup",
    "childhoodName",
    "schoolName",
    "puMing",
    "alias",
    "roomName",
    "panMing",
    "translationLanguage",
    "FamilyOrigin",
    "CountryOfOrigin",
    "AncestralHome",
    "PlaceOfBirth",
    "Gender",
    "theory",
]
