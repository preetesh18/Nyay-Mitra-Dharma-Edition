# Testing Guide - Admin & Logging System

## Test 1: Admin Login

1. Visit login page
2. Enter credentials:
   - Username: `admin`
   - Password: `admin123`
3. Verify login successful
4. Should see admin access in browser console

---

## Test 2: Check Login Logs Created

Open Browser Dev Tools (F12) → Console:

```javascript
// Check if login was logged
const logs = JSON.parse(localStorage.getItem('nyay-login-logs'));
console.log(logs);
// Should show: { logs: [{...login entry...}], summary: {...} }
```

Expected output:
```json
{
  "logs": [
    {
      "id": 1,
      "username": "admin",
      "loginTime": "2026-03-30T...",
      "status": "success",
      ...
    }
  ],
  "summary": {
    "totalLogins": 1,
    "uniqueUsers": 1
  }
}
```

---

## Test 3: Verify Admin Status

In Browser Console:

```javascript
isAdmin()  // Should return: true
```

---

## Test 4: Access Admin Data

In Browser Console:

```javascript
// View login logs
const logs = getLoginLogs();
console.log('Total logins:', logs.summary.totalLogins);

// View query cache
const cache = getQueryCache();
console.log('Cached queries:', cache.metadata.totalCacheItems);

// View training data
const training = getTrainingData();
console.log('Training records:', training.statistics.totalQueries);
```

---

## Test 5: Test Query Caching

In Browser Console:

```javascript
// Simulate a query solution caching
cacheQuerySolution(
  "What is habeas corpus?",
  "Habeas corpus is a legal action to challenge unlawful detention...",
  "legal-knowledge",
  "constitutional-law"
);

// Verify it was cached
const cache = getQueryCache();
console.log(cache.cache.length);  // Should be > 0
console.log(cache.cache[cache.cache.length - 1]);  // Show latest entry
```

Expected: Cache entry with query, solution, timestamps, etc.

---

## Test 6: Test Training Data Logging

In Browser Console:

```javascript
// Log a query for training
logQueryToTraining(
  "How does court procedure work?",
  "Court procedure involves filing, hearing, judgment stages...",
  "procedure",
  "criminal-law",
  "legal-knowledge",
  156,  // response time in ms
  5     // satisfaction 1-5
);

// Verify data was logged
const training = getTrainingData();
console.log('Total queries:', training.trainingData.length);
console.log(training.trainingData[training.trainingData.length - 1]);
```

---

## Test 7: Test Admin Export

In Browser Console:

```javascript
// Export all data to JSON file
exportAllData()
// Should trigger download of: nyay-mitra-data-export-[timestamp].json
```

---

## Test 8: Test Logout Logging

1. After logged in as admin
2. Click Logout button
3. In Browser Console:

```javascript
// Login again and check logout was logged
const logs = JSON.parse(localStorage.getItem('nyay-login-logs'));
const lastLog = logs.logs[logs.logs.length - 1];
console.log(lastLog.logoutTime);  // Should show time
console.log(lastLog.sessionDuration);  // Should show seconds
```

---

## Test 9: Test Cache Reuse

In Browser Console:

```javascript
// First query
cacheQuerySolution(
  "What is tort law?",
  "Tort law deals with civil wrongs...",
  "legal-knowledge",
  "civil-law"
);

// Simulate same query again
cacheQuerySolution(
  "What is tort law?",
  "Tort law deals with civil wrongs...",
  "legal-knowledge",
  "civil-law"
);

// Check cache
const cache = getQueryCache();
const tortEntry = cache.cache.find(c => c.query.includes("tort"));
console.log('Usage count:', tortEntry.usageCount);  // Should be 2
console.log('Users accessed:', tortEntry.usersAccessed);  // Should list users
```

---

## Test 10: Test Role-Based Access

In Browser Console:

```javascript
// Login as demo user first
localStorage.setItem('nyay-current-user', 'demo');

// Try to access admin function
isAdmin()  // Should return: false
getLoginLogs()  // Should return: null with warning

// Then login as admin
localStorage.setItem('nyay-current-user', 'admin');
isAdmin()  // Should return: true
getLoginLogs()  // Should return data
```

---

## Test 11: Verify JSON File Formats

Check these files exist and have correct JSON format:

1. **admin-config.json**
   ```
   Should contain: { "admin": { username, password, role, permissions } }
   ```

2. **login-logs.json**
   ```
   Should contain: { "logs": [...], "summary": {...} }
   ```

3. **query-cache.json**
   ```
   Should contain: { "cache": [...], "metadata": {...} }
   ```

4. **training-data.json**
   ```
   Should contain: { "trainingData": [...], "statistics": {...}, distributions }
   ```

---

## Test 12: Verify Device Type Detection

In Browser Console:

```javascript
console.log(getDeviceType());
// Should return: 'desktop', 'mobile', or 'tablet'
```

---

## Test 13: Verify Tag Extraction

In Browser Console:

```javascript
console.log(extractTags("What are my fundamental rights under constitution?"));
// Should return: ['rights', 'constitution']

console.log(extractTags("Tell me about contract law"));
// Should return: ['contract']
```

---

## Test 14: Clear Cache (Admin Only)

In Browser Console:

```javascript
// Must be logged in as admin
if(isAdmin()){
  clearQueryCache();
  const cache = getQueryCache();
  console.log(cache.cache.length);  // Should be 0
}
```

---

## Test 15: Verify All Users Have Hashed Passwords

In Browser Console:

```javascript
const users = JSON.parse(localStorage.getItem('nyay-users'));
console.log(users);

// Should show:
// admin: password is "YWRtaW4xMjM=" (base64 of admin123)
// demo: password is "cGFzc3dvcmQxMjM=" (base64 of password123)
```

---

## Checklist

- [ ] Admin account created and logs in
- [ ] Login logs created and updated automatically
- [ ] Query cache created and working
- [ ] Training data created and populated
- [ ] Admin functions accessible and restricted
- [ ] All data in JSON format
- [ ] Export feature downloads JSON file
- [ ] Logout records session duration
- [ ] Cache tracks reuse and users
- [ ] Device type detection works
- [ ] Tag extraction works
- [ ] Role-based access control works

---

## Troubleshooting

**Problem:** Login logs not created
- Check browser console for errors
- Verify localStorage is enabled
- Try clearing browser cache

**Problem:** Admin functions returns null
- Verify logged in as admin: `isAdmin()` should be `true`
- Check localStorage for 'nyay-current-user' key

**Problem:** Export not working
- Check browser allows downloads
- Verify admin is logged in
- Check console for errors

**Problem:** Cache not persisting
- Check browser doesn't clear localStorage on close
- Verify cache data in localStorage

---

**Test Date:** March 30, 2026
