
import getpass, os


os.environ["HF_API_TOKEN"] = getpass.getpass("Your Hugging Face token")


import gradio as gr

from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack.components.builders import ChatPromptBuilder
from haystack.dataclasses import ChatMessage
from haystack.components.generators.chat import HuggingFaceAPIChatGenerator
from haystack.components.generators import HuggingFaceAPIGenerator
from haystack.components.builders import PromptBuilder
from haystack.components.writers import DocumentWriter
from haystack.components.converters import MarkdownToDocument, PyPDFToDocument, TextFileToDocument
from haystack.components.preprocessors import DocumentSplitter, DocumentCleaner
from haystack.components.routers import FileTypeRouter
from haystack.components.joiners import DocumentJoiner
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack import Pipeline
from haystack.document_stores.in_memory import InMemoryDocumentStore
document_store = InMemoryDocumentStore()
def process_pdf(pdf_path):
    
   global document_store

   pdf_converter = PyPDFToDocument()
   document_cleaner = DocumentCleaner()
   document_splitter = DocumentSplitter(split_by="word", split_length=150, split_overlap=50)
   document_embedder = SentenceTransformersDocumentEmbedder(model="sentence-transformers/all-MiniLM-L6-v2")
   document_writer = DocumentWriter(document_store)
   pipeline=Pipeline()
   pipeline.add_component("converter", pdf_converter)
   pipeline.add_component("cleaner", document_cleaner)
   pipeline.add_component("splitter", document_splitter)
   pipeline.add_component("embedder", document_embedder)
   pipeline.add_component("writer", document_writer)
   pipeline.connect("converter", "cleaner")
   pipeline.connect("cleaner", "splitter")
   pipeline.connect("splitter", "embedder")
   pipeline.connect("embedder", "writer")
   try:
        a=pipeline.run({"converter": {"sources": [pdf_path]}})

   except Exception as e:
        a=f"Pipeline çalışırken hata oluştu: {e}"
   return a,document_store



prompt_template = """
According to these documents:

{% for doc in documents %}
  {{ doc.content }}
{% endfor %}

Answer the given question: {{query}}
Answer:
"""
prompt_builder= PromptBuilder(template=prompt_template)
generator = HuggingFaceAPIGenerator(api_type="serverless_inference_api",api_params={"model": "mistralai/Mixtral-8x7B-Instruct-v0.1"})


query_pipeline = Pipeline()
query_pipeline.add_component("embedder", SentenceTransformersTextEmbedder(model="sentence-transformers/all-MiniLM-L6-v2"))
query_pipeline.add_component("retriever", InMemoryEmbeddingRetriever(document_store=document_store))
query_pipeline.add_component("prompt_builder", prompt_builder)
query_pipeline.add_component("generator", generator)

query_pipeline.connect("embedder.embedding", "retriever.query_embedding")
query_pipeline.connect("retriever.documents", "prompt_builder.documents")
query_pipeline.connect("prompt_builder", "generator")

def get_generative_answer(query,history):

    results =query_pipeline.run({
      "embedder": {"text": query},
      "prompt_builder": {"query": query} })
    answer = results["generator"]["replies"][0]

  

    return answer

with gr.Blocks() as demo:
    gr.Markdown("# 📄 YOUR PDF BUDDY")

    chatbot = gr.ChatInterface(get_generative_answer, type="messages", autofocus=True)
    with gr.Row():
        pdf_input = gr.File(label="📂 Upload Pdf", type="filepath")
        process_button = gr.Button("🔄 Process Pdf")
    status_output = gr.Textbox(label="Durum", interactive=False)

    process_button.click(fn=process_pdf, inputs=pdf_input, outputs=status_output)




demo.launch(share=True)
