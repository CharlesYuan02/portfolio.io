import './Home.css';
import stonksImage from '../../assets/stonks.png';


const Home = () => {
    return (
        <div className="content">
            <div className="text-content">
                <h1 className="text-intro">My Portfolio is the Best...</h1>
                <h1 className="text-intro">And Now I Can <em>Prove It!</em></h1>
                <a href="https://portfolio-io.streamlit.app/Sign%20Up">
                    <button className="cta-button">Join Now</button>
                </a>
            </div>
            <div className="image-content">
                <img src={stonksImage} alt="Stonks" />
            </div>
        </div>
    )
}

export default Home;
