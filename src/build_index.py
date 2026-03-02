from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

load_dotenv()

def main():
    file_path = 'data/faq_document.txt'
    documents = load_file(file_path)
    chunks = split_into_chunks(documents)
    vectorstore = create_vector_store(chunks, 'chroma_db')
        
    print("\n Verificando indexación...")
    collection = vectorstore._collection
    count = collection.count()
    print(f"✓ Total de documentos indexados: {count}")
    
    print("\n" + "=" * 60)
    print("INDEXACIÓN COMPLETADA EXITOSAMENTE")
    print("=" * 60)
    print("\n Próximos pasos:")
    print("   1. Ejecuta 'python src/query.py' para probar consultas")
    print("   2. Los embeddings están guardados en ./chroma_db/")
    print("   3. No necesitas volver a indexar a menos que cambies el documento")

def load_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f" No se encontró el archivo: {file_path}")
    
    print(f" Cargando documento desde: {file_path}")
    loader = TextLoader(file_path, encoding='utf-8')
    documents = loader.load()
    print(f"✓ Documento cargado exitosamente. Tamaño: {len(documents[0].page_content)} caracteres")
    return documents

def split_into_chunks(documents):
    print("\n Dividiendo documento en chunks...")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,        
        chunk_overlap=200,    
        length_function=len,   
        separators=["\n\n", "\n", " ", ""] 
    )
    
    chunks = text_splitter.split_documents(documents)
    print(f"✓ Documento dividido en {len(chunks)} chunks")
    
    print("\n Información de los chunks:")
    print(f"   - Total de chunks: {len(chunks)}")
    print(f"   - Tamaño del chunk 1: {len(chunks[0].page_content)} caracteres")
    print(f"   - Tamaño del chunk 2: {len(chunks[1].page_content)} caracteres")
    print(f"\n   Preview del primer chunk:")
    print(f"   {chunks[0].page_content[:200]}...")
    return chunks

def create_vector_store(chunks, persist_directory):
    print("\n Generando embeddings con OpenAI...")
    
    embedding_model = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    embeddings = OpenAIEmbeddings(model=embedding_model)
    
    print(f"   - Modelo de embeddings: {embedding_model}")
    print(f"   - Procesando {len(chunks)} chunks...")
    
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory,
        collection_name="faq_collection"
    )
    
    print(f"✓ Embeddings generados y almacenados en ChromaDB")
    print(f"   - Ubicación: {persist_directory}")
    print(f"   - Colección: faq_collection")
    
    return vectorstore

if __name__ == "__main__":
    main()
