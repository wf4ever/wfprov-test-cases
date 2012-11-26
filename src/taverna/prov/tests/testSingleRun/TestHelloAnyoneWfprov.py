'''
Created on Sep 13, 2012

@author: zhaoj
'''

import os, os.path
import sys
import re
import unittest
import logging
import httplib
import urllib
try:
    # Running Python 2.5 with simplejson?
    import simplejson as json
except ImportError:
    import json

# Add main library directory to python path
sys.path.append("../../../..")
sys.path.append("..")

from MiscLib import TestUtils

from SparqlQueryTestCase import SparqlQueryTestCase


class TestHelloAnyoneWfprov(SparqlQueryTestCase):
    
    def setUp(self):
        super(TestHelloAnyoneWfprov, self).setUp()
        return

    def tearDown(self):
        super(TestHelloAnyoneWfprov, self).tearDown()
        return

    def testRUNOfAWorkflow(self):
        sparqlquery  = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX wfprov: <http://purl.org/wf4ever/wfprov> 
            prefix wfdesc: <http://purl.org/wf4ever/wfdesc> 
            SELECT distinct ?run
            WHERE {?run rdf:type wfprov:WorkflowRun; 
                wfprov:describedByWorkflow <http://www.myexperiment.org/workflows/2649/download?version=1> .
            }
            """
        data = self.doQueryPOST(sparqlquery, JSON=True)
        self.assertBindingCount(data, 1)
        
    def testRUNOfAWorkflow2(self):
        sparqlquery  = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX wfprov: <http://purl.org/wf4ever/wfprov#> 
            prefix wfdesc: <http://purl.org/wf4ever/wfdesc#> 
            SELECT distinct ?run
            WHERE {?run rdf:type wfprov:WorkflowRun; 
                wfprov:describedByWorkflow <http://ns.taverna.org.uk/2010/workflowBundle/01348671-5aaa-4cc2-84cc-477329b70b0d/workflow/Hello_Anyone/> .
            }
            """
        data = self.doQueryPOST(sparqlquery, JSON=True)
        self.assertBindingCount(data, 1)
    
    def testNumberOfWorkflowOutputsCOUNT(self):
        sparqlquery  = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX wfprov: <http://purl.org/wf4ever/wfprov#> 
            prefix wfdesc: <http://purl.org/wf4ever/wfdesc#>      
            SELECT distinct ?output
            WHERE {?output wfprov:wasOutputFrom [
                rdf:type wfprov:WorkflowRun ;
                wfprov:describedByWorkflow <http://ns.taverna.org.uk/2010/workflowBundle/01348671-5aaa-4cc2-84cc-477329b70b0d/workflow/Hello_Anyone/>  ]
            }
            """
        data = self.doQueryPOST(sparqlquery, JSON=True)
        self.assertBindingCount(data, 1)

    def testNumberOfWorkflowOutputsCOUNTProv(self):
        sparqlquery  = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX wfprov: <http://purl.org/wf4ever/wfprov#> 
            prefix wfdesc: <http://purl.org/wf4ever/wfdesc#>
            prefix prov: <http://www.w3.org/ns/prov#>       
            SELECT distinct ?output
            WHERE {?output prov:wasGeneratedBy [
                rdf:type wfprov:WorkflowRun ;
                wfprov:describedByWorkflow <http://ns.taverna.org.uk/2010/workflowBundle/01348671-5aaa-4cc2-84cc-477329b70b0d/workflow/Hello_Anyone/>  ]
            }
            """
        data = self.doQueryPOST(sparqlquery, JSON=True)
        self.assertBindingCount(data, 1)
    
    def testNumberOfWorkflowInputsCOUNT(self):
        sparqlquery  = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX wfprov: <http://purl.org/wf4ever/wfprov#> 
            prefix wfdesc: <http://purl.org/wf4ever/wfdesc#>  
            SELECT distinct ?input
            WHERE {?run rdf:type wfprov:WorkflowRun ;
                wfprov:describedByWorkflow <http://ns.taverna.org.uk/2010/workflowBundle/01348671-5aaa-4cc2-84cc-477329b70b0d/workflow/Hello_Anyone/> ;
                wfprov:usedInput ?input .
            }
            """
        data = self.doQueryPOST(sparqlquery, JSON=True)
        self.assertBindingCount(data, 1)
        
    def testNumberOfWorkflowInputsCOUNTProv(self):
        sparqlquery  = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX wfprov: <http://purl.org/wf4ever/wfprov#> 
            prefix wfdesc: <http://purl.org/wf4ever/wfdesc#>
            prefix prov: <http://www.w3.org/ns/prov#>  
            SELECT distinct ?input
            WHERE {?run rdf:type wfprov:WorkflowRun ;
                wfprov:describedByWorkflow <http://ns.taverna.org.uk/2010/workflowBundle/01348671-5aaa-4cc2-84cc-477329b70b0d/workflow/Hello_Anyone/> ;
                prov:used ?input .
            }
            """
        data = self.doQueryPOST(sparqlquery, JSON=True)
        self.assertBindingCount(data, 1)    
        
    def testWorkflowInputPatternSELECT(self):
        sparqlquery  = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
            PREFIX wfprov: <http://purl.org/wf4ever/wfprov#> 
            prefix wfdesc: <http://purl.org/wf4ever/wfdesc#>  
            prefix prov: <http://www.w3.org/ns/prov#>
            SELECT distinct ?input ?inputParameter ?label
            WHERE {?run rdf:type wfprov:WorkflowRun ;
                wfprov:describedByWorkflow <http://ns.taverna.org.uk/2010/workflowBundle/01348671-5aaa-4cc2-84cc-477329b70b0d/workflow/Hello_Anyone/> ;
                prov:qualifiedUsage [prov:hadRole ?inputParameter ].
               ?inputParameter rdfs:label ?label .
               filter regex (?label, "workflow input", "i")
            }
            """
        data = self.doQueryPOST(sparqlquery, JSON=True)
        self.assertBindingCount(data, 1)
    
    #### This fails because the generation of a bundle is also infrrmed by the workflow run
    
    def testNumberOfProcessRunsCount(self):
        sparqlquery  = """
            PREFIX prov: <http://www.w3.org/ns/prov#>
            PREFIX wfprov: <http://purl.org/wf4ever/wfprov#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
            prefix dct: <http://purl.org/dc/elements/1.1/> 
            SELECT distinct ?process
            WHERE { 
            ?run rdf:type wfprov:WorkflowRun ;
                wfprov:describedByWorkflow <http://ns.taverna.org.uk/2010/workflowBundle/01348671-5aaa-4cc2-84cc-477329b70b0d/workflow/Hello_Anyone/>  .
            ?process wfprov:wasPartOfWorkflowRun ?run .  
            }
            """
        data = self.doQueryPOST(sparqlquery, JSON=True)
        self.assertBindingCount(data, 2)
    
    def testStartTimeOfRunSelect(self):
        sparqlquery  = """
            PREFIX prov: <http://www.w3.org/ns/prov#>
            PREFIX wfprov: <http://purl.org/wf4ever/wfprov#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
            prefix dct: <http://purl.org/dc/elements/1.1/> 
            SELECT distinct ?start
            WHERE { 
            ?run rdf:type wfprov:WorkflowRun ;
                wfprov:describedByWorkflow <http://ns.taverna.org.uk/2010/workflowBundle/01348671-5aaa-4cc2-84cc-477329b70b0d/workflow/Hello_Anyone/>  ;
                 prov:startedAtTime ?start .
            }
            """
        data = self.doQueryPOST(sparqlquery, JSON=True)
        self.assertVarBinding(data, "start", "typed-literal", "2012-11-19T17:16:00.058Z")
#    
    def testEndTimeOfRunSelect(self):
        sparqlquery  = """
            PREFIX prov: <http://www.w3.org/ns/prov#>
            PREFIX wfprov: <http://purl.org/wf4ever/wfprov#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
            prefix dct: <http://purl.org/dc/elements/1.1/> 
            SELECT distinct ?end
            WHERE { 
            ?run rdf:type wfprov:WorkflowRun ;
                 wfprov:describedByWorkflow <http://ns.taverna.org.uk/2010/workflowBundle/01348671-5aaa-4cc2-84cc-477329b70b0d/workflow/Hello_Anyone/>  ;
                 prov:endedAtTime ?end .
            }
            """
        data = self.doQueryPOST(sparqlquery, JSON=True)
        self.assertVarBinding(data, "end", "typed-literal", "2012-11-19T17:16:04.574Z")
#    
        
    def testSourceArtifactsOfWfOutputCount(self):
        sparqlquery  = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX prov: <http://www.w3.org/ns/prov#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            prefix wfdesc: <http://purl.org/wf4ever/wfdesc#>
            PREFIX wfprov: <http://purl.org/wf4ever/wfprov#> 
            Select distinct ?input
            where {
                ?run rdf:type wfprov:WorkflowRun ;
                    wfprov:describedByWorkflow <http://ns.taverna.org.uk/2010/workflowBundle/01348671-5aaa-4cc2-84cc-477329b70b0d/workflow/Hello_Anyone/>  .
                ?output    prov:wasGeneratedBy ?run ; 
                           prov:wasGeneratedBy [
                               wfprov:wasPartOfWorkflowRun ?run; 
                               prov:used ?input ].
            }
            """
        data = self.doQueryPOST(sparqlquery, JSON=True)
        self.assertBindingCount(data, 2)
#    
    def testSourceActivitiesOfWfOutputCount(self):
        sparqlquery  = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX prov: <http://www.w3.org/ns/prov#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            prefix wfdesc: <http://purl.org/wf4ever/wfdesc#>
            PREFIX wfprov: <http://purl.org/wf4ever/wfprov#> 
            Select distinct ?processrun
            where {
                ?run rdf:type wfprov:WorkflowRun ;
                    wfprov:describedByWorkflow <http://ns.taverna.org.uk/2010/workflowBundle/01348671-5aaa-4cc2-84cc-477329b70b0d/workflow/Hello_Anyone/>  .
                ?output    prov:wasGeneratedBy ?run ; 
                           prov:wasGeneratedBy ?processrun .
                ?processrun wfprov:wasPartOfWorkflowRun ?run .
            }
            """
        data = self.doQueryPOST(sparqlquery, JSON=True)
        self.assertBindingCount(data, 1)
# 
    def testIntermediateOutputsCount(self):
        sparqlquery  = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            prefix wfdesc: <http://purl.org/wf4ever/wfdesc#>
            PREFIX wfprov: <http://purl.org/wf4ever/wfprov#> 
            prefix prov: <http://www.w3.org/ns/prov#>
            SELECT distinct ?output
            WHERE { 
            ?processrun wfprov:wasPartOfWorkflowRun [
                rdf:type wfprov:WorkflowRun ;
                wfprov:describedByWorkflow <http://ns.taverna.org.uk/2010/workflowBundle/01348671-5aaa-4cc2-84cc-477329b70b0d/workflow/Hello_Anyone/>  ;
            ].
            ?output prov:wasGeneratedBy ?processrun .
            }
            """
        data = self.doQueryPOST(sparqlquery, JSON=True)
        self.assertBindingCount(data, 2)
#   
    def testIntermediateInputsCount(self):
        sparqlquery  = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            prefix wfdesc: <http://purl.org/wf4ever/wfdesc#>
            PREFIX wfprov: <http://purl.org/wf4ever/wfprov#> 
            prefix prov: <http://www.w3.org/ns/prov#>
            SELECT distinct ?input
            WHERE { 
            ?processrun wfprov:wasPartOfWorkflowRun [
                rdf:type wfprov:WorkflowRun ;
                wfprov:describedByWorkflow <http://ns.taverna.org.uk/2010/workflowBundle/01348671-5aaa-4cc2-84cc-477329b70b0d/workflow/Hello_Anyone/>  ;                
            ];
                prov:used ?input .
            }
            """
        data = self.doQueryPOST(sparqlquery, JSON=True)
        self.assertBindingCount(data, 2)
#   
    #### This test passed but the query is a compromised
    #### I want the query to be more like query for the run of that processor, and the output of the run
    #### we can't expect the queryer (human or software) to know that role is the output of that processor
    def testOutputOfConcatenateCount(self):
        sparqlquery  = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            prefix wfdesc: <http://purl.org/wf4ever/wfdesc#>
            PREFIX wfprov: <http://purl.org/wf4ever/wfprov#> 
            SELECT distinct ?entity
            WHERE { 
            ?processrun wfprov:wasPartOfWorkflowRun [
                rdf:type wfprov:WorkflowRun ;
                wfprov:describedByWorkflow <http://ns.taverna.org.uk/2010/workflowBundle/01348671-5aaa-4cc2-84cc-477329b70b0d/workflow/Hello_Anyone/>  ;                
            ];
            rdfs:label ?processName .
            ?entity  wfprov:wasOutputFrom ?processrun .
            filter regex(?processName, "concatenate", 'i')
            }
            """
        data = self.doQueryPOST(sparqlquery, JSON=True)
        self.assertBindingCount(data, 1)
#    
    def testInputsOfConcatenateCount(self):
        sparqlquery  = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            prefix prov: <http://www.w3.org/ns/prov#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            prefix wfdesc: <http://purl.org/wf4ever/wfdesc#>
            PREFIX wfprov: <http://purl.org/wf4ever/wfprov#> 
            SELECT distinct ?input
            WHERE { 
            ?processrun wfprov:wasPartOfWorkflowRun [
                rdf:type wfprov:WorkflowRun ;
                wfprov:describedByWorkflow <http://ns.taverna.org.uk/2010/workflowBundle/01348671-5aaa-4cc2-84cc-477329b70b0d/workflow/Hello_Anyone/>  ;                
                ];
                rdfs:label ?processName ;
                prov:used    ?input .
            filter regex(?processName, "concatenate", 'i')
            }
            """
        data = self.doQueryPOST(sparqlquery, JSON=True)
        self.assertBindingCount(data, 2)
#    
    def testStartTimeOfConcatenateSelect(self):
        sparqlquery  = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            prefix prov: <http://www.w3.org/ns/prov#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            prefix wfdesc: <http://purl.org/wf4ever/wfdesc#>
            PREFIX wfprov: <http://purl.org/wf4ever/wfprov#> 
            SELECT distinct ?start
            WHERE { 
            ?processrun wfprov:wasPartOfWorkflowRun [
                rdf:type wfprov:WorkflowRun ;
                wfprov:describedByWorkflow <http://ns.taverna.org.uk/2010/workflowBundle/01348671-5aaa-4cc2-84cc-477329b70b0d/workflow/Hello_Anyone/>  ;                
                ];
                rdfs:label ?processName ;
                prov:startedAtTime    ?start .
            filter regex(?processName, "concatenate", 'i')
            }
            """
        data = self.doQueryPOST(sparqlquery, JSON=True)
        self.assertVarBinding(data, "start", "typed-literal", "2012-11-19T17:16:04.123Z")
#    
    def testEndTimeOfConcatenateSelect(self):
        sparqlquery  = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            prefix prov: <http://www.w3.org/ns/prov#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            prefix wfdesc: <http://purl.org/wf4ever/wfdesc#>
            PREFIX wfprov: <http://purl.org/wf4ever/wfprov#> 
            SELECT distinct ?end
            WHERE { 
            ?processrun wfprov:wasPartOfWorkflowRun [
                rdf:type wfprov:WorkflowRun ;
                wfprov:describedByWorkflow <http://ns.taverna.org.uk/2010/workflowBundle/01348671-5aaa-4cc2-84cc-477329b70b0d/workflow/Hello_Anyone/>  ;                
                ];
                rdfs:label ?processName ;
                prov:endedAtTime    ?end .
            filter regex(?processName, "concatenate", 'i')
            }
            """
        data = self.doQueryPOST(sparqlquery, JSON=True)
        self.assertVarBinding(data, "end", "typed-literal", "2012-11-19T17:16:04.444Z")


def getTestSuite(select="unit"):
    """
    Get test suite

    select  is one of the following:
            "unit"      return suite of unit tests only
            "component" return suite of unit and component tests
            "all"       return suite of unit, component and integration tests
            "pending"   return suite of pending tests
            name        a single named test to be run
    """
    testdict = {
        "unit":
            [ 
             "testRUNOfAWorkflow",
             "testRUNOfAWorkflow2",
             "testNumberOfWorkflowOutputsCOUNT",
             "testNumberOfWorkflowOutputsCOUNTProv",
             "testNumberOfWorkflowInputsCOUNT",
             "testNumberOfWorkflowInputsCOUNTProv",
             "testWorkflowInputPatternSELECT",
             "testNumberOfProcessRunsCount",
             "testStartTimeOfRunSelect",
             "testEndTimeOfRunSelect",
             "testSourceArtifactsOfWfOutputCount",
             "testSourceActivitiesOfWfOutputCount",
             "testOutputOfConcatenateCount",
             "testInputsOfConcatenateCount",
             "testStartTimeOfConcatenateSelect",
             "testEndTimeOfConcatenateSelect",
             "testIntermediateOutputsCount",
             "testIntermediateInputsCount"
            ],
        }
    return TestUtils.getTestSuite(TestHelloAnyoneWfprov, testdict, select=select)

if __name__ == "__main__":
    TestUtils.runTests("TestHelloAnyoneWfprov", getTestSuite, sys.argv)

# End.
