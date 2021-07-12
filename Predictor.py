import re
import string

class NLP:

    def PreProcessing_Text(self,dataset):
        for i,text in enumerate(dataset):
            dataset[i] = text.lower() #lower characters
            dataset[i] = re.sub(r'\d+', '', dataset[i])  #remove numbers
            dataset[i] = dataset[i].translate(str.maketrans("","", string.punctuation)) #remove punctuations
            dataset[i] = " ".join(dataset[i].split()) #remove white spaces and duplicated space
    
    def RemoveLeastandMostFrequentWords(self,dictionary):
        for key in dictionary:
            if(dictionary[key] <= 2):
                dictionary.pop(key)
        mylist= sorted(dictionary,key =dictionary.get , reverse = True)
        if(len(mylist)>10):
            for key in mylist[:10]:
                dictionary.pop(key)


    def CreateDictionary(self,dataset):
        dictionary = {}
        for sentence in dataset:
            words = sentence.split(' ')
            for word in words:
                if(word in dictionary.keys()):
                    dictionary[word] +=1
                else:
                    dictionary[word] = 1
        return dictionary
    
    def CreateCoupleDictionary(self,dataset):
        dictionary = {}
        for sentence in dataset:
            words = sentence.split(' ')
            for i in range(len(words)):
                if(i!= len(words)-1 and i != 0):
                    key = words[i]+"_"+words[i+1]
                elif(i == 0):
                    key = "<s>" + "_" + words[i]
                else:
                    key = words[i] + "_" +"</s>"
                if(key in dictionary.keys()):
                    dictionary[key] +=1
                else:
                    dictionary[key] = 1
        return dictionary
                  



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
    print(nlp.CreateCoupleDictionary(a))
    print(a)