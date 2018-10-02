# -*- coding: utf-8 -*-

# Copyright 2018, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.


# This file will be modified when the QCircuit interface is updated
# with new simulator commands (Issue #10).
# Thoughout, code segments that are to be removed in this change are surrounded with *** and !!!

'''
Testing the simulators for simple circuits
'''


import test.terra.common as common
import unittest
import qiskit

# ***
from qiskit_addon_qv import AerQvSimulator
# !!!  Replace with  from qiskit_addon_qv import AerQvProvider


class TestSimple(common.QiskitAerTestCase):
    """Simple integrations tests"""
    def setUp(self):
        # ***
        self.qv_backend = AerQvSimulator()

    def test_bell_execution(self):
        """Test the result of executing a simple H"""
        q_reg = qiskit.QuantumRegister(1)
        c_reg = qiskit.ClassicalRegister(1)
        q_circuit = qiskit.QuantumCircuit(q_reg, c_reg)

        q_circuit.h(q_reg[0])
        q_circuit.measure(q_reg[0], c_reg[0])

        qobj = qiskit.compile(q_circuit, backend=self.qv_backend, seed=73846087)
        job = self.qv_backend.run(qobj)
        result = job.result()
        counts = result.get_counts(q_circuit)
        target = {
            '0x0': qobj.config.shots/2,
            '0x1': qobj.config.shots/2
        }
        threshold = 0.04 * qobj.config.shots
        self.assertDictAlmostEqual(counts, target, threshold,
                                   msg=self.generate_circuit_exception_msg(q_circuit))

if __name__ == '__main__':
    unittest.main()
