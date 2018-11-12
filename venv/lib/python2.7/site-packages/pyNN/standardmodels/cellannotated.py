"""
Definition of default parameters (and hence, standard parameter names) for
standard cell models.

Plain integrate-and-fire models:
    IF_curr_exp
    IF_curr_alpha
    IF_cond_exp
    IF_cond_alpha
    
Integrate-and-fire with adaptation:
    IF_cond_exp_gsfa_grr
    EIF_cond_alpha_isfa_ista
    EIF_cond_exp_isfa_ista    
    
Integrate-and-fire model for use with the FACETS hardware
    IF_facets_hardware1
    
Hodgkin-Huxley model
    HH_cond_exp

Spike sources (input neurons) 
    SpikeSourcePoisson
    SpikeSourceArray
    SpikeSourceInhGamma

:copyright: Copyright 2006-2011 by the PyNN team, see AUTHORS.
:license: CeCILL, see LICENSE for details.
"""

import numpy
from pyNN.standardmodels import StandardCellType

class IF_curr_alpha(StandardCellType):
    """
    Leaky integrate and fire model with fixed threshold and alpha-function-
    shaped post-synaptic current.
    """
    <http://p_url.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000066>#Leaky IAF
    <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000026>#current-based model
    <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000116>#alpha function
    
    default_parameters = {
 
        'v_rest'     : -65.0,   # Resting membrane potential in mV. 
 		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000038>#Resting Membrane Potential
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000130>#voltage
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Resting membrane potential
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='v_rest'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=-65
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= mV
                
        'cm'         :   1.0,   # Capacity of the membrane in nF
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000131>#capacitance
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Capacity of the membrane
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='cm'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=1.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= nF

        'tau_m'      :  20.0,   # Membrane time constant in ms.
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000140>#time constant
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Membrane time constant
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='tau_m'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=20.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= ms
        
        'tau_refrac' :   0.1,   # Duration of refractory period in ms. 
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000039>#refractory period
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000208>#duration
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Duration of refractory period
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='tau_refrac'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=0.1
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= ms
        
        'tau_syn_E'  :   0.5,   # Rise time of the excitatory synaptic alpha function in ms.
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000111>#excitatory action
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000140>#time constant
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Rise time of the excitatory synaptic alpha function
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='tau_syn_E'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=0.5
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= ms
                        
        'tau_syn_I'  :   0.5,   # Rise time of the inhibitory synaptic alpha function in ms.
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000112>#inhibitory action
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000140>#time constant
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Rise time of the inhibitory synaptic alpha function
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='tau_syn_I'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=0.5
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= ms
        
        'i_offset'   :   0.0,   # Offset current in nA
        <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000044>#stimulation current
        <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000132>#current
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Offset current
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='i_offset'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=0.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= nA

        'v_reset'    : -65.0,   # Reset potential after a spike in mV.
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000130>#voltage
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Reset potential after a spike
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='v_reset'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=-65
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= mV
        
        'v_thresh'   : -50.0,   # Spike threshold in mV.
	    <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000082>#Fixed threshold        
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000130>#voltage
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Spike threshold
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='v_thresh'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=-50.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= mV
        
    }
    recordable = ['spikes', 'v']
    conductance_based = False
    default_initial_values = {
        'v': -65.0, #'v_rest',
    }

class IF_curr_exp(StandardCellType):
    """
    Leaky integrate and fire model with fixed threshold and
    decaying-exponential post-synaptic current. (Separate synaptic currents for
    excitatory and inhibitory synapses.
    """
    <http://p_url.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000066>#Leaky IAF
    <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000026>#current-based model
    <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000114>#instantaneous rise and monoexponential decay
    
    default_parameters = {
        
        'v_rest'     : -65.0,   # Resting membrane potential in mV. 
 		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000038>#Resting Membrane Potential
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000130>#voltage
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Resting membrane potential
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='v_rest'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=-65
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= mV
        
        'cm'         : 1.0,     # Capacity of the membrane in nF
        <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000131>#capacitance
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Capacity of the membrane
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='cm'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=1.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= nF
                
        'tau_m'      : 20.0,    # Membrane time constant in ms.
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000140>#time constant
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Membrane time constant
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='tau_m'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=20.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= ms
        
        'tau_refrac' : 0.1,     # Duration of refractory period in ms. 
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000039>#refractory period
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000208>#duration
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Duration of refractory period
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='tau_refrac'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=0.1
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= ms
        
        'tau_syn_E'  : 5.0,     # Decay time of excitatory synaptic current in ms.
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000111>#excitatory action
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000140>#time constant
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Decay time of excitatory synaptic current
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='tau_syn_E'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=5.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= ms
        
        'tau_syn_I'  : 5.0,     # Decay time of inhibitory synaptic current in ms.
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000112>#inhibitory action
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000140>#time constant
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Decay time of inhibitory synaptic current
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='tau_syn_I'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=5.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= ms
        
        'i_offset'   : 0.0,     # Offset current in nA
        <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000044>#stimulation current
        <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000132>#current
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Offset current
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='i_offset'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=0.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= nA

        'v_reset'    : -65.0,   # Reset potential after a spike in mV.
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000130>#voltage
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Reset potential after a spike
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='v_reset'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=-65
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= mV

        'v_thresh'   : -50.0,   # Spike threshold in mV.
	    <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000082>#Fixed threshold        
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000130>#voltage
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Spike threshold
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='v_thresh'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=-50.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= mV
        
    }
    recordable = ['spikes', 'v']
    conductance_based = False
    default_initial_values = {
        'v': -65.0, #'v_rest',
    }

class IF_cond_alpha(StandardCellType):
    """
    Leaky integrate and fire model with fixed threshold and alpha-function-
    shaped post-synaptic conductance.
    """
    <http://p_url.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000066>#Leaky IAF
    <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000027>#conductance-based model
    <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000116>#alpha function
        
    default_parameters = {

        'v_rest'     : -65.0,   # Resting membrane potential in mV. 
 		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000038>#Resting Membrane Potential
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000130>#voltage
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Resting membrane potential
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='v_rest'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=-65
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= mV

        'cm'         : 1.0,     # Capacity of the membrane in nF
        <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000131>#capacitance
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Capacity of the membrane
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='cm'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=1.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= nF

        'tau_m'      : 20.0,    # Membrane time constant in ms.
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000140>#time constant
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Membrane time constant
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='tau_m'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=20.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= ms

        'tau_refrac' : 0.1,     # Duration of refractory period in ms.
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000039>#refractory period
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000208>#duration
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Duration of refractory period
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='tau_refrac'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=0.1
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= ms

        'tau_syn_E'  : 0.3,     # Rise time of the excitatory synaptic alpha function in ms.
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000111>#excitatory action
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000140>#time constant
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Rise time of the excitatory synaptic alpha function
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='tau_syn_E'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=0.3
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= ms
        
        'tau_syn_I'  : 0.5,     # Rise time of the inhibitory synaptic alpha function in ms.
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000112>#inhibitory action
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000140>#time constant
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Rise time of the inhibitory synaptic alpha function
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='tau_syn_I'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=0.5
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= ms

        'e_rev_E'    : 0.0,     # Reversal potential for excitatory input in mV
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000130>#voltage
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Reversal potential for excitatory input
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='e_rev_E'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=0.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= mV

        'e_rev_I'    : -70.0,   # Reversal potential for inhibitory input in mV
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000130>#voltage
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Reversal potential for inhibitory input
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='e_rev_I'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=-70.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= mV

        'v_thresh'   : -50.0,   # Spike threshold in mV.
	    <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000082>#Fixed threshold        
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000130>#voltage
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Spike threshold
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='v_thresh'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=-50.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= mV

        'v_reset'    : -65.0,   # Reset potential after a spike in mV.
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000130>#voltage
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Reset potential after a spike
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='v_reset'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=-65
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= mV

        'i_offset'   : 0.0,     # Offset current in nA
        <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000044>#stimulation current
        <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000132>#current
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Offset current
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='i_offset'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=0.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= nA
        
    }
    recordable = ['spikes', 'v', 'gsyn']
    default_initial_values = {
        'v': -65.0, #'v_rest',
    }
    
class IF_cond_exp(StandardCellType):
    """
    Leaky integrate and fire model with fixed threshold and 
    exponentially-decaying post-synaptic conductance.
    """
    <http://p_url.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000066>#Leaky IAF
    <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000027>#conductance-based model
    <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000114>#instantaneous rise and monexponential decay
    
    default_parameters = {
        'v_rest'     : -65.0,   # Resting membrane potential in mV. 
 		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000038>#Resting Membrane Potential
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000130>#voltage
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Resting membrane potential
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='v_rest'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=-65
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= mV

        'cm'         : 1.0,     # Capacity of the membrane in nF
        <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000131>#capacitance
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Capacity of the membrane
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='cm'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=1.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= nF

        'tau_m'      : 20.0,    # Membrane time constant in ms.
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000140>#time constant
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Membrane time constant
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='tau_m'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=20.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= ms

        'tau_refrac' : 0.1,     # Duration of refractory period in ms.
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000039>#refractory period
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000208>#duration
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Duration of refractory period
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='tau_refrac'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=0.1
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= ms

        'tau_syn_E'  : 5.0,     # Decay time of the excitatory synaptic conductance in ms.
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000111>#excitatory action
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000140>#time constant
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Decay time of the excitatory synaptic conductance
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='tau_syn_E'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=5.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= ms

        'tau_syn_I'  : 5.0,     # Decay time of the inhibitory synaptic conductance in ms.
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000112>#inhibitory action
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000140>#time constant
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Decay time of the inhibitory synaptic conductance
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='tau_syn_I'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=5.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= ms

        'e_rev_E'    : 0.0,     # Reversal potential for excitatory input in mV
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000130>#voltage
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Reversal potential for excitatory input
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='e_rev_E'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=0.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= mV

        'e_rev_I'    : -70.0,   # Reversal potential for inhibitory input in mV
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000130>#voltage
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Reversal potential for inhibitory input
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='e_rev_I'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=-70.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= mV

        'v_thresh'   : -50.0,   # Spike threshold in mV.
	    <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000082>#Fixed threshold        
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000130>#voltage
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Spike threshold
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='v_thresh'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=-50.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= mV

        'v_reset'    : -65.0,   # Reset potential after a spike in mV.
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000130>#voltage
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Reset potential after a spike
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='v_reset'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=-65
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= mV

        'i_offset'   : 0.0,     # Offset current in nA
        <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000044>#stimulation current
        <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000132>#current
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Offset current
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='i_offset'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=0.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= nA
        
    }
    recordable = ['spikes', 'v', 'gsyn']
    default_initial_values = {
        'v': -65.0, #'v_rest',
    }

class IF_cond_exp_gsfa_grr(StandardCellType):
    """
    Linear leaky integrate and fire model with fixed threshold,
    decaying-exponential post-synaptic conductance, conductance based
    spike-frequency adaptation, and a conductance-based relative refractory
    mechanism.

    See: Muller et al (2007) Spike-frequency adapting neural ensembles: Beyond
    mean-adaptation and renewal theories. Neural Computation 19: 2958-3010.

    See also: EIF_cond_alpha_isfa_ista
    """

    <http://p_url.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000066>#Leaky IAF
    <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000027>#conductance-based model
    <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000114>#instantaneous rise and monexponential decay
    <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000085>#adaptation current
    
    default_parameters = {
        'v_rest'     : -65.0,   # Resting membrane potential in mV. 
 		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000038>#Resting Membrane Potential
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000130>#voltage
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Resting membrane potential
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='v_rest'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=-65
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= mV

        'cm'         : 1.0,     # Capacity of the membrane in nF
        <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000131>#capacitance
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Capacity of the membrane
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='cm'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=1.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= nF

        'tau_m'      : 20.0,    # Membrane time constant in ms.
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000140>#time constant
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Membrane time constant
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='tau_m'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=20.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= ms

        'tau_refrac' : 0.1,     # Duration of refractory period in ms.
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000039>#refractory period
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000208>#duration
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Duration of refractory period
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='tau_refrac'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=0.1
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= ms

        'tau_syn_E'  : 5.0,     # Decay time of the excitatory synaptic conductance in ms.
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000111>#excitatory action
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000140>#time constant
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Decay time of the excitatory synaptic conductance
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='tau_syn_E'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=5.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= ms

        'tau_syn_I'  : 5.0,     # Decay time of the inhibitory synaptic conductance in ms.
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000112>#inhibitory action
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000140>#time constant
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Decay time of the inhibitory synaptic conductance
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='tau_syn_I'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=5.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= ms

        'e_rev_E'    : 0.0,     # Reversal potential for excitatory input in mV
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000130>#voltage
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Reversal potential for excitatory input
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='e_rev_E'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=0.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= mV

 		'e_rev_I'    : -70.0,   # Reversal potential for inhibitory input in mV
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000130>#voltage
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Reversal potential for inhibitory input
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='e_rev_I'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=-70.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= mV

        'v_thresh'   : -50.0,   # Spike threshold in mV.
	    <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000082>#Fixed threshold        
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000130>#voltage
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Spike threshold
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='v_thresh'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=-50.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= mV

        'v_reset'    : -65.0,   # Reset potential after a spike in mV.
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000130>#voltage
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Reset potential after a spike
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='v_reset'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=-65
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= mV

        'i_offset'   : 0.0,     # Offset current in nA
        <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000044>#stimulation current
        <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000132>#current
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Offset current
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='i_offset'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=0.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= nA

        'tau_sfa'    : 100.0,   # Time constant of spike-frequency adaptation in ms
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000140>#time constant
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Time constant of spike-frequency adaptation
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='tau_sfa'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=100.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= ms        

        'e_rev_sfa'  : -75.0,   # spike-frequency adaptation conductance reversal potential in mV
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000130>#voltage
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=spike-frequency adaptation conductance reversal potential
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='e_rev_sfa'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=-75.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= mV

        'q_sfa'      : 15.0,    # Quantal spike-frequency adaptation conductance increase in nS
        <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000137>#maximal conductance 
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Quantal spike-frequency adaptation conductance increase
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='q_sfa'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=15.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= nS

        'tau_rr'     : 2.0,     # Time constant of the relative refractory mechanism in ms
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000140>#time constant
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Time constant of the relative refractory mechanism
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='tau_rr'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=2.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= ms        

        'e_rev_rr'   : -75.0,   # relative refractory mechanism conductance reversal potential in mV
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000130>#voltage
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=relative refractory mechanism conductance reversal potential
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='e_rev_rr'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=-75.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= mV

        'q_rr'       : 3000.0   # Quantal relative refractory conductance increase in nS   
        <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000137>#maximal conductance 
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Quantal relative refractory conductance increase
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='q_rr'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=3000.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= nS
        
    }
    recordable = ['spikes', 'v', 'gsyn']
    default_initial_values = {
        'v': -65.0, #'v_rest',
    }
    
class IF_facets_hardware1(StandardCellType):
    """
    Leaky integrate and fire model with conductance-based synapses and fixed 
    threshold as it is resembled by the FACETS Hardware Stage 1. 
    
    The following parameters can be assumed for a corresponding software
    simulation: cm = 0.2 nF, tau_refrac = 1.0 ms, e_rev_E = 0.0 mV.  
    For further details regarding the hardware model see the FACETS-internal Wiki:
    https://facets.kip.uni-heidelberg.de/private/wiki/index.php/WP7_NNM
    """
    
    default_parameters = {
        'g_leak'    :   40.0,     # nS
        'tau_syn_E' :   30.0,     # ms
        'tau_syn_I' :   30.0,     # ms
        'v_reset'   :  -80.0,     # mV
        'e_rev_I'   :  -80.0,     # mV,
        'v_rest'    :  -65.0,     # mV
        'v_thresh'  :  -55.0      # mV
    }
    recordable = ['spikes', 'v', 'gsyn']
    default_initial_values = {
        'v': -65.0, #'v_rest',
    }

class HH_cond_exp(StandardCellType):
    """Single-compartment Hodgkin-Huxley model.
    Reference: 
    Traub & Miles, Neuronal Networks of the Hippocampus, Cambridge, 1991.
    """
    <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000020>#detailed model
    <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000027>#conductance-based model
    <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000114>#instantaneous rise and monexponential decay
    
    default_parameters = {

        'gbar_Na'   : 20.0, # uS
        <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000137>#maximal conductance 
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=sodium maximal conductance
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='gbar_Na'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=20.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= uS

        'gbar_K'    : 6.0,  # uS
        <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000137>#maximal conductance 
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=potassium maximal conductance
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='gbar_K'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=6.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= uS

        'g_leak'    : 0.01, # uS
        <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000137>#maximal conductance 
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=leak maximal conductance
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='g_leak'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=0.01
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= uS

        'cm'        : 0.2,  # nF
        <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000131>#capacitance
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Capacity of the membrane
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='cm'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=1.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= nF
        
        'v_offset'  : -63.0, # mV
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000130>#voltage
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Offset voltage
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='v_offset'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=-63.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= mV
        
        'e_rev_Na'  : 50.0,
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000130>#voltage
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Reversal potential for the sodium current
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='e_rev_Na'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=50.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= mV
        
        'e_rev_K'   : -90.0,
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000130>#voltage
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Reversal potential for the potassium current
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='e_rev_K'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=-90.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= mV
        
        'e_rev_leak': -65.0,
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000130>#voltage
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Reversal potential for the leak conductance
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='e_rev_leak'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=-65.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= mV
        
        'e_rev_E'   : 0.0,
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000130>#voltage
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Reversal potential for excitatory input
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='e_rev_E'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=0.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= mV

        'e_rev_I'   : -80.0,
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000130>#voltage
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Reversal potential for inhibitory input
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='e_rev_I'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=-70.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= mV

        'tau_syn_E' : 0.2, # ms
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000111>#excitatory action
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000140>#time constant
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Decay time of the excitatory synaptic conductance
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='tau_syn_E'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=0.2
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= ms

        'tau_syn_I' : 2.0,
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000112>#inhibitory action
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000140>#time constant
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Decay time of the inhibitory synaptic conductance
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='tau_syn_I'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=2.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= ms

        'i_offset'  : 0.0, # nA
        <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000044>#stimulation current
        <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000132>#current
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Offset current
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='i_offset'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=0.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= nA
        
    }
    recordable = ['spikes', 'v', 'gsyn']
    default_initial_values = {
        'v': -65.0, #'v_rest',
    }

class EIF_cond_alpha_isfa_ista(StandardCellType):
    """
    Exponential integrate and fire neuron with spike triggered and
    sub-threshold adaptation currents (isfa, ista reps.) according to:
    
    Brette R and Gerstner W (2005) Adaptive Exponential Integrate-and-Fire Model
    as an Effective Description of Neuronal Activity. J Neurophysiol 94:3637-3642

    See also: IF_cond_exp_gsfa_grr, EIF_cond_exp_isfa_ista
    """
    <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000065>#EIF
    <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000027>#conductance-based model
    <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000116>#alpha function    
    <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000085>#adaptation current    
    
    default_parameters = {
    
    	'cm'        : 0.281,  # Capacitance of the membrane in nF
        <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000131>#capacitance
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Capacitance of the membrane
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='cm'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=0.281
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= nF

        'tau_refrac': 0.1,    # Duration of refractory period in ms.
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000039>#refractory period
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000208>#duration
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Duration of refractory period
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='tau_refrac'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=0.1
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= ms

        'v_spike'   : -40.0,    # Spike detection threshold in mV.
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000130>#voltage
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Spike detection threshold
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='v_spike'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=-40.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= mV
        
        'v_reset'   : -70.6,  # Reset value for V_m after a spike. In mV.
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000130>#voltage
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Reset value for V_m after a spike
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='v_reset'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=-70.6
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= mV
        
        'v_rest'    : -70.6,  # Resting membrane potential (Leak reversal potential) in mV.
 		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000038>#Resting Membrane Potential
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000130>#voltage
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Resting membrane potential (Leak reversal potential)
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='v_rest'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=-70.6
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= mV

        'tau_m'     : 9.3667, # Membrane time constant in ms
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000140>#time constant
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Membrane time constant
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='tau_m'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=9.3667
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= ms
        
        'i_offset'  : 0.0,    # Offset current in nA
        <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000044>#stimulation current
        <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000132>#current
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Offset current
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='i_offset'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=0.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= nA

        'a'         : 4.0,    # Subthreshold adaptation conductance in nS.
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000085>#adaptation current
        <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000137>#maximal conductance 
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Subthreshold adaptation conductance 
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='a'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=4.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= nS

        'b'         : 0.0805, # Spike-triggered adaptation in nA
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000085>#adaptation current
        <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000132>#current
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Spike-triggered adaptation
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='b'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=0.0805
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= nA
		
        'delta_T'   : 2.0,    # Slope factor in mV
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000059>#non-linear spike generation current
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000130>#voltage
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Slope factor
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='delta_T'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=2.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= mV
        
        'tau_w'     : 144.0,  # Adaptation time constant in ms
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000085>#adaptation current
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000140>#time constant
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Adaptation time constant
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='tau_w'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=144.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= ms

        'v_thresh'  : -50.4,  # Spike initiation threshold in mV
	    <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000082>#Fixed threshold        
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000130>#voltage
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Spike initiation threshold
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='v_thresh'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=-50.4
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= mV

        'e_rev_E'   : 0.0,    # Excitatory reversal potential in mV.
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000130>#voltage
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Excitatory reversal potential
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='e_rev_E'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=0.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= mV

        'tau_syn_E' : 5.0,    # Rise time of excitatory synaptic conductance in ms (alpha function).
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000111>#excitatory action
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000140>#time constant
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Rise time of excitatory synaptic conductance
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='tau_syn_E'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=5.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= ms

        'e_rev_I'   : -80.0,  # Inhibitory reversal potential in mV.
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000130>#voltage
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Inhibitory reversal potential
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='e_rev_I'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=-80.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= mV

        'tau_syn_I' : 5.0,    # Rise time of the inhibitory synaptic conductance in ms (alpha function).
       	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000112>#inhibitory action
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000140>#time constant
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Rise time of the inhibitory synaptic conductance
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='tau_syn_I'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=5.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= ms

    }
    recordable = ['spikes', 'v', 'w', 'gsyn']
    default_initial_values = {
        'v': -65.0, #'v_rest',
        'w': 0.0,
    }

class EIF_cond_exp_isfa_ista(StandardCellType):
    """
    Exponential integrate and fire neuron with spike triggered and
    sub-threshold adaptation currents (isfa, ista reps.) according to:
    
    Brette R and Gerstner W (2005) Adaptive Exponential Integrate-and-Fire Model
    as an Effective Description of Neuronal Activity. J Neurophysiol 94:3637-3642

    See also: IF_cond_exp_gsfa_grr, EIF_cond_alpha_isfa_ista
    """
    <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000065>#EIF
    <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000027>#conductance-based model
    <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000114>#instantaneous rise and monexponential decay
    <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000085>#adaptation current    
    
    default_parameters = {
    
        'cm'        : 0.281,  # Capacitance of the membrane in nF
        <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000131>#capacitance
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Capacitance of the membrane
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='cm'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=0.281
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= nF
        
        'tau_refrac': 0.1,    # Duration of refractory period in ms.
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000039>#refractory period
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000208>#duration
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Duration of refractory period
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='tau_refrac'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=0.1
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= ms

        'v_spike'   : -40.0,    # Spike detection threshold in mV.
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000130>#voltage
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Spike detection threshold
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='v_spike'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=-40.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= mV

        'v_reset'   : -70.6,  # Reset value for V_m after a spike. In mV.
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000130>#voltage
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Reset value for V_m after a spike
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='v_reset'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=-70.6
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= mV

        'v_rest'    : -70.6,  # Resting membrane potential (Leak reversal potential) in mV.
  		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000038>#Resting Membrane Potential
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000130>#voltage
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Resting membrane potential (Leak reversal potential)
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='v_rest'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=-70.6
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= mV

 		'tau_m'     : 9.3667, # Membrane time constant in ms
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000140>#time constant
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Membrane time constant
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='tau_m'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=9.3667
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= ms
        
        'i_offset'  : 0.0,    # Offset current in nA
        <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000044>#stimulation current
        <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000132>#current
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Offset current
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='i_offset'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=0.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= nA

        'a'         : 4.0,    # Subthreshold adaptation conductance in nS.
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000085>#adaptation current
        <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000137>#maximal conductance 
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Subthreshold adaptation conductance 
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='a'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=4.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= nS

        'b'         : 0.0805, # Spike-triggered adaptation in nA
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000085>#adaptation current
        <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000132>#current
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Spike-triggered adaptation
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='b'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=0.0805
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= nA
		
        'delta_T'   : 2.0,    # Slope factor in mV
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000059>#non-linear spike generation current
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000130>#voltage
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Slope factor
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='delta_T'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=2.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= mV

        'tau_w'     : 144.0,  # Adaptation time constant in ms
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000085>#adaptation current
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000140>#time constant
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Adaptation time constant
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='tau_w'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=144.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= ms

        'v_thresh'  : -50.4,  # Spike initiation threshold in mV
	    <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000082>#Fixed threshold        
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000130>#voltage
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Spike initiation threshold
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='v_thresh'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=-50.4
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= mV

        'e_rev_E'   : 0.0,    # Excitatory reversal potential in mV.
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000130>#voltage
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Excitatory reversal potential
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='e_rev_E'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=0.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= mV

        'tau_syn_E' : 5.0,    # Decay time constant of excitatory synaptic conductance in ms.
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000111>#excitatory action
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000140>#time constant
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Decay time constant of excitatory synaptic conductance
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='tau_syn_E'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=5.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= ms

        'e_rev_I'   : -80.0,  # Inhibitory reversal potential in mV.
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000130>#voltage
    	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Inhibitory reversal potential
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='e_rev_I'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=-80.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= mV

        'tau_syn_I' : 5.0,    # Decay time constant of the inhibitory synaptic conductance in ms.
       	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000112>#inhibitory action
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000140>#time constant
     	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000144>#name=Decay time constant of the inhibitory synaptic conductance
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000145>#notation='tau_syn_I'
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000146>#numerical value=5.0
		<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000147>#unit= ms

    }
    recordable = ['spikes', 'v', 'w', 'gsyn']
    default_initial_values = {
        'v': -65.0, #'v_rest',
        'w': 0.0,
    }


class SpikeSourcePoisson(StandardCellType):
    """Spike source, generating spikes according to a Poisson process."""
	
	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000013>#point process model
	
    default_parameters = {
    
    
        'rate'     : 1.0,     # Mean spike frequency (Hz)
        <http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000194>#rate
        
        'start'    : 0.0,     # Start time (ms)
        'duration' : 1e10      # Duration of spike sequence (ms)
    }
    recordable = ['spikes']
    injectable = False
    synapse_types = ()


class SpikeSourceInhGamma(StandardCellType):
    """
    Spike source, generating realizations of an inhomogeneous gamma process,
    employing the thinning method.

    See: Muller et al (2007) Spike-frequency adapting neural ensembles: Beyond
    mean-adaptation and renewal theories. Neural Computation 19: 2958-3010.
    """
	<http://purl.org/incf/ontology/Computational_Neurosciences/cno.owl#cno_0000013>#point process model
	
    default_parameters = {
        'a'        : numpy.array([1.0]), # time histogram of parameter a of a gamma distribution (dimensionless)
        'b'        : numpy.array([1.0]), # time histogram of parameter b of a gamma distribution (seconds)
        'tbins'    : numpy.array([0.0]),   # time bins of the time histogram of a,b in units of ms
        'start'    : 0.0,                # Start time (ms)
        'duration' : 1e10                 # Duration of spike sequence (ms)
    }
    recordable = ['spikes']
    injectable = False
    synapse_types = ()


class SpikeSourceArray(StandardCellType):
    """Spike source generating spikes at the times given in the spike_times array."""
    
    default_parameters = { 'spike_times' : [] } # list or numpy array containing spike times in milliseconds.
    recordable = ['spikes']
    injectable = False
    synapse_types = ()    
           
    def __init__(self, parameters):
        if parameters and 'spike_times' in parameters:
            parameters['spike_times'] = numpy.array(parameters['spike_times'], 'float')
        StandardCellType.__init__(self, parameters)
        
