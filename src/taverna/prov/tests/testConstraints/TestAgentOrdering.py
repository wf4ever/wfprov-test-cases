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


class TestAgentOrdering(SparqlQueryTestCase):
    
    def setUp(self):
        super(TestAgentOrdering, self).setUp()
        return

    def tearDown(self):
        super(TestAgentOrdering, self).tearDown()
        return

    #### constraint 49
    
    def testWasAssociatedWithOrdering(self):
        sparqlquery  = """
            PREFIX prov: <http://www.w3.org/ns/prov#>
            prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
            SELECT distinct ?start ?invalid ?generation ?end ?agentEnd ?agentStart
            WHERE {
                ?agent    prov:wasAssociatedWith    ?activity ;
                    prov:generatedAtTime    ?generation ;
                    prov:invalidatedAtTime    ?invalid ;
                    prov:qualifiedStart [
                        rdf:type    prov:Start ;
                        prov:atTime    ?agentStart
                    ];
                    prov:qualifiedEnd [
                        rdf:type    prov:End ;
                        prov:atTime    ?agentEnd
                    ]
                .
                ?activity    prov:startedAtTime    ?start ;
                    prov:endedAtTime    ?end .
                filter (?start>?invalid && ?generation>?end && ?start>?agentEnd && ?agentStart>?end)
            }
            """
        data = self.doQueryPOST(sparqlquery, JSON=True)
        self.assertBindingEqual(data, 0, "Agent and associated activity must be in the right order")
        
    #### constraint 50
    
    def testWasAttributedToOrdering(self):
        sparqlquery  = """
            PREFIX prov: <http://www.w3.org/ns/prov#>
            prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
            SELECT distinct ?generationEntity ?generationAgent ?agentStart 
            WHERE {
                ?entity    prov:wasAttributedTo    ?agent .
                ?entity    prov:generatedAtTime    ?generationEntity .
                ?agent    prov:generatedAtTime    ?generationAgent ;
                    prov:qualifiedStart [
                        rdf:type    prov:Start ;
                        prov:atTime    ?agentStart
                    ];
                .
                filter (?generationEntity > ?generationAgent && ?agentStart > ?generationEntity)
            }
            """
        data = self.doQueryPOST(sparqlquery, JSON=True)
        self.assertBindingEqual(data, 0, "Agent and attributed entity must be in the right order.")
        
    #### constraint 51 wonder whether the 2nd part should be xstart and yend relationship
    
    def testActedOnBehalfOfOrdering(self):
        sparqlquery  = """
            PREFIX prov: <http://www.w3.org/ns/prov#>
            prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
            SELECT distinct ?end1 ?end2
            WHERE {
                ?x    prov:actedOnBehalfOf    ?y .
                ?x    prov:generatedAtTime    ?xtime ;
                    prov:qualifiedEnd [
                        rdf:type    prov:End ;
                        prov:atTime    ?xEnd
                    ];
                .
                ?y    prov:invalidatedAtTime    ?ytime ;
                    prov:qualifiedStart [
                        rdf:type    prov:Start ;
                        prov:atTime    ?yStart
                    ];
                .
                filter (?xtime>?ytime && ?ystart > ?xEnd)
            }
            """
        data = self.doQueryPOST(sparqlquery, JSON=True)
        self.assertBindingEqual(data, 0, "Activity cannot be ended at the same time by two different triggers.")


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
             "testWasAssociatedWithOrdering",
             "testWasAttributedToOrdering",
             "testActedOnBehalfOfOrdering"
            ],
        }
    return TestUtils.getTestSuite(TestAgentOrdering, testdict, select=select)

if __name__ == "__main__":
    TestUtils.runTests("TestAgentOrdering", getTestSuite, sys.argv)

# End.
