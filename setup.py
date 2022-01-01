from glob import glob

from setuptools import setup, find_packages
import pkg_resources

PACKAGE_NAME = "genspa"

# Creates a __version__ variable.
with open(PACKAGE_NAME + "/_version.py") as file:
    exec(file.read())

# Read requirements.
with open('requirements.txt') as fp:
    REQUIREMENTS = [str(r) for r in pkg_resources.parse_requirements(fp)]

print("Requirements:", REQUIREMENTS)

setup(name=PACKAGE_NAME,
      version=__version__,
      description="Genetic Algorithm implementation to classify webpage's components using site's screenshot image.",
      long_description="LONGER DESCRIPTION HERE",
      long_description_content_type="text/markdown",
      keywords="genetic algorithm image webpage single page application wesite classification",
      author="Juan Ignacio Bagnato",
      license="Copyright JIB",
      packages=find_packages(),
      install_requires=REQUIREMENTS,
      entry_points={
          "console_scripts": [
              "{} = {}.__main__:main".format(PACKAGE_NAME, PACKAGE_NAME)
          ]
      },
        include_package_data=True,
        data_files=[
            ('../../config', glob('config/*.json'))
        ],
      zip_safe=False)
