import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar/Navbar';
import Home from './components/Home/Home';
import Leaderboard from './components/Leaderboard/Leaderboard';
import Testimonials from './components/Testimonials/Testimonials';
import CreateUsername from './components/CreateUsername/CreateUsername';
import Dashboard from './components/Dashboard/Dashboard';

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
                <Route path="/create-username" element={<CreateUsername />} />
                <Route path="/dashboard" element={<Dashboard />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
