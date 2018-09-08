#!/usr/bin/env python 

import os
import csv
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys	import Keys

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