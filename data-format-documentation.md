# Nyay Mitra - Admin & Logging System Documentation

## Admin Account Credentials

Admin credentials are stored securely in the system and managed internally.

**Note:** Credentials are not displayed in documentation for security purposes.  
Contact administrator for login details.

---

## Data Storage System

All data is stored in **JSON format only** in localStorage and JSON files. This system provides comprehensive tracking and analytics.

---

## 1. Admin Account Configuration (`admin-config.json`)

Stores admin account details and permissions.

```json
{
  "admin": {
    "username": "admin",
    "password": "YWRtaW43OTc4",  // base64 encoded
    "role": "administrator",
    "createdAt": "2026-03-30T00:00:00Z",
    "lastLogin": null,
    "loginCount": 0,
    "permissions": [
      "view_login_logs",
      "view_query_cache",
      "view_training_data",
      "manage_users",
      "export_data",
      "clear_cache"
    ]
  }
}
```

**Permissions:**
- `view_login_logs`: Access to all user login/logout records
- `view_query_cache`: Access to query-solution cache
- `view_training_data`: Access to model training datasets
- `manage_users`: Create/delete users
- `export_data`: Export all data to JSON
- `clear_cache`: Clear query cache

---

## 2. Login Logs (`login-logs.json`)

Tracks who logs in, when, session duration, and login status.

```json
{
  "logs": [
    {
      "id": 1,
      "username": "demo",
      "loginTime": "2026-03-30T10:00:00Z",
      "logoutTime": "2026-03-30T11:30:00Z",
      "status": "success",
      "ipAddress": "local",
      "userAgent": "Mozilla/5.0...",
      "sessionDuration": 5400  // in seconds
    }
  ],
  "summary": {
    "totalLogins": 1,
    "uniqueUsers": 1,
    "failedAttempts": 0,
    "lastUpdated": "2026-03-30T10:00:00Z"
  }
}
```

**Fields:**
- `id`: Unique login log entry ID
- `username`: User who logged in
- `loginTime`: ISO timestamp of login
- `logoutTime`: ISO timestamp of logout (null if still logged in)
- `status`: "success" or "failed"
- `sessionDuration`: Total session duration in seconds
- `summary`: Aggregate statistics

---

## 3. Query Cache (`query-cache.json`)

Stores query-solution pairs for reuse. If same query asked by different users, cached solution is returned.

```json
{
  "cache": [
    {
      "id": 1,
      "query": "what are fundamental rights",
      "queryHash": "hash_1",
      "solution": "Fundamental Rights are rights guaranteed by constitution...",
      "feature": "legal-knowledge",
      "category": "constitutional-law",
      "timestamps": {
        "created": "2026-03-30T10:00:00Z",
        "lastUsed": "2026-03-30T10:05:00Z"
      },
      "usageCount": 2,
      "usersAccessed": ["demo", "admin"],
      "relevanceScore": 0.95,
      "tags": ["constitution", "rights", "law"]
    }
  ],
  "metadata": {
    "totalCacheItems": 1,
    "cacheSize": "1 KB",
    "hitRate": 0.95,
    "lastUpdated": "2026-03-30T10:05:00Z",
    "maxCacheSize": "10 MB",
    "expirationTime": "30 days"
  }
}
```

**Cache Entry Fields:**
- `id`: Unique cache entry ID
- `query`: The original query text
- `queryHash`: Hash of query for quick lookup
- `solution`: Generated solution/answer
- `feature`: Which feature generated it (e.g., "legal-knowledge")
- `category`: Query category (e.g., "constitutional-law")
- `timestamps`: Created and last used timestamps
- `usageCount`: How many times this cache was used
- `usersAccessed`: List of users who used this cache
- `relevanceScore`: Quality/relevance of solution (0-1)
- `tags`: Auto-extracted keywords from query

---

## 4. Training Data (`training-data.json`)

Comprehensive dataset for model training. Records every query, response time, user satisfaction, and context.

```json
{
  "trainingData": [
    {
      "id": 1,
      "timestamp": "2026-03-30T10:00:00Z",
      "user": "demo",
      "queryText": "what are fundamental rights",
      "queryType": "definition",
      "category": "constitutional-law",
      "feature": "legal-knowledge",
      "solutionGenerated": "Fundamental Rights are rights guaranteed...",
      "solutionType": "definition",
      "responseTime": 245,  // milliseconds
      "userSatisfaction": 5,  // 1-5 rating
      "userFeedback": null,
      "followUpQueries": 0,
      "sessionId": "session_001",
      "context": {
        "previousQuery": null,
        "userRole": "regular",
        "deviceType": "desktop"
      }
    }
  ],
  "statistics": {
    "totalQueries": 1,
    "averageResponseTime": 245,
    "averageSatisfactionScore": 5,
    "uniqueCategories": 1,
    "uniqueQueryTypes": 1,
    "topFeatures": ["legal-knowledge"],
    "topCategories": ["constitutional-law"],
    "topQueryTypes": ["definition"],
    "userEngagementRate": 1.0,
    "cacheHitRate": 0.0,
    "errorRate": 0.0,
    "lastUpdated": "2026-03-30T10:00:00Z"
  },
  "queryTypeDistribution": {
    "definition": 1,
    "procedure": 0,
    "comparison": 0,
    "analysis": 0
  },
  "categoryDistribution": {
    "constitutional-law": 1,
    "civil-law": 0,
    "criminal-law": 0
  }
}
```

**Training Data Fields:**
- `queryText`: The user's question/query
- `queryType`: Type of query (definition, procedure, comparison, analysis, etc.)
- `category`: Legal category (constitutional-law, civil-law, criminal-law, etc.)
- `responseTime`: Response time in milliseconds
- `userSatisfaction`: User rating 1-5
- `userFeedback`: Optional detailed feedback
- `followUpQueries`: Number of follow-up questions
- `context`: Session context including device type and user role

---

## JavaScript API Functions

### 1. Login Logging

```javascript
logUserLogin(username)        // Called automatically on login
logUserLogout(username)       // Called automatically on logout
```

### 2. Query Caching

```javascript
// Add query-solution to cache
cacheQuerySolution(query, solution, feature, category)
```

Example:
```javascript
cacheQuerySolution(
  "What are fundamental rights?",
  "Fundamental Rights are basic human rights...",
  "legal-knowledge",
  "constitutional-law"
)
```

### 3. Training Data Logging

```javascript
// Log query for model training
logQueryToTraining(query, solution, queryType, category, feature, responseTime, userSatisfaction)
```

Example:
```javascript
logQueryToTraining(
  "What are fundamental rights?",
  "Fundamental Rights are basic human rights...",
  "definition",
  "constitutional-law",
  "legal-knowledge",
  245,  // response time in ms
  5     // satisfaction 1-5
)
```

### 4. Admin Functions

```javascript
// Check if current user is admin
isAdmin()

// Retrieve data (returns null if not admin)
getLoginLogs()              // Get all login logs
getQueryCache()             // Get query cache
getTrainingData()           // Get training data

// Admin-only operations
clearQueryCache()           // Clear all cached queries
exportAllData()             // Export all data to JSON file
```

Example Admin Usage:
```javascript
if(isAdmin()){
  const logs = getLoginLogs();
  console.log('Total logins:', logs.summary.totalLogins);
  
  const cache = getQueryCache();
  console.log('Cached queries:', cache.metadata.totalCacheItems);
  
  const training = getTrainingData();
  console.log('Training records:', training.statistics.totalQueries);
  
  // Export everything to JSON
  exportAllData();  // Downloads JSON file
}
```

---

## Storage Locations

### Browser localStorage Paths:
```
'nyay-users'          → All registered users + admin
'nyay-login-logs'     → Login/logout tracking
'nyay-query-cache'    → Query-solution cache
'nyay-training-data'  → Training dataset
'nyay-current-user'   → Current logged-in user
'nyay-session-time'   → Session start time
'nyay-session-id'     → Current session ID
'nyay-last-query'     → Last query made by user
```

### File-based Paths (for backup/reference):
```
/admin-config.json          → Admin account config
/login-logs.json            → Login logs backup
/query-cache.json           → Query cache backup
/training-data.json         → Training data backup
```

---

## Query Types

```
- definition          : Explaining what something is
- procedure           : How to do something
- comparison          : Comparing two or more things
- analysis            : Detailed analysis of a topic
- application         : Real-world application examples
- historical          : Historical context/background
- legal-precedent     : Case law and precedents
- calculation         : Mathematical calculations
- other               : Other types
```

---

## Categories

```
- constitutional-law  : Constitution, rights, governance
- civil-law           : Property, contract, family law
- criminal-law        : Crimes, penalties, procedures
- corporate-law       : Business, corporate matters
- labor-law           : Employment, worker rights
- environmental-law   : Environmental regulations
- family-law          : Marriage, succession, adoption
- intellectual-property : Patents, trademarks, copyrights
- administrative-law  : Government procedures
- other               : Other legal categories
```

---

## Features

```
- legal-knowledge     : General legal knowledge
- case-search         : Case law search
- document-generator  : Document generation
- consultation        : Live consultation
- precedent-finder    : Find relevant precedents
- other               : Other features
```

---

## Usage Examples

### Example 1: Log a Query with Cache

```javascript
// When user asks a question
const query = "What is the right to freedom of speech?";
const solution = "The right to freedom of speech is...";
const feature = "legal-knowledge";
const category = "constitutional-law";

// Log for training
const startTime = Date.now();
logQueryToTraining(
  query,
  solution,
  "definition",
  category,
  feature,
  Date.now() - startTime,
  4  // user satisfaction
);

// Cache for reuse
cacheQuerySolution(query, solution, feature, category);
```

### Example 2: Admin Views Analytics

```javascript
if(isAdmin()){
  // Get query statistics
  const trainingData = getTrainingData();
  console.log('Total queries:', trainingData.statistics.totalQueries);
  console.log('Avg response time:', trainingData.statistics.averageResponseTime, 'ms');
  console.log('Avg satisfaction:', trainingData.statistics.averageSatisfactionScore);
  
  // Get cache statistics
  const cache = getQueryCache();
  console.log('Cached queries:', cache.metadata.totalCacheItems);
  console.log('Cache hit rate:', cache.metadata.hitRate);
  
  // Get usage statistics
  const logs = getLoginLogs();
  console.log('Total user sessions:', logs.summary.totalLogins);
  console.log('Unique users:', logs.summary.uniqueUsers);
}
```

### Example 3: Export Data for Analysis

```javascript
// Admin exports all data
if(isAdmin()){
  exportAllData();  // Downloads file: nyay-mitra-data-export-[timestamp].json
}
```

---

## Data Flow

```
User Login
   ↓
logUserLogin() → Updates login-logs.json
   ↓
User Asks Query
   ↓
Solution Generated
   ↓
logQueryToTraining() → Updates training-data.json
   ↓
cacheQuerySolution() → Updates query-cache.json
   ↓
User Logs Out
   ↓
logUserLogout() → Updates login-logs.json with duration
```

---

## Security Notes

- Passwords are base64 encoded (demo only - use proper hashing in production)
- Admin functions have permission checks
- All logging is automatic on login/logout
- Data can be exported only by admin

---

## File Format

All data is stored in **JSON format only** as requested:
- `admin-config.json` - Admin credentials and config
- `login-logs.json` - User login/logout records
- `query-cache.json` - Query-solution cache
- `training-data.json` - ML training dataset

---

**Last Updated:** March 30, 2026
