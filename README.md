# Smart Email Assistant
A Python automation project that fetches your emails, intelligently categorizes them, and generates suggested replies. Includes a Streamlit dashboard to visualize email trends, top senders, and draft responses.
Built to demonstrate automation, NLP, and productivity-enhancing solutions which is perfect for showing technical and practical skills in data and workflow improvement.

I built this Smart Email Assistant because I receive a large number of emails weeekly, and it gets boring. I was also curious to see analytics related to my emails.

Inspired by *Automate the Boring Stuff with Python*, I wanted to automate a real, personal workflow:

- Automatically fetch emails
- Categorize emails intelligently
- Generate draft replies
- Gain insights from my inbox

## Features

This Smart Email Assistant automates key parts of email management:

- **Fetch Emails**  
  Connect to Gmail via IMAP to automatically pull emails.  
  - Supports fetching by date
  - Stores emails locally in a SQLite database  

- **Smart Categorization**  
  - Keyword-based and NLP-powered categorization  
  - Automatically classifies emails into categories like:
    - Meetings
    - Requests
    - Follow-ups
    - Newsletters 
  - Reduces “Other” emails, making it easier to focus on important messages  

- **Draft Replies**  
  - Automatically generates suggested replies for each category such as: propose meeting times, acknowledge requests, respond to follow-ups  

- **Insights Dashboard using Streamlit**  
  - Visualises email trends and category breakdowns  
  - Shows top senders and most frequent email types  
  - Preview auto-generated draft replies  

## Project Structure
- **scripts/**: contains all Python scripts for fetching, categorising, and drafting replies  
- **dashboard/**: Streamlit app to visualise email trends and suggestions  
- **data/**: stores the local database of emails (kept out of GitHub via `.gitignore`)  
- **.env**: contains sensitive email credentials, never pushed to GitHub

 ## Tech Stack / Tools Used

- **Python** – core programming language for all automation and scripting  
- **imaplib / email** – fetch emails from Gmail/Outlook  
- **SQLite** – local database to store fetched emails  
- **pandas** – data processing and manipulation  
- **spaCy** – natural language processing for smarter email categorisation  
- **Streamlit** – interactive dashboard for visualising email trends and draft replies  
- **dotenv (python-dotenv)** – securely load email credentials from `.env`  

## Lessons Learned

I enjoyed working on this project, though  I encountered bugs which I fixed and hence learn some lessons:
- **IMAP challenges**: Encountered authentication and connection errors with Gmail, which reinforced careful handling of email protocols and app passwords.  
- **Database structure matters**: Initially had mismatched columns in SQLite; fixing this improved data consistency and reduced runtime errors.  
- **Email text processing**: Learned how to handle multipart emails, decode headers, and work with messy real-world text.  
- **NLP for practical automation**: Simple keyword-based categorisation worked initially, but integrating spaCy made the assistant smarter and more accurate.  
- **Debugging in stages**: Running small test scripts before full automation helped identify issues early, such as first testing IMAP connection before fetching thousands of emails.  


## Next Steps
-  Schedule the assistant to run daily using Task Scheduler for Windows.  
- Improve categorisation with advanced NLP or ML models.  
- Enhance draft replies to be context-aware.  
- Upgrade the Streamlit dashboard with interactive charts and better visuals.

## Getting Started — Run It With Your Own Inbox
Follow these steps to set up and run the Smart Email Assistant on your own machine.

### Prerequisites
- Python 3.8 or higher
- A Gmail account with 2-Factor Authentication enabled

### Installation

1. Clone the repository:
```bash
git clone https://github.com/ashiorkornortey/smart-email-assistant.git
cd smart-email-assistant
```

2. Install dependencies:
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

3. Create a `.env` file in the root directory with your email credentials:
```
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
IMAP_SERVER=imap.gmail.com
```

> **Important:** Do not use your regular Gmail password. You need to generate an App Password.

### How to Generate a Gmail App Password

1. Go to your [Google Account Security Settings](https://myaccount.google.com/security)
2. Make sure 2-Step Verification is turned on
3. Go to [App Passwords](https://myaccount.google.com/apppasswords)
4. Select **Mail** as the app and generate a password
5. Copy the generated password into your `.env` file as `EMAIL_PASSWORD`

### Running the Project

Fetch your emails:
```bash
python scripts/fetch_emails.py
```

Categorize the fetched emails:
```bash
python scripts/categorize_emails.py
```

Generate draft replies:
```bash
python scripts/draft_replies.py
```

Launch the Streamlit dashboard:
```bash
streamlit run dashboard/app.py
```

### Notes
- Your email credentials are stored locally in `.env` and are never pushed to GitHub
- Emails are stored in a local SQLite database in the `data/` folder
- The database is created automatically on first run
- This project currently supports Gmail. For Outlook or other providers, update the `IMAP_SERVER` in your `.env` file (e.g., `imap-mail.outlook.com` for Outlook)



