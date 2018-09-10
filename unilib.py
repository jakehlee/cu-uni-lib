#!/usr/bin/env python 

import os
import csv
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys	import Keys
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")


class AffilInfo:
	""" Objects to store affiliate information """
	def __init__(self):
		self.valid = False
		self.uni = ""
		self.tel = ""
		self.c_tel = ""
		self.fax = ""
		self.title = ""
		self.dept = ""
		self.addr = ""
		self.title2 = ""
		self.dept2 = ""
		self.addr2 = ""
		self.h_addr = ""
		self.email = ""

def get_affil_info(uni):
	affiliate = AffilInfo()
	affiliate.uni = uni

	driver = webdriver.Chrome(chrome_options=chrome_options)
	driver.get("https://directory.columbia.edu/people/uni?code="+uni)
	# 
	assert "Columbia University: Directory" == driver.title

	name = driver.find_element_by_xpath("//div[@class='table_results_indiv']/table/tbody/tr/th").text
	result_tds = driver.find_elements_by_xpath("//div[@class='table_results_indiv']/table/tbody/tr/td")

	# clean up output
	clean_output = []
	for a_td in result_tds:
		if a_td.text != '' and a_td.text != ' ':
			clean_output.append(a_td.text)

	if len(clean_output) == 0:
		# invalid UNI
		return affiliate
	else:
		# valid UNI
		affiliate.valid = True

	# UNI is valid, fill in fields
	affiliate.name = name
	t = 0
	d = 0
	a = 0
	for i in range(len(clean_output)):
		if clean_output[i] == 'Title:' and not t:
			i += 1
			affiliate.title = clean_output[i]
			t = 1
		elif clean_output[i] == 'Title:' and t:
			i += 1
			affiliate.title2 = clean_output[i]
		if clean_output[i] == 'Tel:':
			i += 1
			affiliate.tel = clean_output[i]
		if clean_output[i] == 'Department:' and not d:
			i += 1
			affiliate.dept = clean_output[i]
			d = 1
		elif clean_output[i] == 'Department:' and d:
			i += 1
			affiliate.dept2 = clean_output[i]
		if clean_output[i] == 'Campus Tel:':
			i += 1
			ct = clean_output[i]
			if ct[-6:] == '(help)':
				ct = ct[:-8]
				affiliate.c_tel = ct
			else:
				affiliate.c_tel = ct
		if clean_output[i] == 'Address:' and not a:
			i += 1
			affiliate.addr = clean_output[i]
			a = 1
		elif clean_output[i] == 'Address:' and a:
			i += 1
			affiliate.addr2 = clean_output[i]
		if clean_output[i] == 'Email:':
			i += 1
			affiliate.email = clean_output[i].split()[0]
		if clean_output[i] == 'Home Addr:':
			i += 1
			affiliate.h_addr = clean_output[i]

	return affiliate

def test_get_affil_info():
	test_obj = get_affil_info('lcb50')
	assert test_obj.uni == 'lcb50'
	assert test_obj.valid == True
	assert test_obj.name == 'Lee C. Bollinger'
	assert test_obj.title == 'President Columbia University; Seth Low Professor of the University'
	assert test_obj.tel == '+1 212 854 9970'
	assert test_obj.dept == 'Office of the President'
	assert test_obj.c_tel == 'MS 4-9970'
	assert test_obj.addr == '202 Low Library\nMail Code: 4309\nUnited States'
	assert test_obj.email == 'bollinger@columbia.edu'
	assert test_obj.dept2 == 'School of Law'
	test_obj2 = get_affil_info('aaa11')
	assert test_obj2.uni == 'aaa11'
	assert test_obj2.valid == False
	test_obj3 = get_affil_info('jwl3')
	assert test_obj3.uni == 'jwl3'
	assert test_obj3.valid == True
	assert test_obj3.title == 'Senior Lecturer in the Discipline of Computer Science in the Department of Computer Science'
	assert test_obj3.tel == '+1 212 939 7000'
	assert test_obj3.dept == 'Department of Computer Science'
	assert test_obj3.addr == '450 Computer Science Building\nMail Code: 0401\nUnited States'
	assert test_obj3.email == 'jwlee@barnard.edu'
	assert test_obj3.title2 == 'University Affiliate'
	assert test_obj3.dept2 == 'Dean of Studies, Barnard College'
	assert test_obj3.addr2 == 'None Listed\nNew York NY 10027'

def is_valid_uni(uni):
	""" Validate the syntax of a uni string """
	# UNIs are (2 or 3 letters) followed by (1 to 4 numbers)
	# total length 3~7
	if not isinstance(uni,str):
		return False
	if len(uni) < 3 or len(uni) > 7:
		return False

	if uni[:3].isalpha():
		# 3 letters
		return uni[3:].isnumeric()
	elif uni[:2].isalpha():
		# 2 letters
		return uni[2:].isnumeric()
	else:
		return False

def test_is_valid_uni():
	assert is_valid_uni('abc1234')
	assert is_valid_uni('ab1234')
	assert not is_valid_uni('1234567')
	assert not is_valid_uni('123456')
	assert not is_valid_uni('abcdefg')
	assert not is_valid_uni('abcdef')
	assert not is_valid_uni('a123')
	assert not is_valid_uni('abcd123')
	assert not is_valid_uni('abc12345')

	# Bollinger's UNI
	assert is_valid_uni('lcb50')
	# Jae's UNI
	assert is_valid_uni('jwl3')

if __name__ == "__main__":
	test_is_valid_uni()
	test_get_affil_info()