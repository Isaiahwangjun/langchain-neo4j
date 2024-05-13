from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import create_structured_output_runnable
from dotenv import load_dotenv
import os

## 加載 .env 檔案
load_dotenv()

## 現在可以使用 os.environ.get 來存取環境變數
openai_api_key = os.environ.get('OPENAI_API_KEY')

# llm = ChatOpenAI(model_name="gpt-4-0125-preview").bind(
#     response_format={type: "json_object"})  ### json 格式會報錯
llm = ChatOpenAI(model_name="gpt-4-0125-preview")

## 讀檔，並切分區塊
## TextLoader 回傳的會是 document 類型，Document(page_content={內容}, metadata={source_path)}
## 這邊簡單使用 text 讀檔即可
# docs = TextLoader("C:/Users/wang/Desktop/daoyi/HongKong/ocr/result/吳瑞卿.txt",
#                   encoding='utf-8').load()
with open("C:/Users/wang/Desktop/daoyi/HongKong/ocr/result/吳瑞卿.txt",
          encoding='utf-8') as f:
    docs = f.read()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=0)
texts = text_splitter.split_text(docs)
##對於 document type, 需使用 split_document or create_document

## embeddiings and store in VectorStores
db = Chroma.from_texts(texts=texts,
                       embedding=OpenAIEmbeddings())  ##document->from_document

## 直接用問的方式
# query = "當過什麼主持人"
# docs = db.similarity_search(
#     query, k=1)  # k 為產生幾組答案，每個答案就是依照 text_splitter 切出來的 texts 裡面去比較
#print(docs[0].page_content)

## 查看相似度距離
#docs_score = db.similarity_search_with_score(query)
#print(docs_score[0][1])

## 先建立檢索器，再詢問，效果一樣
retriever = db.as_retriever(search_kwargs={"k": 1})
#docs = retriever.get_relevant_documents("當過什麼主持人")

# 雖然 openai response_format={type: "json_object"} 會報錯，可以利用 langchain json output (52~73)
# from pydantic.v1 import BaseModel, Field
# from typing import Optional, Sequence

# class other(BaseModel):
#     名字: str = Field(description="答案")

# parser = JsonOutputParser(pydantic_object=other)

# prompt = PromptTemplate(
#     template="""你是一位文字擷取專家。接下來會給你一段文章，並根據文章內容填入問題。
#      請確實找到文章內容再填入，資料正確很重要，如果沒有答案，就回答NULL。
#     問題:{question}
#     文章:{context}
#     答案: {format_instructions}""",
#     input_variables=["question"],
#     partial_variables={
#         "format_instructions": parser.get_format_instructions()
#     },
# )

#langchain json output 會讓 openai output tokens 多一些，這裡可以用 "問題" 加上 "回答" 自己寫成 json 格式
prompt = PromptTemplate.from_template("""你是一位文字擷取專家。接下來會給你一段文章，並根據文章內容填入問題。
     請確實找到文章內容再填入，資料正確很重要，如果沒有答案，就回答NULL。
    問題:{question}
    文章:{context}
    答案: """)

rag_chain = ({
    "context": retriever,
    "question": RunnablePassthrough()
}
             | prompt
             | llm
             | StrOutputParser())
ans = rag_chain.invoke("名字是?")
print(ans)
