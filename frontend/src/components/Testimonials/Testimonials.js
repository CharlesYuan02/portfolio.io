import React from 'react';
import './Testimonials.css';

const Testimonial = ({ username, subreddit, text }) => (
  <div className="testimonial">
    <div className="user-icon"></div>
    <h3>{username}</h3>
    <p className="subreddit">{subreddit}</p>
    <p>{text}</p>
  </div>
);

const Testimonials = () => {
    const testimonials = [
        { username: "u/Chubbyman2", subreddit: "r/wallstreetbets", text: "Now my poor financial decisions and YOLO strategies can be publicly shamed!" },
        { username: "u/RayDalio49", subreddit: "r/wallstreetbets", text: "Who dares challenge my great portfolio, that I've carefully cultivated over the years?" },
        { username: "u/PeterLynch44", subreddit: "r/investing", text: "I love being able to share the hard work I've put into my stocks with my friends!" },
        { username: "u/BenjaminGraham", subreddit: "r/investing", text: "Everyone compliments me now on my brilliant stock picks!" },
        { username: "u/WarrenBuffet30", subreddit: "r/investing", text: "My best friend Charlie and I run this together, it's been a lot of fun!" },
        { username: "u/RoaringKitten", subreddit: "r/wallstreetbets", text: "What can I say, I just like the stock!" }
    ];

    return (
        <div className="testimonials-container">
        <h1>Loved By Investors</h1>
        <h2>Join Your Fellow Retail Investors Today</h2>
        <div className="testimonials-grid">
            {testimonials.map((testimonial, index) => (
            <Testimonial key={index} {...testimonial} />
            ))}
        </div>
        </div>
    );
};

export default Testimonials;