# SubDoc
Generate subroutine documentation in seconds

Usage: ./makeSubDoc.py inputfile.csv

inputfile.csv is a tab-separated file that contains:
1: The following columns in the following order: NAME	CHANGED_BY	CHANGED_ON	DESCRIPTION	GROUP_NAME	SOURCE_CODE

2: Necessary information needed to create the documentation. This information is obtained by executing the following query to the LIMS database:
SELECT NAME,CHANGED_BY,CHANGED_ON,DESCRIPTION,GROUP_NAME,SOURCE_CODE 
FROM SUBROUTINE WHERE REMOVED = 'F' AND GROUP_NAME != 'HIDDEN'
ORDER BY NAME 
