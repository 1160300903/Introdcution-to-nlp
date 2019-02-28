import time
''' trie tree
'''
class Trie():
    def __init__(self):
        self.root=Node()
        self.maxLength=0
    """ read dic.txt and build a trie tree
    """
    def initFromDic(self,path="dic.txt"):
        with open(path,"r",encoding="utf-8") as file:
            lines=file.read().split("\n")
            for line in lines:
                words=line.split()
                self.addWord(words[0],int(words[1]))
    ''' read 199801_seg.txt and build a trie tree.
        You shuold notice that 199801_seg.txt is edited by using text editor.
        The way in which I edit 199801_seg.txt is shown in README.txt
    '''
    def readSeg(self,path="199801_seg.txt"):
        file = open(path,"r",encoding="utf-8")
        try:
            b = file.read()
        finally:
            file.close()
        words = b.split()
        for word in words:
            self.addWord(word)
    ''' add word to trie tree
        count is the times of word
    '''  
    def addWord(self,word,count=1):
        if word==None or len(word)==0:
            return
        self.maxLength = max(self.maxLength,len(word))
        node = self.root
        for c in word:
            newNode=node.search(c)
            if newNode==None:
                newNode=Node(c)
                node.addSon(newNode)
            node = newNode
        node.isEnd=True
        node.num+=count
    ''' search a word in the trie tree
    '''
    def has(self,word):
        if word==None or len(word)==0:
            return False
        node=self.root
        for c in word:
            newNode=node.search(c)
            if newNode!=None:
                node=newNode
            else:
                return False
        return node.isEnd
    ''' print the trie tree
        node should be self.root, when you call this method
        you don't need to change the value of word
    '''
    def showTree(self,node,word=""):
        if node!=None:
            word+=node.char
        if node.isEnd:
            print(word)
        for l in node.son:
            for newNode in l:
                self.showTree(newNode,word)
        word=word[:len(word)-1]
    ''' output the dic to dic.txt
        node should be self.root, when you call this method
        you don't need to change the values of string, word and file
    '''
    def outputToFile(self,node,string="",word="",file=open("dic.txt","w",encoding="utf-8")):
        if node!=None:
            word+=node.char
        if node.isEnd:
            string+=(word+" "+str(node.num)+"\n")
        if node.son!=None:
            for l in node.son:
                for newNode in l:
                    string=self.outputToFile(newNode,string,word)
        if node==self.root:
            string=string[:-1]
            file.write(string)
            file.close()
        return string
''' node of trie tree
'''
class Node():
    hashLen=100
    def __init__(self,c=""):
        self.num=0#从跟到该节点出现的次数
        self.son=None#储存所有儿子,推迟初始化,在addSon和search中才会进行初始化
        self.isEnd=False#是不是最后一个节点
        self.char=c#节点的字符
    ''' search a specific character in sons of this node 
        c: the character you want to search
        return:if character c is a son of this node, the method return that son.
        Or, the method return None
    '''
    def addSon(self,sonNode):
        if self.son==None:
            self.son=[[] for i in range(Node.hashLen)]
        x=hash(sonNode.char)%Node.hashLen
        self.son[x].append(sonNode)
    def search(self,c):
        if self.son==None:
            return None
        x=hash(c)%Node.hashLen
        for sonNode in self.son[x]:
            if sonNode.char==c:
                return sonNode
        return None
''' This class provide FMM and BMM
'''
class MM:
    ''' Forward maximum matching
        string: the sentence you want to segment
        dic: a trie tree uesd in FMM
    ''' 
    
    def FMM(self,string,dic):
        segList=[]
        while len(string)>0:
            length=min(len(string),dic.maxLength)
            seg=string[0:length]
            while not dic.has(seg):
                if len(seg)==1:
                    break
                seg=seg[:len(seg)-1]
            string=string[len(seg):]
            segList.append(seg)
        return segList
    ''' Backward maximum matching
        string: the sentence you want to segment
        dic: a trie tree uesd in BMM
    ''' 
    def BMM(self,string,dic):
        segList=[]
        while len(string)>0:
            length=min(len(string),dic.maxLength)
            seg=string[-length:]
            while not dic.has(seg):
                if len(seg)==1:
                    break
                seg=seg[1:]
            segList.insert(0,seg)
            string=string[:-len(seg)]
        return segList
    """ segment all the sentences in a file
        file: all sentence in this file is segmented
    """
    def MMForFile(self,dic,file=open("199801_sent.txt","r",encoding="utf-8")):
        FMMFile=open("seg_FMM.txt","w",encoding="utf-8")
        BMMFile=open("seg_BMM.txt","w",encoding="utf-8")
        timeCost=open("timeCost.txt","a",encoding="utf-8")
        lines=file.read().split("\n")
        FMMString=""
        BMMString=""
        startTime=time.time()
        for i in range(len(lines)):
            line=lines[i]
            segList=MM.FMM(None,line,dic)
            FMMString=MM.formatList(None,segList)
            FMMFile.write(FMMString)
        for i in range(len(lines)):
            line=lines[i] 
            segList=MM.BMM(None,line,dic)
            BMMString=MM.formatList(None,segList) 
            BMMFile.write(BMMString)
        endTime=time.time()
        timeCost.write("耗时:"+str(endTime-startTime)+"s\n")
        FMMFile.close()
        BMMFile.close()
    def formatList(self,list):
        string=""
        for word in list:
            string+=word
            string+="/ "
        string=string[:-2]
        string+="\n"
        return string    
""" output a dictionary to dic.txt
"""
def Q3_1(path="199801_seg.txt"):
    dic=Trie()
    dic.readSeg(path)  
    dic.outputToFile(dic.root)   
""" put3.2 and 3.4 together.
    segment all the sentence and output the time cost in timeCost.txt
"""
def Q3_2and3_4(path="199801_sent.txt",dicPath="dic.txt"):
    dic=Trie()
    dic.initFromDic(dicPath)
    MM.MMForFile(None,dic,open(path,"r",encoding="utf-8"))
    
def main():
    Q3_1()#build the dictionary
    Q3_2and3_4()#read the dictionary and segment sentences
if __name__=="__main__":
    main()
