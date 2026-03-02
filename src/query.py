from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import os
import sys
import json

load_dotenv()

def load_vectorstore(persist_directory):
    print(f" Cargando vectorstore desde: {persist_directory}")
    
    embedding_model = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    embeddings = OpenAIEmbeddings(model=embedding_model)
    
    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings,
        collection_name="faq_collection"
    )
    
    print(f"✓ Vectorstore cargado exitosamente")
    return vectorstore

def process_query(qa_chain, question):
    print(f"\n Procesando pregunta: \"{question}\"")
    result = qa_chain.invoke({"query": question})
    answer = result["result"]
    source_docs = result["source_documents"]
    chunks_related = [
        {
            "chunk_id": i + 1,
            "content": doc.page_content,
            "metadata": doc.metadata
        }
        for i, doc in enumerate(source_docs)
    ]
    
    print(f"✓ Respuesta generada usando {len(chunks_related)} chunks relevantes")
    
    response = {
        "user_question": question,
        "system_answer": answer,
        "chunks_related": chunks_related
    }
    
    return response

def create_qa_chain(vectorstore):
    llm_model = os.getenv("LLM_MODEL", "gpt-4o-mini")
    llm = ChatOpenAI(
        model=llm_model,
        temperature=0.3
    )
    
    prompt_template = """Eres un asistente virtual de soporte para un sistema HR SaaS. 
Tu objetivo es ayudar a los usuarios respondiendo sus preguntas basándote ÚNICAMENTE en la documentación proporcionada.

Contexto de la documentación:
{context}

Pregunta del usuario: {question}

Instrucciones:
- Proporciona una respuesta clara, precisa y profesional
- Basa tu respuesta SOLO en la información del contexto proporcionado
- Si la información no está en el contexto, di claramente "No encuentro esta información en la documentación disponible"
- Organiza la información de forma estructurada usando viñetas o pasos numerados cuando sea apropiado
- Sé conciso pero completo

Respuesta:"""

    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )
    
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 4}
    )
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT}
    )
    
    return qa_chain

def main():
    print("SISTEMA RAG DE SOPORTE PARA FAQs - HR SaaS")
    print("=" * 80)
    
    chroma_directory = 'chroma_db'
    vectorstore = load_vectorstore(chroma_directory)
    
    print(" Configurando cadena de pregunta-respuesta...")
    qa_chain = create_qa_chain(vectorstore)
    print("✓ Cadena de QA lista")

    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
    else:
        print("\n" + "=" * 80)
        print("Modo interactivo: Escribe tu pregunta (o 'salir' para terminar)")
        print("=" * 80)
        question = input("\n❓ Tu pregunta: ").strip()
        
        if question.lower() in ['salir']:
            print("¡Hasta luego!")
            return
    
    if not question:
        print(" Error: No se proporcionó ninguna pregunta")
        return
    
    response = process_query(qa_chain, question)
 
    print("\n JSON Response:")
    print(json.dumps(response, indent=2, ensure_ascii=False))

    print(f"\n✅ Consulta procesada exitosamente")
    
if __name__ == "__main__":
    main()