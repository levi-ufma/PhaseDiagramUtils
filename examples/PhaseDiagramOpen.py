#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PhaseDiagramOpen import PhaseDiagramOpenAnalyzer

if __name__ == "__main__":
    pd = PhaseDiagramOpenAnalyzer(system=["Sn", "Mn", "W", "O"], open_element="O")
    # Shows data
    print(pd.get_phase_diagram_data())
