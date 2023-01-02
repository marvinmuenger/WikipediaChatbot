import re
import random
import nltk
import warnings
from contextlib import suppress
from newspaper import Article
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt', quiet=True)

def download_and_parse_articles(urls):
    """
    Downloads and parses the articles at the given URLs.

    Parameters:
    - urls: A list of URLs of Wikipedia articles.

    Returns:
    - A list of tuples, where each tuple contains the title of an article and its parsed text.
    """
    articles = []

    for url in urls:
        article = Article(url)
        with suppress(Exception):
            article.download()
            article.parse()
            article.nlp()
            title = article.title.strip()
            # Replace underscores with spaces and remove leading/trailing whitespace
            title = title.replace('_', ' ').strip()
            articles.append((title, article.text))

    return articles

def greeting_response(text):
    """
    Generates a greeting response for the given text.

    Parameters:
    - text: A string containing a greeting.

    Returns:
    - A string containing a greeting response.
    """
    text = text.lower()
    greeting_pattern = r'\b(hi|hey|hello|greetings|wassup)\b'

    if re.search(greeting_pattern, text):
        bot_greetings = ['Howdy!', 'Hi!', 'Hello!', 'Greetings!']
        return random.choice(bot_greetings)

def index_sort(list_var):
    """
    Sorts the indices of a list in ascending order of their corresponding values.

    Parameters:
    - list_var: A list of values.

    Returns:
    - A list of integers representing the indices of the list in sorted order.
    """
    length = len(list_var)
    list_index = list(range(0, length))

    x = list_var
    for i in range(length):
        for j in range(length):
            if x[list_index[i]] > x[list_index[j]]:
                # Swap
                list_index[i], list_index[j] = list_index[j], list_index[i]

    return list_index

def bot_response(user_input, articles):
    """
    Generates a response for the given user input based on the parsed texts of the given articles.

    Parameters:
    - user_input: A string containing the user's input.
    - articles: A list of tuples, where each tuple contains the title of an article and its parsed text.

    Returns:
    - A string containing the bot's response.
    """
    user_input = user_input.lower()
    response_flag = 0
    bot_response = ''
    max_similarity = 0

    for title, text in articles:
        sentence_list = nltk.sent_tokenize(text)
        sentence_list.append(user_input)
        cm = CountVectorizer().fit_transform(sentence_list)
        similarity_scores = cosine_similarity(cm[-1], cm)
        similarity_scores_list = similarity_scores.flatten()
        index = index_sort(similarity_scores_list)
        index = index[1:]
        j = 0
        for i in range(len(index)):
            if similarity_scores_list[index[i]] > max_similarity:
                max_similarity = similarity_scores_list[index[i]]
                best_article = title
                bot_response = f'{title}: {sentence_list[index[i]]}'
                response_flag = 1
                j = j + 1
            if j > 2:
                break

    if response_flag == 0:
        bot_response = "I apologize, I don't understand."

    return bot_response

def main():
    # Suppress warning messages
    warnings.filterwarnings('ignore')

    print('Hello! What topics would you like to know about?')
    print('Enter the name of a Wikipedia article (e.g. "Japan") or a list of articles separated by commas (e.g. "Japan, DevOps").')
    user_input = input('Enter the topics you are interested in: ')
    titles = [t.strip() for t in re.split(r'[,]+', user_input)]
    urls = [f'https://en.wikipedia.org/wiki/{title.replace(" ", "_")}' for title in titles]
    articles = download_and_parse_articles(urls)

    # Tell the user which articles were successfully parsed and thtat the bot is ready to answer questions
    print('I have parsed the following articles:')
    for title in titles:
        print(f'- {title}')

    print('You can ask me questions about these articles.')

    while True:
        user_input = input('Enter your question: ')
        greeting = greeting_response(user_input)
        if greeting:
            print(greeting)
        else:
            print(bot_response(user_input, articles))

if __name__ == '__main__':
    main()

