import os
import time
import dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings

dotenv.load_dotenv(dotenv_path="./.env")

PINECONE_API_KEY=os.getenv('PINECONE_API_KEY')
GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')

class VectorstoreUploader:
    def __init__(self, data, index_name="intentjs"):

        self.data = data
        self.index_name = index_name

        # pinecone db
        self.pc = Pinecone(api_key=PINECONE_API_KEY)
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=GOOGLE_API_KEY)
        self.index = self.load_pcindex()
        self.vectorstore = PineconeVectorStore(index=self.index, embedding=self.embeddings)

    def load_pcindex(self):

        existing_indexes = [index_info["name"] for index_info in self.pc.list_indexes()]

        if self.index_name not in existing_indexes:
            self.pc.create_index(
                name=self.index_name,
                dimension=768,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
                
            )
            while not self.pc.describe_index(self.index_name).status["ready"]:
                time.sleep(1)

        print("Index loading..")

        return self.pc.Index(self.index_name)
    
    def get_vstore(self):
        return self.vectorstore

    def execute(self):
        for index, d in enumerate(self.data):
            try:
                metadatas=[d['metadata']]
                self.vectorstore.add_texts(d['content'], metadatas)
                print(f"vectorstore uploaded for url: {d['metadata']['url']}")
            except Exception as e:
                print(f"Error occured during url: {d['metadata']['url']}")
                print(e)

        print("vectorstore execution completed.")