# portfolio.io
<img src="https://github.com/Chubbyman2/portfolio.io/blob/main/docs/demo-1.PNG"> 

## Introduction
Have you ever wanted to showcase your portfolio and its performance to your friends? What about discovering new portfolio strategies from others? Well then, portfolio.io is the platform for you! Introducing a new place to share your investment portfolio with your friends, test new strategies, and gain new insights through the power of LLM retrieval-augmented generation!

## Getting Started
To get started, you'll need a [Supabase](https://supabase.com/) account and a table. See [.env.example](https://github.com/Chubbyman2/investment-tracker/blob/main/.env.example) for more details. Make sure to either disable RLS (not recommended) or [add a new policy](https://stackoverflow.com/questions/74302341/supabase-bucket-new-row-violates-row-level-security-policy-for-table-objects)!

You'll also need a [MongoDB](https://www.mongodb.com/) account with a collection, and then [set up your vector index](https://www.mongodb.com/docs/atlas/atlas-vector-search/create-index/) (see [vector_index.json](https://github.com/Chubbyman2/portfolio.io/blob/main/vector_index.json)). This will be used for the RAG chatbot feature.

### Prerequisites
```
edgartools==2.22.1
langchain==0.1.20
langchain-mongodb==0.1.5
langchain-openai==0.1.7
openai==1.30.1
plotly==5.20.0
pymongo==4.6.3
python-dotenv==1.0.1
streamlit==1.33.0
st_pages==0.4.5
supabase==1.0.3
yfinance==0.2.12
```

## Technologies and Packages
### Streamlit
Streamlit was used to create the web app frontend and UI.

### Supabase
Supabase was used to store the information for each user (emails, passwords, portfolio details, etc), in order to display analytics regarding portfolio performances. 

### yfinance
yfinance was used to retrieve historical stock information.

### edgartools
edgartools was the package used to retrieve EDGAR filings, specifically listed company 10-K's and 10-Q's, to embed within MongoDB Atlas Vector Store.

### MongoDB
MongoDB was used to store the vector embeddings, as well as create the index for vector search.

### LangChain
LangChain was used to actually perform the embedding and vector search within the code. 

### OpenAI
OpenAI's embedding model (text-embedding-ada-002) and the LLM for retrieval Q&A (text-davinci-003) were integrated with LangChain to power the AI Stock Insights feature.

## To Do
- Create friends feature, where you can view your friends' portfolio performances
- Create better frontend and improve UI

## Acknowledgements
The AI Stock Insights feature was based on the [Mango10K RAG chatbot](https://github.com/Chubbyman2/Mango10K) built by my team, [Mango10K](https://www.linkedin.com/posts/daniel-chen297_on-april-6th-we-created-mango10k-at-activity-7184621025626615808-aZ97?utm_source=share&utm_medium=member_desktop), for MongoDB's 2024 GenAI Hackathon.

<img src="https://github.com/Chubbyman2/portfolio.io/blob/main/docs/demo-2.PNG"> 

## License
This project is licensed under the MIT License - see the <a href="https://github.com/Chubbyman2/investment-tracker/blob/main/LICENSE">LICENSE</a> file for details.
