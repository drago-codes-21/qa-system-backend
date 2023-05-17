import wikipedia
import re
import nltk 
from nltk.tokenize import word_tokenize, sent_tokenize
import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()
root.configure(background="black")
# root.geometry("1300x700")
question = tk.StringVar()

w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.title("Home Page")

image2 = Image.open('img3.jpg')
image2 = image2.resize((w,h), Image.ANTIALIAS)

background_image = ImageTk.PhotoImage(image2)

background_label = tk.Label(root, image=background_image)

background_label.image = background_image

background_label.place(x=0, y=0)  # , relwidth=1, relheight=1)

label_l2 = tk.Label(root, text="___Question Answering System___",font=("times",20, 'bold'),
                    background="black", fg="white", width=50, height=2)
label_l2.place(x=400, y=0)

def wikipedia():
    import wikipedia
    que = question.get()
    print("Question:",que)
    text = wikipedia.search(que)
    text = wikipedia.summary(text)    
    print(text)
    
    def _create_frequency_table(text_string) -> dict:
        stopWords = set(stopwords.words("english"))
        words = word_tokenize(text_string)
        ps = PorterStemmer()
        freqTable = dict()
        for word in words:
            word = ps.stem(word)
            if word in stopWords:
                continue
            if word in freqTable:
                freqTable[word] += 1
            else:
                freqTable[word] = 1
        return freqTable
    
    def _score_sentences(sentences, freqTable) -> dict:
        sentenceValue = dict()
        for sentence in sentences:
            word_count_in_sentence = (len(word_tokenize(sentence)))
            for wordValue in freqTable:
                if wordValue in sentence.lower():
                    if sentence[:10] in sentenceValue:
                        sentenceValue[sentence[:10]] += freqTable[wordValue]
                    else:
                        sentenceValue[sentence[:10]] = freqTable[wordValue]
    
            sentenceValue[sentence[:10]] = sentenceValue[sentence[:10]] // word_count_in_sentence
    
        return sentenceValue
    def _find_average_score(sentenceValue) -> int:
        sumValues = 0
        for entry in sentenceValue:
            sumValues += sentenceValue[entry]
    
        # Average value of a sentence from original text
        average = int(sumValues / len(sentenceValue))
    
        return average
    def _generate_summary(sentences, sentenceValue, threshold):
        sentence_count = 0
        summary = ''
    
        for sentence in sentences:
            if sentence[:10] in sentenceValue and sentenceValue[sentence[:10]] > (threshold):
                summary += " " + sentence
                sentence_count += 1
    
        return summary
    
    
    from nltk.corpus import stopwords
    from nltk.stem import PorterStemmer
    from nltk.tokenize import word_tokenize, sent_tokenize
    
    # 1 Create the word frequency table
    freq_table = _create_frequency_table(text)
    
    '''
    We already have a sentence tokenizer, so we just need 
    to run the sent_tokenize() method to create the array of sentences.
    '''
    
    # 2 Tokenize the sentences
    sentences = sent_tokenize(text)
    
    # 3 Important Algorithm: score the sentences
    sentence_scores = _score_sentences(sentences, freq_table)
    
    # 4 Find the threshold
    threshold = _find_average_score(sentence_scores)
    
    # 5 Important Algorithm: Generate the summary
    summary = _generate_summary(sentences, sentence_scores, 1.5 * threshold)
    
    print("====================Short Answser===========\n",text)
    result_label1 = tk.Label(root, text="Summary Text", bd=5,width=10, font=("bold", 10),bg='black',fg='white' )
    result_label1.place(x=750, y=300)   
    msg=tk.Text(root, width=80,height=10, bd=5,font=("bold", 15),bg='white',fg='black')
    msg.place(x=300, y=400)
    msg.insert(tk.END, text)
    scrollbar = tk.Scrollbar(root, command=msg.yview, cursor="heart")
    msg['yscrollcommand'] = scrollbar.set
    scrollbar.place(x=1200,y=400, height=235) 



l4 = tk.Label(root, text="ENTER QUESTION :", width=18, font=("Times new roman", 15, "bold"), bg="snow")
l4.place(x=200, y=200)

t3 = tk.Entry(root,bd=5, textvar=question, width=70, font=('', 15))
t3.place(x=500, y=200)


btn = tk.Button(root, text="Search", bg="red",font=("",10),fg="white", width=9, height=1, command=wikipedia)
btn.place(x=1300, y=200)

root.mainloop()