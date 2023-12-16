<!-- Simple back to top -->
<a name="readme-top"></a>

<br />
<div align="center">
  <h3 align="center">Skimmit</h3>
  <p align="center">
    Article and YouTube video summary from URL, powered by GPT-3.5
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

This will be helpful when there are dozen of articles and videos on the subject you're interested in but not sure which one to pick.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Features: What main functionalities you implemented in the project? -->
### Features

* Article summary from URL
* YouTube video summary from URL
* Uses LLM (GPT-3.5) for summarization 
* Dark/Light theme
* More features to come...


<!-- What tech stack you use to develop the project? -->
### Built With

* Python
* Django
* LLM (GPT-3.5)
* PostgreSQL
* Render

<p align="right">(<a href="#readme-top">back to top</a>)</p>



## Getting Started

To get a local copy up and running follow these example steps.


<!-- List prerequisites to use this project (if any) -->
### Prerequisites

* Python installed
* OpenAI account


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