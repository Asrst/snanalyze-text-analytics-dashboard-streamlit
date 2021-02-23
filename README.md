
## SnAnalyze : What it does
SnAnalyzer helps brands & marketers to analyze various social networks to get how users are reacting to their brand in a click of button. The App collects the data from various social networks (twitter, google news) based on keywords or hashtags. Then Expert AI API is being used to Analyze the text data collected and will show the overall results in a simple dashboard.  Brands/Marketers/Support teams can use this to know where they are going wrong, there by making impactful decisions.

**Why social networks ?**

Being one of most powerful source of content, users and enthusiasts take several social networks  to express their feeling or sentiment regarding the newly launched items by several brands on their product/brand pages.

**Why also Google news ?**

Being one of the largest news aggregators, brands will be able to find how media is portraying them with details topics being written on them, sentiment & entities mentioned.

The diagram below shows the flow of the application:

![SnAnalyzer - Flow](https://challengepost-s3-challengepost.netdna-ssl.com/photos/production/software_photos/001/408/425/datas/gallery.jpg)


## Features:

**update** : Added support to search with max date.

**Data Sources: **
- Twitter
- Google News

**Dashboard:**
- Number/Count of Articles by sentiment
- Distribution of Sentiment scores
- Word Clouds By Sentiment
- Entities By Sentiment
- Similar Concepts By Sentiment
- Topics By Sentiment
- Raw Data


## Instructions to Run

1. Install requirements.txt
    - `pip install -r requirements.txt`

    if pattern failed to install, then run
    - `pip install git+https://github.com/uob-vil/pattern.git`

2. Set Expert.ai Auth as Environment variables or Use .env file

    For expert.ai acccount, register @ https://developer.expert.ai/ui/login

    - `export EAI_USERNAME="uuuu@email.com"`
    - `export EAI_PASSWORD="pppp"`

3. Run the streamlit app
    - `streamlit run app.py`


### How I built it & Challenges

I started off by installing expert.ai python client and writing code for various text analysis to get topics, entities & sentiment for given piece of text. Next, I started search for various APIs for collecting the social network data. Next, I started researching on frontend frameworks to create easy dashbaords and found it to be Streamlit. Finally, I integrated all these three to make SnAnalyzer

- I ran into errors using expert.ai python client - 500 Response Error. But I resolved it by proper preprocessing of the text like emojis & Unicode texts. I guess expert.ai is not able to handle them at this point of time.
- Scraping data from social media is difficult on long term & as use dynamic websites which might change with time.

for other details: https://devpost.com/software/snanalyze-social-network-intelligence-for-brands
