import './Navbar.css';
import { useAuth0 } from '@auth0/auth0-react';

const Navbar = () => {
    const { loginWithRedirect } = useAuth0();

    return (
        <nav className="navbar">
            <div className="logo">portfolio.io</div>
            <div className="login">
                <button 
                    className="no-style" 
                    onClick={(e) => {
                        e.preventDefault();
                        loginWithRedirect();
                    }}
                >
                    Login
                </button>
            </div>
        </nav>
    )
}

export default Navbar;