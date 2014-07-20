"""

"""

import networkx as nx


class ElectricalNetwork (object):
    """
    represents a electrical network and all the associated components
    """

    def __init__(self, phaseDesignations):
        """
        phaseDesignations is a value that represents the phases present in the
        newtork and the naming convension used by the user.  ie ABC, XYZ, etc..
        """
        setattr(self, 'phaseDesignations', str(phaseDesignations))
        setattr(self, '__networkGraph__', nx.DiGraph())
        setattr(self, '__circuitSources__', [])
        setattr(self, '__maxNodeEdges__', 6)
        setattr(self, '__maxSwitchDeviceEdges__', 4)

    def __del__ (self):
        pass


    def addNode (self, node):
        """
        Adds a items as a node to the network
        """
        self.__networkGraph__.add_node(node)
        pass


    def addCircuitSource (self, sourceNode):
        """
        Adds a circuit source to the network that represents the source for the
        electrical
        """
        self.__circuitSources__.append(sourceNode)


    def removeNode (self):
        pass


    def addEdge (self, edge, node1, node2):
        self.__networkGraph__.add_edge(node1, node2, data=edge)


    def removeEdge (self, node1, node2):
        self.__networkGraph__.remove_edge(node1,node2)


    def getConnectedEdgeCount (self, node):
        """
        returns the number of edges connected to the node.. ie the degree
        """
        return(self.__networkGraph__.degree(node))


    def getGraph(self):
        return(self.__networkGraph__)



class ElectricalObject (object):
    """
    represnts the basic behaviors and attributes of any item that is part of
    an electrical system.

    phaseDesignation
    """

    def __init__ (self, electricalNetwork, phase, **kwargs):
        self.electricalNetwork = electricalNetwork
        self.setPhase(phase)
        for name, value in kwargs.items():
            setattr(self, name, value)

    def __del__ (self):
        pass


    def __validateVoltage__ (self, voltage):
        """
        Ensures that the a voltage value is suitable number value
        """
        try:
            float(voltage)
            if voltage > 0:
                return True
            else:
                return False
        except ValueError:
            return False

    def  __updateElectricalInfo__ (self):
        """
        run to update the electrical information about an electrical object
        """
        pass

    def setPhase (self, phase):
        """
        validates and sets the phase of the electrical object
        """
        if phase in self.electricalNetwork.phaseDesignations:
            setattr(self, 'phase', phase)
        else:
            raise ValueError('Phase {0} not in Network designations of {1}'.format(phase,self.electricalNetwork.phaseDesignations ))


    def changePhase(self, originalPhase, newPhase):
        """
        Changes the phase of an electrical object.  Original Phases are the phase
        that are to be changed and the newPhases are the phases that they are to
        """
        pass


    def setVoltage (self, voltage, units='volts'):
        """
        sets the electrical voltage all voltages are stored in volts, but may
        be added in kilovolts by specifying different units
        """
        if self.__validateVoltage__(voltage):
            if units.lower() in ['volts','volt','v']:
                setattr(self, 'voltage', voltage)
            elif units.lower() in ['kv', 'kvolts', 'kilovolts', 'kvolt', 'kilovolt']:
                setattr(self, 'voltage', voltage / 1000)
            else:
                raise ValueError("Can not determine the voltage units")
        else:
            raise ValueError("Unable to set the voltage")


    def getNetwork (self):
        return(self.electricalNetwork)


    def getSources (self):
        """
        returns all the source objects for the network that they object can
        reach
        """
        network = self.getNetwork()
        graph = network.getGraph()
        sources = []
        for src in network.__circuitSources__:
            if nx.has_path(graph, src, self):
                sources.append(src)
        return(sources)


    def getVoltage (self, units='volts'):
        """
        determines the voltage of an object based on the connected source
        and any transformation between object and circuit source.  If the object
        itself has a voltage as is the case for a CircuitSource object, then the
        objects voltage is returned
        """
        if hasattr(self, 'voltage'):
            voltage = self.voltage
        else:
            circuitSources = self.getSources()
            voltage = None
            for src in circuitSources:
                if voltage:
                    if src.getVoltage() is not voltage:
                        raise RuntimeError ("Multiple circuit source voltage do not match")
                else:
                    voltage = src.getVoltage()
        return (voltage)


class ElectricalDevice (ElectricalObject):
    """
    Represents an electrical device that is a node in the network
    """

    def __init__ (self, electricalNetwork, phase, **kwargs):
        super(ElectricalDevice, self).__init__(electricalNetwork, phase)
        electricalNetwork.addNode(self)


    def __checkConnectedEdge__ (self):
        """
        verifies that the conencted edges meet the criteria of each subclass
        This methond must be implemented by each subclass
        """
        network = self.electricalNetwork
        if network.getConnectedEdgeCount(self) <= network.__maxNodeEdges__:
            return(True)
        else:
            return (False)


class ElectricalConductor (ElectricalObject):
    """
    Represents and electrical conductor that is a edge in the network
    """

    def __init__ (self, electricalNetwork, phase, node1, node2):
        """
        """
        super(ElectricalConductor, self).__init__(electricalNetwork, phase)
        electricalNetwork.addEdge(self, node1, node2)
        electricalNetwork.addEdge(self,node2, node1)
        if not node1.__checkConnectedEdge__() or not node2.__checkConnectedEdge__():
            electricalNetwork.removeEdge(node1, node2)
            raise RuntimeError("Unable to add conductor as it violates node connectivity rule")


class SimpleConductorJunction (ElectricalDevice):
    """
    represents a simple junction between conductors
    """

    def __init__ (self, electricalNetwork, phase, **kwargs):
        super(SimpleConductorJunction, self).__init__(electricalNetwork, phase)
        electricalNetwork.addNode(self)

##    def __checkConnectedEdge__ (self):
##        """
##        Checks the connected edges to ensure that the connections are correct
##        """
##        network = self.electricalNetwork
##        if nx.degree(self) >= network.__maxNodeEdges__:
##            return(True)
##        else:
##            return (False)


class SwitchableDevice (ElectricalDevice):
    """
    represents any device within an electrical system that can be switched or
    more formal that can have differnt states that interrupt the electical flow
    """

    def __init__(self, electricalNetwork, phase,**kwargs):
        super(SwitchableDevice,self).__init__(electricalNetwork, phase)

        openPhases = {}
        for phs in self.electricalNetwork.phaseDesignations:
            if self.phase == phs:
                openPhases[phs] = False
            else:
                openPhases[phs] = None

        setattr(self, 'openPhases', openPhases)


    def __checkConnectedEdge__ (self):
        """
        Checks the connected edges to ensure that the connections are correct
        """
        network = self.electricalNetwork
        if network.getConnectedEdgeCount(self) <= network.__maxSwitchDeviceEdges__:
            return(True)
        else:
            return (False)


    def open(self, phase='all'):
        """
        Sets the devices status to open on the specified phases. If the phase is
        set to all, all phases will be closed.
        """
        network = self.electricalNetwork
        g = network.getGraph()
        predecessors =  g.predecessors(self)

        if phase.lower() <> 'all':
            for x in phase.upper():
                if self.openPhases[x] is not None:
                    self.openPhases[x] = True
        else:
            for x in self.openPhases:
                if self.openPhases[x] is not None:
                    self.openPhases[x] = True

        for pred in predecessors:
            g.remove_edge(pred, self)

    def close(self, phase='all'):
        """
        Sets the devices status to on on the specified phases.  If the phase is
        set to all, all phases will be closed.
        """

        if phase.lower() <> 'all':
            for x in phase.upper():
                if self.openPhases[x] is not None:
                    self.openPhases[x] = False
        else:
            for x in self.openPhases:
                if self.openPhases[x] is not None:
                    self.openPhases[x] = False

        network = self.electricalNetwork
        g = network.getGraph()
        successors =  g.successors(self)

        for succ in successors:
            if not g.has_edge(succ, self):
                g.add_edge(succ, self)




    def changePhase (self, originalPhase, newPhase):
        """
        Changes the phases from one to another such that the originalPhases become
        the values for the new phases.  For SwitchingDevices this also changes
        the switching configuration so that the phases that were open also swap
        """
        for phs in originalPhase:
            pass


class VoltageTransformer (ElectricalObject):
    """
    A Voltage transformer transforms one voltage to another voltage
    such as taking 13kV and transforming to 120/240 volts
    """


class Conductor (ElectricalObject):
    """
    represents the wire or conductor that connects different electrical compoents
    together
    """


class ElectricalSource (ElectricalObject):
    """
    Represents the source of electricity for an electrical system.  This could be
    a battery, generator, or substation.
    """

    def __init__ (self, electricalNetwork ,designation, voltage, voltageunits='volts', phase='ABC', **kwargs):
        """
        initilizer for the object.  An electrical source must have a voltage,
        phase and designation.  It may have any number of other attributes
        """
        super(ElectricalSource,self).__init__(electricalNetwork, phase)
        electricalNetwork.addCircuitSource(self)
        if designation:
            setattr(self, 'designation', designation)
        else:
            raise AttributeError("Electrical Source must have a designation")
        if voltage:
            self.setVoltage(voltage, voltageunits)
        else:
            raise "Electrical Source must have a voltage"

        for k,v in kwargs.items():
            setattr(self, k,v)


    def __checkConnectedEdge__ (self):
        """
        Checks the connected edges to ensure that the connections are correct
        """
        network = self.electricalNetwork
        if network.getConnectedEdgeCount(self) <= network.__maxNodeEdges__:
            return(True)
        else:
            return (False)


def main():
    pass

if __name__ == '__main__':
    main()
