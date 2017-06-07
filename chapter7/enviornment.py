import os

'''
**args is for any arg type - sent as variables
*kwargs
'''


def run(**args):

    print "[*] In environment module."
    return str(os.environ)