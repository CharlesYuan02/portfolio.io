import './Dashboard.css';
import React, { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { PieChart, Pie, Cell, Legend } from 'recharts';
import { useAuth0 } from '@auth0/auth0-react';
import AddPosition from '../AddPosition/AddPosition';

// Dummy data for the line chart
const performanceData = [
    { date: '2024-01', value: 1000 },
    { date: '2024-02', value: 1200 },
    { date: '2024-03', value: 1100 },
    { date: '2024-04', value: 1400 },
    { date: '2024-05', value: 1300 },
    { date: '2024-06', value: 1600 },
];

// Dummy data for the pie chart
const holdingsData = [
    { name: 'Unilever', value: 31.5 },
    { name: 'Proctor & Gamble', value: 30.5 },
    { name: 'Dial', value: 19 },
    { name: 'Colgate-Palmolive', value: 8 },
    { name: 'All others', value: 11 },
];

// Dummy data for the positions table
const positionsData = [
    { stock: 'AAPL', price: 226.13, shares: 3, date: '08/30/2024' },
    { stock: 'GOOGL', price: 138.21, shares: 5, date: '08/29/2024' },
    { stock: 'MSFT', price: 328.66, shares: 2, date: '08/28/2024' },
];

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'];

const Dashboard = () => {
    const [isPopupOpen, setIsPopupOpen] = useState(false);

    /* Lazy loading */
    const { user, logout } = useAuth0();
    if (!user) {
        return <div>Loading...</div>;
    }

    /* Get username */
    const { name } = user || {};
    const dashboardName = name.endsWith("s") ? `${name}' Dashboard` : `${name}'s Dashboard`;

    const togglePopup = () => {
        setIsPopupOpen(!isPopupOpen);
    };

    const handleLogout = () => {
        logout({ returnTo: window.location.origin });
    };

    return (
        <div className="dashboard">
        <div className="dashboard-header">
            <button className="open-popup-btn" onClick={togglePopup}>
                Add Position
            </button>

            <div className={`add-position-popup ${isPopupOpen ? 'open' : ''}`}>
                <button className="close-popup-btn" onClick={togglePopup}>
                &times;
                </button>
                <AddPosition />
            </div>

            <h1 className="dashboard-title">{dashboardName}</h1>

            <button className="logout-button" onClick={handleLogout}>
                Log Out
            </button>
        </div>

        <div className="dashboard-grid">
            <div className="chart-container performance-chart">
            <h2 className="chart-title">Portfolio Performance</h2>
            <ResponsiveContainer width="100%" height={280}>
                <LineChart data={performanceData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="value" stroke="#8884d8" />
                </LineChart>
            </ResponsiveContainer>
            </div>

            <div className="chart-container portfolio-history">
            <h2 className="chart-title">Portfolio History</h2>
            <table className="portfolio-table">
                <thead>
                <tr>
                    <th>Stock</th>
                    <th>Price</th>
                    <th>Shares</th>
                    <th>Date</th>
                </tr>
                </thead>
                <tbody>
                {positionsData.map((position, index) => (
                    <tr key={index}>
                    <td>{position.stock}</td>
                    <td>${position.price.toFixed(2)}</td>
                    <td>{position.shares}</td>
                    <td>{position.date}</td>
                    </tr>
                ))}
                </tbody>
            </table>
            </div>

            <div className="chart-container holdings-chart">
            <h2 className="chart-title">Portfolio Holdings</h2>
            <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                <Pie
                    data={holdingsData}
                    cx="50%"
                    cy="40%"
                    labelLine={false}
                    outerRadius={100}
                    fill="#8884d8"
                    dataKey="value"
                    label={({ value }) => `${value}`}
                >
                    {holdingsData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                </Pie>
                <Legend wrapperStyle={{bottom: 45}}/>
                </PieChart>
            </ResponsiveContainer>
            </div>
        </div>
        </div>
    );
};

export default Dashboard;