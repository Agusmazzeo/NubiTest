import setuptools

VERSION = '1.0.0'

requirements = ["flask",
                "flask-cors",
                "gunicorn",
                ]

# YOU NEED TO INSTALL THIS FROM THE DIRECTORY THIS FILE IS LOCATED (Currently: $repo/src/.)
setuptools.setup(name='nubi_test',
                 version=VERSION,
                 description='A little program for serving polls.',
                 url='',
                 author='Agustin Mazzeo',
                 author_email='agusmazzeo1@gmail.com',
                 license='Private',
                 packages=setuptools.find_packages(where="src"),
                 package_dir={"": "src"},
                 zip_safe=False,
                 install_requires=requirements)