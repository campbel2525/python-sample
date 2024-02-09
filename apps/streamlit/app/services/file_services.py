import fitz  # PyMuPDF
from langchain.document_loaders import PyMuPDFLoader


class PdfService:

    def __init__(self, filepath: str):
        self.filepath = filepath

    def get_documents(self):
        loader = PyMuPDFLoader(self.filepath)
        documents = loader.load_and_split()
        if len(documents) == 0:
            return None

        return documents


class PdfStreamService:

    def __init__(self, pdf_data):
        self.pdf_data = pdf_data

    def get_documents(self):
        # PDFファイルをメモリ上で開く
        doc = fitz.open(stream=self.pdf_data, filetype="pdf")
        text = ""
        # 各ページのテキストを抽出
        for page in doc:
            text += page.get_text()
        return text
