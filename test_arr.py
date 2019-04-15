#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-

import codecs
import sys
import math
import pickle
from collections import defaultdict

def make_stest(input_file,output_file):
	fin=codecs.open(input_file,'r','utf-8')
	fout=codecs.open(output_file,'w','utf-8')

	for line in fin.readlines():
		word_list=line.strip().split()
		word_line=''.join(word_list)
		fout.write(word_line)
		fout.write("\n")

	fin.close()
	fout.close()

def make_test(input_file,output_file):
	fin=codecs.open(input_file,"r","utf-8")
	fout=codecs.open(output_file,"w","utf-8")

	for line in fin.readlines():
		words_list=line.strip().split();
		for word in words_list:
			word_tag=word.split('/')
			if word_tag[0][0]=='[':
				word_tag[0]=word_tag[0].strip('[')
			fout.write(word_tag[0])
			fout.write("  ")
		fout.write('\n')

	fin.close()
	fout.close()

def make_gold(input_file,output_file):
	fin=codecs.open(input_file,"r","utf-8")
	fout=codecs.open(output_file,"w","utf-8")

	for line in fin.readlines():
		words_list=line.strip().split()
		for word in words_list:
			word_tag=word.split('/')
			if word_tag[0][0]=='[':
				word_tag[0]=word_tag[0].strip('[')
			tag=word_tag[1].split(']')

			fout.write(word_tag[0])
			fout.write('/')
			fout.write(tag[0])
			fout.write("  ")
		fout.write('\n')

	fin.close()
	fout.close()

def score(result_file,gold_file):
	fina=codecs.open(result_file,"r","utf-8")
	finb=codecs.open(gold_file,"r","utf-8")
	data1=fina.read()
	data2=finb.read()
	words1=data1.strip().split()
	words2=data2.strip().split()
	len1=len(words1)
	len2=len(words2)
	if len1!=len2:
		print ("错误！结果文件与标准文件词数不一致")
		return 0

	wrong=0
	correct=0
	for i in range(0,len1):
		if words1[i]==words2[i]:
			correct+=1
		else:
			wrong+=1

	p=correct/len1
	print ("总词数：%d" %(len1))
	print ("正确标注词数：%d" %(correct))
	print ("错误标注词数：%d" %(wrong))
	print ("正确率：%g" %(p))


def inter_socre(result_file,std_file):
	fina=codecs.open(result_file,'r','utf-8')
	finb=codecs.open(std_file,'r','utf-8')
	linea=fina.readlines()
	lineb=finb.readlines()
	correct=0
	counta=0
	countb=0
	for i in range(0,len(linea)):
		worda_list=linea[i].strip().split()
		wordb_list=lineb[i].strip().split()
		words=defaultdict(int)
		for worda in worda_list:
			word_tag=worda.split('/')
			word=word_tag[0]
			tag=word_tag[1]
			words[(word,tag)]+=1
			counta+=1

		for wordb in wordb_list:
			word_tag=wordb.split('/')
			word=word_tag[0]
			tag=word_tag[1]
			words[(word,tag)]+=1
			countb+=1

		for value in words.values():
			if value>=2:
				correct+=math.floor(value/2)

	p=correct/counta
	r=correct/countb
	f=(2*p*r)/(p+r)
	
	print ("正确标注数：%d" %(correct))
	print ("结果文件中总词数：%d" %(counta))
	print ("正确率(P)：%g" %(p))
	print ("标准文件中总词数：%d" %(countb))
	print ("召回率(R):%g" %(r))
	print ("测度值(F):%g" %(f))




if __name__ == '__main__':
#	input_file=sys.argv[1]
#	output_file=input_file+'.test'
#	gold_file=input_file+'.gold'
#	make_test(input_file,output_file)
#	make_gold(input_file,gold_file)

#	input_file=sys.argv[1]
#	gold_file=sys.argv[2]
#	score(input_file,gold_file)

#	make_stest:
#	input_file=sys.argv[1]
#	output_file=input_file+'.stest'
#	make_stest(input_file,output_file)

	input_file=sys.argv[1]
	gold_file=sys.argv[2]
	inter_socre(input_file,gold_file)

	