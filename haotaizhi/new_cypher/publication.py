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

# publication_list = [
#     "Publisher", "PlaceOfPublication", "InceptionDate", "edition",
#     "NarrativeLocation", "workDescTime", "Translator", "Editor", "Modifier",
#     "Oraler", "Collator", "Interviewer", "Illustrator", "Reviewer",
#     "PrefaceAuthor", "column", "issue", "partOfTheSeries", "volume", "page",
#     "totalPage", "LanguageOfWorkOrName", "LiteraryGenre", "imageURL_hasURL",
#     "fileAvailableAt", "FullWorkCopyright", "comment"
# ]
publication_list = [
    "出版品", "作品別名", "出版者", "出版地點", "出版時間", "出版版次", "作品描述區域", "作品描述時間", "歷史分期",
    "撰寫者", "作者", "翻譯者", "共同筆名", "編輯者", "修訂者", "口述者", "整理者", "採訪者", "繪圖者",
    "題字者", "評論者", "序文作者", "贊助者", "刊載處", "欄名", "副欄名", "號", "期", "冊", "版面位置",
    "第幾年", "卷", "所在頁數", "總頁數", "發行方式", "裝訂方式", "作品語言", "作品類型", "文學主題", "文學分類",
    "典藏處", "館藏號碼", "出版品國際編碼", "序文", "作品簡介", "目次", "關鍵字", "翻譯作品", "衍生作品",
    "參考資料", "著作權狀態", "書封照", "圖像權利標註", "網站顯示區域", "全文檔名", "全文檔名顯示名稱", "全文著作權狀態",
    "資料外部連結", "備註", "是否為Lift書系", "原始資料", "是否為peak書系", "友善連結", "虛擬角色",
    "PDF檔翻頁方向"
]
