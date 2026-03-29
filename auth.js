/* ── AUTHENTICATION SYSTEM ── */

// VERSION - Increment this when updating auth system to force localStorage reset
const AUTH_VERSION = '2.0';

// Initialize users in localStorage if not exists
function initializeAuth(){
  // Check if version changed (Vercel deployment) - force reset old data
  const storedVersion = localStorage.getItem('nyay-auth-version');
  if(storedVersion !== AUTH_VERSION){
    console.log('🔄 Auth version changed. Clearing old data...');
    localStorage.clear();
    localStorage.setItem('nyay-auth-version', AUTH_VERSION);
  }
  
  let users=JSON.parse(localStorage.getItem('nyay-users')||'{}');
  
  // Add demo user if missing
  if(!users['demo']){
    users['demo']={
      username:'demo',
      password:btoa('password123'),
      createdAt:new Date().toISOString(),
      role:'regular'
    };
  }
  
  // Add admin user if missing (IMPORTANT: Always ensure admin exists)
  if(!users['admin']){
    users['admin']={
      username:'admin',
      password:btoa('admin123'),
      createdAt:new Date().toISOString(),
      role:'administrator',
      permissions:['view_login_logs','view_query_cache','view_training_data','manage_users','export_data','clear_cache']
    };
  }
  
  localStorage.setItem('nyay-users',JSON.stringify(users));
}

// Hash password (simple base64 - for demo, use proper hashing in production)
function hashPassword(pwd){
  return btoa(pwd);
}

// Handle Login
function handleLogin(){
  const username=document.getElementById('login-username').value.trim();
  const password=document.getElementById('login-password').value;
  const messageDiv=document.getElementById('login-message');
  
  if(!username||!password){
    showMessage(messageDiv,'Please fill in all fields','error');
    return;
  }
  
  initializeAuth();
  const users=JSON.parse(localStorage.getItem('nyay-users')||'{}');
  
  // Debug logging (visible in browser console)
  console.log('🔐 Login attempt:', username);
  console.log('📊 Available users:', Object.keys(users));
  console.log('Admin user exists:', !!users['admin']);
  console.log('Entered password hash:', hashPassword(password));
  console.log('Stored password hash:', users[username]?.password);
  
  if(users[username]&&users[username].password===hashPassword(password)){
    // Success
    console.log('✅ Login successful');
    localStorage.setItem('nyay-current-user',username);
    localStorage.setItem('nyay-session-time',Date.now());
    logUserLogin(username);
    showMessage(messageDiv,'✓ Login successful! Redirecting...','success');
    startSharedAudio();
    setTimeout(()=>{
      window.location.href='index.html';
    },800);
  }else{
    console.log('❌ Login failed - Invalid credentials');
    console.log('User exists:', !!users[username]);
    if(users[username]){
      console.log('Password match:', users[username].password===hashPassword(password));
    }
    showMessage(messageDiv,'Invalid username or password','error');
    document.getElementById('login-password').value='';
  }
}

// Handle Registration
function handleRegister(){
  const username=document.getElementById('register-username').value.trim();
  const password=document.getElementById('register-password').value;
  const confirm=document.getElementById('register-confirm').value;
  const messageDiv=document.getElementById('register-message');
  
  if(!username||!password||!confirm){
    showMessage(messageDiv,'Please fill in all fields','error');
    return;
  }
  
  if(password!==confirm){
    showMessage(messageDiv,'Passwords do not match','error');
    document.getElementById('register-confirm').value='';
    return;
  }
  
  if(password.length<6){
    showMessage(messageDiv,'Password must be at least 6 characters','error');
    return;
  }
  
  initializeAuth();
  const users=JSON.parse(localStorage.getItem('nyay-users')||'{}');
  
  if(users[username]){
    showMessage(messageDiv,'Username already exists','error');
    return;
  }
  
  // Create new user
  users[username]={
    username:username,
    password:hashPassword(password),
    createdAt:new Date().toISOString()
  };
  
  localStorage.setItem('nyay-users',JSON.stringify(users));
  showMessage(messageDiv,'✓ Registration successful! You can now login.','success');
  
  // Clear form
  document.getElementById('register-username').value='';
  document.getElementById('register-password').value='';
  document.getElementById('register-confirm').value='';
  
  // Switch to login tab
  setTimeout(()=>{
    document.querySelector('[data-tab="login"]').click();
  },1000);
}

// Show message
function showMessage(el,msg,type){
  el.innerHTML=`<div class="message ${type}">${msg}</div>`;
  setTimeout(()=>{
    if(el.querySelector('.message')){
      el.querySelector('.message').style.animation='slideIn .4s reverse';
      setTimeout(()=>el.innerHTML='',400);
    }
  },3000);
}

// Check if user is logged in
function isLoggedIn(){
  const user=localStorage.getItem('nyay-current-user');
  return !!user;
}

// Get current user
function getCurrentUser(){
  return localStorage.getItem('nyay-current-user');
}

// Logout
function logout(){
  const currentUser = localStorage.getItem('nyay-current-user');
  if(currentUser){
    logUserLogout(currentUser);
  }
  localStorage.removeItem('nyay-current-user');
  localStorage.removeItem('nyay-session-time');
  localStorage.removeItem('nyay-session-id');
  stopSharedAudio();
  window.location.href='login.html';
}

// ─── ADMIN & LOGGING SYSTEM ───

// Check if user is admin
function isAdmin(){
  const currentUser = localStorage.getItem('nyay-current-user');
  return currentUser === 'admin';
}

// Log user login
function logUserLogin(username){
  try {
    const logData = JSON.parse(localStorage.getItem('nyay-login-logs') || '{"logs":[],"summary":{"totalLogins":0,"uniqueUsers":0,"failedAttempts":0,"lastUpdated":""}}');
    
    const loginEntry = {
      id: logData.logs.length + 1,
      username: username,
      loginTime: new Date().toISOString(),
      logoutTime: null,
      status: 'success',
      ipAddress: 'local',
      userAgent: navigator.userAgent.substring(0, 100),
      sessionDuration: null
    };
    
    logData.logs.push(loginEntry);
    
    // Update summary
    logData.summary.totalLogins = logData.logs.length;
    logData.summary.uniqueUsers = new Set(logData.logs.map(l => l.username)).size;
    logData.summary.lastUpdated = new Date().toISOString();
    
    localStorage.setItem('nyay-login-logs', JSON.stringify(logData));
    localStorage.setItem('nyay-session-id', loginEntry.id);
  } catch(e) {
    console.error('Error logging login:', e);
  }
}

// Log user logout
function logUserLogout(username){
  try {
    const logData = JSON.parse(localStorage.getItem('nyay-login-logs') || '{"logs":[]}');
    const sessionId = parseInt(localStorage.getItem('nyay-session-id') || '0');
    const sessionStart = parseInt(localStorage.getItem('nyay-session-time') || Date.now());
    
    if(logData.logs.length > 0){
      const lastLog = logData.logs[logData.logs.length - 1];
      if(lastLog.username === username && !lastLog.logoutTime){
        lastLog.logoutTime = new Date().toISOString();
        lastLog.sessionDuration = Math.round((Date.now() - sessionStart) / 1000); // in seconds
        logData.summary.lastUpdated = new Date().toISOString();
        localStorage.setItem('nyay-login-logs', JSON.stringify(logData));
      }
    }
  } catch(e) {
    console.error('Error logging logout:', e);
  }
}

// Cache query-solution pair
function cacheQuerySolution(query, solution, feature, category){
  try {
    const cacheData = JSON.parse(localStorage.getItem('nyay-query-cache') || '{"cache":[],"metadata":{"totalCacheItems":0,"cacheSize":"0 KB","hitRate":0,"maxCacheSize":"10 MB"}}');
    
    // Check if query exists
    const existingIndex = cacheData.cache.findIndex(c => c.query.toLowerCase() === query.toLowerCase());
    const currentUser = localStorage.getItem('nyay-current-user');
    
    if(existingIndex !== -1){
      // Update existing cache entry
      cacheData.cache[existingIndex].usageCount++;
      cacheData.cache[existingIndex].timestamps.lastUsed = new Date().toISOString();
      
      if(!cacheData.cache[existingIndex].usersAccessed.includes(currentUser)){
        cacheData.cache[existingIndex].usersAccessed.push(currentUser);
      }
    } else {
      // Create new cache entry
      const cacheEntry = {
        id: cacheData.cache.length + 1,
        query: query,
        queryHash: 'hash_' + Date.now(),
        solution: solution,
        feature: feature,
        category: category,
        timestamps: {
          created: new Date().toISOString(),
          lastUsed: new Date().toISOString()
        },
        usageCount: 1,
        usersAccessed: [currentUser],
        relevanceScore: 0.9,
        tags: extractTags(query)
      };
      cacheData.cache.push(cacheEntry);
    }
    
    cacheData.metadata.totalCacheItems = cacheData.cache.length;
    cacheData.metadata.lastUpdated = new Date().toISOString();
    
    localStorage.setItem('nyay-query-cache', JSON.stringify(cacheData));
  } catch(e) {
    console.error('Error caching query:', e);
  }
}

// Log query to training data
function logQueryToTraining(query, solution, queryType, category, feature, responseTime, userSatisfaction){
  try {
    const trainingData = JSON.parse(localStorage.getItem('nyay-training-data') || '{"trainingData":[],"statistics":{"totalQueries":0,"averageResponseTime":0,"averageSatisfactionScore":0,"uniqueCategories":0,"errorRate":0},"queryTypeDistribution":{},"categoryDistribution":{}}');
    
    const currentUser = localStorage.getItem('nyay-current-user');
    const sessionId = localStorage.getItem('nyay-session-id') || 'session_' + Date.now();
    
    const trainingEntry = {
      id: trainingData.trainingData.length + 1,
      timestamp: new Date().toISOString(),
      user: currentUser,
      queryText: query,
      queryType: queryType,
      category: category,
      feature: feature,
      solutionGenerated: solution,
      solutionType: 'generated',
      responseTime: responseTime,
      userSatisfaction: userSatisfaction || 5,
      userFeedback: null,
      followUpQueries: 0,
      sessionId: sessionId,
      context: {
        previousQuery: localStorage.getItem('nyay-last-query') || null,
        userRole: isAdmin() ? 'admin' : 'regular',
        deviceType: getDeviceType()
      }
    };
    
    trainingData.trainingData.push(trainingEntry);
    
    // Update statistics
    trainingData.statistics.totalQueries = trainingData.trainingData.length;
    trainingData.statistics.averageResponseTime = Math.round(
      trainingData.trainingData.reduce((sum, t) => sum + t.responseTime, 0) / trainingData.trainingData.length
    );
    trainingData.statistics.averageSatisfactionScore = (
      trainingData.trainingData.reduce((sum, t) => sum + t.userSatisfaction, 0) / trainingData.trainingData.length
    ).toFixed(2);
    trainingData.statistics.uniqueCategories = new Set(trainingData.trainingData.map(t => t.category)).size;
    trainingData.statistics.lastUpdated = new Date().toISOString();
    
    // Update distributions
    if(!trainingData.queryTypeDistribution[queryType]){
      trainingData.queryTypeDistribution[queryType] = 0;
    }
    trainingData.queryTypeDistribution[queryType]++;
    
    if(!trainingData.categoryDistribution[category]){
      trainingData.categoryDistribution[category] = 0;
    }
    trainingData.categoryDistribution[category]++;
    
    localStorage.setItem('nyay-training-data', JSON.stringify(trainingData));
    localStorage.setItem('nyay-last-query', query);
  } catch(e) {
    console.error('Error logging training data:', e);
  }
}

// Extract tags from query
function extractTags(query){
  const commonTerms = ['rights', 'law', 'constitution', 'court', 'judge', 'case', 'claim', 'evidence', 'liability', 'contract'];
  const tags = commonTerms.filter(term => query.toLowerCase().includes(term));
  return tags.length > 0 ? tags : ['general'];
}

// Get device type
function getDeviceType(){
  if(/mobile|android|iphone|ipad|phone/i.test(navigator.userAgent)){
    return 'mobile';
  }
  if(/tablet|ipad/i.test(navigator.userAgent)){
    return 'tablet';
  }
  return 'desktop';
}

// Get login logs (for admin)
function getLoginLogs(){
  if(!isAdmin()){
    console.warn('Unauthorized: Only admin can access login logs');
    return null;
  }
  return JSON.parse(localStorage.getItem('nyay-login-logs') || '{"logs":[],"summary":{}}');
}

// Get query cache (for admin)
function getQueryCache(){
  if(!isAdmin()){
    console.warn('Unauthorized: Only admin can access query cache');
    return null;
  }
  return JSON.parse(localStorage.getItem('nyay-query-cache') || '{"cache":[],"metadata":{}}');
}

// Get training data (for admin)
function getTrainingData(){
  if(!isAdmin()){
    console.warn('Unauthorized: Only admin can access training data');
    return null;
  }
  return JSON.parse(localStorage.getItem('nyay-training-data') || '{"trainingData":[],"statistics":{}}');
}

// Clear cache (admin only)
function clearQueryCache(){
  if(!isAdmin()){
    console.warn('Unauthorized: Only admin can clear cache');
    return false;
  }
  localStorage.setItem('nyay-query-cache', JSON.stringify({"cache":[],"metadata":{"totalCacheItems":0,"lastUpdated":new Date().toISOString()}}));
  return true;
}

// Export data to JSON (admin only)
function exportAllData(){
  if(!isAdmin()){
    console.warn('Unauthorized: Only admin can export data');
    return null;
  }
  
  const exportData = {
    exportDate: new Date().toISOString(),
    loginLogs: JSON.parse(localStorage.getItem('nyay-login-logs') || '{}'),
    queryCache: JSON.parse(localStorage.getItem('nyay-query-cache') || '{}'),
    trainingData: JSON.parse(localStorage.getItem('nyay-training-data') || '{}')
  };
  
  // Trigger download
  const dataStr = JSON.stringify(exportData, null, 2);
  const dataBlob = new Blob([dataStr], {type: 'application/json'});
  const url = URL.createObjectURL(dataBlob);
  const link = document.createElement('a');
  link.href = url;
  link.download = 'nyay-mitra-data-export-' + new Date().getTime() + '.json';
  link.click();
  
  return exportData;
}

// ─── DEBUG & RESET FUNCTIONS ───

// View current stored users (for debugging)
function debugUsers(){
  const users=JSON.parse(localStorage.getItem('nyay-users')||'{}');
  console.log('=== STORED USERS ===');
  console.log(users);
  console.log('Admin password stored:', users.admin?.password);
  console.log('Admin password should be: YWRtaW4xMjM=' + ' (base64 of admin123)');
  console.log('Demo password stored:', users.demo?.password);
  console.log('Demo password should be: cGFzc3dvcmQxMjM=' + ' (base64 of password123)');
}

// Force RESET all users (clear everything)
function resetAllUsers(){
  console.warn('⚠️ RESETTING ALL USERS AND DATA...');
  localStorage.clear();
  initializeAuth();
  debugUsers();
  console.log('✅ Reset complete! Refresh the page now.');
  alert('✅ All data cleared and reset! Please refresh the page (F5)');
}

// Force set admin password (emergency)
function forceSetAdminPassword(){
  let users=JSON.parse(localStorage.getItem('nyay-users')||'{}');
  users['admin']={
    username:'admin',
    password:btoa('admin123'),
    createdAt:new Date().toISOString(),
    role:'administrator',
    permissions:['view_login_logs','view_query_cache','view_training_data','manage_users','export_data','clear_cache']
  };
  localStorage.setItem('nyay-users',JSON.stringify(users));
  console.log('✅ Admin password reset to admin123');
  debugUsers();
}

// Initialize on page load
window.addEventListener('load',()=>{
  initializeAuth();
});
