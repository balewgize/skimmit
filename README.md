<br />
<div align="center">
  <h3 align="center">Skimmit</h3>
  <p align="center">
    Article and YouTube video summary from URL, powered by GPT-4 & Gemini Pro
    <br />
    <a href="https://balewgize.app/summarize">View Demo</a>
  </p>
</div>


Skimmit is now available on <a href="https://chat.openai.com/g/g-uNZCnqgvX-skimmit"> *GPT Store* </a>


## About The Project

The main goal of this project is to make content consumption effective. How?

- Quickly get the main idea of any article or video.
- See a short preview to asses if it's worth your time.
- Spend less time consuming, and more time doing.

<br />

### Why Skimmit?

I believe content is being consumed more than ever. So it's important to be selective and make the most of it. 

If you want to give a try, check out the web version at <a href="https://balewgize.app/">https://balewgize.app/</a>


<!-- What tech stack you use to develop the project? -->
### Built With

* Python
* Flask
* LLM (GPT-4 & Gemini Pro)



## Getting Started

To get a local copy up and running follow these example steps.


<!-- List prerequisites to use this project (if any) -->
### Prerequisites

* Python installed
* Gemini Pro API key

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
3. Provide Gemini API key in `.env` file
   ```
   GOOGLE_API_KEY=your-google-gemini-api-key
   ```

4. Start the server.
   ```
   flask run
   ```
5. Goto http://127.0.0.1:5000 on your browser

<br />
Thanks for checking!