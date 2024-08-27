import React, { useState } from 'react';
import AddPosition from '../AddPosition/AddPosition';
import './Dashboard.css';

const Dashboard = () => {
    const [isPopupOpen, setIsPopupOpen] = useState(false);

    const togglePopup = () => {
        setIsPopupOpen(!isPopupOpen);
    };

    return (
        <div className="dashboard-container">
            <h1>Dashboard</h1>
            
            <button className="open-popup-btn" onClick={togglePopup}>
                Add Position
            </button>

            <div className={`add-position-popup ${isPopupOpen ? 'open' : ''}`}>
                <button className="close-popup-btn" onClick={togglePopup}>
                &times;
                </button>
                <AddPosition />
            </div>
        </div>
    );
};

export default Dashboard;