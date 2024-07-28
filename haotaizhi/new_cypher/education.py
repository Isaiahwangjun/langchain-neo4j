# import_education = """
# LOAD CSV WITH HEADERS FROM $source_file_name AS row
#     FOREACH (name IN split(row.name, '\n') |
#         MERGE (person:Person {id: name})
#         MERGE (n:Education {id: coalesce(row.EducatedAt, "Unknown")})
#         MERGE (person)-[r:EducatedAt]->(n)
#         SET r.StartDate = coalesce(row.StartDate, "Unknown")
#         SET r.EndDate = coalesce(row.EndDate, "Unknown")
#         SET r.Examination = coalesce(row.Examination, "Unknown")
#         SET r.AcademicDiscipline = coalesce(row.AcademicDiscipline, "Unknown")
#         SET r.AcademicDegree = coalesce(row.AcademicDegree, "Unknown")
#         SET r.source = $source_file_name
#     );
# """

import_education = """
LOAD CSV WITH HEADERS FROM $source_file_name AS row
    FOREACH (name IN split(row.name, '\n') |
        MERGE (person:Person {id: name})
        MERGE (n:Education {id: coalesce(row.EducatedAt, "Unknown")})
        MERGE (person)-[r:EducatedAt]->(n)
        SET r.StartDate = coalesce(row.StartDate, "Unknown")
        SET r.EndDate = coalesce(row.EndDate, "Unknown")
        SET r.Examination = coalesce(row.Examination, "Unknown")
        SET r.AcademicDiscipline = coalesce(row.AcademicDiscipline, "Unknown")
        SET r.AcademicDegree = coalesce(row.AcademicDegree, "Unknown")
    );
"""
