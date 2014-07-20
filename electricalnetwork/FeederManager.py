"""
Feeder Manager package includes classes and utilities for management of the
electrical network and handles events that occur on the network such
as opening as switch, adding a new device.  It set the appropriate attributes
on the objects that are part of the network that feeder manager operates on.

The main class is the Feeder Manager Class
"""

class FeederManager(object):
    """
    Feeder Manger is a singleton object that manages an individual network
    """
    def __init__ (self, **kargs):
        if kargs.keys() in 'network':
            setattr(self, __network__, kargs['network'])
        if kargs.keys() in 'type':
            if kargs['type'].upper() == 'DISTRIBUTION':
                setattr(self, __type__, "Distribution")
            elif kargs['type'].upper() == 'TRANSMISSION':
                setattr(self, __type__, "Transmission")

        return None

    def __setSource__ (self, ):
        """
        sets the objects as
        """
        return none




def main():
    pass

if __name__ == '__main__':
    main()
