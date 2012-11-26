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
sys.path.append("../../..")
sys.path.append("..")

from MiscLib import TestUtils

from SparqlQueryTestCase import SparqlQueryTestCase


class TestSimplePatterns(SparqlQueryTestCase):


    def setUp(self):
        super(TestSimplePatterns, self).setUp()


    def tearDown(self):
        super(TestSimplePatterns, self).tearDown()


    def testAskQueries(self):
        sparqlquery  = """ASK { ?s ?p ?o }"""
        pattern = re.compile("[ \n]+")
        responsedata = self.doQueryGET(sparqlquery)
        responsedata = pattern.sub("", responsedata)
        self.assertEqual(responsedata, """{"head":{},"boolean":true}""")
        
        
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
            [ "testAskQueries"
            ],
        }
    return TestUtils.getTestSuite(TestSimplePatterns, testdict, select=select)

if __name__ == "__main__":
    TestUtils.runTests("TestSimplePatterns.log", getTestSuite, sys.argv)

# End.
