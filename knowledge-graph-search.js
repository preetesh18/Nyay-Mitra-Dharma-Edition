/**
 * Token-Optimized Graph-Based Search Engine
 * Inspired by code-review-graph: 8.2x token reduction
 * 
 * Core Principle: Build a knowledge graph of your content,
 * then return only semantically relevant context
 */

class KnowledgeGraphSearchEngine {
  constructor() {
    this.graph = {
      nodes: new Map(),      // id → node metadata
      edges: new Map(),      // id → [related ids]
      embeddings: new Map(), // id → vector
      lastUpdated: Date.now()
    };
    
    this.config = {
      maxContextTokens: 2000,
      minRelevanceScore: 0.3,
      maxResults: 5,
      includeNeighbors: true,
      neighborDepth: 2
    };
  }

  /**
   * STEP 1: Build Content Graph
   * Parse content into nodes and relationships
   */
  buildGraph(contentRegistry) {
    console.log('🔨 Building knowledge graph...');
    
    contentRegistry.forEach((content, id) => {
      // Create node with metadata
      const node = {
        id,
        title: content.title,
        type: content.type, // page, section, topic
        content: content.content,
        tokens: this.estimateTokens(content.content),
        category: content.category,
        keywords: this.extractKeywords(content.content),
        relatedTopics: content.relatedTopics || [],
        lastModified: Date.now()
      };
      
      this.graph.nodes.set(id, node);
    });

    // Build relationships
    this.buildEdges();
    console.log(`✅ Graph built with ${this.graph.nodes.size} nodes`);
  }

  /**
   * STEP 2: Build Edges (Relationships)
   * Create connections between related nodes
   */
  buildEdges() {
    const nodes = Array.from(this.graph.nodes.values());
    
    nodes.forEach(nodeA => {
      const relatedIds = new Set();
      
      nodes.forEach(nodeB => {
        if (nodeA.id === nodeB.id) return;
        
        // Similarity score based on:
        const similarity = this.calculateSimilarity(nodeA, nodeB);
        
        // Add edge if similar enough
        if (similarity > 0.3) {
          relatedIds.add({
            targetId: nodeB.id,
            strength: similarity,
            reason: this.getRelationshipReason(nodeA, nodeB)
          });
        }
      });
      
      this.graph.edges.set(nodeA.id, Array.from(relatedIds));
    });
  }

  /**
   * STEP 3: Calculate Content Similarity
   * Multi-factor similarity (keywords, category, topics)
   */
  calculateSimilarity(nodeA, nodeB) {
    let score = 0;
    
    // 1. Category match (30% weight)
    if (nodeA.category === nodeB.category) {
      score += 0.3;
    }
    
    // 2. Keyword overlap (40% weight)
    const keywordOverlap = this.getKeywordOverlap(
      nodeA.keywords,
      nodeB.keywords
    );
    score += keywordOverlap * 0.4;
    
    // 3. Explicit topic links (30% weight)
    if (nodeA.relatedTopics.includes(nodeB.id) ||
        nodeB.relatedTopics.includes(nodeA.id)) {
      score += 0.3;
    }
    
    return Math.min(score, 1);
  }

  /**
   * STEP 4: Semantic Similarity
   * Extract keywords using simple TF-IDF approach
   */
  extractKeywords(content, topN = 10) {
    const words = content
      .toLowerCase()
      .match(/\b\w+\b/g) || [];
    
    // Simple TF calculation (production: use proper NLP)
    const frequency = {};
    words.forEach(word => {
      if (this.isStopword(word)) return;
      frequency[word] = (frequency[word] || 0) + 1;
    });
    
    return Object.entries(frequency)
      .sort((a, b) => b[1] - a[1])
      .slice(0, topN)
      .map(([word]) => word);
  }

  /**
   * STEP 5: Optimized Search
   * Return minimal context with maximum relevance
   */
  search(query, options = {}) {
    const config = { ...this.config, ...options };
    console.log(`🔍 Searching: "${query}"`);
    
    // Step 1: Find directly relevant nodes
    const directMatches = this.findDirectMatches(query, config);
    
    // Step 2: Expand to neighbors (blast radius)
    const expandedContext = this.expandToNeighbors(
      directMatches,
      config.neighborDepth,
      config.maxContextTokens
    );
    
    // Step 3: Rank by relevance
    const ranked = this.rankResults(expandedContext, query);
    
    // Step 4: Build minimal response
    const response = this.buildMinimalContext(
      ranked,
      query,
      config.maxContextTokens
    );
    
    response.tokenSavings = this.calculateTokenSavings(response);
    
    return response;
  }

  /**
   * Find directly matching nodes
   */
  findDirectMatches(query, config) {
    const queryKeywords = this.extractKeywords(query);
    const matches = [];
    
    this.graph.nodes.forEach(node => {
      let score = 0;
      
      // Title match (highest weight)
      if (node.title.toLowerCase().includes(query.toLowerCase())) {
        score += 5;
      }
      
      // Keyword overlap
      const overlap = this.getKeywordOverlap(queryKeywords, node.keywords);
      score += overlap * 3;
      
      // Content relevance
      if (node.content.toLowerCase().includes(query.toLowerCase())) {
        score += 1;
      }
      
      if (score > 0) {
        matches.push({
          nodeId: node.id,
          relevance: score,
          node
        });
      }
    });
    
    return matches.sort((a, b) => b.relevance - a.relevance);
  }

  /**
   * Expand to neighbors (Blast Radius Analysis)
   * Include related nodes up to token budget
   */
  expandToNeighbors(directMatches, maxDepth, maxTokens) {
    const included = new Set();
    let totalTokens = 0;
    const result = [];
    
    // BFS expansion
    const queue = directMatches.map(m => ({ 
      nodeId: m.nodeId, 
      depth: 0, 
      relevance: m.relevance 
    }));
    
    while (queue.length > 0 && totalTokens < maxTokens) {
      const { nodeId, depth, relevance } = queue.shift();
      
      if (included.has(nodeId)) continue;
      if (depth > maxDepth) continue;
      
      const node = this.graph.nodes.get(nodeId);
      if (!node) continue;
      
      // Check token budget
      if (totalTokens + node.tokens > maxTokens) continue;
      
      included.add(nodeId);
      totalTokens += node.tokens;
      result.push({
        nodeId,
        node,
        relevance: relevance * (1 - depth * 0.2), // Decay by depth
        depth
      });
      
      // Add neighbors to queue
      const edges = this.graph.edges.get(nodeId) || [];
      edges.forEach(edge => {
        if (!included.has(edge.targetId) && depth < maxDepth) {
          queue.push({
            nodeId: edge.targetId,
            depth: depth + 1,
            relevance: relevance * edge.strength
          });
        }
      });
    }
    
    return result;
  }

  /**
   * Smart ranking by relevance and proximity
   */
  rankResults(expanded, query) {
    return expanded.sort((a, b) => {
      // Primary: Relevance score
      if (Math.abs(a.relevance - b.relevance) > 0.1) {
        return b.relevance - a.relevance;
      }
      
      // Secondary: Proximity (depth)
      if (a.depth !== b.depth) {
        return a.depth - b.depth;
      }
      
      // Tertiary: Content length (prefer concise)
      return a.node.tokens - b.node.tokens;
    });
  }

  /**
   * Build minimal context response
   * Include snippet + immediate neighbors
   */
  buildMinimalContext(ranked, query, maxTokens) {
    const snippets = [];
    let totalTokens = 0;
    
    ranked.forEach(item => {
      if (totalTokens >= maxTokens) return;
      
      const snippet = {
        id: item.nodeId,
        title: item.node.title,
        excerpt: this.generateExcerpt(item.node.content, query, 200),
        type: item.node.type,
        relevance: Math.round(item.relevance * 100),
        tokenCount: item.node.tokens,
        relatedNodes: this.getRelatedSnippets(item.nodeId, 2)
      };
      
      totalTokens += item.node.tokens;
      snippets.push(snippet);
    });
    
    return {
      query,
      results: snippets,
      totalTokens,
      resultCount: snippets.length,
      timestamp: Date.now()
    };
  }

  /**
   * Generate context-aware excerpt
   */
  generateExcerpt(content, query, maxLength) {
    const lowerContent = content.toLowerCase();
    const lowerQuery = query.toLowerCase();
    
    const index = lowerContent.indexOf(lowerQuery);
    if (index === -1) {
      return content.substring(0, maxLength) + '...';
    }
    
    const start = Math.max(0, index - 50);
    const end = Math.min(content.length, index + maxLength);
    
    return '...' + content.substring(start, end) + '...';
  }

  /**
   * Get related snippets for context
   */
  getRelatedSnippets(nodeId, limit) {
    const edges = this.graph.edges.get(nodeId) || [];
    
    return edges
      .sort((a, b) => b.strength - a.strength)
      .slice(0, limit)
      .map(edge => ({
        id: edge.targetId,
        strength: Math.round(edge.strength * 100),
        title: this.graph.nodes.get(edge.targetId)?.title
      }));
  }

  /**
   * Calculate token savings
   */
  calculateTokenSavings(response) {
    const naiveTokens = Array.from(this.graph.nodes.values())
      .reduce((sum, node) => sum + node.tokens, 0);
    
    const optimizedTokens = response.totalTokens;
    const reduction = ((naiveTokens - optimizedTokens) / naiveTokens) * 100;
    
    return {
      savedTokens: naiveTokens - optimizedTokens,
      reductionPercentage: Math.round(reduction),
      ratio: (naiveTokens / optimizedTokens).toFixed(1) + 'x'
    };
  }

  /**
   * Utility: Estimate tokens (simple approximation)
   * Production: Use proper tokenizer
   */
  estimateTokens(text) {
    return Math.ceil(text.split(/\s+/).length / 4);
  }

  /**
   * Utility: Stop words
   */
  isStopword(word) {
    const stopwords = new Set([
      'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at',
      'to', 'for', 'of', 'with', 'by', 'from', 'is', 'are',
      'was', 'were', 'be', 'that', 'this', 'it', 'as', 'if'
    ]);
    return stopwords.has(word);
  }

  /**
   * Calculate keyword overlap
   */
  getKeywordOverlap(keywords1, keywords2) {
    const set1 = new Set(keywords1);
    const set2 = new Set(keywords2);
    const overlap = [...set1].filter(k => set2.has(k)).length;
    return overlap / Math.max(set1.size, set2.size);
  }

  /**
   * Get relationship reason
   */
  getRelationshipReason(nodeA, nodeB) {
    if (nodeA.category === nodeB.category) return 'same-category';
    if (nodeA.relatedTopics.includes(nodeB.id)) return 'explicit-link';
    return 'semantic-similarity';
  }

  /**
   * Update graph incrementally
   */
  updateNode(nodeId, content) {
    console.log(`📝 Updating node: ${nodeId}`);
    
    const node = this.graph.nodes.get(nodeId);
    if (!node) {
      console.warn(`⚠️ Node not found: ${nodeId}`);
      return;
    }
    
    // Update content metadata
    node.content = content.content;
    node.tokens = this.estimateTokens(content.content);
    node.keywords = this.extractKeywords(content.content);
    node.lastModified = Date.now();
    
    // Rebuild edges for this node
    this.rebuildNodeEdges(nodeId);
    
    console.log(`✅ Updated ${nodeId}`);
  }

  /**
   * Rebuild edges for a specific node
   */
  rebuildNodeEdges(nodeId) {
    const nodeA = this.graph.nodes.get(nodeId);
    const relatedIds = [];
    
    this.graph.nodes.forEach((nodeB, id) => {
      if (id === nodeId) return;
      
      const similarity = this.calculateSimilarity(nodeA, nodeB);
      if (similarity > 0.3) {
        relatedIds.push({
          targetId: id,
          strength: similarity,
          reason: this.getRelationshipReason(nodeA, nodeB)
        });
      }
    });
    
    this.graph.edges.set(nodeId, relatedIds);
  }

  /**
   * Export statistics
   */
  getStats() {
    const totalTokens = Array.from(this.graph.nodes.values())
      .reduce((sum, node) => sum + node.tokens, 0);
    
    const totalEdges = Array.from(this.graph.edges.values())
      .reduce((sum, edges) => sum + edges.length, 0);
    
    return {
      nodeCount: this.graph.nodes.size,
      edgeCount: totalEdges / 2, // Each edge counted twice
      totalTokens,
      averageTokensPerNode: Math.round(totalTokens / this.graph.nodes.size),
      graphDensity: (totalEdges / 2 / (this.graph.nodes.size * (this.graph.nodes.size - 1) / 2)).toFixed(3),
      lastUpdated: new Date(this.graph.lastUpdated).toISOString()
    };
  }
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
  module.exports = KnowledgeGraphSearchEngine;
}
