from setuptools import setup, find_packages


# Путь к библиотеке ax, которая хранится локально на компьютере
PATH_TO_AX_LIBRARY: str = ''
if not PATH_TO_AX_LIBRARY: raise ValueError('Укажите путь к библиотеке ax')

# Добавляем все зависимости парсера
with open('requirements.txt') as f:
    required = f.read().splitlines()
    required.append(f'ax @ file://localhost{PATH_TO_AX_LIBRARY}')

setup(
    name='scraper_olx_co',
    version='1.0.0',
    author='Author Name',
    author_email='ila186295@gmail.com',
    packages=find_packages(),
    install_requires=required,
)

