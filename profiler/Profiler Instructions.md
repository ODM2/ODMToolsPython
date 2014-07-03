cprofile is included in the basic python package
install from source: 
```pip install runsnakerun```

run the following command in the console:
```python -m cProfile -o profile.dat ..\odmtools\ODMToolsPython.py```

ODM Tools python will run. Run the code you want to profile. i.e. click buttons
When you close odm tools python the code will also close and generate the .dat file

Then, run the following command:

```python runsnake.py profile.dat```