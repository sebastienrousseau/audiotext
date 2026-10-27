# Copyright (C) 2023 Sebastien Rousseau.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

setup_requirements = []
test_requirements = ["pytest>=7.4.2"]

setup(
    name="audiotextpro",
    version="0.0.1",
    description="A Python module for interacting with the AssemblyAI API for audio transcription.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Sebastien Rousseau",
    author_email="sebastian.rousseau@gmail.com",
    url="https://github.com/sebastienrousseau/audiotextpro",
    license="Apache Software License",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="assemblyai, transcription, audio, API",
    packages=find_packages(),
    install_requires=[
        "requests>=2.26.0",
        "python-dotenv>=1.2.2",
    ],
    setup_requires=setup_requirements,
    tests_require=test_requirements,
    test_suite="tests",
)
