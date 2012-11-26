'''
Created on Sep 13, 2012

@author: zhaoj
'''
import unittest

import os, os.path
import sys
import logging

# Add main library directory to python path
sys.path.append("../..")

# import querylgpn.AllLGPNTests
import TestSimplePatterns
import testSingleRun.AllSingleTests
import testConstraints.AllConstraintTests

def getTestSuite(select="unit"):
    suite = unittest.TestSuite()
    # suite.addTest(querylgpn.AllLGPNTests.getTestSuite(select=select))
    #suite.addTest(TestSimplePatterns.getTestSuite(select=select))
    suite.addTest(testSingleRun.AllSingleTests.getTestSuite(select=select))
    return suite


from MiscLib import TestUtils

if __name__ == "__main__":
    TestUtils.runTests("AllTests.log", getTestSuite, sys.argv)
