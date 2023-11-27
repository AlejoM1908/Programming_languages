# Plagium CLI

This repository contains the CLI for the plagiarism detection project. It allows to interact with the main core of the project using the command line, with a hand made library to use python3 default libraries to generate the CLI.

## Usage

To use the CLI you can use the following command:

```bash
pip install -r requirements.txt
python3 main.py
```
start configuring the CLI with the `configure start` command, then you can use the `process` command to choose all the directories you want to process and then the files in them, so total control is given to the user.

## Commands

The CLI has the following commands:
- `help`: Shows the help message.
- `exit`: Exits the CLI.
- `process`: Process the files in the given directory.
- `version`: Shows the current version of the CLI.
- `clear`: Clears the screen.
- `configure`: Configures the CLI.

## Environment Variables
To start the CLI you need to configure the following environment variables into a `.env` file in this directory:
- CORE_HOST: The host of the plagium core.
- CORE_PORT: The port of the plagium core.