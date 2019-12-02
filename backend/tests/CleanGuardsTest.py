import unittest
import CleanGuards

cleaner = CleanGuards.CleanGuards("/Users/nalshahwan/ffep/examplesAl/file3a.pre.c.output.guards.complex.cvc")
cleaner.setFormulas()
formulas=cleaner.getTranslation()
print(formulas)
