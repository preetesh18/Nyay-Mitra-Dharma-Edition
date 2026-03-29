# Integration Guide - Using Logging in Features

## Overview

This guide shows how to integrate the logging and caching system into your feature pages (legal-knowledge, case-search, etc.).

---

## Pattern 1: Log Query & Cache Solution

When a user asks a query and gets a solution:

```javascript
// 1. Measure response time
const responseStart = Date.now();

// 2. Generate/retrieve solution
const query = User's question here;
const solution = Generated solution here;
const responseTime = Date.now() - responseStart;

// 3. Log to training data (for ML model)
logQueryToTraining(
  query,
  solution,
  "definition",  // or: procedure, comparison, analysis, etc.
  "constitutional-law",  // category
  "legal-knowledge",  // feature name
  responseTime,
  5  // user satisfaction (ask them or default to 5)
);

// 4. Cache solution for reuse
cacheQuerySolution(
  query,
  solution,
  "legal-knowledge",
  "constitutional-law"
);
```

---

## Pattern 2: Display Admin Dashboard

For admin features page, show analytics:

```javascript
// Check if admin
if(isAdmin()){
  
  // Get all data
  const logs = getLoginLogs();
  const cache = getQueryCache();
  const training = getTrainingData();
  
  // Display statistics
  console.log('=== NYAY MITRA ANALYTICS ===');
  console.log('Total Logins:', logs.summary.totalLogins);
  console.log('Unique Users:', logs.summary.uniqueUsers);
  console.log('Cached Queries:', cache.metadata.totalCacheItems);
  console.log('Training Records:', training.statistics.totalQueries);
  console.log('Avg Response Time:', training.statistics.averageResponseTime, 'ms');
  console.log('Avg Satisfaction:', training.statistics.averageSatisfactionScore);
  
  // Display query type distribution
  console.log('\nQuery Types:', training.queryTypeDistribution);
  console.log('Categories:', training.categoryDistribution);
  console.log('Top Users:', logs.logs.map(l => l.username));
}
```

---

## Pattern 3: Search for Cached Solution

Before generating new solution, check cache:

```javascript
// User's query
const userQuery = document.getElementById('query-input').value;

// Search cache
const cache = JSON.parse(localStorage.getItem('nyay-query-cache') || '{"cache":[]}');
const cachedResult = cache.cache.find(c => 
  c.query.toLowerCase() === userQuery.toLowerCase()
);

if(cachedResult){
  // Use cached solution (faster!)
  displaySolution(cachedResult.solution);
  
  // Update cache usage
  cachedResult.usageCount++;
  cachedResult.timestamps.lastUsed = new Date().toISOString();
  
  // Add current user if new
  if(!cachedResult.usersAccessed.includes(getCurrentUser())){
    cachedResult.usersAccessed.push(getCurrentUser());
  }
  
  // Save updated cache
  localStorage.setItem('nyay-query-cache', JSON.stringify(cache));
  
  console.log('✓ Cached solution used (Response time: instant)');
} else {
  // Generate new solution and cache it
  const solution = generateNewSolution(userQuery);
  cacheQuerySolution(userQuery, solution, "legal-knowledge", "constitutional-law");
  displaySolution(solution);
}
```

---

## Pattern 4: Collect User Satisfaction

After displaying solution:

```javascript
// Ask for rating
const rating = prompt('How satisfied? (1-5)', '5');

// Re-log with actual satisfaction
logQueryToTraining(
  userQuery,
  solution,
  "definition",
  "constitutional-law",
  "legal-knowledge",
  responseTime,
  parseInt(rating) || 5
);
```

---

## Pattern 5: Admin Export Report

Admin button to download analytics:

```html
<button onclick="downloadAnalyticsReport()">📊 Download Report</button>

<script>
function downloadAnalyticsReport(){
  if(!isAdmin()){
    alert('Admin access required');
    return;
  }
  
  // This function is already in auth.js
  exportAllData();
  alert('✓ Report downloaded!');
}
</script>
```

---

## Pattern 6: Display User Analytics

On user dashboard:

```javascript
// Log who is looking at dashboard
const trainingData = getTrainingData();
const userQueries = trainingData.trainingData.filter(t => t.user === getCurrentUser());

console.log(`You've asked ${userQueries.length} questions`);
console.log(`Avg satisfaction: ${
  (userQueries.reduce((sum, q) => sum + q.userSatisfaction, 0) / userQueries.length).toFixed(2)
}`);

// Show most popular query categories for this user
const categories = {};
userQueries.forEach(q => {
  categories[q.category] = (categories[q.category] || 0) + 1;
});
console.log('Your queries by category:', categories);
```

---

## Pattern 7: Admin Moderator Tool

Review and manage cached content:

```javascript
function moderatorPanel(){
  if(!isAdmin()){
    console.warn('Admin access required');
    return;
  }
  
  const cache = getQueryCache();
  
  console.log('=== CACHE MODERATION ===');
  
  cache.cache.forEach(entry => {
    console.log(`
      ID: ${entry.id}
      Query: ${entry.query}
      Usage: ${entry.usageCount}x
      Rating: ${entry.relevanceScore}
      Users: ${entry.usersAccessed.join(', ')}
    `);
  });
  
  // Admin can remove low-quality cache
  // const lowQuality = cache.cache.filter(c => c.relevanceScore < 0.7);
  // console.log('Low quality entries:', lowQuality);
}

moderatorPanel();
```

---

## Pattern 8: Trending Queries

Show most common queries:

```javascript
function getTrendingQueries(limit = 10){
  const training = getTrainingData();
  
  // Count query occurrences
  const queryCount = {};
  training.trainingData.forEach(t => {
    queryCount[t.queryText] = (queryCount[t.queryText] || 0) + 1;
  });
  
  // Sort and get top
  const trending = Object.entries(queryCount)
    .sort((a, b) => b[1] - a[1])
    .slice(0, limit)
    .map(([query, count]) => ({ query, count }));
  
  return trending;
}

// Usage
getTrendingQueries().forEach(item => {
  console.log(`${item.query}: ${item.count} times`);
});
```

---

## Pattern 9: Quality Score System

Track and improve solution quality:

```javascript
function calculateQualityMetrics(){
  const training = getTrainingData();
  
  const metrics = {
    averageSatisfaction: training.statistics.averageSatisfactionScore,
    totalQueries: training.statistics.totalQueries,
    cacheHitRate: training.statistics.cacheHitRate,
    avgResponseTime: training.statistics.averageResponseTime,
    
    // Calculate per-category metrics
    byCategory: {}
  };
  
  training.trainingData.forEach(t => {
    if(!metrics.byCategory[t.category]){
      metrics.byCategory[t.category] = {
        count: 0,
        totalSatisfaction: 0,
        avgTime: 0
      };
    }
    metrics.byCategory[t.category].count++;
    metrics.byCategory[t.category].totalSatisfaction += t.userSatisfaction;
    metrics.byCategory[t.category].avgTime += t.responseTime;
  });
  
  // Calculate averages
  Object.keys(metrics.byCategory).forEach(cat => {
    const stat = metrics.byCategory[cat];
    stat.avgSatisfaction = (stat.totalSatisfaction / stat.count).toFixed(2);
    stat.avgTime = Math.round(stat.avgTime / stat.count);
  });
  
  return metrics;
}

// Usage
const metrics = calculateQualityMetrics();
console.log('Quality Metrics:', metrics);
```

---

## Pattern 10: User Engagement Report

Generate engagement analytics:

```javascript
function generateEngagementReport(){
  const logs = getLoginLogs();
  
  const report = {
    totalSessions: logs.logs.length,
    totalUniqueUsers: logs.summary.uniqueUsers,
    totalSessionTime: 0,
    averageSessionTime: 0,
    sessionsByUser: {}
  };
  
  logs.logs.forEach(log => {
    if(log.sessionDuration){
      report.totalSessionTime += log.sessionDuration;
      
      if(!report.sessionsByUser[log.username]){
        report.sessionsByUser[log.username] = {
          totalSessions: 0,
          totalTime: 0,
          lastLogin: null
        };
      }
      report.sessionsByUser[log.username].totalSessions++;
      report.sessionsByUser[log.username].totalTime += log.sessionDuration;
      report.sessionsByUser[log.username].lastLogin = log.logoutTime;
    }
  });
  
  report.averageSessionTime = Math.round(report.totalSessionTime / logs.logs.length);
  
  return report;
}

// Usage
const report = generateEngagementReport();
console.log('Engagement Report:', report);
```

---

## Full Example: Legal Knowledge Feature

```javascript
// When user searches for legal knowledge

async function handleLegalQuery(){
  const userQuery = document.getElementById('legal-query').value.trim();
  
  if(!userQuery) return;
  
  try {
    // 1. START TIMER
    const startTime = Date.now();
    
    // 2. CHECK CACHE FIRST
    const cache = JSON.parse(localStorage.getItem('nyay-query-cache') || '{"cache":[]}');
    let cached = cache.cache.find(c => c.query.toLowerCase() === userQuery.toLowerCase());
    
    let solution, responseTime, fromCache = false;
    
    if(cached){
      // USE CACHE
      solution = cached.solution;
      responseTime = 50;  // Simulated cache fetch time
      fromCache = true;
      
      // Update cache stats
      cached.usageCount++;
      cached.timestamps.lastUsed = new Date().toISOString();
      if(!cached.usersAccessed.includes(getCurrentUser())){
        cached.usersAccessed.push(getCurrentUser());
      }
      localStorage.setItem('nyay-query-cache', JSON.stringify(cache));
    } else {
      // GENERATE NEW SOLUTION
      solution = await generateSolution(userQuery);  // Your function
      responseTime = Date.now() - startTime;
      
      // CACHE IT
      cacheQuerySolution(
        userQuery,
        solution,
        "legal-knowledge",
        "constitutional-law"  // or detected category
      );
    }
    
    // 3. DISPLAY SOLUTION
    displaySolution(solution, fromCache ? '(cached)' : '');
    
    // 4. LOG TO TRAINING DATA
    logQueryToTraining(
      userQuery,
      solution,
      "definition",  // or detected type
      "constitutional-law",  // or detected category
      "legal-knowledge",
      responseTime,
      5  // default satisfaction
    );
    
    console.log(`✓ Query solved in ${responseTime}ms ${fromCache ? '(from cache)' : '(new)'}`);
    
  } catch(error){
    console.error('Error:', error);
    displayError('Could not process query');
  }
}
```

---

## Configuration for Categories & Types

Add to your pages for consistency:

```javascript
const LEGAL_CATEGORIES = {
  'constitutional-law': 'Constitutional & Fundamental Rights',
  'civil-law': 'Civil Law & Property',
  'criminal-law': 'Criminal Law & Procedure',
  'corporate-law': 'Corporate & Business Law',
  'labor-law': 'Labor & Employment Law',
  'family-law': 'Family Law',
  'environmental-law': 'Environmental Law',
  'ip-law': 'Intellectual Property',
  'admin-law': 'Administrative Law',
  'other': 'Other'
};

const QUERY_TYPES = {
  'definition': 'Definition/Explanation',
  'procedure': 'Procedure/How-to',
  'comparison': 'Comparison',
  'analysis': 'Detailed Analysis',
  'application': 'Real-world Application',
  'historical': 'Historical Context',
  'precedent': 'Legal Precedent',
  'calculation': 'Calculation/Estimation',
  'other': 'Other'
};
```

---

**Always include these in your feature implementations to maintain data consistency!**
