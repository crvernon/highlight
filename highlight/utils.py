import PyPDF2
import tiktoken
from tqdm import tqdm


def get_token_count(text, model="gpt-4o"):
    """
    Calculate the number of tokens in a given text based on the specified model.

    Parameters:
    text (str): The text content to be tokenized.
    model (str): The model to use for tokenization. Default is "gpt-4o".

    Returns:
    int: The number of tokens in the text.
    """

    encoding = tiktoken.encoding_for_model(model)
    encoded_text = encoding.encode(text)
    n_text_tokens = len(encoded_text)

    return n_text_tokens


def read_pdf(file_object: object, reference_indicator: str = "References\n") -> dict:
    """
    Extract text content from a PDF file until a specified reference indicator is encountered.

    Parameters:
    file_object (object): The PDF file object to read from.
    reference_indicator (str): The string indicating the start of the reference section. Default is "References\n".

    Returns:
    dict: A dictionary containing the extracted content, number of pages read, number of characters, 
          number of words, and number of tokens.
    """

    content = ""
    n_pages = 0

    # creating a pdf reader object
    reader = PyPDF2.PdfReader(file_object)

    for page in reader.pages:

        page_content = page.extract_text()

        if reference_indicator in page_content:
            content += page_content
            break

        else:
            content += page_content

        n_pages += 1

    content = content.split(reference_indicator)[0]

    return {
        "content": content,
        "n_pages": n_pages,
        "n_characters": len(content),
        "n_words": len(content.split(" ")),
        "n_tokens": get_token_count(content)
    }


def read_text(file_object: object) -> dict:
    """
    Read text file input and return its content along with metadata.

    Parameters:
    file_object (object): The file object to read from.

    Returns:
    dict: A dictionary containing the content, number of pages, number of characters,
          number of words, and number of tokens.
    """
    content = bytes.decode(file_object.read(), 'utf-8')

    return {
        "content": content,
        "n_pages": 1,
        "n_characters": len(content),
        "n_words": len(content.replace("\n", " ").split()),
        "n_tokens": get_token_count(content)
    }


def content_reduction(
    client,
    document_list,
    system_scope,
    model
):
    """
    Remove irrelevant content from input text.

    Parameters:
    client (OpenAI): The OpenAI client instance.
    document_list (list): A list of documents to process.
    system_scope (str): The system scope or context for the prompt.
    model (str): The model to use for content reduction.

    Returns:
    str: The content with irrelevant parts removed.
    """

    prompt = """Remove irrelevant content from the following text.\n\n{text}\n\n}"""

    content = ""
    for i in tqdm(range(len(document_list))):
        page_content = document_list[i].page_content
        page_tokens = get_token_count(page_content)

        messages = [
            {"role": "system", "content": system_scope},
            {"role": "user", "content": prompt.format(text=page_content)}
        ]

        response = client.chat.completions.create(
            model=model,
            max_tokens=page_tokens,
            temperature=0.0,
            messages=messages
        )

        content += response.choices[0].message.content

    return content


def generate_content(
    client,
    system_scope,
    prompt,
    max_tokens=50,
    temperature=0.0,
    max_allowable_tokens=8192,
    model="gpt-4o"
):
    """
    Generate content using the OpenAI API based on the provided prompt and parameters.

    Parameters:
    client (OpenAI): The OpenAI client instance.
    system_scope (str): The system scope or context for the prompt.
    prompt (str): The user prompt to generate content from.
    max_tokens (int, optional): The maximum number of tokens to generate. Defaults to 50.
    temperature (float, optional): The sampling temperature. Defaults to 0.0.
    max_allowable_tokens (int, optional): The maximum allowable tokens for the prompt and response. Defaults to 8192.
    model (str, optional): The model to use for content generation. Defaults to "gpt-4o".

    Returns:
    str: The generated content.

    Raises:
    RuntimeError: If the total number of tokens in the prompt and response exceeds max_allowable_tokens.
    """

    n_prompt_tokens = get_token_count(prompt) + max_tokens

    if n_prompt_tokens > max_allowable_tokens:
        raise RuntimeError((
            f"ERROR:  input text tokens needs to be reduced due to exceeding the maximum ",
            " allowable tokens per prompt by {n_prompt_tokens - max_allowable_tokens} tokens."
        ))

    messages = [
        {"role": "system", "content": system_scope},
        {"role": "user", "content": prompt}
    ]

    response = client.chat.completions.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        messages=messages
    )

    content = response.choices[0].message.content

    return content
