from setuptools import setup

setup(
    name='chia_anime_downloader',
    version="1.0",
    description='Chia Anime Downloader - To batch download anime from chia-anime.tv',  # noqa
    long_description='Anime batch downloader for chia-anime.tv. Can download any anime from http://chia-anime.tv with varying qualities. Supports episode ranges.',  # noqa
    license='MIT',
    author='Anshuman Verma',
    url='https://github.com/anshumanv/chia-anime-downloader',
    scripts=['chia_anime_downloader.py'],
    entry_points={
        'console_scripts': [
            'chia_anime_downloader = chia_anime_downloader:command_line_runner',  # noqa
        ]
    },
    install_requires=[
        'requests',
        'beautifulsoup4',
        'lxml',
        'docopts'
    ]
)
