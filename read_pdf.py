from langchain_core.tools import tool
import io
import fitz  # PyMuPDF
import requests

@tool
def read_pdf(url: str)-> str:
    """Read and extract text from a pdf file given its URL.
    Args:
        url: the URL of the pdf file to read
        
    return: 
        the extracted text content from the pdf
        """
    try:
        response = requests.get(url)
        pdf_file = io.BytesIO(response.content)
        doc = fitz.open(stream = pdf_file , filetype = "pdf")
        num_page=doc.page_count

        text =""
        for i, page in enumerate(doc, 1):
            print(f"Extracting text from page {i}/{num_page}")
            text += page.get_text() + "\n"
        
        print(f"Successfull extracted {len(text)} characters of text from pdf")

        return text.strip()
    except Exception as e:
            print(f"Error reading PDF: {str(e)}")

            raise
    return text
            