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


class TestHelloAnyone(SparqlQueryTestCase):
    
    def setUp(self):
        super(TestHelloAnyone, self).setUp()
        return

    def tearDown(self):
        super(TestHelloAnyone, self).tearDown()
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
            SELECT distinct ?run
            WHERE {?run prov:qualifiedAssociation 
                [prov:hadPlan 
                    <http://ns.taverna.org.uk/2010/workflowBundle/01348671-5aaa-4cc2-84cc-477329b70b0d/workflow/Hello_Anyone/>]
            optional {?run prov:wasInformedBy ?activity}
            filter (!bound(?activity))
            }
            """
        data = self.doQueryPOST(sparqlquery, JSON=True)
        self.assertBindingCount(data, 1)
    
    def testNumberOfWorkflowOutputsCOUNT(self):
        sparqlquery  = """
            PREFIX prov: <http://www.w3.org/ns/prov#> 
            SELECT distinct ?output
            WHERE {?output prov:wasGeneratedBy ?run . 
            ?run prov:qualifiedAssociation 
                [prov:hadPlan 
                <http://ns.taverna.org.uk/2010/workflowBundle/01348671-5aaa-4cc2-84cc-477329b70b0d/workflow/Hello_Anyone/>]
            optional {?run prov:wasInformedBy ?activity}
            filter (!bound(?activity))
            }
            """
        data = self.doQueryPOST(sparqlquery, JSON=True)
        self.assertBindingCount(data, 1)
        
    def testNumberOfWorkflowInputsCOUNT(self):
        sparqlquery  = """
            PREFIX prov: <http://www.w3.org/ns/prov#> 
            SELECT distinct ?input
            WHERE { 
            ?run prov:qualifiedAssociation 
                [prov:hadPlan 
                <http://ns.taverna.org.uk/2010/workflowBundle/01348671-5aaa-4cc2-84cc-477329b70b0d/workflow/Hello_Anyone/>] ;
                prov:used ?input .
            optional {?run prov:wasInformedBy ?activity}
            filter (!bound(?activity))
            }
            """
        data = self.doQueryPOST(sparqlquery, JSON=True)
        self.assertBindingCount(data, 1)
        
    def testWorkflowInputPatternSELECT(self):
        sparqlquery  = """
            PREFIX prov: <http://www.w3.org/ns/prov#> 
            SELECT distinct ?inputParameter
            WHERE { 
            ?run prov:qualifiedAssociation 
                [prov:hadPlan 
                <http://ns.taverna.org.uk/2010/workflowBundle/01348671-5aaa-4cc2-84cc-477329b70b0d/workflow/Hello_Anyone/>] ;
                prov:qualifiedUsage [prov:entity ?input; prov:hadRole ?inputParameter ]
            optional {?run prov:wasInformedBy ?activity}
            filter (!bound(?activity))
            }
            """
        data = self.doQueryPOST(sparqlquery, JSON=True)
        bindings = data['results']['bindings']
        found = False
        for b in bindings:
            if b == { 'inputParameter': { "type": "uri" , "value": "http://ns.taverna.org.uk/2010/workflowBundle/01348671-5aaa-4cc2-84cc-477329b70b0d/workflow/Hello_Anyone/in/name" } }:
                found = True
        self.assertTrue(found, "Expected to find an input for the name")
    
    #### This fails because the generation of a bundle is also infrrmed by the workflow run
    
    def testNumberOfProcessRunsCount(self):
        sparqlquery  = """
            PREFIX prov: <http://www.w3.org/ns/prov#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
            SELECT distinct ?process
            WHERE { 
            ?run prov:qualifiedAssociation 
                [prov:hadPlan 
                <http://ns.taverna.org.uk/2010/workflowBundle/01348671-5aaa-4cc2-84cc-477329b70b0d/workflow/Hello_Anyone/>] ;
                prov:used ?input .
            optional {?run prov:wasInformedBy ?activity}
            filter (!bound(?activity))
            ?process prov:wasInformedBy ?run ; rdf:type prov:Activity .
            }
            """
        data = self.doQueryPOST(sparqlquery, JSON=True)
        self.assertBindingCount(data, 2)
    
    def testStartTimeOfRunSelect(self):
        sparqlquery  = """
            PREFIX prov: <http://www.w3.org/ns/prov#> 
            SELECT distinct ?start
            WHERE { 
            ?run prov:qualifiedAssociation 
                [prov:hadPlan 
                <http://ns.taverna.org.uk/2010/workflowBundle/01348671-5aaa-4cc2-84cc-477329b70b0d/workflow/Hello_Anyone/>] ;
                prov:qualifiedUsage [prov:entity ?input; prov:hadRole ?inputParameter ]
            optional {?run prov:wasInformedBy ?activity}
            filter (!bound(?activity))
            ?run prov:startedAtTime ?start
            }
            """
        data = self.doQueryPOST(sparqlquery, JSON=True)
        self.assertVarBinding(data, "start", "typed-literal", "2012-09-06T11:51:21.439+01:00")
#    
    def testEndTimeOfRunSelect(self):
        sparqlquery  = """
            PREFIX prov: <http://www.w3.org/ns/prov#> 
            SELECT distinct ?end
            WHERE { 
            ?run prov:qualifiedAssociation 
                [prov:hadPlan 
                <http://ns.taverna.org.uk/2010/workflowBundle/01348671-5aaa-4cc2-84cc-477329b70b0d/workflow/Hello_Anyone/>] ;
                prov:qualifiedUsage [prov:entity ?input; prov:hadRole ?inputParameter ]
            optional {?run prov:wasInformedBy ?activity}
            filter (!bound(?activity))
            ?run prov:endedAtTime ?end
            }
            """
        data = self.doQueryPOST(sparqlquery, JSON=True)
        self.assertVarBinding(data, "end", "typed-literal", "2012-09-06T11:51:31.307+01:00")
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
    def testOutputOfConcatenateCount(self):
        sparqlquery  = """
            PREFIX prov: <http://www.w3.org/ns/prov#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
            SELECT distinct ?entity
            WHERE { 
            ?entity  a    prov:Entity ;
                prov:qualifiedGeneration [
                    a    prov:Generation ;
                    prov:hadRole <http://ns.taverna.org.uk/2010/workflowBundle/01348671-5aaa-4cc2-84cc-477329b70b0d/workflow/Hello_Anyone/processor/Concatenate_two_strings/out/output>
            ]
            }
            """
        data = self.doQueryPOST(sparqlquery, JSON=True)
        self.assertBindingCount(data, 1)
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
             "testStartTimeOfRunSelect",
             "testEndTimeOfRunSelect",
             "testSourceArtifactsOfWfOutputCount",
             "testSourceActivitiesOfWfOutputCount",
             "testAllSourceArtifactsOfWfOutputCount",
             "testAllSourceActivitiesOfWfOutputCount",
             "testOutputOfConcatenateCount",
             "testInputsOfConcatenateCount",
             "testStartTimeOfConcatenateSelect",
             "testEndTimeOfConcatenateSelect"
            ],
        }
    return TestUtils.getTestSuite(TestHelloAnyone, testdict, select=select)

if __name__ == "__main__":
    TestUtils.runTests("TestHelloAnyone", getTestSuite, sys.argv)

# End.
