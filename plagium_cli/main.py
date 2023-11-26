from src.components.cli_terminal import TerminalInterface
from src.components.plagium_cli import PlagiumCLI
from src.components.metadata import Metadata
from dotenv import dotenv_values

def main():
    env = dotenv_values(".env")
    cli = TerminalInterface()

    if not 'META_PATH' in env:
        env['META_PATH'] = ''

    with Metadata(env["META_PATH"]) as metadata:
        try:
            plagium_cli = PlagiumCLI(cli, metadata, env)
            plagium_cli.run()
        except KeyboardInterrupt:
            cli.print("Manually exiting the interface...", static=True)
            cli.print("Goodbye!", static=True)
            exit(0)
        except FileNotFoundError as e:
            cli.print(f"File {e.filename} not found", static=True)
            exit(1)
        finally:
            if 'path' in metadata and metadata['path'] != '':
                env['META_PATH'] = metadata['path']
                with open(".env", "w") as file:
                    for key, value in env.items():
                        file.write(f"{key}={value}\n")

if __name__ == "__main__":
    main()