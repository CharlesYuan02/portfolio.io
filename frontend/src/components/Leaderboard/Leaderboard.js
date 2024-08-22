import React from 'react';
import './Leaderboard.css';
import portfolios from './Leaderboard.json';

const Leaderboard = () => {
    const truncatePortfolioName = (name, maxLength = 25) => {
        if (name.length <= maxLength) return name;
        return `${name.slice(0, maxLength - 3)}...`;
    };

    return (
        <div className="top-public-portfolios">
            <h1>Top Public Portfolios</h1>
            <table>
                <thead>
                <tr>
                    <th></th>
                    <th>Username</th>
                    <th>Portfolio Name</th>
                    <th>% Gain</th>
                    <th>Time Since Incp</th>
                </tr>
                </thead>
            <tbody>
                {portfolios.map((portfolio) => (
                    <tr key={portfolio.rank}>
                    <td>
                        <img src={portfolio.profilePic} alt={portfolio.username} />
                    </td>
                    <td>{portfolio.username}</td>
                    <td>{truncatePortfolioName(portfolio.portfolioName)}</td>
                    <td>{portfolio.gain}</td>
                    <td>{portfolio.timeSinceIncp}</td>
                    </tr>
                ))}
            </tbody>
        </table>
        </div>
    );
};

export default Leaderboard;