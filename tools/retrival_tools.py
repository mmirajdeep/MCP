import asyncio
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from loguru import logger
from pinecone import Pinecone
from fastmcp import FastMCP
from configs.config_loader import settings

class RetrievalTools:
    def __init__(self, mcp: FastMCP):
        self.mcp = mcp
        self.embeddings_model = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key="AIzaSyBeU28CBIje8s-XY2ZeVteWu1xr_do5Yw8",
        )
        self.pinecone_client = Pinecone(
            api_key="pcsk_3a1KGk_9VmJNrS3y3igZLgyExCSGpzE5Q2PV3uXWywMNkuDFJkrDgyj1C26ATi41jrF15w",
            ssl_verify=False,
        )
        self.index = self.pinecone_client.Index("mcp-index")
        self.namespace = "nepal_docs"
        self.index_name = "mcp-index"
        logger.info("Registering RetrievalTools methods...")
        self.register_tools()
    
    async def retriever(self, query: str):
        query_embeddings = await self.embeddings_model.aembed_query(query)
        def run_pinecone():
            if not self.pinecone_client.has_index(self.index_name):
                return None
            index = self.pinecone_client.Index(self.index_name)
            stats = index.describe_index_stats()
            if self.namespace not in stats.get("namespaces", {}):
                return None
            return index.query(
                namespace=self.namespace,
                vector=query_embeddings,
                top_k=5,
                include_values=False,
                include_metadata=True,
            )
        results = await asyncio.to_thread(run_pinecone)
        if not results or not results.matches:
            return None
        return "\n\n".join(m["metadata"]["text"] for m in results.matches)

    def register_tools(self):
        tools = [
            (
                self.retriever,
                "retriever",
                """Retrieve relevant information from the 1996 Nepal Family Health Survey (NFHS) document,
                   including geography, demographics, fertility, family planning, population policies,
                   and health survey methodology, based on a user query.""",
            ),
        ]
        for method, name, desc in tools:
            self.mcp.tool(method, name=name, description=desc)
            logger.info("="*40)
            logger.info(f"Registered tool: {name}")
        logger.info("="*40)
        


