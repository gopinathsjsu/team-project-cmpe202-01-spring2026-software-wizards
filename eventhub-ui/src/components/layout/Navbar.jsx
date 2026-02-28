import { NavLink } from 'react-router-dom';

const navItems = [
  { to: '/', label: 'Home' },
  { to: '/events', label: 'Events' },
  { to: '/login', label: 'Login' },
  { to: '/register', label: 'Register' },
];

export default function Navbar() {
  return (
    <header className="navbar">
      <div className="navbar-brand">EventHub</div>
      <nav className="navbar-links">
        {navItems.map((item) => (
          <NavLink key={item.to} to={item.to} className={({ isActive }) => isActive ? 'active' : ''}>
            {item.label}
          </NavLink>
        ))}
      </nav>
    </header>
  );
}
