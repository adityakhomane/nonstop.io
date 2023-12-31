import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Define the news website URL and classification sections
website_url = "https://www.nytimes.com/"
classification_sections = ["World", "Business", "Technology", "Science", "Health"]

# Initialize an empty list to store scraped articles
scraped_articles = []

# Scrape news articles from the website
def scrape_articles():
    # Send a GET request to the website
    response = requests.get(website_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all news articles
        articles = soup.find_all("article")

        # Extract the title, section, and content for each article
        for article in articles:
            title = article.find("h2").text
            section = article.find("span", {"class": "section"}).text
            content = article.find("div", {"class": "story-body-section"}).text

            # Store the scraped article data
            scraped_articles.append({
                "title": title,
                "section": section,
                "content": content
            })

# Scrape the news articles
scrape_articles()

# Prepare the training and testing data
X_train = []
y_train = []
X_test = []
y_test = []

# Split the scraped articles into training and testing sets
for article in scraped_articles:
    if len(X_train) < 80:
        X_train.append(article["content"])
        y_train.append(article["section"])
    else:
        X_test.append(article["content"])
        y_test.append(article["section"])

# Vectorize the text data using TF-IDF
vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train a Naive Bayes classifier
classifier = MultinomialNB()
classifier.fit(X_train_vec, y_train)

# Evaluate the classifier on the test set
y_pred = classifier.predict(X_test_vec)

# Calculate the accuracy of the classifier
accuracy = classifier.score(X_test_vec, y_test)

# Print the accuracy score
print("Accuracy:", accuracy)

# Generate a CSV/Excel report of the test evaluation
import pandas as pd

df = pd.DataFrame({
    "Actual Section": y_test,
    "Predicted Section": y_pred
})

df.to_csv("test_evaluation.csv", index=False)
