# run profiler, view with runsnakerun
cprofile is included in the basic python package
install from source: 
```pip install runsnakerun```

run the following command in the console:
```python -m cProfile -o profile.dat ..\odmtools\ODMToolsPython.py```

ODM Tools python will run. Run the code you want to profile. i.e. click buttons
When you close odm tools python the code will also close and generate the .dat file

Then, run the following command:

```python runsnake.py profile.dat```


# To run memory profiler with meliae

To install Meliae, you will need a working C extension compilation environment (Meliae uses a Cython extension):

```easy_install meliae```

Now instrument your application to be able to trigger a memory dump at the moment you would like to capture, like so:

```
from meliae import scanner
scanner.dump_all_objects( filename ) # you can pass a file-handle if you prefer
```
The memory dump will generally be quite large (e.g. 2MB to describe an application with 200KB of user-controllable memory usage (i.e. not the interpreter itself)) and for any real application will take an extremely long time to load (multiple minutes for 16MB dumps).

```
$ runsnakemem <filename>
```

