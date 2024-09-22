import './Chatbot.css';
import React, { useState, useRef, useEffect } from 'react';
import { Send } from 'lucide-react';
import axios from 'axios';
import { useAuth0 } from '@auth0/auth0-react';

const Chatbot = ({ resetTrigger, onResetComplete }) => {
    const { user } = useAuth0();
    const [messages, setMessages] = useState([]);
    const [selectedStock, setSelectedStock] = useState('');
    const [isLoading, setIsLoading] = useState(false); // Loading state for chatbot response - prevent multiple requests at once
    const [input, setInput] = useState('');
    const [error, setError] = useState('');
    const [stocks, setStocks] = useState([]);
    const messagesEndRef = useRef(null);
    const hasPremiumAccess = false;

    /* Reset message history when resetTrigger is true */
    useEffect(() => {
        if (resetTrigger) {
            setMessages([]);
            setSelectedStock('');
            setIsLoading(false);
            setInput('');
            setError('')
            onResetComplete();
        }
    }, [resetTrigger, onResetComplete]);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(scrollToBottom, [messages]);

    /* Check if user has premium access */
    useEffect(() => {
        const fetchPremiumStatus = async () => {
            try {
                const response = await axios.post('/backend/premium/', { email: user.email });
                if (!response.data) {
                    setMessages([{ text: "You do not have access to this feature. Please upgrade to premium.", sender: 'bot' }]);
                } else {
                    setMessages([{ text: "Hi there! Ask me anything about one of the listed stocks.", sender: 'bot' }]);
                    hasPremiumAccess = true;
                }
            } catch (err) {
                setError(err.message);
            }
        };
        fetchPremiumStatus();
    }, []);

    /* Fetch available stock tickers for dropdown */
    useEffect(() => {
        const fetchTickers = async () => {
            try {
                const response = await axios.get('/backend/tickers/');
                setSelectedStock(response.data[0]);
                setStocks(response.data);
            } catch (err) {
                setError(err.message);
            }
        };
        fetchTickers();
    }, []);

    const handleSend = () => {
        if (!hasPremiumAccess) return;
        if (input.trim()) {
            setIsLoading(true);
            // Add user message immediately, then chatbot message after fetching response
            setMessages(prevMessages => [...prevMessages, { text: input, sender: 'user' }]);
            setInput('');

            /* Fetch the chatbot response from the backend */
            const fetchResponse = async () => {
                try {
                    const response = await axios.post('/backend/chatbot/', { ticker: selectedStock, query: input });
                    setMessages(prevMessages => [...prevMessages, { text: response.data, sender: 'bot' }]);
                } catch (err) {
                    setError(err.message);
                    setMessages(prevMessages => [...prevMessages, { text: "Sorry, there was an error processing your request.", sender: 'bot' }]);
                } finally {
                    setIsLoading(false);
                }    
            };
            fetchResponse();
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !isLoading) {
            handleSend();
        }
    };

    return (
        <div className="chatbot-container">
            <div className="chatbot-messages">
                {messages.map((msg, index) => (
                    <div key={index} className={`message ${msg.sender}`}>
                        <span className="chatbot-message-content">{msg.text}</span>
                    </div>
                ))}
                <div ref={messagesEndRef} />
            </div>
            <div className="chatbot-footer">
                <div className="chatbot-footer-left">
                    <select
                        value={selectedStock}
                        onChange={(e) => setSelectedStock(e.target.value)}
                        className="stock-selector"
                    >
                        {stocks.map((stock) => (
                            <option key={stock} value={stock}>{stock}</option>
                        ))}
                    </select>
                </div>
                <div className="chatbot-input">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={handleKeyPress}
                        placeholder="What was total profit this year?"
                    />
                    <button onClick={handleSend} className="send-button">
                        <Send size={20} />
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Chatbot;