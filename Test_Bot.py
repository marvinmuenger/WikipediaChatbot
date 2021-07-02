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

#Scrape The Wikipedia Pages
article = Article('https://en.wikipedia.org/wiki/Bühler_Group')
article.download()
article.parse()
article.nlp()
article2 = Article('https://en.wikipedia.org/wiki/Python_(programming_language)')
article2.download()
article2.parse()
article2.nlp()
corpus = article.text 
corpus2 = article2.text


#Tokenization
text_buhler = corpus
sentence_list_buhler = nltk.sent_tokenize(text_buhler) #Create list of sentences
text_python = corpus2
sentence_list_python = nltk.sent_tokenize(text_python)


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
    sentence_list_buhler.append(user_input)
    sentence_list_python.append(user_input)
    bot_response = ''
    cm_buhler = CountVectorizer().fit_transform(sentence_list_buhler)
    cm_python = CountVectorizer().fit_transform(sentence_list_python)
    similarity_scores_buhler = cosine_similarity(cm_buhler[-1], cm_buhler)
    similarity_scores_list_buhler = similarity_scores_buhler.flatten()
    similarity_scores_python = cosine_similarity(cm_python[-1], cm_python)
    similarity_scores_list_python = similarity_scores_python.flatten()
    index_buhler = index_sort(similarity_scores_list_buhler)
    index_buhler = index_buhler[1:]
    index_python = index_sort(similarity_scores_list_python)
    index_python = index_python[1:]
    response_flag = 0

    j = 0
    if similarity_scores_list_buhler[index_buhler[0]] > similarity_scores_list_python[index_python[0]]:
        for i in range(len(index_buhler)):
            if similarity_scores_list_buhler[index_buhler[i]] > 0.0:
                bot_response = 'Bühler Bot: '+ sentence_list_buhler[index_buhler[i]]
                response_flag = 1
                j = j+1
            if j > 2:
                break
        
            if response_flag == 0:
                bot_response = "I apologize, I don't understand."
            
            sentence_list_python.remove(user_input)
            sentence_list_buhler.remove(user_input)
            return bot_response
    else:
        for i in range(len(index_python)):
            if similarity_scores_list_python[index_python[i]] > 0.0:
                bot_response = 'Python Bot: '+ sentence_list_python[index_python[i]]
                response_flag = 1
                j = j+1
            if j > 2:
                break
        
            if response_flag == 0:
                bot_response = bot_response+' '+"I apologize, I don't understand."
            sentence_list_python.remove(user_input)
            sentence_list_buhler.remove(user_input)
            return bot_response

#Start the chat
print('Test Bot: Hi I am a Test Bot. Ask me anything about Bühler or Python.') 

exit_list = ['exit', 'see you later', 'bye', 'quit', 'break', 'stop']


while(True):
    user_input = input()
    if user_input.lower() in exit_list:
        print('Test Bot: Chat with you later!')
        break
    else:
        if greeting_response(user_input) != None:
            print(greeting_response(user_input))
        else:
            print(bot_response(user_input))

    
