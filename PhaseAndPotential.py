from PhaseDiagramOpen import PhaseDiagramOpenAnalyzer
from pymatgen import MPRester, Element
from pymatgen.analysis.phase_diagram import GrandPotentialPhaseDiagram, PhaseDiagram, PDPlotter


pd = PhaseDiagramOpenAnalyzer(system=["Mg", "P","O"], open_element="O")
all_phase_diagrams = pd.get_phase_diagram_data()
# ler o tamanho da lista
number_of_phase_diagrams = len(all_phase_diagrams)

# cria uma lista só com os potenciais químicos
# chempot_list = [all_phase_diagrams[pd_index][1] for pd_index in range(number_of_phase_diagrams)]

open_elements_specific = None
open_element_all = Element("O")
mpr = MPRester("sMnWB7h8Lf4NKmzo")

entries = mpr.get_entries_in_chemsys(['Mg','P','O'], compatible_only=True)

pd2 = PhaseDiagram(entries)

chempot_list = pd2.get_transition_chempots(open_element_all)
pd_index = 0

# cria um dicionário
chempot_range_of_each_phase = {}
for particular_phase_diagram in all_phase_diagrams:
    # recebe o potencial químico
    chempot = chempot_list[pd_index]
    if pd_index is not number_of_phase_diagrams - 1:
        next_chempot = chempot_list[pd_index + 1]
    else:
        next_chempot = chempot_list[pd_index] - 2.0
    chempot_range =  [chempot,next_chempot]   
    # recebe as fases
    phases_list = particular_phase_diagram[0]
        
    for phase in phases_list:
        # Retorna uma visualização do dicionário  de todos as chaves
        if phase in chempot_range_of_each_phase.keys():
            # Retorna uma cópia do dicionário
            chempot_range_of_each_phase[phase][1] = next_chempot.copy()
            
        else:
            # retorna a fase e o intervalo dos potenciais
            chempot_range_of_each_phase[phase] = chempot_range.copy() 
            

    pd_index = pd_index + 1
# print("\n Original list of data from pymatgen API: \n",all_phase_diagrams)        
# print("\n Range of chemical potentials for each phase: \n",chempot_range_of_each_phase)