import unittest

def run_tests():
    # This will discover all modules in the 'tests' directory that match the pattern 'test*.py'.
    loader = unittest.TestLoader()
    suite = loader.discover('tests', pattern='test*.py')

    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

if __name__ == '__main__':
    run_tests()
