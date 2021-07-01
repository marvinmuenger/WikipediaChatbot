from newspaper import Article
import random
import string
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import warnings
warnings.filterwarnings('ignore')

nltk.download('punkt', quiet=True)

#Get The Article
article = Article('https://en.wikipedia.org/wiki/Bühler_Group')
article.download()
article.parse()
article.nlp()
article2 = Article('https://docs.python.org/3/faq/general.html')
article2.download()
article2.parse()
article2.nlp()
corpus = article.text + article2.text

#Print Article
#print(corpus)


#Tokenization
text = corpus
sentence_list = nltk.sent_tokenize(text) #Create list of sentences

#Print List Of Sentences
#print(sentence_list)

#Random Greeting Response Function
def greeting_response(text):
    text = text.lower()

    #Bots greeting response
    bot_greetings = ['Howdy!', 'Hi!', 'Hello!', 'Greetings!']

    #User greeting
    user_greetings = ['hi', 'hey', 'hello', 'greetings', 'wassup']

    for word in text.split():
        if word in user_greetings:
            return random.choice(bot_greetings)


def index_sort(list_var):
    length = len(list_var)
    list_index = list(range(0, length))

    x = list_var
    for i in range(length):
        for j in range(length):
            if x[list_index[i]] > x[list_index[j]]:
                #Swap
                list_index[i], list_index[j]  = list_index[j], list_index[i]

    return list_index

#Bots Response
def bot_response(user_input):
    user_input = user_input.lower()
    sentence_list.append(user_input)
    bot_response = ''
    cm = CountVectorizer().fit_transform(sentence_list)
    similarity_scores = cosine_similarity(cm[-1], cm)
    similarity_scores_list = similarity_scores.flatten()
    index = index_sort(similarity_scores_list)
    index = index[1:]
    response_flag = 0

    j = 0
    for i in range(len(index)):
        if similarity_scores_list[index[i]] > 0.0:
            print(similarity_scores_list[index[i]])
            bot_response = bot_response+' '+sentence_list[index[i]]
            response_flag = 1
            j = j+1
        if j > 2:
            break

        if response_flag == 0:
            bot_response = bot_response+' '+"I apologize, I don't understand."
        sentence_list.remove(user_input)

        return bot_response

#Start the chat
print('Test Bot: Hi I am a Test Bot. Ask me anything about Bühler.') 

exit_list = ['exit', 'see you later', 'bye', 'quit', 'break', 'stop']


while(True):
    user_input = input()
    if user_input.lower() in exit_list:
        print('Test Bot: Chat with you later!')
        break
    else:
        if greeting_response(user_input) != None:
            print('Test Bot: '+greeting_response(user_input))
        else:
            print('Test Bot: '+bot_response(user_input))

            




 

    
    