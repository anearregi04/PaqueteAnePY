from setuptools import setup

setup(
   name='PaqueteAnePY',
   version='0.0.1',
   author='Ane Arregi',
   author_email='aarregi015@ikasle.ehu.eus',
   packages=['PaqueteAnePY'],
   url='https://github.com/anearregi04/PaqueteAnePY',
   license='LICENSE.txt',
   description='Este paquete incluye las funciones utilizadas para la asignatura Software Matemático y estadístico',
   long_description=open('README.txt').read(),
   tests_require=['pytest'],
   install_requires=[
      "pandas >= 0.25.1",
      "matplotlib >= 3.1.1",
      "numpy >=1.17.2"
   ],
)