# portfolio.io
An app to share your investment portfolio with your friends!

## Introduction
Have you ever wanted to showcase your portfolio and its performance to your friends? What about discovering new portfolio strategies from others? Well then, portfolio.io is the platform for you!

## Getting Started
To get started, you'll need a Supabase account and a table. See [.env.example](https://github.com/Chubbyman2/investment-tracker/blob/main/.env.example) for more details. Make sure to either disable RLS (not recommended) or [add a new policy](https://stackoverflow.com/questions/74302341/supabase-bucket-new-row-violates-row-level-security-policy-for-table-objects)!

### Prerequisites
```
plotly==5.20.0
python-dotenv==1.0.1
streamlit==1.33.0
supabase==1.0.3
yfinance==0.2.12
```

## Technologies
### Streamlit
Streamlit was used to create the web app with just Python.

### Supabase
Supabase was used to store the existing positions for each user, in order to display analytics regarding portfolio performances.

### yfinance
yfinance was used to retrieve historical stock information.

## To Do
- Create login and individual user pages
- Create leaderboard and community showcase of portfolios
- Create friends feature, where you can view your friends' portfolio performances
- Create better frontend
- Integrate [Mango10K](https://github.com/Chubbyman2/Mango10K/tree/main) RAG chatbot for investment guidance

## License
This project is licensed under the MIT License - see the <a href="https://github.com/Chubbyman2/investment-tracker/blob/main/LICENSE">LICENSE</a> file for details.
