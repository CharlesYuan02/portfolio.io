import './Navbar.css';
import { useAuth0 } from '@auth0/auth0-react';
import { createClient } from '@supabase/supabase-js';
import { useNavigate } from 'react-router-dom';

const supabaseURL = process.env.REACT_APP_SUPABASE_URL;
const supabaseKey = process.env.REACT_APP_SUPABASE_API_KEY;
const usersTable = process.env.REACT_APP_SUPABASE_USERS_TABLE;
const supabase = createClient(supabaseURL, supabaseKey);

const Navbar = () => {
    const { loginWithRedirect, user } = useAuth0();
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();

        if (!user) {
            loginWithRedirect({
                redirectUri: `${window.location.origin}/create-username`
            });
            return;
        }

        const { email, sub } = user;

        // If user is logged in and has a username, redirect to dashboard
        if (email && sub) {
            // Check if user has username in database
            const { data: username, error: usernameError } = await supabase
                .from(usersTable)
                .select('username')
                .eq('email', email)
                .eq('password', sub);
            if (usernameError) {
                console.error('Error fetching username:', usernameError);
                return;
            }

            if (username.length > 0) {
                navigate('/dashboard');
                return;
            } else {
                navigate('/create-username');
                return;
            }
        }
    }

    return (
        <nav className="navbar">
            <div className="logo">portfolio.io</div>
            <div className="login">
                <button 
                    className="no-style" 
                    onClick={handleLogin}
                >
                    Login
                </button>
            </div>
        </nav>
    )
}

export default Navbar;