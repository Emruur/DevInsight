from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

class SentimentAnalyzer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()


    def get_sentiment(self,text:str)->float:
        '''
        score= [-1 really negative: 1:really positive]
        '''
        if not text:  # Check if the text is empty
            return None
        text= SentimentAnalyzer.preprocess_text(text)
        scores = self.analyzer.polarity_scores(text)
        compound_score = scores['compound']

        return compound_score


    # create preprocess_text function
    def preprocess_text(text:str):

        # Tokenize the text
        if(type(text) == float):
            text = ''

        tokens = word_tokenize(text.lower())
        filtered_tokens = [token for token in tokens if token not in stopwords.words('english')]
        # Lemmatize the tokens

        lemmatizer = WordNetLemmatizer()

        lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]

        # Join the tokens back into a string

        processed_text = ' '.join(lemmatized_tokens)
        return processed_text





analyzer= SentimentAnalyzer()

print(f"Ultra Positive: {analyzer.get_sentiment('This is really good, nice job, amazing, the best thing i have ever seen!')}")
print(f"Positive: {analyzer.get_sentiment('This is really good, nice job!')}")
print(f"Good: {analyzer.get_sentiment('Looks good thanks!')}")
print(f"Neutral: {analyzer.get_sentiment('This is a automatic response.')}")
print(f"Negativish: {analyzer.get_sentiment('Please run gradlew check locally, there seems to be some violation; probably a long line.')}")
print(f"Negativish: {analyzer.get_sentiment('This sucks, really bad pr, shame on you')}")
