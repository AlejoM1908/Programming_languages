# Plagium CORE

This repository contains the main logic for a plagiarism detection project. It deploys a REST API that receives files and returns the plagiarism report over all the files.

## Architecture

The main project architecture is based on the clean architecture, allowing the core to be completely modular and easy to continue developing or add any kind of interface. Uses concurrent programming to analyze the files faster and a ANTLR4 generated parser from the main official [grammars](https://github.com/antlr/grammars-v4) repository.

### Description of the architecture
The architecture is divided in four main types of modules:
- **Entities**: The main data structures of the project.
- **Use Cases**: The main logic of the project.
- **gateways**: The interfaces to interact with the external world.
- **External Interfaces**: The interfaces to interact with the external world.

The main idea is to have a inmutable bussiness logic composed of use cases and entities, and then have the gateways and external interfaces to interact with the external world aeasily added, modified or removed.

This architecture also enhance the testability of the project, allowing to test each module independently or generate mocks interfaces to simulate the external world.

### Concurrency

The core uses concurrency to analyze the files, it converts each file into a AST and then compares each unique pair of ASTs into a thread pool using an inspiration over the [AST-CC algorithm](https://ieeexplore.ieee.org/document/7424821?section=abstract) with takes advantage of a linear data structure filled with sub-trees hashes, then it compares the hashes to find the similarity between the files.

## Current Supported Languages
- Python3

## Deployment

The main REST API is builded with the Flask framework, so it can be deployed with the command:

```bash
pip install -r requirements.txt
flask run
```
Also you can use docker to deploy a container with the following command:

```bash
docker build -t plagium_core .
docker run -d -p 5000:5000 --name plagium_core plagium_core
```