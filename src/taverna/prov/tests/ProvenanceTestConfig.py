#!/usr/bin/python

"""
Define configuration for Taverna prov export testing

"""

class ProveannceTestConfig:

    # Default endpoint details
    #endpointhost = "andros.zoo.ox.ac.uk:8080"
    endpointhost = "open-biomed.org.uk"
    endpointpath = "/sparql/endpoint-lax/ta-provenance"
    #endpointpath = "/sparql/endpoint-lax/prov-constraint"

    # Later, may define methods to override these defaults, e.g. from a configuration file

# End.
