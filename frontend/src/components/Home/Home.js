import './Home.css';
import stonksImage from '../../assets/stonks.png';
import { useAuth0 } from '@auth0/auth0-react';

const Home = () => {
    const { loginWithRedirect } = useAuth0();

    return (
        <div className="content">
            <div className="text-content">
                <h1 className="text-intro">My Portfolio is the Best...</h1>
                <h1 className="text-intro">And Now I Can <em>Prove It!</em></h1>
                <button className="cta-button" onClick={() => loginWithRedirect({
                    authorizationParams: {
                        screen_hint: 'signup'
                    }
                })}>Join Now</button>
            </div>
            <div className="image-content">
                <img src={stonksImage} alt="Stonks" />
            </div>
        </div>
    )
}

export default Home;
