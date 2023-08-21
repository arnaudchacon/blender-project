import bpy
import sys
import numpy as np
import json
import math
import os.path

print("Starting the test_blender_script...")

# ... [All the helper functions from the original script]

def main(argv):
    # Remove starting object cube
    objs = bpy.data.objects
    objs.remove(objs["Cube"], do_unlink=True)

    if len(argv) > 7:  # Note YOU need 8 arguments!
        program_path = argv[5]
        target = argv[6]
        print("Program Path:", program_path)
        print("Target:", target)
    else:
        exit(0)

    # ... [Rest of the main function]

print("Calling main function...")
main(["dummy_arg", "dummy_arg", "dummy_arg", "dummy_arg", "dummy_arg", "dummy_arg", "dummy_arg", "dummy_arg"])
print("Main function executed.")
