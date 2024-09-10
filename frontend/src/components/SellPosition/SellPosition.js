import './SellPosition.css';
import React, { useState, useEffect} from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { useAuth0 } from '@auth0/auth0-react';
import supabase from '../../utils/CreateSupabaseClient'
import axios from 'axios';

const portfoliosTable = process.env.REACT_APP_SUPABASE_PORTFOLIOS_TABLE;
const positionsTable = process.env.REACT_APP_SUPABASE_POSITIONS_TABLE;

const SellPosition = ({ resetTrigger, onResetComplete }) => {
    const [ticker, setTicker] = useState('');
    const [amount, setAmount] = useState('');
    const [dateSold, setDateSold] = useState(new Date());
    const [sellPrice, setSellPrice] = useState('');
    const [selectedPortfolio, setSelectedPortfolio] = useState('');
    const [error, setError] = useState('');
    const [successMessage, setSuccessMessage] = useState('');
    const { user } = useAuth0();
    const { email } = user || {};

    /* Reset success/error messages when resetTrigger is true */
    useEffect(() => {
        if (resetTrigger) {
            setError('')
            setSuccessMessage('');
            setTicker('')
            setAmount('');
            setDateSold(new Date());
            setSellPrice('');
            setSelectedPortfolio('');
            onResetComplete();
        }
    }, [resetTrigger, onResetComplete]);

    /* Retrieve portfolios if user has any */
    const [portfolios, setPortfolios] = useState([]);
    useEffect(() => {
        const fetchPortfolios = async () => {
            try {
                const { data, error } = await supabase
                    .from(portfoliosTable)
                    .select('portfolio')
                    .eq('email', email);
                if (error) throw error;
                setPortfolios(data.map((portfolio) => portfolio.portfolio));
            } catch (error) {
                console.error('Error fetching portfolios:', error);
            }
        };
        fetchPortfolios();
    }, [email]);

    /* Handle submission of new sell position */
    const handleSubmit = async (e) => {
        e.preventDefault();
        error && setError('') && setSuccessMessage(''); // Clear any previous errors

        /* Check if form fields are valid */
        if (dateSold > new Date()) {
            setError('Date sold cannot be in the future.');
            return;
        } else {
            try {
                const response = await axios.post('/backend/daily_price_range/', { ticker: ticker, date: dateSold });
                if (response.data[0] > sellPrice || response.data[1] < sellPrice) {
                    setError('Sell price is not within the daily price range for the selected date.');
                    return;
                }
            } catch (err) {
                setError(err.message);
            }
        }

        /* Get all positions in selectedPortfolio to ensure user has enough to sell */
        try {
            const { data, error } = await supabase
                .from(positionsTable)
                .select('amount')
                .eq('owner', email)
                .eq('portfolio', selectedPortfolio)
                .eq('stock', ticker);
            if (error) throw error;
            const totalAmount = data.reduce((acc, { amount }) => acc + amount, 0);
            if (data.length === 0) {
                setError('You do not have this stock in your portfolio.');
                return;
            }
            if (totalAmount < amount) {
                setError('You do not have enough shares to sell.');
                return;
            }
        } catch (error) {
            console.error('Error fetching positions:', error);
            setError('Could not fetch positions. Please try again later.');
            return;
        }

        /* Insert position into positions table */
        try {
            const { data, error } = await supabase
                .from(positionsTable)
                .insert([
                    {  
                        stock: ticker,
                        amount: -1 * amount,
                        unit_price: sellPrice,
                        total_price: -1 * amount * sellPrice,
                        date_purchased: dateSold,
                        owner: email,
                        portfolio: selectedPortfolio,
                    }
                ]);
            if (error) throw error;
            console.log('Position stored successfully:', data);
            setSuccessMessage('Sell position added successfully!');

        } catch (error) {
            console.error('Error storing position:', error);
            setError('Could not store position into database. Please try again later.');
            return;
        }
    };

    return (
        <div className="add-position-container">
            <h2>Sell Position</h2>
            <form onSubmit={handleSubmit}>
            <div className="form-group">
                    <label htmlFor="portfolio">Sell From:</label>
                    <div className="input-wrapper">
                        <select
                        id="portfolio"
                        value={selectedPortfolio}
                        onChange={(e) => setSelectedPortfolio(e.target.value)}
                        required
                        >
                        <option value="">Select a portfolio</option>
                        {portfolios.map((portfolio) => (
                            <option key={portfolio} value={portfolio}>
                            {portfolio}
                            </option>
                        ))}
                        </select>
                    </div>
                </div>

                <div className="form-group">
                    <label htmlFor="ticker">Stock Ticker:</label>
                    <div className="input-wrapper">
                        <input
                        type="text"
                        id="ticker"
                        value={ticker}
                        onChange={(e) => setTicker(e.target.value)}
                        placeholder="e.g. AAPL"
                        required
                        />
                    </div>
                </div>
        
                <div className="form-group">
                    <label htmlFor="amount">Amount:</label>
                    <div className="input-wrapper">
                        <input
                        type="number"
                        id="amount"
                        value={amount}
                        onChange={(e) => setAmount(e.target.value)}
                        step="0.001"
                        min="0"
                        placeholder="e.g. 100"
                        required
                        />
                    </div>
                </div>

                <div className="form-group">
                    <label htmlFor="dateSold">Date Sold:</label>
                    <div className="input-wrapper">
                        <DatePicker
                        selected={dateSold}
                        onChange={(date) => setDateSold(date)}
                        dateFormat="MM/dd/yyyy"
                        className="date-picker"
                        />
                    </div>
                </div>
        
                <div className="form-group">
                    <label htmlFor="sellPrice">Sell Price:</label>
                    <div className="input-wrapper">
                        <input
                        type="number"
                        id="sellPrice"
                        value={sellPrice}
                        onChange={(e) => setSellPrice(e.target.value)}
                        step="0.01"
                        min="0"
                        placeholder="e.g. 189.73"
                        required
                        />
                    </div>
                </div>

                {error && <div className="error-message">{error}</div>}
                {successMessage && <div className="success-message">{successMessage}</div>}
        
                {!successMessage && (
                    <button type="submit" className="submit-btn">Sell Position</button>
                )}
            </form>
        </div>
    );
};

export default SellPosition;