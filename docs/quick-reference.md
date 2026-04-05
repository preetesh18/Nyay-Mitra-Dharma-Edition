# Quick Reference - Admin & Logging System

## Login Credentials

**Admin credentials:** Stored in secure system  
**Demo account:** Available for testing (see admin for password)

⚠️ **Important:** Never share credentials in documentation or public files.

---

## JSON Data Files

All data stored in **JSON format only**:

| File | Purpose |
|------|---------|
| `admin-config.json` | Admin account settings |
| `login-logs.json` | User login/logout records |
| `query-cache.json` | Cached queries & solutions |
| `training-data.json` | ML training dataset |

---

## Admin Functions (JavaScript Console)

```javascript
// Check if admin
isAdmin()

// View logs
getLoginLogs()        // → JSON object with login records
getQueryCache()       // → JSON object with cached queries
getTrainingData()     // → JSON object with training data

// Admin actions
clearQueryCache()     // Clears all cached queries
exportAllData()       // Downloads all data to JSON file
```

---

## Automatic Logging

Happens automatically:

```
✓ Login  → Recorded in login-logs.json
✓ Query  → Recorded in training-data.json
✓ Cache  → Recorded in query-cache.json
✓ Logout → Session duration calculated
```

---

## Data Flow

```
User logs in
    ↓ [Auto-logged to login-logs.json]
User asks query
    ↓ [Auto-logged to training-data.json]
Solution cached
    ↓ [Auto-stored in query-cache.json]
User logs out
    ↓ [Auto-recorded logout time]
```

---

## Browser localStorage Keys

```
nyay-users           → All users (demo + admin)
nyay-login-logs      → Login tracking
nyay-query-cache     → Query cache
nyay-training-data   → Training data
nyay-current-user    → Logged-in user name
nyay-session-time    → Session start time
nyay-session-id      → Session ID
nyay-last-query      → Last query made
```

---

## Export to JSON

Admin can download all data:

```javascript
exportAllData()  // File: nyay-mitra-data-export-[timestamp].json
```

---

## Admin Permissions

- ✓ View all login logs
- ✓ View query cache
- ✓ View training data
- ✓ Clear cache
- ✓ Export all data
- ✓ Manage users

---

## Tips

1. Each time a query is asked, it's automatically:
   - Logged to training data (for ML)
   - Cached (for reuse by other users)
   
2. Cache is reused if same query asked again:
   - Faster response
   - Tracks usage count per query
   - Tracks which users accessed each cached solution

3. Login logs track:
   - Who logged in
   - When they logged in/out
   - Total session duration
   - User agent info

4. Training data includes:
   - Query text and type
   - Category (constitution, civil, criminal, etc.)
   - Response time
   - User satisfaction rating
   - Device type and user role
   - Context information

---

**All data stored in JSON format only** ✓
