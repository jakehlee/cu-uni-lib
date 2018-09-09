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

	result_div = driver.find_elements_by_xpath("//div[@class='table_results_indiv']/table/tbody/tr/td")
	print(len(result_div))

	# clean up output
	clean_output = []
	for a_td in result_div:
		if a_td.text != '' and a_td.text != ' ':
			clean_output.append(a_td.text)
	print(len(clean_output))
	print(clean_output)

	if len(clean_output) == 0:
		# invalid UNI
		return affiliate
	else:
		# valid UNI
		affiliate.valid = True
	return affiliate
	#result_div = driver.find_elements_by_css_selector('div.table_results_indiv tr')
	#for a_row in result_div:
	#	print(a_row.text)

def test_get_affil_info():
	test_obj = get_affil_info('lcb50')
	assert test_obj.uni == 'lcb50'
	assert test_obj.valid == True
	test_obj2 = get_affil_info('aaa11')
	assert test_obj2.uni == 'aaa11'
	assert test_obj2.valid == False

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