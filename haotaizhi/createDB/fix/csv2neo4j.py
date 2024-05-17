from neo4j import GraphDatabase
import os


class DataLoader:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def load_data(self, query, base_file_name, org_file_name):
        with self.driver.session() as session:
            # Execute the query and get results
            result = session.run(query, {
                "base_file_name": base_file_name,
                "org_file_name": org_file_name
            })
            # Process and print the results for each record
            for record in result:
                print(record)


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    uri = "bolt://localhost:7687"  # or your Neo4j URI
    user = "neo4j"
    password = "12345678"
    data_loader = DataLoader(uri, user, password)
    base_file_name = 'file:///tww_BasicInfo_2024_4_1.csv'
    org_file_name = 'file:///tww_Organization_2024_4_1.csv'

    # base_file_name = 'https://drive.google.com/file/d/1JjD7aJkPpINGQ7atxWu-ISNzWIbcSaAK/view?usp=sharing'
    # org_file_name = 'https://drive.google.com/file/d/1WsE2M8fy63gEMYo_ZDl7OjcHE6Aq6jcm/view?usp=sharing'

    # base_file_name = 'https://drive.google.com/uc?export=download&id=1JjD7aJkPpINGQ7atxWu-ISNzWIbcSaAK'
    # org_file_name = 'https://drive.google.com/uc?export=download&id=1WsE2M8fy63gEMYo_ZDl7OjcHE6Aq6jcm'

    # Load BaseInfo.csv

    query_baseinfo = """
    LOAD CSV WITH HEADERS FROM $base_file_name AS row
        MERGE (document:Document {textKG: coalesce(row.givenName + ',' + row.source, "Unknown"), source: $base_file_name})
        MERGE (person:Person {nameID: row.nameID})
        ON CREATE SET person.id = coalesce(row.givenName, "Unknown"),
                person.artName = coalesce(row.artName, "Unknown"),
                person.courtesyName = coalesce(row.courtesyName, "Unknown"),
                person.penName = coalesce(row.penName, "Unknown"),
                person.hasGender = coalesce(row.hasGender, "Unknown")
        MERGE (person)<-[r:MENTION]-(document)
        SET r.source = $base_file_name

        WITH person, document, row
        // Conditional creation for PlaceOfBirth directly after WITH to keep row in scope
            FOREACH(ignoreMe IN CASE WHEN row.hasPlaceOfBirth IS NOT NULL THEN [1] ELSE [] END |
                MERGE (birthPlace:Place {id: row.hasPlaceOfBirth})
                MERGE (person)-[r:BORN_IN]->(birthPlace)
                SET r.source = $base_file_name
                MERGE (birthPlace)<-[rr:MENTION]-(document)
                SET rr.source = $base_file_name
            )

            FOREACH(ignoreMe IN CASE WHEN row.hasPlaceOfDeath IS NOT NULL THEN [1] ELSE [] END |
                MERGE (deathPlace:Place {id: row.hasPlaceOfDeath})
                MERGE (person)-[r:DIED_IN]->(deathPlace)
                SET r.source = $base_file_name
                MERGE (deathPlace)<-[rr:MENTION]-(document)
                SET rr.source = $base_file_name
            )

            FOREACH(ignoreMe IN CASE WHEN row.hasAncestralHome IS NOT NULL THEN [1] ELSE [] END |
                MERGE (ancestralHome:Place {id: row.hasAncestralHome})
                MERGE (person)-[r:HAS_ANCESTRAL_HOME]->(ancestralHome)
                SET r.source = $base_file_name
                MERGE (ancestralHome)<-[rr:MENTION]-(document)
                SET rr.source = $base_file_name
            )

            FOREACH(ignoreMe IN CASE WHEN row.hasBirthDate IS NOT NULL THEN [1] ELSE [] END |
                MERGE (birthDate:Date {id: row.hasBirthDate})
                MERGE (person)-[r:BORN_ON]->(birthDate)
                SET r.source = $base_file_name
                MERGE (birthDate)<-[rr:MENTION]-(document)
                SET rr.source = $base_file_name
            )

            FOREACH(ignoreMe IN CASE WHEN row.hasDeathDate IS NOT NULL THEN [1] ELSE [] END |
                MERGE (deathDate:Date {id: row.hasDeathDate})
                MERGE (person)-[r:DIED_ON]->(deathDate)
                SET r.source = $base_file_name
                MERGE (deathDate)<-[rr:MENTION]-(document)
                SET rr.source = $base_file_name
            );
    """
    data_loader.load_data(query_baseinfo, base_file_name, org_file_name)

    # Load OrgEvent.csv
    query_orgevent = """
    LOAD CSV WITH HEADERS FROM $org_file_name AS row
    FOREACH (name IN split(row.name, '\n') |
        MERGE (person:Person {id: name})

        MERGE (document:Document {text: coalesce(row.name + ',' + row.source, "Unknown"), source: $org_file_name})

        FOREACH(ignoreMe IN CASE WHEN row.hasFounded IS NOT NULL THEN [1] ELSE [] END |
            FOREACH (orgName IN split(row.hasFounded, '\n') |
                MERGE (founded:Organization {id: orgName})
                MERGE (person)-[r:FOUNDED]->(founded)
                SET r.startDate = coalesce(row.hasStartDate, "Unknown")
                SET r.endDate = coalesce(row.hasEndDate, "Unknown")
                SET r.position = coalesce(row.hasPosition, "Unknown")
                SET r.source = $org_file_name
                MERGE (founded)<-[rr:MENTION]-(document)
                SET rr.source = $org_file_name
            )
        )

        FOREACH(ignoreMe IN CASE WHEN row.hasParticipant IS NOT NULL THEN [1] ELSE [] END |
            FOREACH (orgName IN split(row.hasParticipant, '\n') |
                MERGE (participant:Organization {id: orgName}) 
                MERGE (person)-[r:HAS_PARTICIPANT]->(participant)
                SET r.startDate = coalesce(row.hasStartDate, "Unknown")
                SET r.endDate = coalesce(row.hasEndDate, "Unknown")
                SET r.position = coalesce(row.hasPosition, "Unknown")
                SET r.source = $org_file_name
                MERGE (participant)<-[rr:MENTION]-(document)
                SET rr.source = $org_file_name
            )
        )
    );
    """
    data_loader.load_data(query_orgevent, base_file_name, org_file_name)

    # Load OrgInfo.csv
    #     query_orginfo = """
    #     LOAD CSV WITH HEADERS FROM 'file:///OrgInfo.csv' AS row
    # MERGE (org:Organization {id: row.OrgID, name: row.name})
    #     ON CREATE SET org.startDate = row.hasStartDate, org.endDate = row.hasEndDate, org.description = row.desc

    # FOREACH(ignoreMe IN CASE WHEN row.hasLocationOfFormation IS NOT NULL THEN [1] ELSE [] END |
    #     MERGE (locationOfFormation:Place {name: row.hasLocationOfFormation})
    #     MERGE (org)-[:FORMED_IN]->(locationOfFormation)
    # )

    # FOREACH(ignoreMe IN CASE WHEN row.hasWorkLocation IS NOT NULL THEN [1] ELSE [] END |
    #     MERGE (workLocation:Place {name: row.hasWorkLocation})
    #     MERGE (org)-[:WORKS_IN]->(workLocation)
    # )

    # FOREACH(ignoreMe IN CASE WHEN row.hasInteractive IS NOT NULL THEN [1] ELSE [] END |
    #     MERGE (interactive:Event {name: row.hasInteractive}) // Assuming this refers to an event or some interactive activity
    #     MERGE (org)-[:INTERACTS_WITH]->(interactive)
    # );
    #     """
    # data_loader.load_data(query_orginfo)

    # Link More Nodes
    # query_orgevent = """
    # LOAD CSV WITH HEADERS FROM 'file:///five_people_test/org.csv' AS row
    # MATCH (event:Event {id: row.OrgEventID})
    # MATCH (person:Person {id: row.hasParticipant}) // Assuming 'hasParticipant' refers to the Person ID
    # MERGE (person)-[:PARTICIPATED_IN]->(event)
    # MERGE (org:Organization {name: row.name}) // Assuming you can link events to organizations by name or some ID
    # MERGE (person)-[:AFFILIATED_WITH]->(org);
    # """
    # data_loader.load_data(query_orgevent)

    data_loader.close()

    # add entity labels
    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver.session() as session:
        result = session.run("""
            MATCH (n) WHERE NOT n:Document
            SET n:__Entity__
        """)
    driver.close()


if __name__ == "__main__":
    main()
