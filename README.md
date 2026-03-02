# Sistema RAG para FAQs - HR SaaS Platform

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.3+-green.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-orange.svg)
![License](https://img.shields.io/badge/license-Educational-lightgrey.svg)

Sistema de Retrieval-Augmented Generation (RAG) que permite consultar documentación de FAQs usando procesamiento de lenguaje natural y búsqueda semántica.

---

## 📑 Tabla de Contenidos

- [Quick Start](#-quick-start)
- [Descripción](#-descripción)
- [Características Principales](#-características-principales)
- [Tecnologías](#️-tecnologías)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Uso](#-uso)
- [Ejemplos de Consultas](#-ejemplos-de-consultas)
- [Solución de Problemas](#-solución-de-problemas)
- [Preguntas Frecuentes](#-preguntas-frecuentes)
- [Decisiones técnicas](#-decisiones-tecnicas)

---

## � Quick Start

```bash
# 1. Instalar dependencias
pip3 install -r requirements.txt

# 2. Configurar API key
cp env.example .env
# Edita .env y agrega tu OPENAI_API_KEY

# 3. Indexar documentación
python3 src/build_index.py

# 4. Hacer una consulta
python3 src/query.py "¿Cómo solicitar vacaciones?"
```

---

## �📋 Descripción

Este proyecto implementa un sistema RAG que:

- 📄 Indexa documentación de preguntas frecuentes en una base de datos vectorial (ChromaDB)
- 🔍 Permite realizar consultas en lenguaje natural
- 🤖 Genera respuestas contextualizadas usando GPT-4o-mini
- 📚 Devuelve los chunks de documentación utilizados como fuente
- 💾 Exporta respuestas en formato JSON para integración con otros sistemas

## ✨ Características Principales

- **Búsqueda Semántica**: Encuentra información relevante basándose en el significado, no solo palabras clave
- **Respuestas Contextualizadas**: Genera respuestas naturales basadas únicamente en la documentación indexada
- **Trazabilidad**: Muestra exactamente qué partes de la documentación se usaron para generar cada respuesta
- **Modo Interactivo y por Línea de Comandos**: Flexible para diferentes casos de uso
- **Configuración Simple**: Solo necesitas una API key de OpenAI para comenzar
- **Bajo Costo**: Usando modelos optimizados para mantener costos mínimos (~$0.001-0.005 por consulta)

## 🛠️ Tecnologías

- **LangChain**: Framework para aplicaciones RAG
- **OpenAI**: Embeddings (`text-embedding-3-small`) y LLM (`gpt-4o-mini`)
- **ChromaDB**: Base de datos vectorial para almacenar embeddings
- **Python 3**: Lenguaje de programación

## 📦 Requisitos Previos

- Python 3.8 o superior
- Cuenta de OpenAI con API key activa ([Crear cuenta](https://platform.openai.com/signup))
- Saldo disponible en tu cuenta de OpenAI para uso de API
- pip3 instalado

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
cd https://github.com/estefanno18/PI2-henry
```

### 2. Crear y activar entorno virtual (recomendado)

```bash
python3 -m venv venv
source venv/bin/activate  # En macOS/Linux
# o
venv\Scripts\activate  # En Windows
```

### 3. Instalar dependencias

```bash
pip3 install -r requirements.txt
```

### 4. Configurar variables de entorno

Copia el archivo de ejemplo y edítalo con tu API key de OpenAI:

```bash
cp env.example .env
```

Luego edita el archivo `.env` con tu editor preferido y agrega tu API key:

```bash
# API Key de OpenAI (REQUERIDO)
# Obtén tu API key en: https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-your-openai-api-key-here

# Modelo de Embeddings (OPCIONAL)
EMBEDDING_MODEL=text-embedding-3-small

# Modelo LLM para generación de respuestas (OPCIONAL)
LLM_MODEL=gpt-4o-mini
```

## 📂 Estructura del Proyecto

```
PI2/
├── data/
│   └── faq_document.txt          # Documento de FAQs a indexar
├── src/
│   ├── build_index.py            # Script para crear el índice vectorial
│   └── query.py                  # Script para realizar consultas
├── outputs/
│   └── sample_queries.json       # Ejemplos de consultas ejecutadas
├── chroma_db/                    # Base de datos vectorial (se genera)
├── requirements.txt              # Dependencias del proyecto
├── env.example                   # Plantilla de variables de entorno
└── README.md                     # Este archivo
```

## 🔧 Uso

### Paso 1: Indexar la documentación

Antes de realizar consultas, debes indexar el documento de FAQs:

```bash
python3 src/build_index.py
```

**Salida esperada:**

```
📄 Cargando documento desde: data/faq_document.txt
✓ Documento cargado exitosamente
🔪 Dividiendo documento en chunks...
✓ Documento dividido en N chunks
🧠 Generando embeddings con OpenAI...
✓ Embeddings generados y almacenados en ChromaDB
```

**Nota**: Solo necesitas ejecutar este script una vez, o cuando actualices el documento `faq_document.txt`.

### Paso 2: Realizar consultas

Existen dos formas de hacer consultas:

#### Modo Interactivo

```bash
python3 src/query.py
```

El sistema te pedirá que ingreses tu pregunta:

```
❓ Tu pregunta: ¿Cómo solicitar vacaciones?
```

#### Modo de Línea de Comandos

```bash
python3 src/query.py "¿Cómo solicitar vacaciones?"
```

### Salida del Sistema

El sistema mostrará:

1. **Respuesta formateada** con la información relevante
2. **Chunks relacionados** que se utilizaron como fuente
3. **Respuesta en formato JSON** para integración con otros sistemas

Ejemplo de salida JSON:

```json
{
  "user_question": "¿Cómo solicitar vacaciones?",
  "system_answer": "Para solicitar vacaciones, sigue estos pasos:\n1. Ve a 'Mi Tiempo' > 'Solicitar Ausencia' > 'Vacaciones'\n2. Selecciona las fechas de inicio y fin...",
  "chunks_related": [
    {
      "chunk_id": 1,
      "content": "¿Cómo solicitar días de vacaciones?\nPara solicitar vacaciones...",
      "metadata": {...}
    }
  ]
}
```

## Ejemplos de Consultas

El proyecto incluye ejemplos de consultas exitosas en `outputs/sample_queries.json`. Puedes revisar este archivo para ver:

- Tipos de preguntas que el sistema puede responder
- Formato esperado de las respuestas
- Cómo se estructuran los chunks relacionados

## Reindexar Documentación

Si actualizas el archivo `data/faq_document.txt`, simplemente vuelve a ejecutar:

```bash
python3 src/build_index.py
```

El sistema eliminará automáticamente el índice anterior y creará uno nuevo.

## 🐛 Solución de Problemas

### Error: `ModuleNotFoundError`

Instala las dependencias:

```bash
pip3 install -r requirements.txt
```

Asegúrate de estar en el entorno virtual correcto.

**Nota**: Si ves errores con imports de LangChain (como `ModuleNotFoundError: No module named 'langchain.chains'`), asegúrate de tener las versiones correctas instaladas ejecutando:

```bash
pip3 install --upgrade -r requirements.txt
```

### Error: `OpenAI API key not found`

Verifica que el archivo `.env` existe y contiene:

```bash
OPENAI_API_KEY=tu-api-key-aqui
```

### Error: `No matching distribution found for langchain-text-splitters>=2.0.0`

Asegúrate de tener la versión correcta en `requirements.txt`:

```
langchain-text-splitters>=0.3.0
```

### Chunks duplicados en las respuestas

Elimina y reindexa:

```bash
rm -rf chroma_db/
python3 src/build_index.py
```

## ❓ Preguntas Frecuentes

### ¿Puedo usar este sistema con mis propios documentos?

Sí, simplemente reemplaza el contenido de `data/faq_document.txt` con tu documentación y ejecuta `python3 src/build_index.py` para reindexar.

### ¿Funciona en otros idiomas además de español?

Sí, los modelos de OpenAI soportan múltiples idiomas. El sistema funcionará en el idioma de tu documentación.

### ¿Necesito reindexar cada vez que hago una consulta?

No, solo necesitas indexar una vez. Después puedes hacer tantas consultas como quieras sin reindexar, a menos que cambies el documento fuente.

### ¿Puedo usar este sistema sin conexión a Internet?

No, el sistema requiere conexión a Internet para comunicarse con la API de OpenAI.

### ¿Los datos se comparten con OpenAI?

Sí, las consultas y documentos se envían a OpenAI para generar embeddings y respuestas. Revisa la [política de privacidad de OpenAI](https://openai.com/policies/privacy-policy) para más detalles.

### ¿Qué pasa si mi pregunta no está en la documentación?

El sistema responderá "No encuentro esta información en la documentación disponible" si no encuentra contexto relevante.

## 📄 Licencia

Este proyecto es de uso educativo/interno.

## ❓ Decisiones técnicas

- Luego de realizar pruebas con el embedding model text-embedding-3-small y text-embedding-3-large, los resultados no tenian mucha diferencia en si, y considerando que un FAQ no cambia de manera constante, preferi usar el modelo text-embedding-3-small
