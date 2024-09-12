# portfolio.io
<img src="https://github.com/Chubbyman2/portfolio.io/blob/main/docs/homepage.png"> 

## Introduction
Have you ever wanted to showcase your portfolio and its performance to your friends? What about discovering new portfolio strategies from others? Well then, portfolio.io is the platform for you! Introducing a new place to share your investment portfolio with your friends, test new strategies, and gain new insights through the power of LLM retrieval-augmented generation!

## Getting Started
To get started, you'll need the following:

### <a href="https://auth0.com/">Auth0</a>
Auth0 is used to provide user authentication (login and signup). You'll need your application's domain and client ID. See the frontend [.env.example](https://github.com/CharlesYuan02/portfolio.io/blob/main/frontend/.env.example) for the required environment variables. Make sure to add "http\://127.0.0.1:8000, http\://127.0.0.1:8000/create-username, http\://127.0.0.1:8000/dashboard" to the **Allowed Callback URLs**on your Auth0 dashboard. Also, add "http\://127.0.0.1:8000" to the **Allowed Logout URLs** and **Allowed Web Origins**. Change these to match your domain upon deployment.

### <a href="https://supabase.com/">Supabase</a>
Supabase is used to store the user data, portfolio data, and stock data. You'll need three tables to store the aforementioned information. See the frontend [.env.example](https://github.com/CharlesYuan02/portfolio.io/blob/main/frontend/.env.example) and the backend [.env.example](https://github.com/Chubbyman2/investment-tracker/blob/main/.env.example) for the required environment variables. Make sure to either disable RLS (not recommended) or [add a new policy](https://stackoverflow.com/questions/74302341/supabase-bucket-new-row-violates-row-level-security-policy-for-table-objects)!

### <a href="https://www.pinecone.io/">Pinecone</a>
Pinecone powers the vector embeddings and search used in RAG. You'll need an index, with the configuration being: **Dimensions = 1536** and **Metric = cosine**. See the backend [.env.example](https://github.com/Chubbyman2/investment-tracker/blob/main/.env.example) for the required environment variables. This will be used for the Chatbot feature. 

### <a href="https://openai.com/index/openai-api/">OpenAI API</a>
OpenAI's API provides the LLM used to create vector embeddings and generate responses after vector search. See the backend [.env.example](https://github.com/Chubbyman2/investment-tracker/blob/main/.env.example) for the required environment variable.

### <a href="https://pypi.org/project/edgartools/">EdgarTools</a>
To create the 10-K and 10-Q embeddings to add to Pinecone, the edgartools package in Python is required to download the reports. An identity needs to be set, so add your name and email to the backend [.env.example](https://github.com/Chubbyman2/investment-tracker/blob/main/.env.example).

### <a href="https://github.com/CharlesYuan02/portfolio.io/blob/main/frontend/package.json">React Prerequisites</a>
```
"@auth0/auth0-react": "^2.2.4",
"@supabase/supabase-js": "^2.45.2",
"@testing-library/jest-dom": "^5.17.0",
"@testing-library/react": "^13.4.0",
"@testing-library/user-event": "^13.5.0",
"lucide-react": "^0.439.0",
"react": "^18.3.1",
"react-datepicker": "^7.3.0",
"react-dom": "^18.3.1",
"react-router-dom": "^6.26.1",
"react-scripts": "5.0.1",
"recharts": "^2.12.7",
"web-vitals": "^2.1.4"
```

### <a href="https://github.com/CharlesYuan02/portfolio.io/blob/main/requirements.txt">Python Prerequisites</a>
```
edgartools==2.22.1
langchain==0.1.20
langchain-pinecone==0.1.1
langchain-openai==0.1.7
openai==1.30.1
python-dotenv==1.0.1
supabase==2.5.1
yfinance==0.2.12
```

### Launching the App
Once you have done all this, you can finally launch the app! Make sure to run <a href="https://github.com/CharlesYuan02/portfolio.io/blob/main/backend/rag/embed.py">embed.py</a> if you want the chatbot feature to work. Otherwise:
```
cd frontend
npm run build
cd ..
python manage.py runserver
```

## Other Technologies and Packages
### React
React was chosen as the frontend Javascript framework. Along with rendering the site's pages and components, Axios was also used to make calls to the backend.

### Django
Django was used as the backend for creating endpoints. I'd like to add more to the app in the future to fully leverage Django's capabilities, and maybe move some of the calls to Supabase from the React frontend.

### Recharts
Recharts was used to easily add React components displaying the line graph of performance and the pie chart for portfolio composition.

### yfinance
yfinance was used to retrieve historical stock information.

## Demo
<img src="https://github.com/Chubbyman2/portfolio.io/blob/main/docs/dashboard.PNG"> 
<img src="https://github.com/Chubbyman2/portfolio.io/blob/main/docs/dashboard-2.PNG"> 

## Acknowledgements
The AI Stock Insights feature was based on the [Mango10K RAG chatbot](https://github.com/Chubbyman2/Mango10K) built by my team, [Mango10K](https://www.linkedin.com/posts/daniel-chen297_on-april-6th-we-created-mango10k-at-activity-7184621025626615808-aZ97?utm_source=share&utm_medium=member_desktop), for MongoDB's 2024 GenAI Hackathon. I swapped out MongoDB in favor of Pinecone's increased storage (0.5GB vs 2GB), though the scripts can be easily modified to be used with either.

## License
This project is licensed under the MIT License - see the <a href="https://github.com/Chubbyman2/investment-tracker/blob/main/LICENSE">LICENSE</a> file for details.
