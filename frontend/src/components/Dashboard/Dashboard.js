import './Dashboard.css';
import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { PieChart, Pie, Cell, Legend } from 'recharts';
import { useAuth0 } from '@auth0/auth0-react';
import axios from 'axios';
import AddPosition from '../AddPosition/AddPosition';
import SellPosition from '../SellPosition/SellPosition';
import Chatbot from '../Chatbot/Chatbot';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'];

const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
        const roundedValue = Number(payload[0].value).toFixed(2);
        return (
          <div className="bg-white border border-gray-300 p-2 shadow-md">
            <p className="text-gray-700">{`Date: ${label}`}</p>
            <p className="text-gray-700">{`Value: ${roundedValue}`}</p>
          </div>
        );
    }
    return null;
};

const Dashboard = () => {
    const { user, logout } = useAuth0();
    const [isAddPositionPopupOpen, setIsAddPositionPopupOpen] = useState(false);
    const [isSellPositionPopupOpen, setIsSellPositionPopupOpen] = useState(false);
    const [isChatbotPopupOpen, setIsChatbotPopupOpen] = useState(false);
    const [performanceData, setPerformanceData] = useState([]);
    const [holdingsData, setHoldingsData] = useState([]);
    const [historyData, setHistoryData] = useState([]);
    const [portfolios, setPortfolios] = useState([]);
    const [selectedPortfolio, setSelectedPortfolio] = useState(null);
    const [resetAddPosition, setResetAddPosition] = useState(false); // For resetting success/error messages 
    const [resetSellPosition, setResetSellPosition] = useState(false);
    const [resetChatbot, setResetChatbot] = useState(false);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    /* Make initial call to retrieve data from Supabase and populate backend cache */
    useEffect(() => {
        if (!user) return;

        const fetchPortfolios = async () => {
            try {
                const response = await axios.post('/backend/all_portfolios/', { email: user.email });
                setPortfolios(response.data);
                if (response.data.length > 0) setSelectedPortfolio(response.data[0]);
            } catch (err) {
                setError(err.message);
            }
        };

        fetchPortfolios();
    }, [user]);

    /* Obtain data for performance, holdings, history */
    useEffect(() => {
        if (!user || !selectedPortfolio) return;

        const fetchPortfolioData = async () => {
            setIsLoading(true);
            try {
                const [performanceRes, holdingsRes, historyRes] = await Promise.all([
                    axios.post('/backend/portfolio_performance/', { email: user.email, portfolio: selectedPortfolio }),
                    axios.post('/backend/portfolio_holdings/', { email: user.email, portfolio: selectedPortfolio }),
                    axios.post('/backend/portfolio_history/', { email: user.email, portfolio: selectedPortfolio }),
                ]);

                setPerformanceData(performanceRes.data.map(([date, value]) => ({ date, value })));
                setHoldingsData(Object.entries(holdingsRes.data).map(([name, { total_value }]) => ({ name, value: total_value })));
                setHistoryData(historyRes.data);
            } catch (err) {
                setError(err.message);
            } finally {
                setIsLoading(false);
            }
        };

        fetchPortfolioData();
    }, [user, selectedPortfolio]);

    /* Lazy loading */
    if (!user) {
        return <div>Loading...</div>;
    }

    /* Get username */
    const { name } = user || {};
    const dashboardName = name.endsWith("s") ? `${name}' Dashboard` : `${name}'s Dashboard`;

    const toggleAddPositionPopup = () => {
        setIsAddPositionPopupOpen(!isAddPositionPopupOpen);
        if (isAddPositionPopupOpen) {
            setResetAddPosition(true);
        }
    };

    const toggleSellPositionPopup = () => {
        setIsSellPositionPopupOpen(!isSellPositionPopupOpen);
        if (isSellPositionPopupOpen) {
            setResetSellPosition(true);
        }
    };

    const toggleChatbotPopup = () => {
        setIsChatbotPopupOpen(!isChatbotPopupOpen);
        if (isChatbotPopupOpen) {
            setResetChatbot(true);
        }
    };

    const handleLogout = () => {
        logout({ returnTo: window.location.origin });
    };

    const handlePortfolioChange = (event) => {
        setSelectedPortfolio(event.target.value);
    };

    return (
        <div className="dashboard">
        <div className="dashboard-header">
            <button className="open-popup-btn" onClick={toggleAddPositionPopup}>
                Add Position
            </button>

            <div className={`add-position-popup ${isAddPositionPopupOpen ? 'open' : ''}`}>
                <button className="close-popup-btn" onClick={toggleAddPositionPopup}>
                    &times;
                </button>
                <AddPosition resetTrigger={resetAddPosition} onResetComplete={() => setResetAddPosition(false)} />
            </div>

            <button className="open-popup-btn" onClick={toggleSellPositionPopup}>
                Sell Position
            </button>

            <div className={`sell-position-popup ${isSellPositionPopupOpen ? 'open' : ''}`}>
                <button className="close-popup-btn" onClick={toggleSellPositionPopup}>
                    &times;
                </button>
                <SellPosition resetTrigger={resetSellPosition} onResetComplete={() => setResetSellPosition(false)} />
            </div>

            <button className="open-popup-btn" onClick={toggleChatbotPopup}>
                Chatbot
            </button>

            <div className={`chatbot-popup ${isChatbotPopupOpen ? 'open' : ''}`}>
                <button className="close-popup-btn-chatbot" onClick={toggleChatbotPopup}>
                    &times;
                </button>
                <Chatbot resetTrigger={resetChatbot} onResetComplete={() => setResetChatbot(false)} />
            </div>

            <h1 className="dashboard-title">{dashboardName}</h1>

            <select 
                value={selectedPortfolio} 
                onChange={handlePortfolioChange}
                className="portfolio-selector"
            >
                {portfolios.map((portfolio) => (
                    <option key={portfolio} value={portfolio}>
                        {portfolio}
                    </option>
                ))}
            </select>

            <button className="logout-button" onClick={handleLogout}>
                Log Out
            </button>
        </div>

        <div className="dashboard-grid">
            <div className="chart-container performance-chart">
            <h2 className="chart-title">Portfolio Performance</h2>
            <ResponsiveContainer width="93%" height={280}>
                <LineChart data={performanceData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis dataKey="value" tickFormatter={(value) => value.toFixed(0)} domain={['dataMin', 'dataMax']}/>
                <Tooltip content={<CustomTooltip />} />
                <Line type="monotone" dataKey="value" stroke="#38BC81" />
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
                    <th>Action</th>
                </tr>
                </thead>
                <tbody>
                {historyData.map((position, index) => (
                    <tr key={index}>
                    <td>{position.stock}</td>
                    <td>${position.unit_price.toFixed(2)}</td>
                    <td>{position.amount > 0 ? position.amount : -1 * position.amount}</td>
                    <td>{position.date_purchased}</td>
                    <td>{position.amount > 0 ? 'Buy' : 'Sell'}</td>
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
                    cy="43%"
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
                <Legend wrapperStyle={{bottom: 40}}/>
                </PieChart>
            </ResponsiveContainer>
            </div>
        </div>
        </div>
    );
};

export default Dashboard;