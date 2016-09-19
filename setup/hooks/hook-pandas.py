
from PyInstaller.utils.hooks import exec_statement
#from PyInstaller.build import Tree

pandas_path = exec_statement("import pandas; print pandas.__path__[0]")
print pandas_path

#dict_tree = Tree(pandas_path, prefix='pandas', excludes=["*.pyc"])
#datas = dict_tree
#binaries = filter(lambda x: 'pandas' not in x[0], binaries)
