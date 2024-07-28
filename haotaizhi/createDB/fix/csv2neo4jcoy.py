from neo4j import GraphDatabase
import os


class DataLoader:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def load_data(self, query, source_file_name):
        with self.driver.session() as session:
            # Execute the query and get results
            result = session.run(query, {"source_file_name": source_file_name})
            # Process and print the results for each record
            for record in result:
                print(record)


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # uri = "bolt://192.168.1.241:7690"  # or your Neo4j URI
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "12345678"
    data_loader = DataLoader(uri, user, password)

    import sys
    sys.path.insert(
        1,
        r'C:\Users\wang\Desktop\daoyi\myCV\langchain-neo4j\haotaizhi\new_cypher'
    )

    # from article import import_article
    # source_file_name = 'file:///Article.csv'
    # data_loader.load_data(import_article, source_file_name)

    # from award import import_award
    # source_file_name = 'file:///Award.csv'
    # data_loader.load_data(import_award, source_file_name)

    from basicInfo import import_basicInfo, baseicInfo_list
    source_file_name = 'file:///BasicInfo_url.csv'
    for i in range(len(baseicInfo_list)):
        query_ = import_basicInfo.format(baseicInfo_list[i])
        data_loader.load_data(query_, source_file_name)

    # from education import import_education
    # source_file_name = 'file:///Education.csv'
    # data_loader.load_data(import_education, source_file_name)

    # from event import import_event
    # source_file_name = 'file:///Event.csv'
    # data_loader.load_data(import_event, source_file_name)

    # from foundation import import_foundation
    # source_file_name = 'file:///Foundation.csv'
    # data_loader.load_data(import_foundation, source_file_name)

    # from location import import_location, location_list
    # source_file_name = 'file:///Location.csv'
    # for i in range(len(location_list)):
    #     query_ = import_location.format(location_list[i])
    #     data_loader.load_data(query_, source_file_name)

    # from organization import import_organization
    # source_file_name = 'file:///Organization.csv'
    # data_loader.load_data(import_organization, source_file_name)

    # from OrganizationInfo import import_organizationInfo
    # source_file_name = 'file:///OrganizationInfo.csv'
    # data_loader.load_data(import_organizationInfo, source_file_name)

    # from project import import_project
    # source_file_name = 'file:///Project.csv'
    # data_loader.load_data(import_project, source_file_name)

    # from publication import import_publication, publication_list
    # source_file_name = 'file:///Publication_test.csv'
    # for i in range(len(publication_list)):
    #     query_ = import_publication.format(publication_list[i])
    #     data_loader.load_data(query_, source_file_name)

    # from relationship import import_relationship
    # source_file_name = 'file:///Relationship.csv'
    # data_loader.load_data(import_relationship, source_file_name)

    # from replaceOrg import import_replaceOrg
    # source_file_name = 'file:///ReplaceOrg.csv'
    # data_loader.load_data(import_replaceOrg, source_file_name)

    # from specialty import import_specialty
    # source_file_name = 'file:///Specialty.csv'
    # data_loader.load_data(import_specialty, source_file_name)

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
