import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from wordcloud import WordCloud, STOPWORDS
from helpers import fetch_and_analyze
from collections import Counter
from itertools import chain
from datetime import date
import re

st.title("Dashboard - Social Network Intelligence")
st.sidebar.title("SnAnalyze - Text Analytics")

data_df = pd.DataFrame()
### Search and Analayze ###
st.sidebar.subheader('Search Keywords')
# website source
source_selected = st.sidebar.selectbox('Source', ['Twitter', 'News', 'Facebook'], key='1')
# date input
date_until = st.sidebar.date_input('Date Until:', max_value = date.today())
# Get user input
query = st.sidebar.text_input('Query:', '#')
# submit button
if st.sidebar.button('Submit') or len(query) > 1:
    with st.spinner(f'Searching and Analyzing for {query} ...'):
        data_df = fetch_and_analyze(query, source_selected, date_until)

wdf = data_df.copy()

# bar plot of sentiments
if len(wdf):
    sent_df = wdf['sentiment'].value_counts().to_frame().reset_index()
    sent_df.columns = ['sentiment_type', 'count']
    st.markdown("### Number of texts by sentiment")
    fig = px.bar(sent_df, x='sentiment_type', y='count', 
                        color='sentiment_type', text='count')
    st.plotly_chart(fig)
    st.markdown("### Distrubution of sentiment scores")
    hist = px.histogram(wdf, x="sentiment_score", color="sentiment", nbins=9)
    st.plotly_chart(hist)



# draw word clouds for all sentiments
world_clouds_exp = st.beta_expander('Word Clouds By Sentiment')
if len(wdf):
    with world_clouds_exp:
        word_sentiment = st.selectbox('Sentiment Type', 
                        ['positive', 'neutral', 'negative'], key='1')
        wcdf = wdf[wdf['sentiment']==word_sentiment].copy()
        words = ' '.join(wcdf['text'])
        wc_words = ' '.join([w for w in words.split() if not w.startswith('@') and w != 'RT'])

        if len(wc_words):
            st.markdown('#### Word cloud for %s sentiment' % (word_sentiment))
            wc = WordCloud(stopwords=STOPWORDS, background_color='white', width=768, height=480)
            fig = plt.figure()
            plt.imshow(wc.generate(wc_words))
            plt.xticks([])
            plt.yticks([])
            st.pyplot(fig)
        else:
            st.markdown("#### No Words to Plot.")
            st.write('\n\n\n')


## show ent types (bar) by sentiment
ent_exp = st.beta_expander('Entities By Sentiment')
if len(wdf):
    with ent_exp:
        ent_sentiment = st.selectbox('Sentiment Type', 
                        ['positive', 'neutral', 'negative'], key='3')
        etdf = wdf[wdf['sentiment']==ent_sentiment].copy()
        ent_list = [c for clist in etdf['entities'].tolist() for c in clist]
        ent_counts = Counter([t[0] for t in ent_list])
        etdf = pd.DataFrame.from_dict(ent_counts, orient='index').reset_index()
        etdf.columns = ['entity', 'count']
        etdf.sort_values(by = ['count'], inplace = True, ascending = False)
        st.markdown('#### Top Entities for %s sentiment' % (ent_sentiment))
        st.markdown('Entity Types, refer:https://docs.expert.ai/nlapi/v1/reference/entity-types/')
        fig = px.bar(etdf.head(10), x='entity', y='count', color='entity', text='count')
        st.plotly_chart(fig)


## show syncons (bar) by sentiment
syn_exp = st.beta_expander('Similar Concepts By Sentiment')
if len(wdf):
    with syn_exp:
        syn_sentiment = st.selectbox('Sentiment Type', 
                        ['positive', 'neutral', 'negative'], key='4')
        sydf = wdf[wdf['sentiment']==syn_sentiment].copy()
        syn_list = [c for clist in sydf['syncons'].tolist() for c in clist]
        syn_counts = Counter([t[0] for t in syn_list])
        sydf = pd.DataFrame.from_dict(syn_counts, orient='index').reset_index()
        sydf.columns = ['syncon', 'count']
        sydf.sort_values(by = ['count'], inplace = True, ascending = False)
        st.markdown('#### Top SynCons for %s sentiment' % (syn_sentiment))
        fig = px.bar(sydf.head(10), x='syncon', y='count', color='syncon', text='count')
        st.plotly_chart(fig)


## show topics (bar) by sentiment
topics_exp = st.beta_expander('Topics By Sentiment')
if len(wdf):
    with topics_exp:
        topic_sentiment = st.selectbox('Sentiment Type', 
                        ['positive', 'neutral', 'negative'], key='2')
        wcdf = wdf[wdf['sentiment']==topic_sentiment].copy()
        topics_list = [c for clist in wcdf['topics'].tolist() for c in clist]
        topics_counts = Counter([t[0] for t in topics_list])
        tdf = pd.DataFrame.from_dict(topics_counts, orient='index').reset_index()
        tdf.columns = ['topic', 'count']
        tdf.sort_values(by = ['count'], inplace = True, ascending = False)
        st.markdown('#### Top Topics for %s sentiment' % (topic_sentiment))
        fig = px.bar(tdf.head(10), x='topic', y='count', color='topic', text='count')
        st.plotly_chart(fig)


## show the raw data
raw_data = st.beta_expander('Raw Data')
if len(wdf):
    with raw_data:
        st.table(wdf[['text', 'shares', 'sentiment_score']])
        
