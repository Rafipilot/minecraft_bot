
# -*- coding: utf-8 -*-
"""
// aolabs.ai software >ao_core/Arch.py (C) 2023 Animo Omnis Corporation. All Rights Reserved.

Thank you for your curiosity!

Arch file for recommender
"""

import ao_arch as ar
import numpy as np

description = "Basic Recommender System"

#genre, length
arch_i = [1, 1, 1]   
arch_z = [1,1 ]           
arch_c = []           
connector_function = "full_conn"

# To maintain compatibility with our API, do not change the variable name "Arch" or the constructor class "ao.Arch" in the line below (the API is pre-loaded with a version of the Arch class in this repo's main branch, hence "ao.Arch")
Arch = ar.Arch(arch_i, arch_z, arch_c, connector_function, description)

c0 = 3
def c0_instinct_rule(INPUT, Agent):
    if INPUT[0] == 1 or INPUT[1] == 1 or INPUT[2] == 1:        # self.Z__flat[0] needs to be adjusted as per the agent, which output the designer wants the agent to repeat while learning postively or negatively
        if (Agent.story[ Agent.state-1,  Agent.arch.Z__flat[0]] == 1 and Agent.story[ Agent.state-1,  Agent.arch.Z__flat[1]] == 0) or (Agent.story[ Agent.state-1,  Agent.arch.Z__flat[0]] == 0 and Agent.story[ Agent.state-1,  Agent.arch.Z__flat[1]] == 1):
            print("Moving round obstacle pleasure signal!")
            instinct_response = [1, "c0 instinct triggered"]
        else:
            instinct_response = [0, "c0 pass"]  
    else:
        instinct_response = [0, "c0 pass"]    
    return instinct_response            
Arch.C__flat_pleasure = np.append(Arch.C__flat_pleasure, Arch.C__flat[c0])
Arch.datamatrix[4, Arch.C[1][0]] = c0_instinct_rule



