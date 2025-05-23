// Helper to manage login user data in localStorage

export function saveUser(user) {
  localStorage.setItem('suems_user', JSON.stringify(user));
}

export function getUser() {
  const user = localStorage.getItem('suems_user');
  return user ? JSON.parse(user) : null;
}

export function logout() {
  localStorage.removeItem('suems_user');
}

export function isLoggedIn() {
  return !!getUser();
}

export function isAdmin() {
  const user = getUser();
  return user?.role === 'Administrator';
}
