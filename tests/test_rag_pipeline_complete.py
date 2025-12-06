"""
Comprehensive tests for rag_pipeline.py module
Tests ModalMistralLLM and DetoxifyRAGPipeline classes
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from unittest.mock import Mock, patch

# Import after path setup
from app.rag_pipeline import ModalMistralLLM, DetoxifyRAGPipeline


class TestModalMistralLLM:
    """Test ModalMistralLLM class"""

    def test_init_default_params(self):
        """Test initialization with default parameters"""
        llm = ModalMistralLLM()
        assert llm.max_tokens == 100
        assert llm.temperature == 0.7

    def test_init_custom_params(self):
        """Test initialization with custom parameters"""
        llm = ModalMistralLLM(max_tokens=200, temperature=0.5)
        assert llm.max_tokens == 200
        assert llm.temperature == 0.5

    def test_llm_type(self):
        """Test _llm_type property"""
        llm = ModalMistralLLM()
        assert llm._llm_type == "modal_mistral"

    def test_identifying_params(self):
        """Test _identifying_params property"""
        llm = ModalMistralLLM(max_tokens=150, temperature=0.8)
        params = llm._identifying_params

        assert params["model"] == "mistralai/Mistral-7B-Instruct-v0.1"
        assert params["platform"] == "Modal"
        assert params["max_tokens"] == 150
        assert params["temperature"] == 0.8

    @patch("app.rag_pipeline.modal.Cls.from_name")
    def test_call_method(self, mock_modal):
        """Test _call method invokes Modal correctly"""
        # Mock Modal response
        mock_model_instance = Mock()
        mock_model_instance.generate.remote.return_value = "Generated response"
        mock_model_class = Mock()
        mock_model_class.return_value = mock_model_instance
        mock_modal.return_value = mock_model_class

        llm = ModalMistralLLM(max_tokens=100, temperature=0.7)
        response = llm._call("Test prompt")

        assert response == "Generated response"
        mock_modal.assert_called_once_with("detoxifyai-mistral", "MistralModel")
        mock_model_instance.generate.remote.assert_called_once_with(
            "Test prompt", max_tokens=100, temperature=0.7
        )

    @patch("app.rag_pipeline.modal.Cls.from_name")
    def test_call_with_custom_params(self, mock_modal):
        """Test _call with custom max_tokens and temperature"""
        mock_model_instance = Mock()
        mock_model_instance.generate.remote.return_value = "Response"
        mock_model_class = Mock()
        mock_model_class.return_value = mock_model_instance
        mock_modal.return_value = mock_model_class

        llm = ModalMistralLLM(max_tokens=200, temperature=0.9)
        llm._call("Prompt")

        mock_model_instance.generate.remote.assert_called_once_with(
            "Prompt", max_tokens=200, temperature=0.9
        )


class TestDetoxifyRAGPipelineInit:
    """Test DetoxifyRAGPipeline initialization"""

    @patch("app.rag_pipeline.DetoxifyRAGPipeline._init_chain")
    @patch("app.rag_pipeline.DetoxifyRAGPipeline._init_llm")
    @patch("app.rag_pipeline.DetoxifyRAGPipeline._load_faiss_index")
    def test_init(self, mock_load, mock_llm, mock_chain):
        """Test initialization calls all setup methods"""
        pipeline = DetoxifyRAGPipeline(
            azure_connection_string="test_conn", azure_container="test_container"
        )

        assert pipeline.azure_connection_string == "test_conn"
        assert pipeline.azure_container == "test_container"
        mock_load.assert_called_once()
        mock_llm.assert_called_once()
        mock_chain.assert_called_once()


class TestLoadFAISSIndex:
    """Test FAISS index loading from Azure"""

    @patch("app.rag_pipeline.HuggingFaceEmbeddings")
    @patch("app.rag_pipeline.FAISS.load_local")
    @patch("app.rag_pipeline.BlobServiceClient")
    @patch("app.rag_pipeline.tempfile")
    @patch("app.rag_pipeline.zipfile.ZipFile")
    def test_load_faiss_index(
        self, mock_zip, mock_temp, mock_blob, mock_faiss, mock_embed
    ):
        """Test FAISS index is loaded from Azure"""
        # Mock temp file
        mock_temp_file = Mock()
        mock_temp_file.name = "/tmp/test.zip"
        mock_temp.NamedTemporaryFile.return_value.__enter__.return_value = (
            mock_temp_file
        )
        mock_temp.mkdtemp.return_value = "/tmp/extract"

        # Mock blob
        mock_blob_client = Mock()
        mock_blob_data = Mock()
        mock_blob_client.download_blob.return_value = mock_blob_data
        mock_blob_service = Mock()
        mock_blob_service.get_blob_client.return_value = mock_blob_client
        mock_blob.from_connection_string.return_value = mock_blob_service

        # Mock FAISS
        mock_vectorstore = Mock()
        mock_retriever = Mock()
        mock_vectorstore.as_retriever.return_value = mock_retriever
        mock_faiss.return_value = mock_vectorstore

        # Mock embeddings
        mock_embed.return_value = Mock()

        # Mock zipfile
        mock_zip_file = Mock()
        mock_zip.return_value.__enter__.return_value = mock_zip_file

        # # Create pipeline (triggers _load_faiss_index)
        # with patch.object(DetoxifyRAGPipeline, '_init_llm'), \
        #      patch.object(DetoxifyRAGPipeline, '_init_chain'):
        # pipeline = DetoxifyRAGPipeline("conn_string", "container")

        # Verify blob client was called
        mock_blob.from_connection_string.assert_called_once_with("conn_string")
        mock_blob_service.get_blob_client.assert_called_once_with(
            container="container", blob="faiss_index.zip"
        )


class TestInitLLM:
    """Test LLM initialization"""

    @patch("app.rag_pipeline.DetoxifyRAGPipeline._init_chain")
    @patch("app.rag_pipeline.DetoxifyRAGPipeline._load_faiss_index")
    @patch("app.rag_pipeline.ModalMistralLLM")
    def test_init_llm(self, mock_llm_class, mock_load, mock_chain):
        """Test LLM is initialized with correct params"""
        mock_llm_instance = Mock()
        mock_llm_class.return_value = mock_llm_instance

        pipeline = DetoxifyRAGPipeline("conn", "container")

        assert pipeline.llm == mock_llm_instance
        mock_llm_class.assert_called_once_with(max_tokens=100, temperature=0.7)


class TestInitChain:
    """Test LangChain chain initialization"""

    @patch("app.rag_pipeline.DetoxifyRAGPipeline._load_faiss_index")
    @patch("app.rag_pipeline.DetoxifyRAGPipeline._init_llm")
    @patch("app.rag_pipeline.PromptTemplate")
    @patch("app.rag_pipeline.StrOutputParser")
    def test_init_chain(self, mock_parser, mock_template, mock_llm, mock_load):
        """Test chain is initialized with prompt template"""
        mock_template_instance = Mock()
        mock_template.return_value = mock_template_instance
        mock_parser_instance = Mock()
        mock_parser.return_value = mock_parser_instance

        # Mock the pipeline operator
        mock_template_instance.__or__ = Mock(
            return_value=Mock(__or__=Mock(return_value="chain"))
        )

        # pipeline = DetoxifyRAGPipeline("conn", "container")

        # Verify PromptTemplate was created
        mock_template.assert_called_once()
        call_kwargs = mock_template.call_args[1]
        assert "input_variables" in call_kwargs
        assert "template" in call_kwargs


class TestFormatExamples:
    """Test example formatting for prompts"""

    @patch("app.rag_pipeline.DetoxifyRAGPipeline._init_chain")
    @patch("app.rag_pipeline.DetoxifyRAGPipeline._init_llm")
    @patch("app.rag_pipeline.DetoxifyRAGPipeline._load_faiss_index")
    def test_format_examples_empty(self, mock_load, mock_llm, mock_chain):
        """Test formatting with no examples"""
        pipeline = DetoxifyRAGPipeline("conn", "container")
        result = pipeline._format_examples([], k=5)

        assert result == ""

    @patch("app.rag_pipeline.DetoxifyRAGPipeline._init_chain")
    @patch("app.rag_pipeline.DetoxifyRAGPipeline._init_llm")
    @patch("app.rag_pipeline.DetoxifyRAGPipeline._load_faiss_index")
    def test_format_examples_with_docs(self, mock_load, mock_llm, mock_chain):
        """Test formatting with example documents"""
        pipeline = DetoxifyRAGPipeline("conn", "container")

        # Mock documents
        doc1 = Mock()
        doc1.metadata = {
            "toxic": "you are stupid",
            "professional": "I respectfully disagree",
            "category": "disagreement",
        }
        doc2 = Mock()
        doc2.metadata = {
            "toxic": "this is terrible",
            "professional": "This could be improved",
            "category": "criticism",
        }

        result = pipeline._format_examples([doc1, doc2], k=2)

        assert "Example 1:" in result
        assert "you are stupid" in result
        assert "I respectfully disagree" in result
        assert "Example 2:" in result
        assert "this is terrible" in result

    @patch("app.rag_pipeline.DetoxifyRAGPipeline._init_chain")
    @patch("app.rag_pipeline.DetoxifyRAGPipeline._init_llm")
    @patch("app.rag_pipeline.DetoxifyRAGPipeline._load_faiss_index")
    def test_format_examples_respects_k(self, mock_load, mock_llm, mock_chain):
        """Test formatting respects k parameter"""
        pipeline = DetoxifyRAGPipeline("conn", "container")

        # Create 5 mock documents
        docs = []
        for i in range(5):
            doc = Mock()
            doc.metadata = {
                "toxic": f"toxic{i}",
                "professional": f"prof{i}",
                "category": "test",
            }
            docs.append(doc)

        result = pipeline._format_examples(docs, k=3)

        # Should only have 3 examples
        assert result.count("Example") == 3
        assert "toxic0" in result
        assert "toxic1" in result
        assert "toxic2" in result
        assert "toxic3" not in result


class TestRephrase:
    """Test the main rephrase method"""

    @patch("app.rag_pipeline.DetoxifyRAGPipeline._init_chain")
    @patch("app.rag_pipeline.DetoxifyRAGPipeline._init_llm")
    @patch("app.rag_pipeline.DetoxifyRAGPipeline._load_faiss_index")
    def test_rephrase_full_flow(self, mock_load, mock_llm, mock_chain):
        """Test complete rephrase flow"""
        pipeline = DetoxifyRAGPipeline("conn", "container")

        # Mock retriever
        doc1 = Mock()
        doc1.metadata = {
            "toxic": "you are wrong",
            "professional": "I have a different perspective",
            "category": "disagreement",
        }
        mock_retriever = Mock()
        mock_retriever.invoke.return_value = [doc1]
        pipeline.retriever = mock_retriever

        # Mock chain
        mock_chain_obj = Mock()
        mock_chain_obj.invoke.return_value = (
            "Professional Rephrase: I respectfully disagree with your view"
        )
        pipeline.chain = mock_chain_obj

        result = pipeline.rephrase("you are stupid", k=5)

        assert result["toxic_input"] == "you are stupid"
        assert "respectfully disagree" in result["professional_rephrase"]
        assert len(result["retrieved_examples"]) == 1
        assert result["num_examples_used"] == 5
        assert "langchain_components" in result

    @patch("app.rag_pipeline.DetoxifyRAGPipeline._init_chain")
    @patch("app.rag_pipeline.DetoxifyRAGPipeline._init_llm")
    @patch("app.rag_pipeline.DetoxifyRAGPipeline._load_faiss_index")
    def test_rephrase_without_prefix(self, mock_load, mock_llm, mock_chain):
        """Test rephrase when response doesn't have 'Professional Rephrase:' prefix"""
        pipeline = DetoxifyRAGPipeline("conn", "container")

        # Mock retriever
        mock_retriever = Mock()
        mock_retriever.invoke.return_value = []
        pipeline.retriever = mock_retriever

        # Mock chain - no prefix
        mock_chain_obj = Mock()
        mock_chain_obj.invoke.return_value = "This is a polite response"
        pipeline.chain = mock_chain_obj

        result = pipeline.rephrase("test", k=3)

        assert result["professional_rephrase"] == "This is a polite response"

    @patch("app.rag_pipeline.DetoxifyRAGPipeline._init_chain")
    @patch("app.rag_pipeline.DetoxifyRAGPipeline._init_llm")
    @patch("app.rag_pipeline.DetoxifyRAGPipeline._load_faiss_index")
    def test_rephrase_with_multiple_examples(self, mock_load, mock_llm, mock_chain):
        """Test rephrase with multiple retrieved examples"""
        pipeline = DetoxifyRAGPipeline("conn", "container")

        # Mock retriever with multiple docs
        docs = []
        for i in range(5):
            doc = Mock()
            doc.metadata = {
                "toxic": f"toxic{i}",
                "professional": f"prof{i}",
                "category": f"cat{i}",
            }
            docs.append(doc)

        mock_retriever = Mock()
        mock_retriever.invoke.return_value = docs
        pipeline.retriever = mock_retriever

        # Mock chain
        mock_chain_obj = Mock()
        mock_chain_obj.invoke.return_value = "Polite output"
        pipeline.chain = mock_chain_obj

        result = pipeline.rephrase("test input", k=5)

        assert len(result["retrieved_examples"]) == 5
        assert result["retrieved_examples"][0]["toxic"] == "toxic0"

    @patch("app.rag_pipeline.DetoxifyRAGPipeline._init_chain")
    @patch("app.rag_pipeline.DetoxifyRAGPipeline._init_llm")
    @patch("app.rag_pipeline.DetoxifyRAGPipeline._load_faiss_index")
    def test_rephrase_k_parameter(self, mock_load, mock_llm, mock_chain):
        """Test rephrase respects k parameter"""
        pipeline = DetoxifyRAGPipeline("conn", "container")

        # Mock retriever with 10 docs
        docs = [Mock() for _ in range(10)]
        for i, doc in enumerate(docs):
            doc.metadata = {"toxic": f"t{i}", "professional": f"p{i}", "category": "c"}

        mock_retriever = Mock()
        mock_retriever.invoke.return_value = docs
        pipeline.retriever = mock_retriever

        mock_chain_obj = Mock()
        mock_chain_obj.invoke.return_value = "Output"
        pipeline.chain = mock_chain_obj

        result = pipeline.rephrase("test", k=3)

        # Should only return 3 examples even though 10 were retrieved
        assert len(result["retrieved_examples"]) == 3
        assert result["num_examples_used"] == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
