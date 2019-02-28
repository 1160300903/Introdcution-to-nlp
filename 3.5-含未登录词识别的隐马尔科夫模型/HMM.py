import copy
from math import log
from math import exp
class HMM():
    """ 初始化HMM算法
        trans为转移矩阵，4x4,dic(dic)
        B为产生文字的概率矩阵，4xn,dic(dic)
        PI为初始状态矩阵，1x2,dic
        TPro为句子以S和E结束的的概率,1x2,dic
    """
    def __init__(self,PI={},trans={},B={},TPro={}):
        self.PI=PI
        self.trans=trans
        self.B=B
        self.suffixDict={}#前缀词典
        self.states=set()
        self.TPro=TPro
        self.OOVDic=set()
        self.maxLength = 0
    def viterbi(self, sentence):
        length=len(sentence)#求句子长度
        d={}
        for state in self.states:
            d[state]=float("-inf")
        pro=[copy.deepcopy(d) for i in range(length)]
        for state in self.states:
            d[state]=(0,0)
        path=[copy.deepcopy(d) for i in range(length)]
    
        DAG=HMM.getDAG(self,sentence)
        for x in DAG[0]:
            word=sentence[0]
            for state in self.states:
                if word in B[state]:
                        out=B[state][word]
                else:
                    out=HMM.myLog(self,0)
                pro[0][state]=self.PI[state]+out
        for i in range(1,length):
            for x in DAG[i]:
                word = sentence[x:i+1]
                for state2 in self.states:
                    if word in B[state2]:
                        out=B[state2][word]
                    else:
                        out=HMM.myLog(self,0)
                    tempPro:float=0
                    for state1 in pro[x-1]:
                        if not x:#即sentence[0,i+1]为一个词
                            tempPro=self.PI[state2]+out
                        else:
                            tempPro=pro[x-1][state1]+self.trans[state1][state2]+out
                        if tempPro>pro[i][state2]:
                            pro[i][state2]=tempPro
                            path[i][state2]=(x,state1)
        result=HMM.backTracing(self,sentence,length,pro,path,TPro)
        return result
    def backTracing(self,sentence,length,pro,path,TPro):
        bestPro=float("-inf")
        result=[]
        for state in pro[length-1]:
            tmpPro=pro[length-1][state]+TPro[state]
            if tmpPro>=bestPro:
                bestPro=tmpPro
                x,preState=path[length-1][state]
        result.append(sentence[x:])
        while x>0:#x是已经分完的词的序号，x==0时说明整个句子都分完了
            j,preState=path[x-1][preState]
            result.append(sentence[j:x])
            x=j
        result.reverse()
        string = HMM.findCharacterList(self,result)
        return string
    """ 对log(0)抛异常的情况进行了处理
    """
    def myLog(self,a):
        if a==0:
            return -708.3964185322641
        else:
            return log(a)
    """ 初始化参数PI,B,TPro
    """
    def initParameter(self):
        oovFile = open("OOVDic.txt","r",encoding="utf-8")
        oovWords = oovFile.read().split()
        for word in oovWords:
            self.OOVDic.add(word)
            self.maxLength = max(self.maxLength,len(word))
        inputFile=open("199801_seg.txt","r",encoding="utf-8")
        lines=inputFile.read().split("\n")
        inputFile.close()
        PI=self.PI
        trans=self.trans
        B=self.B
        TPro=self.TPro
        mySet=set()
        for line in lines:
            words = line.split()
            for word in words:
                word,curState = self.splitWord(word)
                self.states.add(curState)
        for state1 in self.states:#初始化timesPerStat,trans,B
            trans[state1]={}
            B[state1]={}
            for state2 in self.states:
                trans[state1][state2]=1
        for state in self.states:#用于初始化PI
            PI[state]=0
            TPro[state]=0
        for line in lines:
            if line=="":#去除空行
                continue
            words=line.split()
            word,curState=HMM.splitWord(self,words[0])#curState为current State
            HMM.addWordCount(self,B,mySet,curState,word)
            PI[curState]+=1
            preState=curState
            for i in range(1,len(words)):
                word,curState=HMM.splitWord(self,words[i])
                HMM.addWordCount(self,B,mySet,curState,word)
                trans[preState][curState]+=1
                preState=curState
            TPro[preState]+=1#记录句子的终结状态
        sumOfRow={}#转移矩阵每一行的数字和
        for state1 in self.states:
            sum=0
            for state2 in self.states:
                sum+=trans[state1][state2]
                sumOfRow[state1]=self.myLog(sum)
        timesPerStat={}#用于记录每一状态出现的次数
        for state in self.states:
            sum=0
            for word in B[state]:
                sum+=B[state][word]
                timesPerStat[state] = self.myLog(sum)
        lineNum=len(lines)#计算行数
        lineNum=self.myLog(lineNum)
        for pro in TPro:
            TPro[pro]=self.myLog(TPro[pro])-lineNum
        for pro in PI:
            PI[pro]=self.myLog(PI[pro])-lineNum
        for state1 in self.states:
            for state2 in self.states:
                trans[state1][state2]=self.myLog(trans[state1][state2])-sumOfRow[state1]
        for state in self.states:
            for word in B[state]:
                B[state][word]=self.myLog(B[state][word])-timesPerStat[state]
        #初始化前缀词典
        HMM.genSuffixDict(self,mySet)
    def showArray(self,PI,trans,B):
        print("PI:")
        count=0
        for state in self.states:
              count+=exp(PI[state])
        print(count)
        print("trans:")
        for state1 in self.states:
            count=0
            for state2 in self.states:
                count+=exp(trans[state1][state2])
            print(state1+str(count))
        print("B:")
        for state in self.states:
            count=0
            for char in B[state]:
                count+=exp(B[state][char])
            print(state+str(count))
    """ 从“词/词性”的单位当中切分出词性
    """
    def splitWord(self,word):
        location=word.index("/")
        return word[:location],word[location+1:]
    """ 给发射矩阵B统计每个字出现的次数(不是频率)
    """
    def addWordCount(self,B,mySet,curState,word):
        if word not in mySet:
            mySet.add(word)
        if word not in B[curState]:
            B[curState][word]=1
        else:
            B[curState][word]+=1
    """ 生成后缀词典
    """
    def genSuffixDict(self,mySet):
        for word in mySet:
            self.suffixDict[word] = 1
            for i in range(1,len(word)):
                frag=word[i:]
                if frag not in self.suffixDict:
                    self.suffixDict[frag] = 0
    def getDAG(self,sentence):
        DAG={}
        length=len(sentence)
        for i in range(length):
            tempList=[]
            j = i
            frag=sentence[j]
            while j>-1 and frag in self.suffixDict:
                if self.suffixDict[frag]==1:
                    tempList.append(j)
                j = j-1
                frag = sentence[j:i+1]
            if len(tempList)==0:
                tempList.append(i)#防止为空
            DAG[i]=tempList
        return DAG
    def findCharacterList(self,segList):
        count = 0
        resultList = []
        for i in range(len(segList)):
            length = len(segList[i])
            if length == 1:
                count +=1
            elif length == 0:
                print("1111111111111111111111111")
            else:
                if count > 1:
                    subList = self.findOOV("".join(segList[i-count:i]))
                    resultList = resultList+subList
                else:
                    resultList = resultList + segList[i-count:i]
                count = 0 
                resultList.append(segList[i])
        if count > 1:
            subList = self.findOOV("".join(segList[len(segList)-count:]))
            resultList = resultList+subList
        else:
            resultList = resultList + segList[len(segList)-count:]
        return "/ ".join(resultList)

        
    def findOOV(self,string):
        segList=[]
        while len(string)>0:
            length=min(len(string),self.maxLength)
            seg=string[-length:]
            while seg not in self.OOVDic:
                if len(seg)==1:
                    break
                seg=seg[1:]
            segList.insert(0,seg)
            string=string[:-len(seg)]
        return segList
if __name__=="__main__":
    trans={}
    B={}
    PI={}
    TPro={}
    HInstance=HMM(PI,trans,B,TPro)
    HInstance.initParameter()
    with open("199801_sent.txt","r",encoding="utf-8") as file:
        with open("seg_LM.txt","w",encoding="utf-8") as outputFile:
            lines=file.read().split("\n")
            for i in range(len(lines)):
                line = lines[i]
                if line=="":#去除空行
                    continue
                outputFile.write(HInstance.viterbi(line)+"\n")
                if i%100==0:
                    print(i)


