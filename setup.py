from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r', encoding='utf-8') as f:
    return f.read()

setup(
  name='pycc',
  version='1.0.0',
  author='SystemSoftware',
  author_email='dimasoft976@gmail.com',
  description='Компилятор C в Python',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/SystemSoftware2/pycc',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.13',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='python c compiler',
  python_requires='>=3.7'
)
