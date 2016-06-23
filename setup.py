from setuptools import setup

setup(name='address-book',
      version='1.0',
      description='https://github.com/gingerpayments/hiring/blob/master/coding-assignments/python-address-book-assignment.rst',
      url='',
      author='Dominik Zabron',
      author_email='dominik.zabron@gmail.com',
      license='MIT',
      packages=['address_book'],
      install_requires=[
          'nose',
          'fake-factory',
      ],
      zip_safe=False)
