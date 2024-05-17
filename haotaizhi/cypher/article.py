import_article = """
LOAD CSV WITH HEADERS FROM $source_file_name AS row
    FOREACH (name IN split(row.name, '\n') |
        MERGE (person:Person {id: name})

        MERGE (document:Document {text: coalesce(row.name + ',' + row.source, "Unknown"), source: $source_file_name})

        FOREACH(ignoreMe IN CASE WHEN row.label_Article IS NOT NULL THEN [1] ELSE [] END |
            FOREACH (label_Article IN split(row.label_Article, '\n') |
                MERGE (n:Article {id: label_Article})
                MERGE (person)-[r:hasArticle]->(n)
                SET r.srcID = coalesce(row.srcID, "Unknown")
                SET r.PublishedIn = coalesce(row.PublishedIn, "Unknown")
                SET r.InceptionDate = coalesce(row.InceptionDate, "Unknown")
                SET r.LanguageOfWorkOrName = coalesce(row.LanguageOfWorkOrName, "Unknown")
                SET r.LiteraryGenre = coalesce(row.LiteraryGenre, "Unknown")
                SET r.source = $source_file_name
                MERGE (n)<-[rr:MENTION]-(document)
                SET rr.source = $source_file_name
            )
        )
    );
"""
