import re
import string

class NLP:

    def PreProcessing_Text(self,dataset):  #checked
        for i,text in enumerate(dataset):
            dataset[i] = text.lower() #lower characters
            dataset[i] = re.sub(r'\d+', '', dataset[i])  #remove numbers
            dataset[i] = dataset[i].translate(str.maketrans("","", string.punctuation)) #remove punctuations
            dataset[i] = " ".join(dataset[i].split()) #remove white spaces and duplicated space
    
    def CreateDictionary(self,dataset): #checked
        dictionary = {'<s>':0,'</s>':0}
        for sentence in dataset:
            words = sentence.split(' ')
            for word in words:
                if(word in dictionary.keys()):
                    dictionary[word] +=1
                else:
                    dictionary[word] = 1
            dictionary['</s>']+= 1
            dictionary['<s>'] += 1
        return dictionary
    
    def CreateCoupleDictionary(self,dataset): #checked
        dictionary = {}
        for sentence in dataset:
            words = sentence.split(' ')
            for i in range(len(words)-1):
                two_words = (words[i],words[i+1])
                if(two_words in dictionary.keys()):
                    dictionary[two_words] += 1
                else:
                    dictionary[two_words] = 1
            two_words = ("<s>",words[0])
            if(two_words in dictionary.keys()):
                dictionary[two_words] += 1
            else:
                dictionary[two_words] = 1
            two_words = (words[-1],"</s>")
            if(two_words in dictionary.keys()):
                dictionary[two_words] += 1
            else:
                dictionary[two_words] = 1
        return dictionary

    def RemoveLeastandMostFrequentWords(self,dictionary):
        for word in list(dictionary):
            if(dictionary[word]<2):
                del dictionary[word]
        mylist= sorted(dictionary,key =dictionary.get , reverse = True)
        for word in mylist[2:12]:
            del dictionary[word]
    
    def RemoveLeastandMostFrequentWords_c(self,dictionary):
        for key in list(dictionary):
            if(dictionary[key]<2):
                del dictionary[key]

    def CalculateProbabilty_BackOffModel(self,key,Lambda1,Lambda2,Lambda3,Epsilon,dictionary,dictionary_c):
        return Lambda3*self.CalculateProbabilty_Bigram(key,dictionary_c,dictionary) + Lambda2*self.CalculateProbabilty_unigram(key[1],dictionary) + Lambda1*Epsilon

    def CalculateProbabilty_Bigram(self,key,dictionary_c,dictionary):
        if (key in dictionary_c.keys() and key[0] in dictionary.keys()):
            return dictionary_c[key]/dictionary[key[0]]
        else:
            return 0
    
    def CalculateProbabilty_unigram(self,key,dictionary):
        totalcount = sum(dictionary.values())
        if (key in dictionary.keys()):
            return dictionary[key]/totalcount
        else:
            return 0
    
    def CalculateProbabilty_lang(self,sentence,dictionary,dictionary_c,P_lang):
        Epsilon=0.01
        Lambda1=0.1
        Lambda2=0.2
        Lambda3=0.9
        sentence = [sentence]
        self.PreProcessing_Text(sentence)
        sentence = sentence[0]
        words = sentence.split(' ')
        result = 1
        #beginning
        key = ("<s>",words[0])
        result *= self.CalculateProbabilty_BackOffModel(key,Lambda1,Lambda2,Lambda3,Epsilon,dictionary,dictionary_c)
        #ending
        key = (words[-1],"</s>")
        result *= self.CalculateProbabilty_BackOffModel(key,Lambda1,Lambda2,Lambda3,Epsilon,dictionary,dictionary_c)
        for i in range(1,len(words)):
            key = (words[i-1],words[i])
            result *= self.CalculateProbabilty_BackOffModel(key,Lambda1,Lambda2,Lambda3,Epsilon,dictionary,dictionary_c)
        return result*P_lang

if __name__ == "__main__":
    f  = open("rt-polarity.pos","r")
    positives = f.readlines()
    f.close()
    f = open("rt-polarity.neg","r")
    negatives = f.readlines()
    f.close()
    nlp = NLP()
    train_positive = positives[:int(len(positives)*0.9)]
    test_positive = positives[int(len(positives)*0.9):]
    train_negatives = negatives[:int(len(negatives)*0.9)]
    test_negatives = negatives[int(len(negatives)*0.9):]
    nlp.PreProcessing_Text(train_positive)
    pdictionary = nlp.CreateDictionary(train_positive)
    nlp.RemoveLeastandMostFrequentWords(pdictionary)
    pdictionary_c = nlp.CreateCoupleDictionary(train_positive)
    nlp.RemoveLeastandMostFrequentWords_c(pdictionary_c)
    nlp.PreProcessing_Text(train_negatives)
    ndictionary = nlp.CreateDictionary(train_negatives)
    nlp.RemoveLeastandMostFrequentWords(ndictionary)
    ndictionary_c = nlp.CreateCoupleDictionary(train_negatives)
    nlp.RemoveLeastandMostFrequentWords_c(ndictionary_c)
    #test accuracy for positive
    counter = 0
    for i in range(len(test_positive)):
        sentence = test_positive[i]
        if nlp.CalculateProbabilty_lang(sentence, pdictionary, pdictionary_c, 0.5)>nlp.CalculateProbabilty_lang(sentence, ndictionary, ndictionary_c, 0.5):
            counter += 1
    print("Accuracy for positives:",counter/len(test_positive))

    #test accuracy for negatives
    counter = 0
    for i in range(len(test_negatives)):
        sentence = test_negatives[i]
        if nlp.CalculateProbabilty_lang(sentence, pdictionary, pdictionary_c, 0.5)<nlp.CalculateProbabilty_lang(sentence, ndictionary, ndictionary_c, 0.5):
            counter += 1
    print("Accuracy for negatives:",counter/len(test_negatives))
        