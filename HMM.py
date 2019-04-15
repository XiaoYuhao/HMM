#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-

import codecs
import sys
import math
import pickle
from collections import defaultdict

#中文分词
#转移概率
#P(ti|ti-1)=(训练集中ti出现在ti-1之后的次数)/(训练集中ti-1出现的次数)
#输出概率
#p(wi|ti)=(训练集中wi的标记被标记为ti的次数)/(训练集中ti出现的次数)

#词性标注
#转移概率
#P(ti|ti-1)=(训练集中ti出现在ti-1之后的次数)/(训练集中ti-1出现的次数)
#输出概率
#p(wi|ti)=(训练集中wi的词性被标记为ti的次数)/(训练集中ti出现的次数)

#名词 	n
#时间词 	t
#处所词	s
#方位词	f
#数词	m
#量词	q
#区别词	b
#代词	r
#动词	v
#形容词	a
#状态词	z
#副词	d
#介词	p
#连词	c
#助词	u
#语气词	y
#叹词	e
#拟声词	o
#成语	i
#习用语	l
#简称	j
#前接成分	h
#后接成分	k
#语素	g
#非语素字	x
#标点符号	w
#人名	nr
#地名	ns
#团体机关单位名称	nt
#其他专用名词
#名语素	Ng
#动语素	Vg
#形容语素	Ag
#时语素	Tg
#副语素	Dg
#...

class HMM:
	def __init__(self):
		self._words=set([])		#词集合
		self._tags=set([])		#词性集合
		self._word_tag_num=defaultdict(int)	#每个词对应的标签的个数
		self._words_num=defaultdict(int)	#训练集中词的个数
		self._tags_num=defaultdict(int)		#训练集中词性次数
		self._tags_tran=defaultdict(int)	#训练集中ti出现在ti-1之后的次数

		self._swords=set([])				#字集合
		self._stags=set([])					#标记集合
		self._sword_stag_num=defaultdict(int)	#每个字和对应标记出现的次数
		self._swords_num=defaultdict(int)		#训练集中字的个数
		self._stags_num=defaultdict(int)		#训练集中标注的个数
		self._stags_tran=defaultdict(int)		#训练集中ti出现在ti-1之后的次数


	def load_file(self,file_name):
		input_data=codecs.open(file_name,"r","utf-8",'ignore')
		last_tag='null'
		cword=[]
		last_ctag='null'
		last_stag='null'
		flag=0
		for line in input_data.readlines():
			words_list=line.strip().split()	#对每一行进行切片处理

			#print (words_list)
			for words in words_list:

				word_tag=words.split('/')
				if word_tag[0][0]=='[':
				#	print (word_tag)
					word_tag[0]=word_tag[0].strip('[')
					cword.append(word_tag[0])
					last_ctag=last_tag
					flag=1
				#	print (word_tag)
				elif flag==1:
					cword.append(word_tag[0])


				#print (word_tag)

				ctag=word_tag[1].split(']')
				if len(ctag)==2:
				#	print (word_tag)
				#	cword.append(word_tag[0])
					strr=''.join(cword)
					self._words.add(strr)
					self._tags.add(ctag[1])
					self._words_num[strr]+=1
					self._tags_num[ctag[1]]+=1
					self._word_tag_num[(strr,ctag[1])]+=1
					self._tags_tran[(ctag[1],last_ctag)]+=1
				#	print (strr,ctag[1],last_ctag)
					flag=0
					cword.clear()

				word=word_tag[0]
				tag=ctag[0]
				self._words.add(word)
				self._tags.add(tag)
				self._words_num[word]+=1
				self._tags_num[tag]+=1
				self._word_tag_num[(word,tag)]+=1
				self._tags_tran[(tag,last_tag)]+=1
				last_tag=tag

				#对于训练集出现的每一个词
				if (1==len(word)):
					self._swords.add(word)
					self._stags.add('S')
					self._swords_num[word]+=1
					self._stags_num['S']+=1
					self._sword_stag_num[(word,'S')]+=1
					self._stags_tran['S',last_stag]+=1
					last_stag='S'
				else:
					self._swords.add(word[0])
					self._stags.add('B')
					self._swords_num[word[0]]+=1
					self._stags_num['B']+=1
					self._sword_stag_num[(word[0],'B')]+=1
					self._stags_tran['B',last_stag]+=1
					last_stag='B'
					for w in word[1:len(word)-1]:
						self._swords.add(w)
						self._stags.add('M')
						self._swords_num[w]+=1
						self._stags_num['M']+=1
						self._sword_stag_num[w,'M']+=1
						self._stags_tran['M',last_stag]+=1
						last_stag='M'
					self._swords.add(word[-1])
					self._stags.add('E')
					self._swords_num[word[-1]]+=1
					self._stags_num['E']+=1
					self._sword_stag_num[word[-1],'E']+=1
					self._stags_tran['E',last_stag]+=1
					last_stag='E'


	def show_data(self):
		#print (self._words)
		#print (self._tags)
		#for word in self._words:
		#	print (word,self._words_num[word])
		#for tag in self._tags:
		#	print (tag,self._tags_num[tag])

		#print (self._tags_tran)

		for sword in self._swords:
			print (sword,self._swords_num[sword])
		for stag in self._stags:
			print (stag,self._stags_num[stag])


	def _sperdict(self,line):
		N=len(line)
		M=len(self._stags_num)
		#print (M)
		swords=list(self._swords)
		stags=list(self._stags)

		P1=[[0 for i in range(M)] for j in range(N)]
		P2=[[0 for i in range(M)] for j in range(M)]
		flag=0
		for i in range(0,N):
			for j in range(0,M):
				p=self._sword_stag_num[(line[i],stags[j])]/self._stags_num[stags[j]]
				if line[i]==u"共" and flag==0:
					print (stags[j])
					print (self._sword_stag_num[(line[i],stags[j])],self._stags_num[stags[j]])
					print (math.log(p))
				if p==0:
					p=0.0000000001
				P1[i][j]=math.log(p)
			flag=1

		for i in range(0,M):
			for j in range(0,M):
				p=self._stags_tran[(stags[i],stags[j])]/self._stags_num[stags[j]]
				if p==0:
					p=0.0000000001
				P2[i][j]=math.log(p)



		DP=[[0 for i in range(M)] for j in range(N)]
		ans=[0 for i in range(N)]

		mmax=-3.14e+100
		#btags=['S','B']	#最开始的字只能是S或B开头
		for j in range(0,M):
			if stags[j]=='S':
				DP[0][j]=-1.4652633398537678+P1[0][j]
			elif stags[j]=='B':
				DP[0][j]=-0.26268660809250016+P1[0][j]
			elif stags[j]=='M':
				DP[0][j]=-3.14e+100
			else:
				DP[0][j]=-3.14e+100
			if DP[0][j]>mmax:
				mmax=DP[0][j]
				ans[0]=stags[j]

		#	p1=(self._sword_stag_num[(line[0],stags[j])]/self._stags_num[stags[j]])
		#	if p1==0:
		#		p1=0.001
		#	DP[0][j]=math.log(p1)
		#	if DP[0][j]>mmax:
		#		mmax=DP[0][j]
		#		ans[0]=stags[j]

		for i in range(1,N):
			imax=-3.14e+100
			for j in range(0,M):
				jmax=-3.14e+100
				for k in range(0,M):
					p3=DP[i-1][k]+P1[i][j]+P2[j][k]
					if p3>jmax:
						jmax=p3
				DP[i][j]=jmax
			for j in range(0,M):
				if DP[i][j]>imax:
					imax=DP[i][j]
					ans[i]=stags[j]

		return ans

	def stest(self,test_file,result_file):
		fin=codecs.open(test_file,'r','utf-8')
		fout=codecs.open(result_file,'w','utf-8')
		for line in fin.readlines():
			line=line.strip()
			if len(line)==0:
				continue
			ans=self._sperdict(line)
			j=0
			#wordl=[]
			for i in range(0,len(ans)):
				if ans[i]=='S':
					fout.write(line[j])
					j+=1
					fout.write('  ')
					#wordl.clear()
				elif ans[i]=='B':
					fout.write(line[j])
					#wordl.append(line[j])
					j+=1
				elif ans[i]=='M':
					fout.write(line[j])
					#wordl.append(line[j])
					j+=1
				else:
					fout.write(line[j])
					#wordl.append(line[j])
					j+=1
					#w=''.join(wordl)
					#fout.write(w)
					fout.write('  ')
					#wordl.clear()
			fout.write('\n')
		fin.close()
		fout.close()

	def _perdict(self,words_list):
		N=len(words_list)
		M=len(self._tags_num)
		words=list(self._words)
		tags=list(self._tags)

		P1=[[0 for i in range(M)] for j in range(N)]
		P2=[[0 for i in range(M)] for j in range(M)]

		for i in range(0,N):
			for j in range(0,M):
				p=(self._word_tag_num[(words_list[i],tags[j])])/self._tags_num[tags[j]]
				if p==0:
					p=0.000000001
				P1[i][j]=math.log(p)

		for i in range(0,M):
			for j in range(0,M):
				p=self._tags_tran[(tags[i],tags[j])]/self._tags_num[tags[j]]
				if p==0:
					p=0.000000001
				P2[i][j]=math.log(p)

		#DP=[[0]*M]*N
		#print (P1)
		#print (P2)
		DP=[[0 for i in range(M)] for j in range(N)]
		ans=[0 for i in range(N)]
		mmax=-3.14e+100
		mult=1000

		for j in range(0,M):
			DP[0][j]=P1[0][j]
			if DP[0][j]>mmax:
				mmax=DP[0][j]
				ans[0]=tags[j]


		for i in range(1,N):
			imax=-3.14e+100
			for j in range(0,M):
				jmax=-3.14e+100
				for k in range(0,M):
					p3=DP[i-1][k]+P1[i][j]+P2[j][k]
					if p3>jmax:
						jmax=p3
				DP[i][j]=jmax
			for j in range(0,M):
				if DP[i][j]>imax:
					imax=DP[i][j]
					ans[i]=tags[j]
		#print (ans)
		return ans

	def test(self,test_file,result_file):

		fin=codecs.open(test_file,"r","utf-8")
		fout=codecs.open(result_file,"w","utf-8")
		for line in fin.readlines():
			words_list=line.strip().split()
			if len(words_list)==0:
				fout.write('\n')
				continue
			ans=self._perdict(words_list)
			for i in range(0,len(words_list)):
				fout.write(words_list[i])
				fout.write('/')
				fout.write(ans[i])
				fout.write('  ')
			fout.write('\n')
		fin.close()
		fout.close()





if __name__ == '__main__':
	train_file=sys.argv[1]
	test_file=sys.argv[2]
	result_file=test_file+'.result'
	h=HMM()
	h.load_file(train_file)
	#h.show_data()
	#h.test(test_file,result_file)
	h.stest(test_file,result_file)

 