#Santiago Solórzano
#Proyecto 2 task 1

import re
import itertools
import collections
import numpy
import random
import sys

with open("test_corpus.txt") as f:
    content = f.read().splitlines()
mails = []
for s in content:
    mails.append(s.split("\t"))    

# Splitting 
#   80% Train
#   10% Cross Validation
#   10% Test    
 
random.shuffle(mails)
percent = [0.8,0.9,1.0]
idx1 = [0] + list(int(len(mails) * p) for p in percent[:-1])
idx2 = idx1[1:] + [len(mails)]
all = list(mails[i1:i2] for i1,i2 in zip(idx1, idx2))
train = all[0]
cross = all[1]
test = all[2]

# Test Data is ordered
# Using Regex classifies ham or spam messages

ham  = [re.findall(r'[^\s!,.?":;0-9]+',x[1].lower()) for x in train if x[0] == "ham"]
spam  = [re.findall(r'[^\s!,.?":;0-9]+',x[1].lower()) for x in train if x[0] == "spam"]

# Dictionaries are created
hamDic = list(itertools.chain.from_iterable(ham))
frequenciesHam = collections.defaultdict(int)
for palabra in hamDic:
    frequenciesHam[palabra] += 1

spamDic = list(itertools.chain.from_iterable(spam))
frequenciesSpam = collections.defaultdict(int)
for palabra in spamDic:
    frequenciesSpam[palabra] += 1    
    
# Variables for testing

pSpam = len(spam)/len(train)
pHam = len(ham)/len(train)

def pPalabraDado(palabra, spamOrHam,k):
    if (spamOrHam == "spam"):
        if not(frequenciesSpam.get(palabra)):
            a = 0
        else:
            a = frequenciesSpam.get(palabra)
        return (a+k)/(sum(frequenciesSpam.values())+k*(len(frequenciesSpam)))
    elif (spamOrHam == "ham"):
        if not(frequenciesSpam.get(palabra)):
            a = 0
        else:
            a = frequenciesSpam.get(palabra)
        return (a+k)/(sum(frequenciesHam.values())+k*(len(frequenciesHam)))

def pMensajesDado(mensaje,conditional,spamOrHam):
    if (spamOrHam == "spam"):
        multSpam = 1
        multHam = 1
        for index,word in enumerate(mensaje):
            multSpam = multSpam * conditional[index][1]
            multHam = multHam * conditional[index][2]
            
        multSpam = multSpam * pSpam
        multHam = multHam * pHam
        if(multSpam + multHam <= 0):
            return(multSpam/(1e-200))
        else:
            return(multSpam/(multSpam + multHam))
        
    elif (spamOrHam == "ham"):
        multSpam = 1
        multHam = 1
        for index,word in enumerate(mensaje):
            multSpam = multSpam * conditional[index][1]
            multHam = multHam * conditional[index][2]
          
        multSpam = multSpam * pSpam
        multHam = multHam * pHam
        if(multHam + multSpam <= 0):
            return(multHam/(1e-200))
        else:
            return(multHam/(multHam + multSpam))
                  
        
# Cross validation
# First split the words
crossValidationMails = []
for mail in cross:
    t =[]
    t.append(mail[0])
    t.append(re.findall(r'[^\s!,.?":;0-9]+',mail[1].lower()))
    crossValidationMails.append(t)
kn = 0.1
while (kn < 5.5):	
	goodPredictions = 0
	totalPredictions = 0
	# Second use function to get probability of ham or spam for each mail
	for index, mail in enumerate(crossValidationMails):
		wordConditionalProbabilities = []
		for word in mail[1]:
			p = []
			p.append(word)
			p.append(pPalabraDado(word,"spam",kn))
			p.append(pPalabraDado(word,"ham",kn))
			wordConditionalProbabilities.append(p)
		pSpam = pMensajesDado(mail[1],wordConditionalProbabilities,"spam")
		pHam = pMensajesDado(mail[1],wordConditionalProbabilities,"ham")
		
	# Third compare results and get percentage of accuracy
		if(pSpam>pHam):
			#print("El mensaje {} es spam".format(mail[0]))
			if("spam"==mail[0]):
				goodPredictions+=1
		elif(pSpam<pHam):
			#print("El mensaje {} es ham".format(mail[0]))
			if("spam"==mail[0]):
				goodPredictions+=1
	print("K = {}, Acc = {}".format(kn,(goodPredictions/len(crossValidationMails))*100))	
	kn += 0.1
	
    
    
#mensaje = raw_input("Ingrese el mensaje a detectar: ")
#mensaje = re.findall(r'[^\s!,.?":;0-9]+',mensaje.lower())

#P de m sea spam
#P de m sea ham
import tkinter

def hola():
    msg = tkinter.messagebox.showinfo("hola","adios")

top = tkinter.Tk()
top.geometry("200x100")
var = tkinter.StringVar()
label = tkinter.Label(top, textvariable = var)
var.set("SPAM or HAM")
b = tkinter.Button(top,text="Probar",command = hola)
b.place(x=50,y=50)
text = tkinter.Text(top)
label.pack()
text.pack()
top.mainloop()






