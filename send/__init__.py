import sys, types

m = types.ModuleType('kafka.vendor.six.moves', 'Mock module')
setattr(m, 'range', range)
sys.modules['kafka.vendor.six.moves'] = m
