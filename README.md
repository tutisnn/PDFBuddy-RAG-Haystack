# PDF Buddy-RAG-Haystack

## Description

PDF Buddy-RAG-Haystack is a Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents, process their content, and interact with them using a chatbot interface. Built using **Haystack**, **Gradio**, and **Hugging Face API**, this project enables users to retrieve relevant document content and generate AI-powered responses to queries.

## Installation

To run this project locally, ensure you have Python installed and then install the required dependencies:

```sh
pip install gradio farm-haystack transformers sentence-transformers
```

## Usage

Run the script to launch the Gradio web interface:

```sh
python app.py
```

Then, open the interface in your browser, upload a PDF, and start interacting with the chatbot.

## Components

- **Document Processing Pipeline**: Converts, cleans, and embeds PDF text for retrieval.
- **Query Pipeline**: Retrieves relevant document snippets and generates AI-powered answers.
- **Gradio Chatbot**: Provides an easy-to-use web-based interface for user interaction.

## How It Works

1. **Upload a PDF**: The document is processed and stored.
2. **Ask a Question**: The system retrieves relevant document content.
3. **Generate an Answer**: The AI model formulates a response based on the retrieved content.

## Technologies Used

- **Haystack** for document processing and retrieval.
- **Hugging Face API** for response generation.
- **Gradio** for the user interface.
- **SentenceTransformers** for text embeddings.

