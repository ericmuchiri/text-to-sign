import json

import nltk
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.staticfiles import finders
from django.views.decorators.csrf import csrf_exempt
from nltk import word_tokenize, WordNetLemmatizer

from convert import keyword_list
from convert.models import Conversion
import os.path


@csrf_exempt
def animation_view(request):
    if request.method == 'POST':
        text = request.POST.get('sen')
        # capitalize every word
        text = text.title()
        conversion = Conversion()
        # conversion.user = request.user
        conversion.search_text = text
        conversion.save()

        # tokenizing the sentence
        text.lower()
        # tokenizing the sentence
        words = word_tokenize(text)

        tagged = nltk.pos_tag(words)
        tense = {}
        tense["future"] = len([word for word in tagged if word[1] == "MD"])
        tense["present"] = len([word for word in tagged if word[1] in ["VBP", "VBZ", "VBG"]])
        tense["past"] = len([word for word in tagged if word[1] in ["VBD", "VBN"]])
        tense["present_continuous"] = len([word for word in tagged if word[1] in ["VBG"]])

        # stopwords that will be removed
        stop_words = set(
            ["mightn't", 're', 'wasn', 'wouldn', 'be', 'has', 'that', 'does', 'shouldn', 'do', "you've", 'off', 'for',
             "didn't", 'm', 'ain', 'haven', "weren't", 'are', "she's", "wasn't", 'its', "haven't", "wouldn't", 'don',
             'weren', 's', "you'd", "don't", 'doesn', "hadn't", 'is', 'was', "that'll", "should've", 'a', 'then', 'the',
             'mustn', 'i', 'nor', 'as', "it's", "needn't", 'd', 'am', 'have', 'hasn', 'o', "aren't", "you'll",
             "couldn't", "you're", "mustn't", 'didn', "doesn't", 'll', 'an', 'hadn', 'whom', 'y', "hasn't", 'itself',
             'couldn', 'needn', "shan't", 'isn', 'been', 'such', 'shan', "shouldn't", 'aren', 'being', 'were', 'did',
             'ma', 't', 'having', 'mightn', 've', "isn't", "won't"])

        # removing stopwords and applying lemmatizing nlp process to words
        lr = WordNetLemmatizer()
        filtered_text = []
        for w, p in zip(words, tagged):
            if w not in stop_words:
                if p[1] == 'VBG' or p[1] == 'VBD' or p[1] == 'VBZ' or p[1] == 'VBN' or p[1] == 'NN':
                    filtered_text.append(lr.lemmatize(w, pos='v'))
                elif p[1] == 'JJ' or p[1] == 'JJR' or p[1] == 'JJS' or p[1] == 'RBR' or p[1] == 'RBS':
                    filtered_text.append(lr.lemmatize(w, pos='a'))

                else:
                    filtered_text.append(lr.lemmatize(w))

        # adding the specific word to specify tense
        print("filtered")
        print(filtered_text)
        # defined_words = []
        # for word in filtered_text:
        #     file_name = word.capitalize() + ".mp4"
        #     print(file_name)
        #     if os.path.exists('static/media/' + file_name):
        #         defined_words.append(file_name)
        #     else:
        #         print("path does not exist")

        words = filtered_text
        temp = []
        for w in words:
            if w == 'I':
                temp.append('Me')
            else:
                temp.append(w)
        words = temp
        probable_tense = max(tense, key=tense.get)

        if probable_tense == "past" and tense["past"] >= 1:
            temp = ["Before"]
            temp = temp + words
            words = temp
        elif probable_tense == "future" and tense["future"] >= 1:
            if "Will" not in words:
                temp = ["Will"]
                temp = temp + words
                words = temp
            else:
                pass
        elif probable_tense == "present":
            if tense["present_continuous"] >= 1:
                temp = ["Now"]
                temp = temp + words
                words = temp

        filtered_text = []
        for word in words:
            print(word)
            upperW = word.capitalize()
            print(word)
            path = word + ".mp4"
            file_name = word.capitalize() + ".mp4"
            print(file_name)
            if os.path.exists('static/media/' + file_name):
                # otherwise animation of word
                filtered_text.append(word.capitalize())
            else:
                # other wise letters
                for c in word:
                    filtered_text.append(c.capitalize())
        words = filtered_text
        print(filtered_text)
        return HttpResponse(json.dumps(filtered_text))

    else:

        path = "static/image-sign/"  # insert the path to your directory
        img_list = os.listdir(path)
        print(img_list)

    return render(request, 'animation.html', {'keywords': keyword_list.get_list(), 'img_list': img_list})
