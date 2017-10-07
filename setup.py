from setuptools import setup, find_packages
import chia_anime_downloader

setup(
    name='chia_anime_downloader',
    version="1.0",
    description='chia_anime_downloader',
    long_description='Anime batch downloader for chia-anime',
    license='MIT',
    author='Anshuman Verma',
    url='https://github.com/anshumanv/chia-anime-downloader',
    scripts=['chia_anime_downloader.py'],
    entry_points={
        'console_scripts': [
            'chia_anime_downloader = chia_anime_downloader:command_line_runner',
        ]
    },
    install_requires=[
        'requests',
        'beautifulsoup4'
    ]
)
