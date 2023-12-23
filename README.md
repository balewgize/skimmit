<!-- Simple back to top -->
<a name="readme-top"></a>

<br />
<div align="center">
  <h3 align="center">Skimmit</h3>
  <p align="center">
    Article and YouTube video summary from URL, powered by GPT-3.5 & Gemini Pro
    <br />
    <a href="https://skimmit.onrender.com/">View Demo</a>
  </p>
</div>



## About The Project

<!-- Use relative path to reference images you want to use in the README -->
[![Screenshot](static/images/screenshot.png?raw=true "Skimmit")](https://skimmit.onrender.com/)

The main goal of this project is to make content consumption effective. How?

**Time Saver**: Instantly grasp key insights without the need to read the entire article or watch the whole video. 

The AI summaries powered by GPT-3.5 save you valuable time, making information consumption efficient.

**Informed Choices**: Preview articles and videos before committing. Know what's inside and make informed decisions about what to read and watch. 

This will be helpful when there are dozens of articles and videos on the subject you're interested in but not sure which one to pick.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Features: What main functionalities you implemented in the project? -->
### Features

* Article summary from URL
* YouTube video summary from URL
* LLM for summarization: ```GPT-3.5``` & ```Gemini Pro``` 
* User preference: LLM model choice and summary length 
* Bookmark summaries for later reading
* Dark/Light theme

If you don't want to create an account, you can use the following guest credentials.

Email: ```guest@example.com``` <br>
Password: ```welc0me2```

<!-- What tech stack you use to develop the project? -->
### Built With

* Python
* Django
* LLM (GPT-3.5, Gemini Pro)
* Bootstrap
* Render

<p align="right">(<a href="#readme-top">back to top</a>)</p>



## Getting Started

To get a local copy up and running follow these example steps.


<!-- List prerequisites to use this project (if any) -->
### Prerequisites

* Python installed
* OpenAI API key
* Gemini Pro API key
* Email service (or setting up Google app password for your Gmail)

### Installation

1. Clone the repo and navigate to ```skimmit``` directory 
   ```
   git clone https://github.com/balewgize/skimmit.git
   ```
2. Install required packages (virtual environments recommended)
   ```
   python3 -m venv venv && source venv/bin/activate
   ```
   ```
   pip install -r requirements.txt
   ```
3. Provide credentials in .env (example in .env.dev file)
   ```
   DJANGO_SECRET_KEY=
   DJANGO_DEBUG=

   DATABASE_URL= (managed PostgreSQL, optional)

   OPENAI_API_KEY=
   GOOGLE_API_KEY=

   EMAIL_HOST=
   EMAIL_HOST_USER=
   EMAIL_HOST_PASSWORD=
   ```

4. Apply migrations and start the server. The server starts in production settings by default.
   ```
   export DJANGO_SETTINGS_MODULE=config.settings.local
   ```
   ```
   python manage.py migrate
   ```
   ```
   python manage.py runserver
   ```
5. Goto http://127.0.0.1:8000 on your browser

<p align="right">(<a href="#readme-top">back to top</a>)</p>


Thanks!