import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar/Navbar';
import Home from './components/Home/Home';
import Leaderboard from './components/Leaderboard/Leaderboard';
import Testimonials from './components/Testimonials/Testimonials';

function App() {
    return (
        <Router>
            <div className="app-container">
                <Routes>
                <Route path="/" element={
                    <>
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
                    </>
                } />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
