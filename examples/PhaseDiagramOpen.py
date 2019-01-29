#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PhaseDiagramOpen import PhaseDiagramOpen

if __name__ == "__main__":
    pd = PhaseDiagramOpen(system=["Sn", "Mn", "W", "O"], open_element="O")
    # Shows data
    print(pd.get_phase_diagram_data())
