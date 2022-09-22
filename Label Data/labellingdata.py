import numpy as np
import pandas as pd
import os
import json
import spacy
from spacy.language import Language

cdir1 ='C:\Users\mariam.riaz\PycharmProjects\Scientific-Paper-Summarizer\Label Data\json_txt_files'
cdir2 ='C:\Users\mariam.riaz\PycharmProjects\Scientific-Paper-Summarizer\Data\talksummaries'

@Language.component('set_custom_boundaries')
def set_custom_boundaries(doc):
    for token in doc[:-1]:
        if ((token.text == ("al")) and (token.i != len(doc) - 2)):
            doc[token.i+2].is_sent_start = False
    return doc

nlp = spacy.load("en_core_web_lg")
nlp.add_pipe('set_custom_boundaries', before="parser")
nlp.pipeline


title = []
abstract = []
sections2 = []
whole_paper = []

i = 0

for subdir, dirs, files in os.walk(cdir1):
    for file in files:
        f1 = os.path.join(subdir, file)
        with open(f1) as f:
            data = json.load(f)
        for section in data:
            if (section == 'title'):
                line3 = np.array([data[section], section])
                sections2.append(line3)
            elif (section == 'abstractText'):
                doc = nlp(data[section])
                for sent in doc.sents:
                    line4 = np.array([sent, section])
                    sections2.append(line4)
            elif (section == 'sections'):
                for sect in data[section]:
                    if len(sect) >= 2:
                        doc2 = nlp(sect["text"])
                        for sent in doc2.sents:
                            line2 = np.array([sent, sect['heading']])
                            sections2.append(line2)
                    else:
                        line = np.array([sect["text"], "text"])
                        sections2.append(line)

            else:
                i = i + 1
                #print(i)

        data = np.array(sections2)
        df = pd.DataFrame(data=data)
        df3 = pd.DataFrame(data=data)
        df2 = pd.read_csv(cdir2 +'\\'+ os.path.splitext(file)[0]+".txt" ,sep="\t", header=None)

        label22 = []
        summ_sentences = []
        for i, j in df.iterrows():
            label21 = []
            sentence = []
            if (type(j[0])==str):
                doc1 = nlp(j[0])
            else:
                doc1 = nlp(j[0].text)
            for a, b in df2.iterrows():
                doc2 = nlp(b[2])
                similarity = doc1.similarity(doc2)
                if similarity > 0.80:
                    label21.append(similarity)
                    sentence.append(doc2.text)
                    #print("similarity = " + str("%.2f" % (float(doc1.similarity(doc2)) * 100)) + "%\n")
                    #print("document-1 is: " + doc1.text)
                    #print("document-2 is: " + doc2.text)
                    df2 = df2.drop([a])
                    break
                else:
                    pass
            if len(label21) == 0:
                label21.append(0)
                sentence.append(0)
                df = df.drop([i])

            label22.append(label21)
            summ_sentences.append(sentence)

        df3["label2"] = label22
        df3["summary_sentences"] = summ_sentences
        df3.to_csv('C:\Users\mariam.riaz\PycharmProjects\Scientific-Paper-Summarizer\Label Data\results'+ os.path.splitext(file)[0] +'.csv', encoding="utf-8", index=None)
        print(os.path.splitext(file)[0] + " ----------> DONE")