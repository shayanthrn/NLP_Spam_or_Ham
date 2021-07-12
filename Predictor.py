import re
import string

class NLP:
    
    def PreProcessing_Text(self,dataset):
        for i,text in enumerate(dataset):
            dataset[i] = text.lower() #lower characters
            dataset[i] = re.sub(r'\d+', '', dataset[i])  #remove numbers
            dataset[i] = dataset[i].translate(str.maketrans("","", string.punctuation)) #remove punctuations
            dataset[i] = " ".join(dataset[i].split()) #remove white spaces and duplicated space

    def CreateDictionary(self,dataset):
        dictionary = {}
        for sentence in dataset:
            words = sentence.split(' ')
            for word in words:
                if(word in dictionary.keys()):
                    dictionary[word] +=1
                else:
                    dictionary[word] = 1
        print(dictionary)
            



if __name__ == "__main__":
    f  = open("rt-polarity.pos","r")
    positives = f.readlines()
    f.close()
    f = open("rt-polarity.neg","r")
    negatives = f.readlines()
    f.close()
    nlp = NLP()
    a = ["Asqar,,xv *&WDFS sdfsdfk23424   pxopokv    234 pxopokv ,, asfpoksf \t \t \t \n asldkfmsldf\n","asdfzxcxvcxv234234CCCCCCCSFSDFffv&***x\t\t\n"]
    nlp.PreProcessing_Text(a)
    nlp.CreateDictionary(a)
    print(a)