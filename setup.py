from setuptools import setup

setup(
    name='bibclean',
    version='2.0.0',
    description='A BibTeX processing utility',
    author='Toby Fleming',
    author_email='tobywf@users.noreply.github.com',
    packages=['bibclean'],
    install_requires=[
        'click',
        'bibtexparser',
        'fuzzywuzzy',
        'python-Levenshtein'
    ],
    package_data={
        'bibclean': ['data/*']
    },
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'bibclean = bibclean.clean:cli',
            'bibextra = bibclean.extra:cli',
        ]
    }
)
