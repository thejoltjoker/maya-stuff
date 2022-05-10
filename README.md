# Maya scripts and stuff

Scripts and other handy maya things.

Most of the scripts are quite customized for my workflow or previous problems I've had to solve.
But it might serve as a base for something else hopefully!

I'm learning more for every script I make, and I try to go back and update some scripts with the new things I've learned.

## Contents

### scripts 📜

Sorted python scripts that should run in Maya.

### expressions 🔢

Some expressions I've found useful.

### sandbox 🏖️

Random scripts and snippets that are either unfinished or just not suitable elsewhere. Don't expect anything to run.

### shelves 📚

My custom shelf. It's a bit messy.

## Setup
- Add parent folder of this repo to `PYTHONPATH`
- Add this code your userSetup.py
    ```Python
    from maya_scripts import scripts_to_menu
    scripts_to_menu.create_menu()
    ```
  