# Compass

Safety-First Coaching with Bounded LLM & Evidence Gate

## Overview

Compass is a safety-first coaching system that provides evidence-based guidance using a counseling Q&A corpus. The system:

1. **Searches** for relevant cases from a counseling corpus using hybrid retrieval (dense + lexical)
2. **Generates** safety-first coaching responses using LLM synthesis with strict evidence grounding
3. **Enforces** safety through crisis detection and evidence verification gates
4. **Provides** transparent, observable results with citations and metrics

## Architecture

### Backend (FastAPI + Python)

**Core Services:**
- **IndexManager**: Thread-safe singleton managing FAISS vector indices
- **EmbeddingService**: Sentence transformers for dense embeddings
- **RetrievalService**: Hybrid search (dense + BM25 lexical + RRF fusion + MMR diversification)
- **SafetyService**: Crisis detection and evidence verification
- **CoachService**: LLM synthesis with evidence grounding

**Data Flow:**
1. **Indexing**: Cases are processed into context and response sentence embeddings
2. **Search**: Hybrid retrieval finds top-k relevant cases
3. **Coaching**: LLM synthesizes response using selected cases with citations
4. **Verification**: Evidence gate ensures response is grounded in corpus

**Key Components:**
- **Vector Stores**: FAISS indices for context and response sentences
- **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2` (384-dim)
- **LLM**: GPT-4o-mini for synthesis (JSON-only output)
- **Safety**: Crisis patterns + evidence overlap verification

### Frontend (React + Tailwind CSS)

**Components:**
- **SearchSection**: Query input and results display
- **CoachSection**: Coaching response with markdown rendering
- **CaseCard**: Individual case display with selection
- **SearchResults**: Results list with case selection
- **CoachPanel**: Coaching interface and response display

**State Management:**
- **useAppState**: Centralized state management hook
- **API Integration**: Direct fetch calls to backend endpoints

## Features

### Search & Retrieval
- **Hybrid Search**: Combines dense embeddings with BM25 lexical search
- **RRF Fusion**: Reciprocal Rank Fusion for combining search results
- **MMR Diversification**: Maximum Marginal Relevance for result diversity
- **Sentence-Level**: Retrieves individual sentences with character offsets

### Coaching & Safety
- **LLM Synthesis**: Single LLM call generates full response with citations
- **Evidence Gate**: Verifies response grounding using ROUGE-L overlap
- **Crisis Detection**: Pattern-based crisis language detection
- **Citation Tracking**: Precise sentence-level citations with offsets

### Observability
- **Metrics**: Request counts, latencies, gate pass/fail rates
- **Logging**: Comprehensive logging throughout the pipeline
- **Health Checks**: Service status and initialization state

## Technical Architecture Deep Dive

### Retrieval Architecture

The retrieval system uses a **4-stage hybrid approach**:

**Stage 1: Dense Retrieval**
```python
# Generate query embedding
query_embedding = embedding_service.embed_text(query)
# Search context index for top-k1 candidates
dense_hits = context_index.search(query_embedding[0], k1=100)
```

**Stage 2: Lexical Search**
```python
# BM25 search on tokenized contexts
lexical_results = bm25.get_scores(query_tokens)
# Normalize and rank results
```

**Stage 3: RRF Fusion**
```python
# Reciprocal Rank Fusion combines both approaches
rrf_score = 1 / (rank_dense + rank_lexical + c)
# c = 60 (configurable constant)
```

**Stage 4: MMR Diversification**
```python
# Maximum Marginal Relevance balances relevance and diversity
mmr_score = λ * relevance_score + (1-λ) * diversity_score
# λ = 0.7 (configurable)
```

**Key Parameters:**
- `k1`: 100 (initial candidates)
- `n`: 10 (cases to probe)
- `top_final`: 3 (final results)
- `rrf_c`: 60 (fusion constant)
- `mmr_lambda`: 0.7 (diversity weight)

### Embedding Architecture

**Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Dimensions**: 384
- **Normalization**: Unit length (cosine similarity)
- **Batch Processing**: 32 sentences per batch

**Two-Level Embedding Structure:**

1. **Context Embeddings**:
   ```python
   contexts = [case.context for case in cases]
   context_embeddings = embed_text(contexts)  # Shape: (n_cases, 384)
   ```

2. **Response Sentence Embeddings**:
   ```python
   # Flatten all sentences across cases
   response_sentences = []
   for case in cases:
       for sent in case.response_sentences:
           response_sentences.append(sent.text)
   
   # Generate embeddings
   sentence_embeddings = embed_text(response_sentences)  # Shape: (n_sentences, 384)
   ```

**Index Structure:**
- **Context Index**: 2,467 vectors (one per case)
- **Response Index**: 26,253 vectors (one per sentence)
- **Payload Storage**: Case metadata, sentence offsets, character spans

**Search Process:**
1. Query → 384-dim embedding
2. Context search → Top-100 cases
3. Sentence search → Individual sentence retrieval
4. RRF fusion → Combined ranking
5. MMR diversification → Final top-3

## Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- LLM API key (OpenAI)

### Backend Setup

1. **Clone and navigate:**
   ```bash
   cd Legacy
   ```

2. **Install Python dependencies:**
   ```bash
   cd src/backend
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set environment variables:**
   ```bash
   cp env.example .env
   # Edit .env with your LLM API key
   export LLM_API_KEY="your-openai-api-key"
   ```

### Frontend Setup

1. **Install Node dependencies:**
   ```bash
   cd src/frontend
   npm install
   ```

## Usage

### Development

1. **Start backend:**
   ```bash
   cd src/backend
   python3 main.py --host 0.0.0.0 --port 8000 --reload
   ```

2. **Start frontend:**
   ```bash
   cd src/frontend
   npm start
   ```

3. **Access application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

### Production

1. **Build frontend:**
   ```bash
   cd src/frontend
   npm run build
   ```

2. **Run backend with production settings:**
   ```bash
   cd src/backend
   python3 main.py --host 0.0.0.0 --port 8000
   ```

## API Endpoints

### Core Endpoints
- `POST /api/search_cases`: Search for relevant cases
- `POST /api/coach`: Generate coaching response
- `GET /health`: Health check and service status
- `GET /api/cases/{case_id}`: Get specific case details

### Request/Response Formats

**Search Request:**
```json
{
  "query": "I feel anxious and overwhelmed",
  "k": 3
}
```

**Search Response:**
```json
[
  {
    "case_id": 123,
    "context": "Client reports anxiety...",
    "response": "It's normal to feel this way...",
    "score": 0.85
  }
]
```

**Coach Request:**
```json
{
  "query": "I feel anxious and overwhelmed",
  "case_ids": [123, 456, 789]
}
```

**Coach Response:**
```json
{
  "answer_markdown": "Based on the evidence...",
  "citations": [
    {
      "case_id": 123,
      "sent_id": 2,
      "start": 45,
      "end": 89,
      "text": "It's important to practice self-care..."
    }
  ],
  "refused": false
}
```

## Configuration

### Environment Variables
- `LLM_API_KEY`: OpenAI API key (required for coaching)
- `DATA_DIR`: Data directory path (default: `data`)
- `DATASET_PATH`: Dataset file path (default: `data/combined_dataset.json`)
- `CASES_PATH`: Cases file path (default: `data/cases.json`)
- `INDEX_DIR`: Indices directory (default: `data/indices`)
- `EMBED_MODEL`: Embedding model (default: `sentence-transformers/all-MiniLM-L6-v2`)
- `SEARCH_TIMEOUT`: Search timeout in seconds (default: 10)
- `COACH_TIMEOUT`: Coach timeout in seconds (default: 20)

### Dataset Format

The system expects NDJSON format with `Context` and `Response` fields:

```json
{"Context": "I'm feeling depressed and anxious", "Response": "It's normal to feel this way..."}
{"Context": "I'm struggling with work stress", "Response": "Work stress can be overwhelming..."}
```

## Safety Features

### Crisis Detection
- Pattern-based detection of crisis language
- Automatic refusal for high-severity cases
- Resource-only responses for crisis situations

### Evidence Verification
- ROUGE-L overlap verification (threshold: 0.15)
- Minimum citation requirements (2+ citations)
- Case diversity requirements
- Policy violation detection

### Bounded LLM
- JSON-only output format
- Structured synthesis approach
- Citation requirements enforced
- Template-based response assembly

## Development

### Project Structure
```
Legacy/
├── src/
│   ├── backend/
│   │   ├── api/           # FastAPI routes and middleware
│   │   ├── models/        # Pydantic schemas
│   │   ├── services/      # Core business logic
│   │   ├── utils/         # Data loading utilities
│   │   └── main.py        # Entry point
│   └── frontend/
│       ├── src/
│       │   ├── components/ # React components
│       │   ├── hooks/      # Custom React hooks
│       │   └── config.js   # Configuration
│       └── package.json
├── data/                  # Data files and indices
└── tests/                # Test files
```

### Key Design Patterns
- **Singleton IndexManager**: Thread-safe index management
- **Service Dependency Injection**: Clean service composition
- **Async/Await**: Non-blocking I/O throughout
- **Error Boundaries**: Graceful error handling
- **Observable Metrics**: Comprehensive monitoring




## Disclaimer

This is a demonstration system only and not intended to provide medical or clinical advice. In case of crisis, please contact appropriate emergency services or crisis hotlines.

## Acknowledgements

- Built with FastAPI, React, and modern AI/ML libraries
- Design based on retrieval-augmented generation best practices
- Prioritizes safety, evidence, and transparency over generative capabilities
