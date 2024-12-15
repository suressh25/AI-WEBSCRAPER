from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import logging
from typing import List

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

model = OllamaLLM(model="llama3.2")


def parse_with_ollama(dom_chunks: List[str], parse_description: str) -> str:
    """
    This function takes in a list of DOM chunks and a parse description,
    and returns the extracted information based on the provided description.

    Args:
    dom_chunks (List[str]): A list of DOM chunks to parse.
    parse_description (str): A description of the information to extract.

    Returns:
    str: The extracted information.
    """
    logging.info("Starting parsing process")
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        try:
            logging.info(f"Parsing batch: {i} of {len(dom_chunks)}")
            response = chain.invoke(
                {"dom_content": chunk, "parse_description": parse_description}
            )
            logging.info(f"Parsed batch: {i} of {len(dom_chunks)}")
            parsed_results.append(response)
        except Exception as e:
            logging.error(f"Error parsing batch {i}: {str(e)}")

    logging.info("Parsing process completed")
    return "\n".join(parsed_results)
