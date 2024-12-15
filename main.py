import streamlit as st
from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_dom_content,
)
from parse import parse_with_ollama
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

st.title("AI Web Scraper")
url = st.text_input("Enter Website URL", placeholder="https://example.com")

if st.button("Scrape Website"):
    if url:
        try:
            logging.info("Scraping the website...")
            with st.spinner("Scraping the website..."):
                dom_content = scrape_website(url)
                logging.info("Extracting body content...")
                body_content = extract_body_content(dom_content)
                logging.info("Cleaning body content...")
                cleaned_content = clean_body_content(body_content)

            st.session_state.dom_content = cleaned_content

            with st.expander("View DOM Content"):
                st.text_area("DOM Content", cleaned_content, height=300)
        except Exception as e:
            logging.error("Error scraping website: %s", e)
            st.error("Error scraping website")

if "dom_content" in st.session_state:
    parse_description = st.text_area(
        "Describe what you want to parse", placeholder="Enter parse description"
    )

    if st.button("Parse Content"):
        if parse_description:
            try:
                logging.info("Parsing the content...")
                with st.spinner("Parsing the content..."):
                    dom_chunks = split_dom_content(st.session_state.dom_content)
                    parsed_result = parse_with_ollama(dom_chunks, parse_description)
                    logging.info("Parsed result: %s", parsed_result)
                    st.write(parsed_result)
            except Exception as e:
                logging.error("Error parsing content: %s", e)
                st.error("Error parsing content")
