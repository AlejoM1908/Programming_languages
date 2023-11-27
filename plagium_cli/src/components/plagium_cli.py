from src.components.cli_terminal import TerminalInterface
from dataclasses import dataclass
import requests
import json
import os

class OptionsError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

class NotConfiguredError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

class ExitCommand(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

@dataclass
class Command:
    name: str
    general: str
    specific: str

    def __eq__(self, other: str) -> bool:
        if isinstance(other, Command):
            return self.name == other.name
        elif isinstance(other, str):
            return self.name == other
        else:
            return False

class PlagiumCLI:
    def __init__(self, cli: TerminalInterface, metadata: dict, env:dict) -> None:
        self.interface = cli
        self.metadata = metadata
        
        if 'CORE_HOST' in env and 'CORE_PORT' in env:
            self.core_url = f"{env['CORE_HOST']}:{env['CORE_PORT']}"
        else:
            raise ValueError('No connection to the Plaguium Core')

        self._AVAILABLE_EXTENSIONS:list[str] = ['.py']

        with open('src/assets/man.json') as file:
            self._AVAILABLE_COMMANDS:list[Command] = [Command(**command) for command in json.load(file)]

    def _runCommand(self, command: list[str]) -> None:
        if hasattr(self, f"_run{command[0].capitalize()}Command"):
            try:
                getattr(self, f"_run{command[0].capitalize()}Command")(command[1:])
            except OptionsError:
                self.interface.print(f"The options <{' '.join(command[1:])}> are not valid for the command {command[0]}. Type 'help {command[0]}' to see the available options.")
            except NotConfiguredError:
                self.interface.print("You must configure the CLI before using it. Type 'config start' to start the configuration process.")
        else:
            raise NotImplementedError(f"Command {command[0]} not implemented")
        
    def _checkConfigured(self) -> bool:
        if 'new_user' in self.metadata:
            return not self.metadata['new_user']
        
        return False

    def _runHelpCommand(self, options: list) -> None:
        if len(options) <= 1:
            # General help
            if len(options) == 0:
                self.interface.print("Available commands:")
                for command in self._AVAILABLE_COMMANDS:
                    self.interface.print(f"{command.name} - {command.general}")

            # Specific help for a command
            else:
                if options[0] in self._AVAILABLE_COMMANDS:
                    command_index = self._AVAILABLE_COMMANDS.index(options[0])
                    command_description = self._AVAILABLE_COMMANDS[command_index].specific
                    self.interface.print(f"{options[0]} - {command_description}")
                else:
                    raise OptionsError(f"Command {options[0]} not found")

        else:
            raise OptionsError("Too many options")
        
    def _runExitCommand(self, options: list) -> None:
        if len(options) == 0:
            self.interface.print("Exiting Plagium Detector CLI...", static=True)
            self.interface.print("Goodbye!", static=True)
            raise ExitCommand("Exiting Plagium Detector CLI...")
        else:
            raise OptionsError("Too many options")
        
    def _runVersionCommand(self, options: list) -> None:
        if len(options) == 0:
            self.interface.print("Plagium Detector CLI v1.0.0")
        else:
            raise OptionsError("Too many options")
        
    def _runClearCommand(self, options: list) -> None:
        if len(options) == 0:
            self.interface._clearTerminal()
        else:
            raise OptionsError("Too many options")
        
    def _runConfigCommand(self, options: list) -> None:
        if len(options) > 1:
            raise OptionsError("Too many options")

        configured = self._checkConfigured()

        if len(options) == 0:
            self.interface.print("Available configuration:")

            for key, value in self.metadata.items():
                self.interface.print(f"{key} -> {value}")
            
            return

        if options[0] == 'start' and not configured:
            option = self.interface.booleanInput("Do you want to save the configuration in other directory? (y/n): ", clear=False)

            if not option:
                self.metadata['path'] = os.getcwd() + '/metadata.json'
                self.metadata['new_user'] = False
                return

            path, _ = self.interface.fileExplorer(text="Select the directory where the configuration will be stored: ", only_directories=True)
            self.metadata['path'] = path + '/metadata.json'
            self.metadata['new_user'] = False
            return
        elif options[0] == 'edit':
            if not configured:
                raise NotConfiguredError("user not configured")
            
            self._editConfig(self.metadata)
        elif options[0] == 'reset':
            if not configured:
                raise NotConfiguredError("user not configured")
            
            self.metadata['new_user'] = True
            self.metadata['path'] = ''
        else:
            raise OptionsError("Invalid option")
        
    def _selectDirectories(self) -> list[str]:
        directories = []

        while True:
            if len(directories) > 0:
                self.interface._clearTerminal()
                self.interface.print("Selected directories:")
                self.interface._printList(directories)

                option = self.interface.booleanInput("Do you want to add another directory? (y/n): ", clear=False)

                if not option:
                    break

            directories.append(self.interface.fileExplorer(text="Select the directories where the files to be processed are located: ", only_directories=True)[0])

        return directories
    
    def _selectFiles(self, directories: list[str]) -> list[str]:
        files = []

        for directory in directories:
            for file in os.listdir(directory):
                if os.path.splitext(file)[1] in self._AVAILABLE_EXTENSIONS:
                    files.append(directory + '/' + file)
        
        return self.interface.multiselect("Select the files to be processed: ", files)
        
    def _runProcessCommand(self, options: list) -> None:
        if len(options) > 0:
            raise OptionsError("Too many options")

        directories = self._selectDirectories()

        files = self._selectFiles(directories)

        # Generate request to core
        body = {os.path.basename(file): open(file, 'rb') for file in files}
        
        try:
            response = requests.post(f"http://{self.core_url}/v1.1/process", files=body)
        except requests.exceptions.InvalidSchema:
            self.interface.print("No connection to the Plaguium Core. Check if the server is running.")
            return
        finally:
            # Ensure files are closed
            for file in body.values():
                file.close()

        if response.status_code == 200:
            report = [f"{data['file1']} - {data['file2']} -> {data['similarity']}" for data in response.json()['report']]
            self.interface.print("Report:")
            self.interface._printList(report, enumerate_options=False)
        else:
            self.interface.print('Ocurrió un error al procesar los archivos. Intente nuevamente.')

    def _editConfig(self, config: dict) -> None:
        if config is None:
            config = {
                'new_user': True,
                'path': ''
            }

        while True:
            option = self.interface.generateMenu('Editing configuration', [f"{key} -> {value}" for key, value in config.items()], return_message="Finalizar edición")

            if option == -1:
                break

            new_value = self.interface.stringInput("Value: ", clear=False)
            config[list(config.keys())[option]] = new_value

    def showWelcome(self) -> None:
        self.interface._clearTerminal()
        self.interface.print("Welcome to Plagium Detector CLI!")
        self.interface.print("Type 'help' to see the available commands.")

        if not 'new_user' in self.metadata or self.metadata['new_user']:
            self.interface.print("As a new user, you should configure the CLI before using it.")
            self.interface.print("Type 'config start' to start the configuration process.")

    def run(self) -> None:
        self.showWelcome()
        while True:
            command = self.interface.stringInput("plagium-cli > ", clear=False).split()

            if len(command) == 0:
                continue

            if command[0] in self._AVAILABLE_COMMANDS:
                try:
                    self._runCommand(command)
                except ExitCommand:
                    break
            else:
                self.interface.print("Invalid command. Type 'help' to see the available commands.")
