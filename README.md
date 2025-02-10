# PR_Review_App
This is a GitHub PR(Pull Requests) Review App developed using Langraph for the backend and Streamlit for the Frontend UI.

I've made use of the following in the backend which I've done using Langraph:

1) Groq-- used this AI inference platform's ChatGroq to call Gemma2-9b-It, an AI model running on Groq's infrastructure.
       -- It processes the prompts and returns LLM-generated responses for PR summaries, issues, and comments.

2) Langsmith-- used for logging and monitoring LLM calls for debugging and performance tracking.
3) GitHub Token-- used to authenticate API requests, allowing the app to fetch PR details, access comments, and read repository metadata securely. It ensures higher rate limits and prevents unauthorized access. The token is stored securely using Streamlit's secret management to avoid exposure.

For the frontend UI, I've used Streamlit:

I've done the deployment on Streamlit Cloud.


Streamlit App URL: https://prreviewappgit-yurancpapp9rx7umly2hdur.streamlit.app/

