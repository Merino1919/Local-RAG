from langchain_community.document_loaders import PyMuPDFLoader, UnstructuredExcelLoader

def select_loader(file_path: str):
    if file_path.endswith('.pdf'):
        return PyMuPDFLoader(file_path)
    elif file_path.endswith(('.xlsx', '.xls')):
        # mode="elements" helps keeping table structure
        return UnstructuredExcelLoader(file_path, mode="elements")
    else:
        raise ValueError(f"Formato no soportado: {file_path}")