from dotenv import load_dotenv
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.graphs import Neo4jGraph
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableBranch, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from vector import index
from structuredRetriever import structured_retriever
import history
from langchain_community.callbacks import get_openai_callback
from entityChain import extract_question


def chain(user_question):

    load_dotenv()
    openai_api_key = os.environ.get('OPENAI_API_KEY')
    NEO4J_URI = os.environ.get('NEO4J_URI')
    NEO4J_USERNAME = os.environ.get('NEO4J_USERNAME')
    NEO4J_PASSWORD = os.environ.get('NEO4J_PASSWORD')
    graph = Neo4jGraph()

    UNSTRUCTURE_DATA_LIMIT = os.getenv("UNSTRUCTURE_DATA_LIMIT")
    MODEL_NAME = os.getenv("MODEL_NAME")

    print(f"NEO4J_URI:{NEO4J_URI}")
    # if (NEO4J_URI == "bolt://192.168.1.241:7689"):
    #     print("非固定節點")
    # else:
    #     print("固定節點")

    llm = ChatOpenAI(temperature=0, model_name=MODEL_NAME)

    # 建立索引 & 索引器
    vector_index = index()

    # 創建一個 "entity" 全文索引，是根據帶有 __Entity__ 標籤的節點裡 id 屬性創建
    graph.query(
        "CREATE FULLTEXT INDEX entity IF NOT EXISTS FOR (e:__Entity__) ON EACH [e.id]"
    )

    def retriever(question: str):
        # print(f"Search query: {question}")
        question = question.replace('原住民',
                                    '原住民、阿美族、排灣族、泰雅族、布農族、太魯閣族、卑南族、賽夏族、達悟族')
        question = question.replace('原民',
                                    '原住民、阿美族、排灣族、泰雅族、布農族、太魯閣族、卑南族、賽夏族、達悟族')

        structured_data = structured_retriever(question)

        entity_chain = extract_question(llm=llm)
        entities = entity_chain.invoke({"question": question})
        all_unstructured_data = []
        for entity in entities.names:
            unstructured_data = [
                el.page_content for el in vector_index.similarity_search(
                    entity, k=int(UNSTRUCTURE_DATA_LIMIT))
            ]
            all_unstructured_data.extend(unstructured_data)

        final_data = f"""Structured data:
    {structured_data}
    Unstructured data:
    {"#Document ". join(all_unstructured_data)}
        """
        # print(f"input: {final_data}")
        return final_data

    _search_query = RunnableBranch(
        # If input includes chat_history, we condense it with the follow-up question
        (
            RunnableLambda(lambda x: bool(x.get("chat_history"))).with_config(
                run_name="HasChatHistoryCheck"
            ),  # Condense follow-up question and chat into a standalone_question
            RunnablePassthrough.assign(chat_history=lambda x: history.
                                       _format_chat_history(x["chat_history"]))
            | history.template()
            | ChatOpenAI(temperature=0)
            | StrOutputParser(),
        ),
        # Else, we have no chat history, so just pass through the question
        RunnableLambda(lambda x: x["question"]),
    )

    template = """Answer the question based only on the following context:
    {context}

    Question: {question}
    Use natural language and be concise.
    Please use Traditional Chinese.
    當問題中的人名正確再回答。
    我要文章中確實的答案。
    提供我相關的source。
    "原民" 等於 "原住民"。
    Answer:"""
    prompt = ChatPromptTemplate.from_template(template)

    def inspect(state):
        # print(state['context'])
        return state

    chain = (RunnableParallel({
        "context": _search_query | retriever,
        "question": RunnablePassthrough(),
    })
             | RunnableLambda(inspect)
             | prompt
             | llm
             | StrOutputParser())

    with get_openai_callback() as cb:

        print(f"question: {user_question}\n")

        result = chain.invoke({"question": user_question})
        query = retriever(user_question)

        response = {"query": query, "answer": result}
        print(f"query: {query}\n")
        print(f"answer: {result}\n")
        print(cb)

        return response
