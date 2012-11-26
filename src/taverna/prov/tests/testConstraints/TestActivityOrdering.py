'''
Created on Sep 14, 2012

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


class TestActivityOrdering(SparqlQueryTestCase):
    
    def setUp(self):
        super(TestActivityOrdering, self).setUp()
        return

    def tearDown(self):
        super(TestActivityOrdering, self).tearDown()
        return

    #### constraint 32
    
    def testStartPrecedesEnd(self):
        sparqlquery  = """
            PREFIX prov: <http://www.w3.org/ns/prov#>
            prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
            SELECT distinct ?start ?end
            WHERE {
                ?activity prov:startedAtTime ?start ; prov:endedAtTime ?end .
                filter (?start > ?end)
            }
            """
        data = self.doQueryPOST(sparqlquery, JSON=True)
        self.assertBindingEqual(data, 0, "Activity was started after it ended")
        
    #### constraint 33
    
    def testStartStartOrdering(self):
        sparqlquery  = """
            PREFIX prov: <http://www.w3.org/ns/prov#>
            prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
            SELECT distinct ?start1 ?start2
            WHERE {
                ?activity prov:startedAtTime ?start1 .
                optional {?activity prov:wasStartedBy ?trigger1 } .
                ?activity prov:startedAtTime ?start2 .
                optional {?activity    prov:wasStartedBy ?trigger2 } .
                filter (?start1 != ?start2)
            }
            """
        data = self.doQueryPOST(sparqlquery, JSON=True)
        self.assertBindingEqual(data, 0, "Activity cannot be started at the same time by two different triggers.")
        
    #### constraint 34
    
    def testEndEndOrdering(self):
        sparqlquery  = """
            PREFIX prov: <http://www.w3.org/ns/prov#>
            prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
            SELECT distinct ?end1 ?end2
            WHERE {
                ?activity prov:endedAtTime ?end1 .
                optional {?activity prov:wasEndedBy ?trigger1 } .
                ?activity prov:endedAtTime ?end2;
                optional {?activity prov:wasEndedBy ?trigger2 } .
                filter (?end1 != ?end2)
            }
            """
        data = self.doQueryPOST(sparqlquery, JSON=True)
        self.assertBindingEqual(data, 0, "Activity cannot be ended at the same time by two different triggers.")
    
    #### constraint 35

    def testUsageWithinActivity(self):
        sparqlquery  = """
            PREFIX prov: <http://www.w3.org/ns/prov#>
            prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
            SELECT distinct ?start ?used ?end
            WHERE {
                ?activity prov:startedAtTime ?start ;
                        prov:endedAtTime    ?end .
                ?activity prov:qualifiedUsage [
                    prov:atTime ?used
                ]
                filter (?start > ?used && ?used > ?end)
            }
            """
        data = self.doQueryPOST(sparqlquery, JSON=True)
        self.assertBindingEqual(data, 0, "Activity must be started before it can use anything and be ended after its using of something.")
        
    #### constraint 36

    def testGenerationWithinActivity(self):
        sparqlquery  = """
            PREFIX prov: <http://www.w3.org/ns/prov#>
            prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
            SELECT distinct ?start ?generation ?end
            WHERE {
                ?activity prov:startedAtTime ?start ;
                        prov:endedAtTime    ?end .
                ?entity prov:wasGeneratedBy    ?activity ;
                        prov:generatedAtTime    ?generation .
                filter (?start > ?generation && ?generation > ?end)
            }
            """
        data = self.doQueryPOST(sparqlquery, JSON=True)
        self.assertBindingEqual(data, 0, "Activity must be started before it can generate anything and be ended after its generation of something.")

    #### constraint 37
    
    def testWasInformedByOrdering(self):
        sparqlquery  = """
            PREFIX prov: <http://www.w3.org/ns/prov#>
            prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  
            SELECT distinct ?informedEnding ?informerStart
            WHERE {
                ?activity prov:wasInformedBy ?informer .
                ?activity prov:endedAtTime ?informedEnding .
                ?informer prov:startedAtTime ?informerStart .
                filter (?informedEnding < ?informerStart)
            }
            """
        data = self.doQueryPOST(sparqlquery, JSON=True)
        self.assertBindingEqual(data, 0, "The informed activity should end after the start of the informing activity.")


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
             "testStartPrecedesEnd",
             "testStartStartOrdering",
             "testEndEndOrdering",
             "testUsageWithinActivity",
             "testGenerationWithinActivity",
             "testWasInformedByOrdering"
            ],
        }
    return TestUtils.getTestSuite(TestActivityOrdering, testdict, select=select)

if __name__ == "__main__":
    TestUtils.runTests("TestActivityOrdering", getTestSuite, sys.argv)

# End.
