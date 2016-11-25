from distutils.core import setup
import py2exe
import sys
 
#this allows to run it with a simple double click.
sys.argv.append('py2exe')

py2exe_options = {
        "includes": ["sip",],  # 如果打包文件中有PyQt代码，则这句为必须添加的
        #"excludes": ["CommuMain","Para","Translate",],
        "dll_excludes": ["MSVCP90.dll",],  # 这句必须有，不然打包后的程序运行时会报找不到MSVCP90.dll，如果打包过程中找不到这个文件，请安装相应的库
        "compressed": 1,
        "optimize": 2,
        "ascii": 0,
        "bundle_files": 2,  # 关于这个参数请看第三部分中的问题(2)
        }
 
setup(
      name = 'PyQt Demo',
      version = '1.0',
      windows = ['Main_UpSite.py',],   # 括号中更改为你要打包的代码文件名
      zipfile = None,
      options = {'py2exe': py2exe_options}
      )

import os
import shutil
import PyQt4
path = os.path.dirname(PyQt4.__file__)
path += r"/plugins/imageformats"
shutil.rmtree("dist/imageformats", True) 
shutil.copytree(path, "dist/imageformats")
shutil.copytree('data', "dist/data")
shutil.copytree('image', "dist/image")