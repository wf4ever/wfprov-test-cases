'''
Created on Sep 13, 2012

@author: zhaoj
'''
import os, os.path
import sys
import unittest
import logging

# Add main library directory to python path
sys.path.append("../../..")
sys.path.append("..")

import TestUniqueness
import TestActivityOrdering
import TestEntityOrdering
import TestAgentOrdering

def getTestSuite(select="unit"):
    suite = unittest.TestSuite()
    suite.addTest(TestUniqueness.getTestSuite(select=select))
    suite.addTest(TestActivityOrdering.getTestSuite(select=select))
    suite.addTest(TestEntityOrdering.getTestSuite(select=select))
    suite.addTest(TestAgentOrdering.getTestSuite(select=select))
    return suite

from MiscLib import TestUtils

if __name__ == "__main__":
    TestUtils.runTests("AllConstraintTests", getTestSuite, sys.argv)
