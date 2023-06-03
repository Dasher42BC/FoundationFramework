# In most versioned mods, the __init__.py of the latest version is intended
# to hold version numbers and dependency requirements. -Dasher42

__version__ = 20230603

# Other versioned mods should probably load their versioned dependencies here.

print "Foundation 2023 initializing"

pFoundation = __import__("Foundation")
pNewFoundation = __import__("_Foundation")

pFoundation.__dict__.update(pNewFoundation.__dict__)