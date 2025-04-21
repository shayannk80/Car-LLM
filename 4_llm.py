import os
from langchain_ollama.llms import OllamaLLM
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain_ollama import OllamaEmbeddings

db_path = "db"  # Path to store the vector store

cached_llm = OllamaLLM(model="gemma3:1b")
embedding = OllamaEmbeddings(model="mxbai-embed-large")

raw_prompt = PromptTemplate.from_template(
    """ 
    <s>[INST] You are a technical assistant good at searching documents. 
    If you do not have an answer from the provided information, say so. [/INST] </s>
    [INST] {input}
           Context: {context}
           Answer:
    [/INST]
"""
)


def chat_with_llm(query):
    # Load the vector store and create the retriever
    vector_store = Chroma(persist_directory = db_path, embedding_function = embedding)
    retriever = vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"k": 5, "score_threshold": 0.3},
    )


    document_chain = create_stuff_documents_chain(cached_llm, raw_prompt)
    retrieval_chain = create_retrieval_chain(
        retriever=retriever,
        combine_docs_chain=document_chain,
    )
    # Get the answer and update chat history
    result = retrieval_chain.invoke({"input": query})
    print(result["answer"])
    
    return {"answer": result["answer"]}

# Function to simulate a conversation
def conversation():
    print("Starting conversation...\n")
    # Start asking questions based on the PDF content
    while True:
        query = input("\nYou: ")
        if query.lower() == "exit":
            break

        response = chat_with_llm(query)
        print("\nBot:", response["answer"])

# Start the conversation
conversation()
