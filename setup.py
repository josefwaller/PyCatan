from setuptools import setup

setup(name='pycatan',
      version='0.12',
      description='A Python Module for playing The Settlers of Catan',
      url='https://github.com/josefwaller/PyCatan',
      long_description=open("readme.md").read(),
      author='Josef Waller',
      author_email='josef@siriusapplications.com',
      license='MIT',
      install_requires=[
            "quotequail"
      ],
      packages=['PyCatan'],
      zip_safe=False)