#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-

import codecs
import sys
import math
import pickle
from collections import defaultdict

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


	def load_file(self,file_name):
		input_data=codecs.open(file_name,"r","utf-8",'ignore')
		last_tag='null'
		cword=[]
		last_ctag='null'
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

	def show_data(self):
		#print (self._words)
		#print (self._tags)
		for word in self._words:
			print (word,self._words_num[word])
		for tag in self._tags:
			print (tag,self._tags_num[tag])

		print (self._tags_tran)



	def _perdict(self,words_list):
		
		N=len(words_list)
		M=len(self._tags_num)
		#DP=[[0]*M]*N
		DP=[[0 for i in range(M)] for j in range(N)]
		ans=[0 for i in range(N)]
		mmax=0
		words=list(self._words)
		tags=list(self._tags)
		#print (N)
		#print (words_list)
		#print (len(tags),M)
		#print (tags)
		mult=1000
		for j in range(0,M):
			#print (self._word_tag_num[(words_list[0],tags[j])],self._tags_num[tags[j]])
			p1=(self._word_tag_num[(words_list[0],tags[j])]/self._tags_num[tags[j]])*mult
			if p1==0:
				p1=0.000001
			DP[0][j]=p1
			#print (DP[0][j])
			if DP[0][j]>mmax:
				mmax=DP[0][j]
				ans[0]=tags[j]


		for i in range(1,N):
			imax=-10
			for j in range(0,M):
				jmax=-10
				p1=(self._word_tag_num[(words_list[i],tags[j])])/self._tags_num[tags[j]]
				if p1==0:
					p1=0.000001
				#print (words_list[i],tags[j],self._word_tag_num[(words_list[i],tags[j])])
				#print (tags[j],self._tags_num[tags[j]])
				#print ("p1=%g" %(p1))
				#if self._word_tag_num[(words_list[i],tags[j])]>0:
				#	print (words_list[i],tags[j])
				#	print (self._word_tag_num[(words_list[i],tags[j])],self._tags_num[tags[j]])
				#	print (p1)
				for k in range(0,M):
					p2=self._tags_tran[(tags[j],tags[k])]/self._tags_num[tags[k]]
					#print (tags[j],tags[k],self._tags_tran[(tags[j],tags[k])])
					#print (tags[k],self._tags_num[tags[k]])
					#print ("p2=%g" %(p2))
					#print ("DP[%d][%d]=%g" %(i-1,k,DP[i-1][k]))
					p3=DP[i-1][k]*p1*p2
					#p3=p1*p2
					#print ("p3=%g" %(p3))
					if p3>jmax:
						jmax=p3
				#print ("jmax=%g" %(jmax))
				DP[i][j]=jmax*mult
				#print ("DP[%d][%d]=%g" %(i,j,DP[i][j]))
			for j in range(0,M):
				if DP[i][j]>imax:
					imax=DP[i][j]
					ans[i]=tags[j]
			#print (DP[i])

		#for i in range(0,N):
		#	print (DP[i])

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
	h.test(test_file,result_file)

 