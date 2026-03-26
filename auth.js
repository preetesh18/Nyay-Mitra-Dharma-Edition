/* ── AUTHENTICATION SYSTEM ── */

// Initialize users in localStorage if not exists
function initializeAuth(){
  if(!localStorage.getItem('nyay-users')){
    // Default demo user
    const users={
      'demo':{
        username:'demo',
        password:btoa('password123'),
        createdAt:new Date().toISOString()
      }
    };
    localStorage.setItem('nyay-users',JSON.stringify(users));
  }
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
  
  if(users[username]&&users[username].password===hashPassword(password)){
    // Success
    localStorage.setItem('nyay-current-user',username);
    localStorage.setItem('nyay-session-time',Date.now());
    showMessage(messageDiv,'✓ Login successful! Redirecting...','success');
    startSharedAudio();
    setTimeout(()=>{
      window.location.href='index.html';
    },800);
  }else{
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
  localStorage.removeItem('nyay-current-user');
  localStorage.removeItem('nyay-session-time');
  stopSharedAudio();
  window.location.href='login.html';
}

// Initialize on page load
window.addEventListener('load',()=>{
  initializeAuth();
});
