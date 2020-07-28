from setuptools import setup, find_packages

setup(name='age of triggers',
      version='0.0',
      description='Age of Empire 2 HD/DE python API',
      author='Nicolas Carrara',
      author_email='nicolas.carrara1u@gmail.com',
      url='https://github.com/ncarrara/age-of-triggers',
      package_data={'aot.meta_triggers.api': ['templates/*.aoe2scenario']},
      include_package_data=True,
      packages=['aot',
                'aot.assets',
                'aot.model',
                'aot.meta_triggers',
                'aot.utilities',
                'aot.model',
                'aot.model.controller',
                'aot.model.enums'])
