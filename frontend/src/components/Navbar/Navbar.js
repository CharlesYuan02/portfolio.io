import './Navbar.css';

const Navbar = () => {
    return (
        <nav className="navbar">
            <div className="logo">portfolio.io</div>
            <div className="login">
                <a href="https://portfolio-io.streamlit.app/" className="no-link-style">Login</a>
            </div>
        </nav>
    )
}

export default Navbar;