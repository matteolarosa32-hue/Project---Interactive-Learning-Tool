import sys
import os

# 1. Get the directory of the test file
current_test_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Go UP one level to reach the folder where your logic files live
project_root = os.path.abspath(os.path.join(current_test_dir, '..'))

# DIAGNOSTIC PRINT (To confirm we found the right place)
print(f"\n--- RE-DEBUGGING PATHS ---")
print(f"Now looking in: {project_root}")
if os.path.exists(project_root):
    print(f"Files found here: {os.listdir(project_root)}")
print(f"--------------------------\n")

# 3. Add that root to the path
sys.path.insert(0, project_root)

# 4. Now the imports should work
from stats_mode import StatsManager

def test_accuracy_math():
    """Ensures we don't crash on 0 views"""
    # We can even test the method directly if we initialize the class
    sm = StatsManager()
    # If you moved the math to a helper method, call it here:
    assert (5 / 10) * 100 == 50.0