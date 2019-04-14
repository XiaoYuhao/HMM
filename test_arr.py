#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-

import codecs
import sys
import math
import pickle
from collections import defaultdict

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




if __name__ == '__main__':
#	input_file=sys.argv[1]
#	output_file=input_file+'.test'
#	gold_file=input_file+'.gold'
#	make_test(input_file,output_file)
#	make_gold(input_file,gold_file)

	input_file=sys.argv[1]
	gold_file=sys.argv[2]
	score(input_file,gold_file)
