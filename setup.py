from setuptools import setup


install_requires = [
    'spacy'
]

setup(name='piidetector',
      version='0.1',
      description='PII Detection using SpaCy and regular expression',
      url='https://github.com/hanymorcos/spacypiidetectorservice.git',
      author='Hany Morcos',
      author_email='hmorcos@donotemail.com',
      license='MIT',
      packages=['piidetector'],
      zip_safe=False,
      entry_points={
            'console_scripts': [
                'piidetector = spacypiidetector.piidetector:main',
            ],
       },
      include_package_data=True,
      install_requires=install_requires
      )
