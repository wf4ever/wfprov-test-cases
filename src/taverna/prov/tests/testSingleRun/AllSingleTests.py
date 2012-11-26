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

import TestHelloAnyone
import TestHelloAnyoneWfprov
import TestHelloAnyoneHandmade

def getTestSuite(select="unit"):
    suite = unittest.TestSuite()
    #suite.addTest(TestHelloAnyone.getTestSuite(select=select))
    suite.addTest(TestHelloAnyoneWfprov.getTestSuite(select=select))
    #suite.addTest(TestHelloAnyoneHandmade.getTestSuite(select=select))
    return suite

from MiscLib import TestUtils

if __name__ == "__main__":
    TestUtils.runTests("AllSingleTests.log", getTestSuite, sys.argv)
