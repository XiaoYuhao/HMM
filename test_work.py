#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-

import codecs
import sys
import math
from collections import defaultdict

global correct



def tag_test(test_file,test_tag_file):
	fin=codecs.open(test_file,'r','utf-8')
	fout=codecs.open(test_tag_file,'w','utf-8')

	for line in fin.readlines():
		words_list=line.strip().split();
		for word in words_list:
			if(1==len(word)):
				fout.write(word+"/S")
			else:
				fout.write(word[0]+"/B")
				for w in word[1:len(word)-1]:
					fout.write(w+'/M')
				fout.write(word[-1]+'/E')
		#fout.write('\n')

	fin.close()
	fout.close()

def tag_compare(test_file_a,std_file):
	fin_a=codecs.open(std_file,"r","utf-8")
	fin_b=codecs.open(test_file_a,"r","utf-8")
	#fout=codecs.open(diff_file,"w","utf-8")
	diff_list=[]
	diff_count=0
	total=0

	contents_a=fin_a.read()
	contents_b=fin_b.read()
	#index=range(0,len(contents_a))
	words_len=len(contents_a)	
	i=0

	while i<words_len:
		if(contents_b[i]=='S'):
			total+=1
			if(contents_a[i]!='S'):
				diff_count+=1
		if(contents_b[i]=='B'):
			flag=0
			while i<words_len:
				if(contents_a[i]!=contents_b[i]):
					flag=1
				if(contents_b[i]=='E'):
					total+=1
					break
				i+=1
			if flag==1:
				diff_count+=1
		i+=1
	global correct		
	correct=total-diff_count
	print ("分词结果中总词数：%d" %(total))
	print ("分词结果中正确切分的总词数：%d" %(correct))
	p=correct/total
	print ("正确率(P)=%g" %(p))
	fin_a.close()
	fin_b.close()

	return p


def words_count(std_file):
	fin=codecs.open(std_file,"r","utf-8")
	contents=fin.read()
	count=0
	words_len=len(contents)
	i=0

	while i<words_len:
		if(contents[i]=='S'):
			count+=1
		if(contents[i]=='B'):
			while i<words_len:
				if(contents[i]=='E'):
					count+=1
					break
				i+=1
		i+=1

	print ("标准文本中总词数：%d" %(count))
	return count


if __name__ == '__main__':
	test_file=sys.argv[1]
	std_file=sys.argv[2]
	test_tag_file=test_file+'.tag'
	std_tag_file=std_file+'.tag'
	#diff_file=test_file_a+'.diff'
	tag_test(test_file,test_tag_file)
	tag_test(std_file,std_tag_file)
	p=tag_compare(test_tag_file,std_tag_file)
	count=words_count(std_tag_file)
	global correct
	r=correct/count
	f=(2*p*r)/(p+r)
	print ("召回率(R)=%g" %(r))
	print ("F度量值(F1)=%g" %(f))
