import os, time, requests, json, html2text
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from cleantext import clean
from langchain_cohere import ChatCohere, CohereEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_cohere import ChatCohere
from langchain_core.messages import HumanMessage
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

import warnings
warnings.filterwarnings("ignore")


#GLOBALS:
#HTML tags cleaner:
text_maker = html2text.HTML2Text()
text_maker.ignore_links = True

#LOAD .ENV:
_ = load_dotenv(find_dotenv())
cohere_api_key = os.environ["COHERE_API_KEY"]
guardian_api_key = os.environ["GUARDIAN_API_KEY"]


#FUNCTIONS:
#1.A) GET DATA: Guardian API:
def get_articles(sections):
    results = []

    for section in sections:
        request = requests.get(
                f"https://content.guardianapis.com/search?tag=-tone/minutebyminute&section={section}&show-fields=headline,trailText,body",
                headers={"api-key": guardian_api_key},
                timeout=10
            )

        results += request.json().get("response", {}).get("results", [])
        print(len(results))
        time.sleep(1)

    return results


#1.B) STORE & CLEAN:
def clean_articles(results, export=False):
    latest_articles = []
    for i in range(len(results)):
        res = results[i]
        #HEADLINE:
        headline = res.get("fields", {}).get("headline", "").lower()
        headline = f"{headline}. " if headline != "" else headline
        #print(headline)
        #TRAILTEXT:
        trailtext = res.get("fields", {}).get("trailText", "").lower()
        trailtext = f"{trailtext}. " if trailtext != "" else trailtext
        #BODY:
        body = res.get("fields", {}).get("body", "")
        body = text_maker.handle(body)
        body = clean(body, no_emoji=True)
        body = body.replace(">", "").replace("\n\n", "###").replace(".\n", ".###").replace("\n", " ").replace("###", "\n")
        results[i]["fields"]["body"] = body
        #CONCATENATE:
        latest_articles.append(f"{headline}{trailtext}{body}")

    #export:
    if export:
        json.dump(results, open(os.path.join("data", f"{datetime.strftime(datetime.now(), '%Y-%m-%d_%H:%M')}test.json"), "w"))

    print(len(latest_articles))
    #print(latest_articles[0])
    return latest_articles


#2.A) GET CHUNKS:
def get_chunks(latest_articles):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200, add_start_index=True
    )

    documents = text_splitter.create_documents(latest_articles)
    # print(documents[0])
    # print(documents[1])
    chunks = text_splitter.split_documents(documents)
    return chunks


#2.B) LOAD VECTORSTORE & RETRIEVER:
def get_vectorstore(chunks):
    #Create Vector DB:
    vectorstore = Chroma.from_documents(documents=chunks, embedding=CohereEmbeddings())
    #Init retriever:
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6})
    return vectorstore, retriever


#3.A) Post-processing:
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


#3.B) Define RAG chain:
def load_chain(retriever, prompt, llm):
    rag_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain



#MAIN:
if __name__ == "__main__":
    #Get data:
    #e.g. world, us-news, football, sport, business, film, stage
    sections = ["us-news", "world", "sport", "football"]
    print("\n######## NEWS TALK ########")
    print(f"Available sections: {', '.join(sections)}")
    print("Loading articles... Please wait.")
    results = get_articles(sections)
    print("Articles downloaded!")
    latest_articles = clean_articles(results, export=True)

    print("Preparing agent... Please wait.")
    #Vectorize:
    chunks = get_chunks(latest_articles)
    vectorstore, retriever = get_vectorstore(chunks)

    #Init Foundation LLM:
    llm = ChatCohere(temperature=0.3, cohere_api_key=cohere_api_key)

    #Prompt template:
    template = """You are a journalist and you are giving answers to the audience's questions. For all questions, use the following pieces of retrieved context to answer the question. If the user asks you to give a summary of what you know, just say what you're reporting about. If you know the answer to the user's question, use five sentences maximum and be as detailed as possible. If you don't know the answer, say that you don't have any information on that, then briefly tell the user what you know on the requested topic in two sentences maximum. 

    Question: {question}

    Context: {context}

    Answer:
    """

    #Build prompt:
    prompt = ChatPromptTemplate.from_template(template)

    #Load RAG chain:
    rag_chain = load_chain(retriever, prompt, llm)

    print("AGENT READY!")
    while True:
        question = input("\nPlease ask your question!\n")
        for chunk in rag_chain.stream(question):
            print(chunk, end="", flush=True)
        print("\n")


    # #SET STREAMLIT PAGE:
    # #Page title and header
    # st.set_page_config(page_title="News Talk!")
    # st.header("Ask any question about the latest articles from the Guardian!")
    
    # #Input Sections:
    # st.markdown("## Ask any question!")
    # st.markdown(f"Topics: {sections.join(", ")}")
    
