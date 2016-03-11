#!/usr/bin/python
# -*- coding: utf-8 -*-

######################################################################################
#
# Written by: Niklas Malmqvist, 2014-10-29
#
# Description:
# ------------
# Generates a documentation text file that contains the header info and description
# for all subroutines in the import file. All calls to other subroutines (GoSub and
# Subroutine) are also listed for each subroutine. A tree-list of all nested calls
# is also generated and displayed at the end of the output text file. Calls to 
# unknown subroutines are ignored.
#
# Input file format:
# ------------------
# Tab-separated text file containing the following columns in the following order:
# NAME	CHANGED_BY	CHANGED_ON	DESCRIPTION	GROUP_NAME	SOURCE_CODE
# 
# Query used to generate import data in the file:
# -----------------------------------------------
# SELECT NAME,CHANGED_BY,CHANGED_ON,DESCRIPTION,GROUP_NAME,SOURCE_CODE 
# FROM SUBROUTINE WHERE REMOVED = 'F' AND GROUP_NAME != 'HIDDEN'
# ORDER BY NAME 
#
######################################################################################

import sys
import re
import datetime

def makeMatchPretty(matchtext):
	 return matchtext.replace(" '","\n")

def printCallsRec(calledSub, dictOfCalls, parentNodes, depth):
	listOfCalls = []
	listOfCalls = dictOfCalls.get(calledSub, "")
	identation = depth * "\t"
	treeString = ""
	if listOfCalls and calledSub not in parentNodes:
		parentNodes.append(calledSub)
		for call in listOfCalls:
			treeString += "\n" + identation + call + printCallsRec(call, dictOfCalls, parentNodes, (depth+1))
		return treeString
	else:
		return treeString

def constructCallTree(dictOfCalls):
	callTreeContent = ""
	keyList = []
	for key in dictOfCalls:
		keyList.append(key)
	
	keyList = sorted(keyList)	
	
	for key in keyList:
		callTreeContent += "\n" + key + printCallsRec(key, dictOfCalls, [], 1) + "\n"

	return callTreeContent

def getSubCalls(sourcetext):
	gosubCalls = []
	matches = re.findall(r'(GOSUB\s+|SUBROUTINE\(\")([\w\_\w]+)', sourcetext, re.IGNORECASE)
	if matches:
		for match in matches:
			matchAsText = str(match[1])
			if matchAsText not in gosubCalls:
				gosubCalls.append(str(match[1]))
	
	return gosubCalls

def extractHeaderInfo(sourcetext):
	headerInfo = ""
	match = re.search(r'(Abstract\:.*)Inputs:', sourcetext)
	if match:
		headerInfo += makeMatchPretty(match.group(1))
		
	match = re.search(r'(Inputs\:.*)Outputs:', sourcetext)
	if match:
		headerInfo += makeMatchPretty(match.group(1))
		
	match = re.search(r'(Outputs\:.*)Change\s+History:', sourcetext)
	if match:
		headerInfo += makeMatchPretty(match.group(1))
		
	return headerInfo

def main():

	if len(sys.argv) < 2:
		print "Missing input!"
		sys.exit

	inFile = sys.argv[1]
	subCallsThisLine = []
	allSubCalls = {}
	now = datetime.datetime.now()
	
	fh = open(inFile, "rU")
	fw = open("SubroutineDocs.txt", "w")
	fw.write("######################################\n")
	fw.write(" SCARAB LIMS SUBROUTINE DOCUMENTATION\n")
	fw.write(" Generated: " + now.strftime("%Y-%m-%d %H:%M") + "\n")
	fw.write(" Input file: " + inFile + "\n")
	fw.write("######################################\n\n")
	
	for line in fh:
		splitline = line.split("\t")
		subName = splitline[0]
		subChangedBy = splitline[1]
		subChangedOn = splitline[2]
		subDesc = splitline[3]
		subGroupName = splitline[4]
		subSource = splitline[5]	
		
		subCallsThisLine = getSubCalls(subSource)
		allSubCalls[subName] = subCallsThisLine
		
		fw.write("Subroutine: " + subName + "\n")
		fw.write("Description: " + subDesc + "\n")
		fw.write("Changed by: " + subChangedBy + " on " + subChangedOn + "\n")
		fw.write("Group name: " + subGroupName + "\n")
		fw.write(extractHeaderInfo(subSource) + "\n")
		fw.write("Subroutine calls:\n")
		for row in subCallsThisLine:
			fw.write(" " + row + "\n")
		fw.write("\n####################################\n\n")
	
	fh.close()
	fw.write("Subroutine call tree:\n")
	fw.write("---------------------\n")
	fw.write(constructCallTree(allSubCalls))	
	fw.close()
	
if __name__ == '__main__':
	main()