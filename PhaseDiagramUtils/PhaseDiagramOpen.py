#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import settings
from thermodynamics import Thermodynamics
from pymatgen import MPRester, Element
from pymatgen.analysis.phase_diagram import GrandPotentialPhaseDiagram, PhaseDiagram, PDPlotter
from pymatgen.ext.matproj import MPRester
from pymatgen.apps.borg.hive import VaspToComputedEntryDrone
from pymatgen.apps.borg.queen import BorgQueen
from pymatgen.entries.compatibility import MaterialsProjectCompatibility


class PhaseDiagramOpenAnalyzer:
    """
    Phase diagram
    """

    def __init__(self, system=[], open_element=""):
        """
        Phase diagram constructor
        :param system: elements of system to analyze
        :param open_element: element for potential change
        """
        self.system = system
        self.open_element = open_element

    @staticmethod
    def plot_phase_diagram(pd, show_unstable=False):
        """
        Plot phase diagram for an specific composite
        :param pd:
        :param show_unstable:
        """
        plotter = PDPlotter(pd, show_unstable=show_unstable)
        plotter.show()

    @staticmethod
    def analyze_phase_diagram(phase_diagram):
        """
        Analyze phase diagram for an specific composite
        :param phase_diagram:
        """
        for e in phase_diagram.stable_entries:
            print(e.composition.reduced_formula, e.entry_id)

        for e in phase_diagram.unstable_entries:
            decomp, e_above_hull = phase_diagram.get_decomp_and_e_above_hull(e)
            pretty_decomp = [("{}:{}".format(k.composition.reduced_formula, k.entry_id), round(v, 2)) for k, v in
                             decomp.items()]
            print(e.composition.reduced_formula, e.entry_id, "%.3f" % e_above_hull, pretty_decomp)

    def get_grand_potential_phase_diagram(self, gcpdobj=None):
        """
        Returns grand potential phase diagram
        :param gcpdobj:
        :return: All phases with their own potential
        """
        if gcpdobj is None:
            return []

        potential = [v for el, v in gcpdobj.chempots.items()]
        phases = [entry.name for entry in gcpdobj.stable_entries]
        # return phases, potential[0]
        return phases, potential[0]

    def get_phase_diagram_data(self):
        """
        Returns grand potential phase diagram data to external plot
        Assumes openelement specific element equals None
        :return: Data to external plot
        """
        open_elements_specific = None
        open_element_all = Element(self.open_element)
        mpr = MPRester("key")

        # import do dados dos arquivos tipo vasp
        drone = VaspToComputedEntryDrone()
        queen = BorgQueen(drone, rootpath=".")
        entries = queen.get_data()

        # Get data to make phase diagram
        mp_entries = mpr.get_entries_in_chemsys(self.system, compatible_only=True)

        entries.extend(mp_entries)

        compat = MaterialsProjectCompatibility()
        entries = compat.process_entries(entries)
        #explanation_output = open("explain.txt",'w')
        entries_output = open("entries.txt",'w')
        compat.explain(entries[0])
        print(entries, file=entries_output)
        #print(entries)

        if open_elements_specific:
            gcpd = GrandPotentialPhaseDiagram(entries, open_elements_specific)
            self.plot_phase_diagram(gcpd, False)
            self.analyze_phase_diagram(gcpd)

        if open_element_all:
            pd = PhaseDiagram(entries)
            chempots = pd.get_transition_chempots(open_element_all)
            #print(chempots)
            #all_gcpds = list()
            toplot = []
            # dic = {}
            for idx in range(len(chempots)):
                if idx == len(chempots) - 1:
                    avgchempot = chempots[idx] - 0.1
                else:
                    avgchempot = 0.5 * (chempots[idx] + chempots[idx + 1])
                gcpd = GrandPotentialPhaseDiagram(entries, {open_element_all: avgchempot}, pd.elements)
                # toplot.append(self.get_grand_potential_phase_diagram(gcpd))

                min_chempot = None if idx == len(chempots) - 1 else chempots[idx + 1]
                max_chempot = chempots[idx]
                #gcpd = GrandPotentialPhaseDiagram(entries, {open_element_all: max_chempot}, pd.elements)
                
                toplot.append(self.get_grand_potential_phase_diagram(gcpd))
                #toplot.append(max_chempot)


                #self.plot_phase_diagram(gcpd, False)
                #print({open_element_all: max_chempot})

            # Data to plot phase diagram
            return toplot
            #print(toplot)

    


    

