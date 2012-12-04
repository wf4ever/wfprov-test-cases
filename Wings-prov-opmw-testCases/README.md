WINGS test cases
=================
* Test Case 1: Find out the workflow template from a run id.
* Test Case 2: Find out the runs of a particular workflow.
* Test Case 3: Find out the outputs of a particular run.
* Test Case 4: Find out the intputs of a particular run.
* Test Case 5: Find out the processes executed in a particular run.
* Test Case 6: Find out the services executed for all the processes taken place in a particular run.
* Test Case 7: Find out which inputs belonged to each process, given a run.
* Test Case 8: Find out what outputs were produced by a particular process
* Test Case 9: Find out when the workflow run was started.
* Test Case 10: Find out when the workflow run finished.
* Test Case 11: Find out who executed the workflow.
* Test Case 12: Find out the executions that failed and the workflow they belong to.
* Test Case 13: Tell me for each workflow the successful executions I can find.
* Test Case 14: Given a specific component of the component catalog/service, in which templates is it used?.
* Test Case 15: What are the most used components across the workflows? How many times are they used.
* Test Case 16: Title/name of the workflow (label).
* Test Case 17: Designer of the workflow.

Endpoint
========
* This program performs queries to the OPMW endpoint: http://www.opmw.org/sparql

Execution
=========
Executing the test: An internet connection is required.
* Download /dist folder
* Double click on ProvTestCases-Wings.jar. The jar needs to be in the same folder where the /Lib files are.
* Select the text case to test or test all test cases in the interface. For each one a OK/FAIL message will appear
on the LOG window. 

Additional considerations
==========
All values are static at the moment. If you want to change them then go to the Constants Class
in the /src folder and add the value you want.

