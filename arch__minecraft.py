
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
arch_i = [1, 1]   
arch_z = [1,1 ]           
arch_c = [0]           
connector_function = "full_conn"

# To maintain compatibility with our API, do not change the variable name "Arch" or the constructor class "ao.Arch" in the line below (the API is pre-loaded with a version of the Arch class in this repo's main branch, hence "ao.Arch")
Arch = ar.Arch(arch_i, arch_z, arch_c, connector_function, description)





