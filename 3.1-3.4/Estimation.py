import re
class Estimation():
    """ compute precision and recall
        file:the file you want to comput precision and recall of.
    """
    def precisionAndRecall(self,file,standard):
        staList=standard.read().split()
        fileList=file.read()
        fileList = re.split("/ |\n",fileList)
        while "" in fileList:
            fileList.remove("")
        while "" in staList:
            staList.remove("")
        rightCount=Estimation.inter(None,staList,fileList)
        file.close()
        standard.close()
        p = 1.0*rightCount/len(fileList)
        r = 1.0*rightCount/len(staList)
        f = 2.0*p*r/(p+r)

        return str(p),str(r),str(f)
    """ count the number of the same words between two different list
        staList: standard list, which contains the standard answer
        fileList:the list you want to test
    """
    def inter(self,staList,fileList):
        staLen=len(staList)
        fileLen=len(fileList)
        i,j=0,0
        unmatchedI,unmatchedJ=0,0
        wordLenI,wordLenJ=0,0
        rightCount=0
        while i<staLen and j<fileLen:
            countFlag=0
            if unmatchedI==0 and unmatchedJ==0:#if the code read two words, register it in countFlag
                countFlag=1
                wordLenI=len(staList[i])#get the length of next word
                unmatchedI=wordLenI
                wordLenJ=len(fileList[j])
                unmatchedJ=wordLenJ
                i+=1
                j+=1
            elif unmatchedI==0:
                wordLenI=len(staList[i])
                unmatchedI=wordLenI
                i+=1
            elif unmatchedJ==0:
                wordLenJ=len(fileList[j])
                unmatchedJ=wordLenJ
                j+=1
            
            if unmatchedI>unmatchedJ:#compare the length of unmatched word
                unmatchedI-=unmatchedJ
                unmatchedJ=0
            elif unmatchedI<unmatchedJ:
                unmatchedJ-=unmatchedI
                unmatchedI=0
            elif unmatchedI==unmatchedJ:
                unmatchedI=0
                unmatchedJ=0
                if countFlag:
                    rightCount+=1
        return rightCount     
def Q3_3(BMMPath="seg_BMM.txt",FMMPath="seg_FMM.txt",path="199801_seg.txt",score="score.txt"):
    outputFile=open("score.txt","w",encoding="utf-8")
    precisio1,recall1,f1=Estimation.precisionAndRecall(None,open(FMMPath,"r",encoding="utf-8"),open(path,"r",encoding="utf-8"))
    precisio2,recall2,f2=Estimation.precisionAndRecall(None,open(BMMPath,"r",encoding="utf-8"),open(path,"r",encoding="utf-8"))
    outputFile.write("FMM\n") 
    outputFile.write("precision: "+precisio1+"\n")
    outputFile.write("recall: "+recall1+"\n")
    outputFile.write("F:"+str(f1)+"\n")
    outputFile.write("BMM\n") 
    outputFile.write("precision: "+precisio2+"\n")
    outputFile.write("recall: "+recall2+"\n")
    outputFile.write("F:"+str(f2)+"\n")
    outputFile.close()
if __name__=="__main__":
    Q3_3()