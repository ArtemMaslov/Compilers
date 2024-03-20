# Compilers

Compilers is a project to test basic compiler optimization's algorithms.

### Requirements

1. `Python`. Version >= 3.11. Version is obligatory to use some features of typing module.
    Installation example for Ubuntu 22.04
    ```
    sudo apt install python3.11
    ```
    after that you should use `python3.11`, rather than `python3` or `python`.
1. `jsoncomment` to parse jsons with comments. 
    Installation (You should change `python` to your python's interpreter path):
    ```
    python -m pip install jsoncomment
    ```
1. `colorama` for colored text. Version >= 0.4.6. 
    Installation (You should change `python` to your python's interpreter path):
    ```
    python -m pip install colorama
    ```
    Attention: preinstalled with python colorama version might be older, than required.
    To install newest version run (You should change `python` to your python's interpreter path):
    ```
    python -m pip install --force-reinstall colorama
    ```

### Project structure

1. `CFG`. Control flow graph class.
1. `DomTree`. Dominators tree.
1. `test`. Folder with different tests.