import setuptools

requirements = []
with open('requirements.txt') as f:
  requirements = f.read().splitlines()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Taho-Permissions",
    version="0.0.1",
    license="MIT",
    author="Baptiste",
    author_email="taho.discordbot@gmail.com",
    description="Permission system for Taho. Inspired by Rapptz's code (discord.py)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Taho-DiscordBot/Taho-Permissions",
    project_urls={
        "Bug Tracker": "https://github.com/Taho-DiscordBot/Taho-Permissions/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8.0",
    install_requires=requirements,
)