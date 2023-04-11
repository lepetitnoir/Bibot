from setuptools import setup

setup(name="JPV-DE-project",
      version="0.1",
      description="JPV-DE-project",
      url="https://github.com/DataScientest-Studio/JPV-DE-project",
      author="JPV",
      author_email="",
      license="Apache-2.0",
      packages=["bibot"],
      install_requires=[
          "python-dotenv",
          "binance-connector",
          "aiohttp",
          "elasticsearch",
          "sqlalchemy",
          "matplotlib",
          "statsmodels",
          "jupyter"

      ],
      zip_safe=False)
