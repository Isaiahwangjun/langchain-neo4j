from langchain_openai import ChatOpenAI
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from dotenv import load_dotenv
from langchain_community.graphs import Neo4jGraph
import os
from prompt import getPrompt
from cypher import createSource
import csv


def createDB(graph, text, source):

    default_prompt = getPrompt()

    llm = ChatOpenAI(temperature=0, model_name="gpt-4-0125-preview")
    llm_transformer = LLMGraphTransformer(llm=llm, prompt=default_prompt)
    # llm_transformer 會將文章轉成節點跟關係

    ## 若為檔案直接用 TextLoader 讀取，返回即是 document type
    #[Document(page_content='劉達文(自傳)本人一九五二年生於廣東東莞,在中國受教育。有筆名蘇立文、曉沖', metadata={'source': 'test.txt'})]
    # docs = TextLoader("../five_people_test/丁日昌.txt", encoding='utf-8').load()
    # graph_documents = llm_transformer.convert_to_graph_documents(docs)

    ##  貼入文字的話，先轉成 document type，裡面可放來源 (metadata)
    metadata = {"source": source}
    docs = [Document(page_content=text, metadata=metadata)]
    graph_documents = llm_transformer.convert_to_graph_documents(docs)

    print(f"Nodes:{graph_documents[0].nodes}")
    print(f"Relationships:{graph_documents[0].relationships}")

    graph.add_graph_documents(
        graph_documents,
        baseEntityLabel=True,  # 會對每個節點加一個 "__entity__" 標籤，後續用來建立索引
        include_source=True)  # 加入來源


if __name__ == "__main__":

    load_dotenv()
    NEO4J_URI = os.environ.get('NEO4J_URI')
    NEO4J_USERNAME = os.environ.get('NEO4J_USERNAME')
    NEO4J_PASSWORD = os.environ.get('NEO4J_PASSWORD')
    graph = Neo4jGraph()

    file_path = r"C:\Users\wang\Downloads\tww_BasicInfo_2024_4_19.csv"
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)

        for row in csv_reader:
            createDB(graph, row['introduction'], file_path)

    # file_path = r"C:\Users\wang\Desktop\daoyi\HongKong\OCR_10_person\LineOCR\txt\金庸.txt"
    # with open(file_path, 'r', encoding='utf-8') as txtfile:
    #     content = txtfile.read()

    #     createDB(graph, content, file_path)

    createSource(NEO4J_URI, NEO4J_USERNAME,
                 NEO4J_PASSWORD)  # 額外寫的函數，用來對每個 node & relationship 增加資料來源
