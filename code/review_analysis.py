import config
from dataclasses import dataclass
from sentiment_analysis import SentimentAnalyzer

github_key = config.GITHUB_KEY

@dataclass        
class DevSentiments:
    name: str
    total_sentiment_score: float = 0.0
    num_of_contributed_prs: int = 0

    def __init__(self, name) -> None:
        self.name = name

    def add_score(self, score) -> None:
        self.num_of_contributed_prs += 1
        self.total_sentiment_score += score
    
    def get_sentiment_score(self) -> float:
        if self.num_of_contributed_prs == 0:
            return 0.0
        return self.total_sentiment_score / self.num_of_contributed_prs

@dataclass 
class SentimentalAnalysis:
    dev_dict: dict[str, DevSentiments]

    def __init__(self,pr_reviews_dict) -> None:
        self.dev_dict = {}
        pr_sentiments= SentimentalAnalysis.analyze_sentiments(pr_reviews_dict)
        self.credit_pr_commiters(pr_sentiments, pr_reviews_dict)

    def add_developer_score(self, score: float, dev_name: str) -> None:
        if dev_name in self.dev_dict:
            self.dev_dict[dev_name].add_score(score)
        else:
            new_developer = DevSentiments(name=dev_name)
            new_developer.add_score(score)
            self.dev_dict[dev_name] = new_developer

    def credit_pr_commiters(self, pr_sentiments, pr_reviews_dict):
        for pr_no, score in pr_sentiments.items():
            if pr_no in pr_reviews_dict:
                committers = set(pr_reviews_dict[pr_no]['commits'])  # Use a set to avoid duplicate committers
                for committer in committers:
                    self.add_developer_score(score, committer)

    def __str__(self) -> str:
        developers_summary = []
        for dev_name, developer in self.dev_dict.items():
            developers_summary.append(f"{dev_name}: Sentiment Score = {developer.get_sentiment_score():.2f}, PRs Contributed = {developer.num_of_contributed_prs}")
        return "\n".join(developers_summary)

    def analyze_sentiments(pr_reviews_dict) -> dict[int, float]:
        '''
        Returns a dictionary for PR review sentiment scores: dict[pr_number, average_score]
        '''
        analyzer = SentimentAnalyzer()
        # Stores, for a PR -> (total PR score, number of reviews/comments)
        sentiment_dict: dict[int, (float, int)] = {}

        for pr_number, pr_details in pr_reviews_dict.items():
            total_score = 0.0
            count = 0

            for review in pr_details['reviews']:
                if review["text"] != "":
                    score = analyzer.get_sentiment(review['text'])
                    total_score += score
                    count += 1

            for comment in pr_details['comments']:
                if comment["text"] != "":
                    score = analyzer.get_sentiment(comment['text'])
                    total_score += score
                    count += 1

            sentiment_dict[pr_number] = (total_score, count)

        # Calculate the average score for each PR, ensuring not to divide by zero
        return {pr_no: pr_score / num_prs if num_prs != 0 else 0 for pr_no, (pr_score, num_prs) in sentiment_dict.items()}




if __name__ == "__main__":
    repo_url = "https://github.com/bumptech/glide"

    fetcher= GitHubFetcher(github_key, repo_url)


    reviews = fetcher.pr_reviews()

    dev_sentiments= SentimentalAnalysis(reviews)

    print(dev_sentiments)
    # TODO should we account for comments of contributors?



