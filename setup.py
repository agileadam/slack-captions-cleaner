from setuptools import setup, find_packages

setup(
    name="slack-captions-cleaner",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "beautifulsoup4",
    ],
    entry_points={
        "console_scripts": [
            "slack-captions-cleaner=slack_captions_cleaner.cleaner:main",
        ],
    },
    description="A tool to clean Slack Huddle captions exports",
    author="Adam Courtemanche",
    author_email="adam.courtemanche@gmail.com",
)
