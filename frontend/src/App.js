import './App.css';
import Navbar from './components/Navbar/Navbar';
import Home from './components/Home/Home';
import Leaderboard from './components/Leaderboard/Leaderboard';
import Testimonials from './components/Testimonials/Testimonials';


function App() {
    return (
        <div className="app-container">
            <section className="landing-page">
                <Navbar />
                <Home />
            </section>
            <section className="leaderboard-page">
                <Leaderboard />
            </section>
            <section className="testimonials-page">
                <Testimonials />
            </section>
        </div>
      );
}

export default App;
