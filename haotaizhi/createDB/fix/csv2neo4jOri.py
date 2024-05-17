from neo4j import GraphDatabase
import os


class DataLoader:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def load_data(self, query):
        with self.driver.session() as session:
            # Execute the query and get results
            result = session.run(query)
            # Process and print the results for each record
            for record in result:
                print(record)


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    uri = "bolt://192.168.1.241:7688"  # or your Neo4j URI
    user = "neo4j"
    password = "12345678"
    data_loader = DataLoader(uri, user, password)

    # Load BaseInfo.csv
    query_baseinfo = """
    LOAD CSV WITH HEADERS FROM 'file:///five_people_test/base.csv' AS row
MERGE (person:Person {nameID: row.nameID})
ON CREATE SET person.givenName = coalesce(row.givenName, "Unknown"),
            person.artName = coalesce(row.artName, "Unknown"),
            person.courtesyName = coalesce(row.courtesyName, "Unknown"),
            person.penName = coalesce(row.penName, "Unknown"),
            person.hasGender = coalesce(row.hasGender, "Unknown")
WITH person, row
// Conditional creation for PlaceOfBirth directly after WITH to keep row in scope
FOREACH(ignoreMe IN CASE WHEN row.hasPlaceOfBirth IS NOT NULL THEN [1] ELSE [] END |
    MERGE (birthPlace:Place {name: row.hasPlaceOfBirth})
    MERGE (person)-[:BORN_IN]->(birthPlace)
)
WITH person, row
FOREACH(ignoreMe IN CASE WHEN row.hasPlaceOfBirth IS NOT NULL THEN [1] ELSE [] END |
    MERGE (birthPlace:Place {name: row.hasPlaceOfBirth})
    MERGE (person)-[:BORN_IN]->(birthPlace)
)
FOREACH(ignoreMe IN CASE WHEN row.hasPlaceOfDeath IS NOT NULL THEN [1] ELSE [] END |
    MERGE (deathPlace:Place {name: row.hasPlaceOfDeath})
    MERGE (person)-[:DIED_IN]->(deathPlace)
)
FOREACH(ignoreMe IN CASE WHEN row.hasAncestralHome IS NOT NULL THEN [1] ELSE [] END |
    MERGE (ancestralHome:Place {name: row.hasAncestralHome})
    MERGE (person)-[:HAS_ANCESTRAL_HOME]->(ancestralHome)
)
FOREACH(ignoreMe IN CASE WHEN row.hasBirthDate IS NOT NULL THEN [1] ELSE [] END |
    MERGE (birthDate:Date {date: row.hasBirthDate})
    MERGE (person)-[:BORN_ON]->(birthDate)
)
FOREACH(ignoreMe IN CASE WHEN row.hasDeathDate IS NOT NULL THEN [1] ELSE [] END |
    MERGE (deathDate:Date {date: row.hasDeathDate})
    MERGE (person)-[:DIED_ON]->(deathDate)
)
FOREACH(ignoreMe IN CASE WHEN row.hasGender IS NOT NULL THEN [1] ELSE [] END |
    MERGE (gender:Gender {gender: row.hasGender})
    MERGE (person)-[:HAS_GENDER]->(gender)
);
    """
    data_loader.load_data(query_baseinfo)

    # Load OrgEvent.csv
    query_orgevent = """
    LOAD CSV WITH HEADERS FROM 'file:///five_people_test/org.csv' AS row
MATCH (person:Person {givenName: row.name}) // Assuming direct name matching for simplicity
MERGE (event:OrgEvent {id: row.OrgEventID, name: row.name})
    ON CREATE SET event.startDate = row.hasStartDate, event.endDate = row.hasEndDate

FOREACH(ignoreMe IN CASE WHEN row.hasFounded IS NOT NULL THEN [1] ELSE [] END |
    MERGE (founded:Organization {name: row.hasFounded})
    MERGE (event)-[:FOUNDED]->(founded)
)

FOREACH(ignoreMe IN CASE WHEN row.hasParticipant IS NOT NULL THEN [1] ELSE [] END |
    MERGE (participant:Person {givenName: row.hasParticipant}) // Adjust as necessary for participant identification
    MERGE (event)-[:HAS_PARTICIPANT]->(participant)
)

FOREACH(ignoreMe IN CASE WHEN row.hasPosition IS NOT NULL THEN [1] ELSE [] END |
    MERGE (position:Position {name: row.hasPosition})
    MERGE (person)-[:HOLDS_POSITION]->(position)
    MERGE (position)-[:IN_EVENT]->(event)
);
    """
    data_loader.load_data(query_orgevent)

    #     # Load OrgInfo.csv
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
    #     data_loader.load_data(query_orginfo)

    # Link More Nodes
    query_orgevent = """
    LOAD CSV WITH HEADERS FROM 'file:///five_people_test/org.csv' AS row
    MATCH (event:Event {id: row.OrgEventID})
    MATCH (person:Person {id: row.hasParticipant}) // Assuming 'hasParticipant' refers to the Person ID
    MERGE (person)-[:PARTICIPATED_IN]->(event)
    MERGE (org:Organization {name: row.name}) // Assuming you can link events to organizations by name or some ID
    MERGE (person)-[:AFFILIATED_WITH]->(org);
    """
    data_loader.load_data(query_orgevent)

    data_loader.close()


if __name__ == "__main__":
    main()
