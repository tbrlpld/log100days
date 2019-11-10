from setuptools import find_packages, setup


def get_requirements():
    with open("requirements.txt") as reqf:
        return [line.strip() for line in reqf.readlines()]


setup(
    name="log100days",
    version="1.1.0",
    description="Quart app to display my Markdown 100-days-log as HTML",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=get_requirements(),
)
