import_basicInfo = """
LOAD CSV WITH HEADERS FROM $source_file_name AS row
        MERGE (document:Document {{text: coalesce(row.姓名 + ',' + row.作家簡介, "Unknown"), url: row.url}})
        MERGE (person:Person {{srcID: row.人名ID}})
        ON CREATE SET person.id = coalesce(row.姓名, "Unknown")

        WITH person, document, row
        // Conditional creation for {0} directly after WITH to keep row in scope
            FOREACH(ignoreMe IN CASE WHEN row.{0} IS NOT NULL THEN [1] ELSE [] END |
                MERGE (n:{0} {{id: row.{0}}})
                MERGE (person)-[r:{0}]->(n)
                SET r.url = coalesce(row.url, "Unknown")
            )
    """

baseicInfo_list = [
    "出生時間", "辭世時間", "字", "號", "原名", "姓", "諱名", "筆名", "幼名", "學名", "譜名", "別號",
    "居室名", "泮名", "共同筆名", "其它名稱", "翻譯的語言別", "原民族群", "祖籍", "原籍", "籍貫", "出生地",
    "辭世地點", "性別", "理論", "圖像預覽", "引用自", "圖像權利註記", "網站顯示區域", "提要撰寫", "朝代", "年號",
    "作品出處", "宗教信仰", "稱譽", "當代相關研究", "族群", "維基數據", "虛擬國際權威檔案", "資料外部連結", "備註",
    "原始資料", "最後修改時間"
]
