"""
DetoxifyAI RAG Pipeline - Production Version with LangChain Integration
Uses LangChain: Custom LLM, Retriever, PromptTemplate, and Chain
"""

# import os
import modal
from typing import List, Dict, Optional, Any
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# from langchain.llms.base import LLM
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain
from langchain_core.language_models.llms import LLM
from langchain_core.prompts import PromptTemplate

# from langchain.chains import LLMChain
# from langchain.chains.llm import LLMChain
from langchain_core.output_parsers import StrOutputParser


# Custom Modal LLM Wrapper for LangChain
class ModalMistralLLM(LLM):
    """
    LangChain LLM wrapper for Modal-hosted Mistral-7B
    This integrates Modal with LangChain's ecosystem
    """

    max_tokens: int = 100
    temperature: float = 0.7

    @property
    def _llm_type(self) -> str:
        return "modal_mistral"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[Any] = None,
        **kwargs: Any,
    ) -> str:
        """Call Modal Mistral-7B endpoint"""
        MistralModel = modal.Cls.from_name("detoxifyai-mistral", "MistralModel")

        response = MistralModel().generate.remote(
            prompt, max_tokens=self.max_tokens, temperature=self.temperature
        )

        return response

    @property
    def _identifying_params(self) -> dict:
        return {
            "model": "mistralai/Mistral-7B-Instruct-v0.1",
            "platform": "Modal",
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
        }


class DetoxifyRAGPipeline:
    """
    Production RAG pipeline using LangChain components:
    - Custom LLM (Modal wrapper)
    - VectorStoreRetriever (FAISS)
    - PromptTemplate
    - LLMChain
    """

    def __init__(self, azure_connection_string: str, azure_container: str):
        self.azure_connection_string = azure_connection_string
        self.azure_container = azure_container

        # Initialize LangChain components
        self._load_faiss_index()
        self._init_llm()
        self._init_chain()

    def _load_faiss_index(self):
        """Load FAISS index from Azure Blob Storage"""
        from azure.storage.blob import BlobServiceClient
        import tempfile
        import zipfile

        print("📥 Loading FAISS index from Azure Blob...")

        # Download FAISS index from Azure
        blob_service = BlobServiceClient.from_connection_string(
            self.azure_connection_string
        )
        blob_client = blob_service.get_blob_client(
            container=self.azure_container, blob="faiss_index.zip"
        )

        # Download to temp directory
        with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp_file:
            blob_data = blob_client.download_blob()
            blob_data.readinto(tmp_file)
            zip_path = tmp_file.name

        # Extract FAISS index
        extract_dir = tempfile.mkdtemp()
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_dir)

        # Load with LangChain
        embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

        self.vectorstore = FAISS.load_local(
            extract_dir, embedding_model, allow_dangerous_deserialization=True
        )

        # Create LangChain retriever
        self.retriever = self.vectorstore.as_retriever(
            search_type="similarity", search_kwargs={"k": 5}
        )

        print("✅ FAISS index loaded with LangChain retriever")

    def _init_llm(self):
        """Initialize LangChain LLM wrapper for Modal"""
        print("🔗 Initializing LangChain LLM (Modal Mistral-7B)...")
        self.llm = ModalMistralLLM(max_tokens=100, temperature=0.7)
        print("✅ LangChain LLM ready")

    def _init_chain(self):
        """Initialize LangChain chain with PromptTemplate"""
        print("⛓️  Building LangChain chain...")

        # Define prompt template
        template = """You are a professional communication expert. Your task is to rephrase toxic messages into polite, professional alternatives while preserving the original intent and length of the message.

Here are some examples of toxic messages transformed into professional communication:

{examples}

Now, please rephrase the following toxic message into a professional alternative:

Toxic Message: {toxic_input}

Professional Rephrase:\n"""

        self.prompt_template = PromptTemplate(
            input_variables=["examples", "toxic_input"], template=template
        )

        # Create LangChain LLMChain
        # self.chain = LLMChain(
        #     llm=self.llm,
        #     prompt=self.prompt_template
        # )

        # Modern LangChain LCEL chain (replaces LLMChain)
        self.chain = self.prompt_template | self.llm | StrOutputParser()

        print("✅ LangChain chain initialized")

    def _format_examples(self, retrieved_docs: List, k: int = 5) -> str:
        """Format retrieved examples for prompt"""
        examples_text = ""
        for i, doc in enumerate(retrieved_docs[:k], 1):
            examples_text += f"""Example {i}:
Toxic: "{doc.metadata["toxic"]}"
Professional: "{doc.metadata["professional"]}"

"""
        return examples_text.strip()

    def rephrase(self, toxic_text: str, k: int = 5) -> Dict:
        """
        Main RAG pipeline using LangChain components

        Args:
            toxic_text: Toxic message to rephrase
            k: Number of examples to retrieve

        Returns:
            Dictionary with original, rephrased, and metadata
        """
        # Step 1: Retrieve using LangChain retriever
        # retrieved_docs = self.retriever.get_relevant_documents(toxic_text)
        retrieved_docs = self.retriever.invoke(toxic_text)

        # Step 2: Format examples
        examples = self._format_examples(retrieved_docs, k=k)

        # Step 3: Run LangChain chain
        response = self.chain.invoke({"examples": examples, "toxic_input": toxic_text})

        # Extract only the rephrased part
        if "Professional Rephrase:" in response:
            rephrased = response.split("Professional Rephrase:")[-1].strip()
        else:
            rephrased = response.strip()

        return {
            "toxic_input": toxic_text,
            "professional_rephrase": rephrased,
            "retrieved_examples": [
                {
                    "toxic": doc.metadata["toxic"],
                    "professional": doc.metadata["professional"],
                    "category": doc.metadata["category"],
                }
                for doc in retrieved_docs[:k]
            ],
            "num_examples_used": k,
            "langchain_components": {
                "llm": "ModalMistralLLM (Custom LangChain wrapper)",
                "retriever": "VectorStoreRetriever (FAISS)",
                "prompt": "PromptTemplate",
                "chain": "LLMChain",
            },
        }
