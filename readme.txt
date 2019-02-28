一、3.1-3.4文件夹中存了3.1-3.4的程序。
	(1)其中EstablishDic.py包含了3.1构建词典(Trie.readSeg函数)，3.2正反向最大匹配(MM.FMM和MM.BMM函数,MM.MMForFile函数		调用FMM和BMM将199801_seg.txt分词并输出到文件),3.4速度优化(在MM.MMForFile函数中分词部分有函数调用time.time()语句。该		语句进行时间统计)。直接运行EstablishDic.py可以构建词典并分词
	(2)Estimation.py中包含了3.3的性能分析的程序(Estimation.precisionAndRecall函数用于计算准确率和召回率，Estimation.Q3_3函数调		用该函数计算FMM和BMM的准确率召回率并输出)。直接运行Estimation.py可对分词结果进行评估
二、3.5-含未登录词识别的隐马尔可夫模型
	HHM.py中为隐马尔可夫模型。主要的函数为initParameter和viterbi，分别初始化参数和分词。加入了几个未登录词识别的函数。			oovDic.txt为未登录词的词典。


注意：1.前四问中，我对199801_seg.txt进行了处理。我用nodepad++将其中每行开始的时间词去掉了，并且把中括号（例如：[中国/ns  政府/n]nt）去掉了，并且把每个词的词性删掉了。EstablishDic.txt和Estimation.txt所用的标准文本是这个被处理过的199801_seg.txt。
2.在第五问中的文本处理
(1)在带分词的隐马尔可夫中，我对199801_seg.txt进行了处理。我用nodepad++将每行开始的时间词去掉了，并且把中括号全去了，保留了词和词性
3.所有199801_seg.txt和199801_sent.txt中的空行均去了，为了程序的方便，如果加上可能会引起程序出错
4.在输出的文本中用'/ '进行分词，并且在句末没有'/ '
5.第五问中隐马尔科夫模型的运行时间很长，20000句分词大概用20分钟到30分钟。并且该程序每分100行会打印下完成的行数




