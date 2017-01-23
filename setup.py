from setuptools import setup, find_packages

setup(
    name='pardot-api-client',
    version='0.0.1',
    description='Pardot API Client',
    author='Max Naude',
    author_email='maxnaude@gmail.com',
    url='https://github.com/maxnaude/pardot-api-client',
    packages=find_packages(),
    dependency_links=[],
    install_requires=[
        'hammock==0.2.4',
        'pprintpp==0.3.0',
        'six==1.10.0',
    ],
    test_suite='nose.collector',
    tests_require=['nose', 'responses'],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Office/Business',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
