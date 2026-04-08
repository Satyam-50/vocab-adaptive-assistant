from setuptools import find_packages, setup


setup(
	name="vocab-adaptive-assistant",
	version="1.0.0",
	packages=find_packages(),
	include_package_data=True,
	install_requires=[
		"fastapi>=0.110,<1.0",
		"uvicorn[standard]>=0.27,<1.0",
		"pydantic>=2.0,<3.0",
		"scikit-learn>=1.3,<2.0",
		"numpy>=1.24,<3.0",
		"joblib>=1.3,<2.0",
	],
)

