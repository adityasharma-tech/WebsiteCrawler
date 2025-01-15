import os
import dotenv
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_google_genai import ChatGoogleGenerativeAI

dotenv.load_dotenv(dotenv_path="./.env")

PINECONE_API_KEY=os.getenv('PINECONE_API_KEY')
GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')

class DataLLM:
    def __init__(self, vstore):

        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=GOOGLE_API_KEY)
        
        self.qa_system_prompt = """You are an AI assistant specialized in providing information about IntentJS, a web application framework built on top of NestJS.\
            IntentJS offers declarative APIs to develop and ship sophisticated solutions with ease. \
            It includes features like database integration, storage solutions, message queues, mailers, caching, logging, validations, transformers, helpers, localization, and console commands. Your role is to assist users by answering questions related to IntentJS's features, installation, usage, and best practices.\
            If you don't know the answer, it's okay to say you don't know. Keep your responses concise and relevant to IntentJS.\

        {context}"""
        if vstore is None:
            raise Exception("vectorstore called before initialization.")

        self.retriever = vstore.as_retriever()
        print("retriever loaded")

        self.qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.qa_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        self.store = {}

        self.question_answer_chain = create_stuff_documents_chain(self.llm, self.qa_prompt)
        self.rag_chain = create_retrieval_chain(self.retriever, self.question_answer_chain)

        self.conversational_rag_chain = RunnableWithMessageHistory(
            self.rag_chain,
            self.get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )

    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()
        return self.store[session_id]
    
    def query(self, query: str, session_id: str):
        try:
            response = self.conversational_rag_chain.invoke(
                {"input": f"{query}"},
                config={
                    "configurable": {"session_id": f"{session_id}"}
                },
            )
            result = response["answer"]

            return result
        except Exception as e:
            print(e)
            return "Some error occured during getting the response."