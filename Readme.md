2024/3/7

* 前言: 目前港中語意擷取一次價格要在 $1 以內，因有 11 張表單內容要擷取，目前做法是分 11 次輸入給模型 (每一次都是"文章內容"加上 "prompt")。prompt 平均 1000 個 tokens($0.01)，輸出平均 1400 個 tokens(0.042)，而 1 張表單約能用 0.09，即內容字數約可用 0.09-0.042-0.01=0.038，大概 3800 tokens (1900 個中文字)。
* 解決: 提高使用者能輸入的字數
* 想法: 利用 RAG 讓每次的 input 不是全部文章內容，而只包含部分相似內容。
* RAG: 先將文章內容做分割 (每幾個字為一個，可以想成分為一句一句話)，並將這些分割的句子經由 embedding 轉成向量形式，而後儲存在 vectorspace。使用時，因先提問，會先將問題經由 embedding ，再去 vectorspsce 進行相似度搜索，這裡有個問題是: RAG 是進行相似度搜尋，當我提問 "名字是什麼"，當文章中沒有提及 "名字"，而是直接說 "我是xxx"，這兩句話再 vectorspace 不一定離的近**。**
* 還有個問題是，即使有找到相似度內容，但一張表格內的欄位有好幾個 (如: 本名、出生日期)，這些內容可能分布在文章各角落，RAG 的流程是先在 vectorspace 搜尋到相似句子，再把 "問題" 加上 "相似句子" 一起丟給 LLM 來分析，因此相似句子可能只包含 "本名"，不包含 "出生日期"，原因是這個 "相似句子" 的長度是經由參數決定，假如我設定長度=50，LLM就只會拿到長度為 50 的句子 (相似句子) 加上 "問題"，LLM 會從這長度 50 的句子來語意擷取，但這長度 50 可能只包含部份我們要擷取的內容。可能解決的方案是將每張表單的每個欄位分別 RAG，但這導致 (prompt + LLM 拿到的相似句子) 大量重複，tokens 並不會較少。

2024/4/8

* RunnableParallel 用來並行處理，可節省時間。[https://blog.csdn.net/zgpeace/article/details/135290412](https://blog.csdn.net/zgpeace/article/details/135290412)
* RunnablePassthrough 傳遞參數用，通常搭配 RunnableParallel，標準用法如下

---

```
vectorstore = FAISS.from_texts(
    ["harrison worked at kensho"], embedding=OpenAIEmbeddings()
)
retriever = vectorstore.as_retriever()
template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
model = ChatOpenAI()

retrieval_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

retrieval_chain.invoke("where did harrison work?")

```

* 透過 RunnablePassthrough 讓使用者輸入問題，之後會找到對應的 key
