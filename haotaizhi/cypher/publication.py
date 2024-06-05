# import_publication = """
# LOAD CSV WITH HEADERS FROM $source_file_name AS row
#         MERGE (publication:Publication {{srcID: row.srcID}})
#         ON CREATE SET publication.id = coalesce(row.label_Publication, "Unknown")
#         FOREACH(ignoreMe IN CASE WHEN row.name IS NOT NULL THEN [1] ELSE [] END |
#             FOREACH (name IN split(row.name, '\n') |
#                 MERGE (person:Person {{id: name}})
#                 MERGE (person)-[r:hasPublication]->(publication)
#                 SET r.source = $source_file_name
#             )
#         )

#         WITH publication, row
#         // Conditional creation for {0} directly after WITH to keep row in scope
#             FOREACH(ignoreMe IN CASE WHEN row.{0} IS NOT NULL THEN [1] ELSE [] END |
#                 MERGE (n:{0} {{id: row.{0}}})
#                 MERGE (publication)-[r:{0}]->(n)
#                 SET r.source = $source_file_name
#             )
# """

import_publication = """
LOAD CSV WITH HEADERS FROM $source_file_name AS row
        MERGE (publication:Publication {{srcID: row.srcID}})
        ON CREATE SET publication.id = coalesce(row.label_Publication, "Unknown")
        FOREACH(ignoreMe IN CASE WHEN row.name IS NOT NULL THEN [1] ELSE [] END |
            FOREACH (name IN split(row.name, '\n') |
                MERGE (person:Person {{id: name}})
                MERGE (person)-[r:hasPublication]->(publication)
                SET r.url = coalesce(row.url, "Unknown")
            )
        )

        WITH publication, row
        // Conditional creation for {0} directly after WITH to keep row in scope
            FOREACH(ignoreMe IN CASE WHEN row.{0} IS NOT NULL THEN [1] ELSE [] END |
                MERGE (n:{0} {{id: row.{0}}})
                MERGE (publication)-[r:{0}]->(n)
                SET r.url = coalesce(row.url, "Unknown")
            )
"""

publication_list = [
    "Publisher", "PlaceOfPublication", "InceptionDate", "edition",
    "NarrativeLocation", "workDescTime", "Translator", "Editor", "Modifier",
    "Oraler", "Collator", "Interviewer", "Illustrator", "Reviewer",
    "PrefaceAuthor", "column", "issue", "partOfTheSeries", "volume", "page",
    "totalPage", "LanguageOfWorkOrName", "LiteraryGenre", "imageURL_hasURL",
    "fileAvailableAt", "FullWorkCopyright", "comment"
]
