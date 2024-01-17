from io import BytesIO

import tiktoken
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

from prompts import build_prompt_template


def get_token_count(text, model="gpt-4-1106-preview"):
    """Get the token count of text content based on the model"""

    encoding = tiktoken.encoding_for_model(model)
    encoded_text = encoding.encode(text)
    n_text_tokens = len(encoded_text)

    return n_text_tokens


def load_pdf(uploaded_file: BytesIO):
    """
    Load a PDF from a given file path and split it into chunks.

    This function uses the PyPDFLoader to load a PDF file, split it into
    pages, and then extract content from each page. It returns a dictionary
    with the content, number of pages, number of words, and number of tokens.

    :param uploaded_file: The uploaded file from the streamlit uploader
    :type uploaded_file: BytesIO
    :return: A dictionary with keys 'content', 'n_pages', 'n_words', and 'n_tokens'.
    :rtype: dict
    """
    # have to first save to temp file
    temp_file = "./temp.pdf"
    with open(temp_file, "wb") as file:
        file.write(uploaded_file.getvalue())
        file_name = uploaded_file.name

    loader = PyPDFLoader(temp_file)

    # load documents and splits into chunks
    pages = loader.load_and_split()

    return {
        "content": pages,
        "n_pages": len(set([i.metadata["page"] for i in pages])),
        "n_words": sum([len(i.page_content.split()) for i in pages]),
        "n_tokens": get_token_count(" ".join([i.page_content for i in pages]))
    }


def read_text(file_object: object,) -> dict:
    """Read text file input."""

    content = bytes.decode(file_object.read(), 'utf-8')

    return {
        "content": content,
        "n_pages": 1,
        "n_characters": len(content),
        "n_words": len(content.replace("\n", " ").split()),
        "n_tokens": get_token_count(content)
    }








def build_conversational_chain(
    chat_template: str,
    vector_store: FAISS,
    memory: ConversationBufferMemory,  
    temperature: float = 0.0,
    model: str = "gpt-4-1106-preview",
    max_tokens: int = 50
) -> ConversationalRetrievalChain:
    """
    Build a conversational retrieval chain for interacting with a language model.

    This function initializes a language model with specified parameters and
    constructs a conversational chain that can be used to retrieve information
    and generate responses based on a given chat template, vector store, and memory.

    :param chat_template: The template used to format the chat prompts.
    :param vector_store: The vector store that provides retrieval capabilities.
    :param memory: The memory buffer to store conversation history.
    :param temperature: The sampling temperature for the language model's responses.
    :param model: The identifier of the language model to be used.
    :param max_tokens: The maximum number of tokens to generate in each response.
    :return: A ConversationalRetrievalChain object.
    """
    # instantiate llm
    llm = ChatOpenAI(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens
    )

    # construct conversational chain
    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(),
        memory=memory,
        combine_docs_chain_kwargs={
            "prompt": chat_template
        },
    ) 


def build_vector_store(
    chunks: list,
    local_db_path: str = "./tempdb",
    load_from_file: bool = False
) -> FAISS:
    """
    Build a vector store from document chunks and save or load it locally.

    This function takes a list of document chunks, generates embeddings for them,
    and builds a FAISS vector store. The vector store can either be saved to a
    local database path or loaded from it, depending on the `load_from_file` flag.

    :param chunks: A list of document chunks to be embedded and stored.
    :param local_db_path: The local file path to save or load the vector store.
    :param load_from_file: A boolean flag to load the vector store from the local
                           path instead of saving it. Defaults to False.
    :return: A FAISS vector store containing the document embeddings.
    """
    # generate embeddings object
    embeddings = OpenAIEmbeddings()

    # build vector db
    vector_store = FAISS.from_documents(
        chunks, embeddings
    )

    if load_from_file:
        vector_store = FAISS.load_local(local_db_path, embeddings)
    else:
        vector_store.save_local(local_db_path)

    return vector_store








