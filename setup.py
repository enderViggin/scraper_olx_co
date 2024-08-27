from setuptools import setup, find_packages


# Добавляем все зависимости парсера
with open('requirements.txt') as f: required = f.read().splitlines()

setup(
    name='scraper_olx_co',
    version='1.0.0',
    author='Author Name',
    author_email='ila186295@gmail.com',
    packages=find_packages(),
    install_requires=required,
)

