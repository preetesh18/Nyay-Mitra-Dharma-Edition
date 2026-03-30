# Token Optimization Analysis & Implementation Guide

## 1. Code Review Graph Approach (8.2x Token Reduction)

### Core Strategy: Graph-Based Context Selection
Instead of naively including all code, code-review-graph builds a **knowledge graph** and returns only semantically relevant context.

### Architecture Pipeline:
```
Repository Code
    ↓
Tree-Sitter Parser (AST)
    ↓
Graph Builder (Functions, Classes, Imports, Dependencies)
    ↓
SQLite Graph Database
    ↓
Blast Radius Analysis (What's affected?)
    ↓
Minimal Context Set → Claude (8.2x fewer tokens)
```

## 2. Key Token-Saving Techniques

### A. **Dependency Tracing (Blast Radius)**
- Instead of: Including entire files
- Do: Follow only the call chain affected by changes
- Result: 49x reduction on daily coding tasks

### B. **Incremental Updates**
- Parse only changed files
- Update only affected graph edges
- Cache results in SQLite
- Updates complete in <2 seconds

### C. **Graph Query Optimization**
1. **Transitive Dependencies**: What imports this? What does this import?
2. **Type Information**: Class hierarchies, interface implementations
3. **Test Coverage Mapping**: Link tests to functions they cover
4. **Community Detection**: Cluster related code (Leiden algorithm)

### D. **Hybrid Search Strategy**
```
Query → Semantic Similarity (Vector Embeddings)
      → Keyword Match (FTS5)
      → Graph Relations (Neighbors)
      → Rank by Relevance + Proximity
```

## 3. Implementation for Nyay Mitra Search Engine

### Supported Techniques:
1. ✅ AST-based parsing (use Tree-sitter for HTML/JavaScript)
2. ✅ Graph relationship mapping
3. ✅ SQLite storage (local, no cloud)
4. ✅ Incremental updates on file changes
5. ✅ Semantic search with embeddings
6. ✅ Multi-language support (18 languages)

### Optimization Strategies for Your Project:
1. **Content Graph**: Parse documentation structure
2. **Author/Topic Relations**: Link related content
3. **Cross-Reference Map**: Legal concepts linking
4. **Search Ranking**: By relevance + graph locality
5. **Minimal Context**: Return only snippet + related sections

## 4. Expected Token Reduction
- **Before**: Full content from all matching pages
- **After**: Snippet + immediate neighbors in graph
- **Target**: 5-8x reduction compared to naive search

## 5. Files to Modify/Create
1. `search-graph.js` - Graph builder and query engine
2. `graph-db.json` - SQLite equivalent (JSON for web)
3. `semantic-search.js` - Vector embedding search
4. `search-optimization-config.json` - Configuration

---

## Next Steps:
Building the full implementation in your workspace...
