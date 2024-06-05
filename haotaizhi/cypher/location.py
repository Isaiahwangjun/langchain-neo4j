# import_location = """
# LOAD CSV WITH HEADERS FROM $source_file_name AS row
#         MERGE (location:Location {{srcID: row.srcID}})
#         ON CREATE SET location.id = coalesce(row.Location, "Unknown")

#         WITH location, row
#         // Conditional creation for {0} directly after WITH to keep row in scope
#             FOREACH(ignoreMe IN CASE WHEN row.{0} IS NOT NULL THEN [1] ELSE [] END |
#                 MERGE (n:{0} {{id: row.{0}}})
#                 MERGE (location)-[r:{0}]->(n)
#                 SET r.source = $source_file_name
#             )
#     """

import_location = """
LOAD CSV WITH HEADERS FROM $source_file_name AS row
        MERGE (location:Location {{srcID: row.srcID}})
        ON CREATE SET location.id = coalesce(row.Location, "Unknown")

        WITH location, row
        // Conditional creation for {0} directly after WITH to keep row in scope
            FOREACH(ignoreMe IN CASE WHEN row.{0} IS NOT NULL THEN [1] ELSE [] END |
                MERGE (n:{0} {{id: row.{0}}})
                MERGE (location)-[r:{0}]->(n)
            )
    """

location_list = [
    "isAreaOf", "Country", "Province", "City", "Township", "CurrentCountry",
    "CurrentCity", "CurrentTownship", "geoLongitude", "geoLatitude"
]
