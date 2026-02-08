from textblob import TextBlob
def sentiment_score(news):
 s=0
 for n in news:
  p=TextBlob(n).sentiment.polarity
  if p>0.1: s+=1
  elif p<-0.1: s-=1
 return s
