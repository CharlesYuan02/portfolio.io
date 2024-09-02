import './Home.css';
import stonksImage from '../../assets/stonks.png';
import { useAuth0 } from '@auth0/auth0-react';
import { useNavigate } from 'react-router-dom';
import supabase from '../../utils/CreateSupabaseClient';

const usersTable = process.env.REACT_APP_SUPABASE_USERS_TABLE;

const Home = () => {
    const { loginWithRedirect, isAuthenticated, user } = useAuth0();
    const { email, sub } = user || {};
    const navigate = useNavigate();
    
    const handleSignUp = async (e) => {
        e.preventDefault();

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

        if (username.length > 0) { // Redirect to dashboard if user has username
            navigate('/dashboard');
            return;
        } else if (isAuthenticated) { // Redirect to create-username page if user is authenticated
            navigate('/create-username');
            return;
        }
        
        // Remember to add /create-username to the allowed callback URLs in the Auth0 dashboard
        loginWithRedirect({
            authorizationParams: {
                screen_hint: 'signup',
                redirect_uri: `${window.location.origin}/create-username`
            },
        });
    };

    return (
        <div className="content">
            <div className="text-content">
                <h1 className="text-intro">My Portfolio is the Best...</h1>
                <h1 className="text-intro">And Now I Can <em>Prove It!</em></h1>
                <button className="cta-button" onClick={handleSignUp}>Join Now</button>
            </div>
            <div className="image-content">
                <img src={stonksImage} alt="Stonks" />
            </div>
        </div>
    )
}

export default Home;
