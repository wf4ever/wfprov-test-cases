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


class TestHelloAnyoneHandmade(SparqlQueryTestCase):
    
    def setUp(self):
        super(TestHelloAnyoneHandmade, self).setUp()
        return

    def tearDown(self):
        super(TestHelloAnyoneHandmade, self).tearDown()
        return

    def testRunASK(self):
        sparqlquery  = """
            PREFIX prov: <http://www.w3.org/ns/prov#> 
            ASK {?run prov:qualifiedAssociation [prov:hadPlan <http://ns.taverna.org.uk/2010/workflowBundle/01348671-5aaa-4cc2-84cc-477329b70b0d/workflow/Hello_Anyone/>]}
            """
        data = self.doQueryGET(sparqlquery, JSON=True)
        self.assertEqual(data['head'],    {})
        self.assertEqual(data['boolean'], True)
        self.assertEqual(data.keys(), ['head', u'boolean'])
    
    def testRUNSELECT1(self):
        sparqlquery  = """
            PREFIX prov: <http://www.w3.org/ns/prov#> 
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
            prefix wfprov: <http://purl.org/wf4ever/wfprov#>
            SELECT distinct ?run
            WHERE {?run    rdf:type wfprov:WorkflowRun ;
                prov:qualifiedAssociation 
                [prov:hadPlan 
                    <http://ns.taverna.org.uk/2010/workflowBundle/01348671-5aaa-4cc2-84cc-477329b70b0d/workflow/Hello_Anyone/>]
            }
            """
        data = self.doQueryPOST(sparqlquery, JSON=True)
        self.assertBindingCount(data, 1)
    
    def testNumberOfWorkflowOutputsCOUNT(self):
        self.fail("Workflow outout is not expressed in the example handmade")
        
    def testNumberOfWorkflowInputsCOUNT(self):
        sparqlquery  = """
            PREFIX prov: <http://www.w3.org/ns/prov#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
            prefix wfprov: <http://purl.org/wf4ever/wfprov#> 
            SELECT distinct ?input
            WHERE { 
            ?run    rdf:type wfprov:WorkflowRun;
                prov:qualifiedAssociation 
                [prov:hadPlan 
                <http://ns.taverna.org.uk/2010/workflowBundle/01348671-5aaa-4cc2-84cc-477329b70b0d/workflow/Hello_Anyone/>] ;
                prov:used ?input .
            }
            """
        data = self.doQueryPOST(sparqlquery, JSON=True)
        self.assertBindingCount(data, 1)
        
    def testWorkflowInputPatternSELECT(self):
        sparqlquery  = """
            PREFIX prov: <http://www.w3.org/ns/prov#> 
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
            prefix wfprov: <http://purl.org/wf4ever/wfprov#>
            SELECT distinct ?inputParameter
            WHERE { 
            ?run rdf:type    wfprov:WorkflowRun ;
                prov:qualifiedAssociation 
                [prov:hadPlan 
                <http://ns.taverna.org.uk/2010/workflowBundle/01348671-5aaa-4cc2-84cc-477329b70b0d/workflow/Hello_Anyone/>] ;
                prov:qualifiedUsage [prov:entity ?input; prov:hadRole ?inputParameter ]
            }
            """
        data = self.doQueryPOST(sparqlquery, JSON=True)
        self.assertVarBinding(data, "inputParameter", "uri", "http://ns.taverna.org.uk/2010/workflowBundle/01348671-5aaa-4cc2-84cc-477329b70b0d/workflow/Hello_Anyone/in/name")
    
    #### This fails because the generation of a bundle is also infrrmed by the workflow run
    
    def testNumberOfProcessRunsCount(self):
        sparqlquery  = """
            PREFIX prov: <http://www.w3.org/ns/prov#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
            prefix wfprov: <http://purl.org/wf4ever/wfprov#>
            SELECT distinct ?process
            WHERE { 
            ?run rdf:type wfprov:WorkflowRun ;
                prov:qualifiedAssociation 
                [prov:hadPlan 
                <http://ns.taverna.org.uk/2010/workflowBundle/01348671-5aaa-4cc2-84cc-477329b70b0d/workflow/Hello_Anyone/>] .
            ?process wfprov:wasPartOfWorkflowRun ?run ; rdf:type wfprov:ProcessRun .
            }
            """
        data = self.doQueryPOST(sparqlquery, JSON=True)
        self.assertBindingCount(data, 1)
        
    def testNumberOfProcessRunsCount2(self):
        sparqlquery  = """
            PREFIX prov: <http://www.w3.org/ns/prov#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
            prefix wfprov: <http://purl.org/wf4ever/wfprov#>
            prefix dcterms: <http://purl.org/dc/terms/> 
            SELECT distinct ?process
            WHERE { 
            ?run rdf:type wfprov:WorkflowRun ;
                prov:qualifiedAssociation 
                [prov:hadPlan 
                <http://ns.taverna.org.uk/2010/workflowBundle/01348671-5aaa-4cc2-84cc-477329b70b0d/workflow/Hello_Anyone/>] .
            ?process dcterms:partOf ?run ; rdf:type prov:Activity .
            }
            """
        data = self.doQueryPOST(sparqlquery, JSON=True)
        self.assertBindingCount(data, 1)
    
    def testStartTimeOfRunSelect(self):
        sparqlquery  = """
            PREFIX prov: <http://www.w3.org/ns/prov#> 
            prefix wfprov: <http://purl.org/wf4ever/wfprov#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
            SELECT distinct ?start
            WHERE { 
            ?run rdf:type wfprov:WorkflowRun ; 
                prov:qualifiedAssociation 
                [prov:hadPlan 
                <http://ns.taverna.org.uk/2010/workflowBundle/01348671-5aaa-4cc2-84cc-477329b70b0d/workflow/Hello_Anyone/>] .
            ?run prov:startedAtTime ?start
            }
            """
        data = self.doQueryPOST(sparqlquery, JSON=True)
        self.assertVarBinding(data, "start", "typed-literal", "2012-09-12T14:49:45.75+01:00")
#    
    def testEndTimeOfRunSelect(self):
        sparqlquery  = """
            PREFIX prov: <http://www.w3.org/ns/prov#> 
            prefix wfprov: <http://purl.org/wf4ever/wfprov#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
            SELECT distinct ?end
            WHERE { 
            ?run rdf:type wfprov:WorkflowRun ; 
                prov:qualifiedAssociation 
                [prov:hadPlan 
                <http://ns.taverna.org.uk/2010/workflowBundle/01348671-5aaa-4cc2-84cc-477329b70b0d/workflow/Hello_Anyone/>] .
            ?run prov:endedAtTime ?end
            }
            """
        data = self.doQueryPOST(sparqlquery, JSON=True)
        self.assertVarBinding(data, "end", "typed-literal", "2012-09-12T14:49:48.829+01:00")
#    
    def testSourceArtifactsOfWfOutputCount(self):
        self.fail("Can't find a query to find IMMEDIATE source DATA contributing to a workflow output")
#    
    def testSourceActivitiesOfWfOutputCount(self):
        self.fail("Can't find a query to find IMMEDIATE source PROCESS RUNS contributing to a workflow output")

    def testAllSourceArtifactsOfWfOutputCount(self):
        self.fail("Can't find a query to find ALL source DATA contributing to a workflow output")
#    
    def testAllSourceActivitiesOfWfOutputCount(self):
        self.fail("Can't find a query to find ALL source PROCESS RUNS contributing to a workflow output")
#    
    #### This test passed but the query is a compromised
    #### I want the query to be more like query for the run of that processor, and the output of the run
    #### we can't expect the queryer (human or software) to know that role is the output of that processor
    def testOutputOfHelloCount(self):
        self.fail("Can't find a query to find run of the processor hello")
#    
    def testInputsOfConcatenateCount(self):
        self.fail("Can't find a query to find all inputs to the concatenate processor run")
#    
    def testStartTimeOfConcatenateSelect(self):
        self.fail("Basically I can't find out how to find out the run of that concatenate process")
#    
    def testEndTimeOfConcatenateSelect(self):
        self.fail("Basically I can't find out how to find out the run of that concatenate process")


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
             "testRunASK",
             "testRUNSELECT1",
             "testNumberOfWorkflowOutputsCOUNT",
             "testNumberOfWorkflowInputsCOUNT",
             "testWorkflowInputPatternSELECT",
             "testNumberOfProcessRunsCount",
             "testNumberOfProcessRunsCount2",
             "testStartTimeOfRunSelect",
             "testEndTimeOfRunSelect",
             "testSourceArtifactsOfWfOutputCount",
             "testSourceActivitiesOfWfOutputCount",
             "testAllSourceArtifactsOfWfOutputCount",
             "testAllSourceActivitiesOfWfOutputCount",
             "testOutputOfHelloCount",
             "testInputsOfConcatenateCount",
             "testStartTimeOfConcatenateSelect",
             "testEndTimeOfConcatenateSelect"
            ],
        }
    return TestUtils.getTestSuite(TestHelloAnyoneHandmade, testdict, select=select)

if __name__ == "__main__":
    TestUtils.runTests("TestHelloAnyoneHandmade", getTestSuite, sys.argv)

# End.
