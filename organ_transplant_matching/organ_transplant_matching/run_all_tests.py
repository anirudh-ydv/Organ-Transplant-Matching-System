"""Runs every test in the project: python run_all_tests.py"""
import unittest
import dp_organ_matching
import test_phase1_structures

suite = unittest.TestSuite()
loader = unittest.defaultTestLoader
suite.addTests(loader.loadTestsFromModule(dp_organ_matching))          # 18 DP tests (Phase 2)
suite.addTests(loader.loadTestsFromModule(test_phase1_structures))     # 17 structure tests (Phase 1)
result = unittest.TextTestRunner(verbosity=1).run(suite)
print(f"\nTOTAL: {result.testsRun} tests, {len(result.failures)} failures, {len(result.errors)} errors")
