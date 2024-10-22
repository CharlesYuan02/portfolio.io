import './AddPosition.css';
import React, { useState, useEffect} from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { useAuth0 } from '@auth0/auth0-react';
import supabase from '../../utils/CreateSupabaseClient'
import axios from 'axios';

const portfoliosTable = process.env.REACT_APP_SUPABASE_PORTFOLIOS_TABLE;
const positionsTable = process.env.REACT_APP_SUPABASE_POSITIONS_TABLE;

const AddPosition = ({ resetTrigger, onResetComplete }) => {
    const [ticker, setTicker] = useState('');
    const [amount, setAmount] = useState('');
    const [datePurchased, setDatePurchased] = useState(new Date());
    const [purchasePrice, setPurchasePrice] = useState('');
    const [selectedPortfolio, setSelectedPortfolio] = useState('');
    const [newPortfolioName, setNewPortfolioName] = useState('');
    const [makePublic, setMakePublic] = useState(true);
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
            setDatePurchased(new Date());
            setPurchasePrice('');
            setSelectedPortfolio('');
            setNewPortfolioName('');
            setMakePublic(true);
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

    /* Handle submission of new buy position */
    const handleSubmit = async (e) => {
        e.preventDefault();
        error && setError('') && setSuccessMessage(''); // Clear any previous errors

        /* Check if form fields are valid */
        if (datePurchased > new Date()) {
            setError('Date purchased cannot be in the future.');
            return;
        } else if (selectedPortfolio === 'createNew' && !newPortfolioName) {
            setError('Please enter a name for the new portfolio.');
            return;
        } else if (selectedPortfolio === 'createNew' && portfolios.includes(newPortfolioName)) {
            setError('Portfolio name already exists. Please choose a different name.');
            return;
        } else {
            try {
                const response = await axios.post('/backend/daily_price_range/', { ticker: ticker, date: datePurchased });
                if (response.data[0] > purchasePrice || response.data[1] < purchasePrice) {
                    setError('Purchase price is not within the daily price range for the selected date.');
                    return;
                }
            } catch (err) {
                setError(err.message);
            }
        }

        /* If a new portfolio is created, insert into portfolios table */
        if (selectedPortfolio === 'createNew' && newPortfolioName) {
            try {
                const { data, error } = await supabase
                    .from('portfolios')
                    .insert([
                        { 
                            email: email, 
                            portfolio: newPortfolioName,
                            is_public: makePublic,
                        }
                    ]);
                if (error) throw error;
                console.log('New portfolio stored successfully:', data);
            
            } catch (error) {
                console.error('Error storing new portfolio:', error);
                setError('Could not store new portfolio into database. Please try again later.');
                return;
            }
        }

        /* Insert position into positions table */
        try {
            const { data, error } = await supabase
                .from(positionsTable)
                .insert([
                    {  
                        stock: ticker,
                        amount: amount,
                        unit_price: purchasePrice,
                        total_price: amount * purchasePrice,
                        date_purchased: datePurchased,
                        owner: email,
                        portfolio: selectedPortfolio === 'createNew' ? newPortfolioName : selectedPortfolio,
                    }
                ]);
            if (error) throw error;
            console.log('Position stored successfully:', data);
            setSuccessMessage('Buy position added successfully!');

        } catch (error) {
            console.error('Error storing position:', error);
            setError('Could not store position into database. Please try again later.');
            return;
        }
    };

    return (
        <div className="add-position-container">
          <h2>Add Position</h2>
          <form onSubmit={handleSubmit}>
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
                <label htmlFor="datePurchased">Date Purchased:</label>
                <div className="input-wrapper">
                    <DatePicker
                    selected={datePurchased}
                    onChange={(date) => setDatePurchased(date)}
                    dateFormat="MM/dd/yyyy"
                    className="date-picker"
                    />
                </div>
            </div>
    
            <div className="form-group">
                <label htmlFor="purchasePrice">Purchase Price:</label>
                <div className="input-wrapper">
                    <input
                    type="number"
                    id="purchasePrice"
                    value={purchasePrice}
                    onChange={(e) => setPurchasePrice(e.target.value)}
                    step="0.01"
                    min="0"
                    placeholder="e.g. 189.73"
                    required
                    />
                </div>
            </div>
    
            <div className="form-group">
                <label htmlFor="portfolio">Add To:</label>
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
                    <option value="createNew">Create New</option>
                    </select>
                </div>
            </div>
    
            {selectedPortfolio === 'createNew' && (
                <>
                    <div className="form-group">
                        <label htmlFor="newPortfolio">New Portfolio Name:</label>
                        <div className="input-wrapper">
                            <input
                                type="text"
                                id="newPortfolio"
                                value={newPortfolioName}
                                onChange={(e) => setNewPortfolioName(e.target.value)}
                                required
                            />
                        </div>
                    </div>
                    <div className="form-group make-public-group">
                        <label htmlFor="makePublic">Make Portfolio Public:
                            <input
                                type="checkbox"
                                id="makePublic"
                                checked={makePublic}
                                onChange={(e) => setMakePublic(e.target.checked)}
                                defaultChecked
                            />
                        </label>
                    </div>
                </>
            )}

            {error && <div className="error-message">{error}</div>}
            {successMessage && <div className="success-message">{successMessage}</div>}
    
            {!successMessage && (
                    <button type="submit" className="submit-btn">Add Position</button>
            )}
          </form>
        </div>
    );
};

export default AddPosition;