# _*_ coding: utf-8 _*_
import string
import sys
import operator
reload(sys)
sys.setdefaultencoding('utf-8')

allOfData = []
category = []
X2statistic =[]

#f1 = open("DON.txt",'r')
#f1 = open("04train.txt",'r')
f1 = open("HKIB-20000_001.txt",'r')
f2 = open("HKIB-20000_002.txt",'r')
f3 = open("HKIB-20000_003.txt",'r')
f4 = open("HKIB-20000_004.txt",'r')
data = f1.read()
data = data + f2.read()
data = data + f3.read()
data = data + f4.read()
data = data.split('@DOCUMENT')
data.pop(0)
DocSize = len(data) #도큐먼트의 개수
twoDimention = [[] for row in range(DocSize)]


for idx,sentence in enumerate(data):
    sentence = sentence.split("#TEXT")
    #sentence.pop(0)
    headText = sentence[0].split("#")
    headText = headText[2].split('/')
    category.append(headText[1])  # 카테고리 저장

compressCategory = list(set(category))
countingCategroy = [0]* len(compressCategory)

for idx,sentence in enumerate(data):
    sentence = sentence.split("#TEXT")
    # sentence.pop(0)
    headText = sentence[0].split("#")
    headText = headText[2].split('/')
    key = compressCategory.index(category[idx])  # Key값저장
    countingCategroy[key] = countingCategroy[key]+1
    sentence[1] = sentence[1].replace(',', ' ').replace('.', ' ').replace('"', ' ').replace("'", '').replace('(',' ').replace(')', ' ').replace('-', ' ').replace('[', ' ').replace(']', ' ').replace(':', '').replace('-', '').replace('{', ' ').replace('}', ' ').replace('!', ' ').replace('^', ' ').replace('+', ' ').replace('<', ' ').replace('>', ' ').replace('*', '').replace('&', ' ').replace('%', ' ').replace('『', ' ').replace('』', ' ').replace('”', ' ').replace('~',' ')
    dataText = sentence[1].split('<KW>')
    DocumentText = dataText[0].split()  # 단어별로 자르기

    seen1 = set()
    result1 = []
    for item in DocumentText:
        if item not in seen1:
            item = item.strip()
            seen1.add(item)
            result1.append(item)
    DocumentText = result1

    for item in DocumentText:
        list = []
        list.append(item)
        list.append(idx)
        list.append(key)
        allOfData.append(list)


for i  in compressCategory:
    print i,"   ",
print ""
for i in countingCategroy:
    print i," ",
print ""

print len(allOfData)
#allOfData = [list(t) for t in set(tuple(element) for element in allOfData)]

seen = set()
newlist = []
for item in allOfData:
    t = tuple(item)
    if t not in seen:
        newlist.append(item)
        seen.add(t)
allOfData = newlist

allOfData = sorted(allOfData ,key=operator.itemgetter(0))


listset= [0,0,0,0,0,0,0,0]
A = 0
B = 0
C = 0
D = 0
RESULTNUM = -100000

keyItem = allOfData[0][0]
categoryList =[]
for i in allOfData:
    if i[0] == keyItem:
        listset[i[2]] = listset[i[2]]+1
        categoryList.append(i[1])
    else:
        sum = 0
        for j in range(len(compressCategory)):
            sum = sum + listset[j]
        for j in range(len(compressCategory)):
            A = listset[j]
            B = countingCategroy[j] - listset[j]
            C = sum - listset[j]
            D = (DocSize - countingCategroy[j]) - C
            temp = (DocSize * (A * D - B * C) * (A * B - B * C)) / ((A + C) * (C + D) * (B + D) * (A + B) * 1.0)
            if temp > RESULTNUM:
                RESULTNUM = temp
        # All of X2statistic LIST Append list. format is [Text, X2value , [Document list]]
        templist = []
        templist.append(keyItem)
        templist.append(RESULTNUM)
        templist.append(categoryList)
        X2statistic.append(templist)
        for i in range(len(listset)):
            listset[i] =0
        RESULTNUM = -100000
        categoryList =[]
        keyItem = i[0]
        listset[i[2]] = listset[i[2]] + 1
        categoryList.append(i[1])

## Ended for loop, Lastly Calculate X2 Value
sum = 0
for j in range(len(compressCategory)):
    sum = sum + listset[j]
for j in range(len(compressCategory)):
    A = listset[j]
    B = countingCategroy[j] - listset[j]
    C = sum - listset[j]
    D = (DocSize - countingCategroy[j]) - C

    temp = (DocSize * (A * D - B * C) * (A * B - B * C)) / ((A + C) * (C + D) * (B + D) * (A + B) * 1.0)
    if temp > RESULTNUM:
        RESULTNUM = temp
templist = []
templist.append(keyItem)
templist.append(RESULTNUM)
templist.append(categoryList)
X2statistic.append(templist)

X2statistic = sorted(X2statistic ,key=operator.itemgetter(1), reverse=True) #sorting

X2Keyword = {}
X2Value = []
print "--------------------- "

for i in range(0,2000):
    print i + 1, " : ", X2statistic[i][1], " <-", X2statistic[i][0]
for idx,i in enumerate(X2statistic):
    #print idx+1," : ",i[1]," <-",i[0]
    item = X2statistic[idx][0]
    X2statistic[idx].append(idx)

    #input dict
    X2Keyword[item] = idx
    X2Value.append(X2statistic[idx][1])

    for j in i[2]:
        twoDimention[j].append(X2statistic[idx])


print "THAN"

wf = open('training.txt', 'w')
for idx,i in enumerate(twoDimention):
    #Category index number
    stp = str(compressCategory.index(category[idx])+1)+" "
    wf.write(stp)

    for j in i:
        stp = str(j[3]+1)+":"+str(round(j[1] ,6))+" "
        wf.write(stp)

    wf.write("\n")


f5 = open("HKIB-20000_005.txt",'r')
testData = f5.read()
testData = testData.split('@DOCUMENT')
testData.pop(0)
testDocSize = len(testData)
tupleDimention =[]
tw = open('test.txt','w')
for idx,sentence in enumerate(testData):
    tupleDimention = []
    sentence = sentence.split("#TEXT")
    headText = sentence[0].split("#")
    headText = headText[2].split('/')
    key = compressCategory.index(headText[1]) #compressCategory -> Remove duplicate Category set
    str1 = str(key+1) + " "
    tw.write(str1)
    sentence[1] = sentence[1].replace(',', ' ').replace('.', ' ').replace('"', ' ').replace("'", '').replace('(',' ').replace(')', ' ')\
        .replace('-', ' ').replace('[', ' ').replace(']', ' ').replace(':', '').replace('-', '').replace('{', ' ').replace('}', ' ')\
        .replace('!',' ').replace('^', '').replace('+', ' ').replace('<', ' ').replace('>', ' ').replace('*', '').replace('&', ' ')\
        .replace('%', ' ').replace('『',' ').replace('』', ' ').replace('”', ' ').replace('~',' ')
    sentence[1] = sentence[1]
    dataText = sentence[1].split('<KW>')
    DocumentText = dataText[0].split()  # 단어별로 자르기
    DocumentText = set(DocumentText) # Duplicate tuple Delete


    result1 = []
    for item in DocumentText:
        try:
            X2id = X2Keyword[item] #X2Keyword set is [textName, textIndex]
            result1.append(X2id)
        except KeyError:
            continue
    result1.sort()

    for item in result1:
        str1 = str(item+1)+":"+str(round(X2Value[item],6))+" " #Write test.txt
        tw.write(str1)
    tw.write("\n")


tw.close()
wf.close()
f1.close()
f2.close()
f3.close()
f4.close()
f5.close()