import os
import string
from pathlib import Path
from getpass import getpass
from ..colors.color import *

class TerminalInterface:
    def __init__(self) -> None:
        self._static_messages = []
        self._current_dir = os.getcwd()

    def _printStaticMessages (self) -> None:
        for message in self._static_messages:
            print(f'{CYAN}... {WHITE}{message}')

    def _clearTerminal(self, *, print_static:bool = False) -> None:
        '''
        Clears the terminal and reprint the static messages if print_static is True

        Keyword-Only Arguments:
            print_static {bool} -- Whether to reprint the static messages (default: False)

        Raises:
            OSError: If the terminal cannot be cleared
        '''
        os.system('cls' if os.name == 'nt' else 'clear')

        if print_static: self._printStaticMessages()

    def _calculateTableWidth(self, table: list[list[str]], *, headers: list[str] = None) -> list[int]:
        '''
        Calculate the max width of each column of a given table

        Positional Arguments:
            table {list[list[str]]} -- The table where the width will be calculated

        Keyword-Only Arguments:
            headers {list[str]} -- The headers of the table (default: None)

        Returns:
            list[int] -- A list with the width of each item, empty if the table is empty or is not provided

        Raises:
            ValueError: If the rows have different lengths

        Examples:
            >>> table = [['a', 'bb', 'ccc'], ['dd', 'eee', 'f']]
            >>> _calculateTableWidth(table)
            [2, 3, 3]

            >>> table = [['a', 'bb', 'ccc'], ['dd', 'eee', 'f']]
            >>> headers = ['Test1', 'Test2', 'Test3']
            >>> _calculateTableWidth(table, headers=headers)
            [5, 5, 5]

            >>> table = [['a', 'bb', 'ccc'], ['dd', 'eee', 'f', 'gg']]
            >>> _calculateTableWidth(table)
            ValueError: All lists must have the same length
        '''
        # Check if the list is empty
        if not table: return []

        # Check if every row has the same length
        row_length = len(table[0]) if not headers else len(headers)
        for row in table:
            if len(row) != row_length:
                raise ValueError('All lists must have the same length')

        # Add headers as a row to the beginning of the table
        if headers:
            table = [headers] + table

        # Transpose the table to iterate over each column
        transposed_table = list(zip(*table))

        # Calculate the max width of each column
        final_widths = [max(len(str(item)) for item in column) for column in transposed_table]
        return final_widths

    def _printTableRow(self, row: list[str], *, widths: list[int] = None, border_character: str = '|', middle_character: str = '|') -> None:
        '''
        Prints a given row with the given widths and characters in a pretty way

        The main structure of the row printing is:
        Border + Item + Middle + Item + Middle + ... + Item + Border

        Positional Arguments:
            row {list[str]} -- The list of items to print

        Keyword-Only Arguments:
            widths {list[int]} -- The width of each column (default: {None})
            border_character {str} -- The character to use for the start and end of the row (default: '|')
            middle_character {str} -- The character to use every change of column (default: '|')

        Examples:
            >>> row = ['a', 'bb', 'ccc']
            >>> _printTableRow(row)
            |a|bb|ccc|

            >>> row = ['a', 'bb', 'ccc']
            >>> widths = [5, 5, 5]
            >>> _printTableRow(row, widths=widths)
            |  a  |  bb | ccc |

            >>> row = ['a', 'bb', 'ccc']
            >>> widths = [5, 5, 5]
            >>> _printTableRow(row, widths=widths, border_character='-', middle_character='+')
            -  a  +  bb + ccc -
        '''
        if widths is None:
            widths = [len(str(item)) for item in row]

        if not row:
            return

        # Print the row with the given borders and items
        item_strings = [f'{WHITE}{item.center(widths[index])}' for index, item in enumerate(row)]
        content_string = f'{YELLOW}{middle_character}'.join(item_strings)
        result_string = f'{YELLOW}{border_character}{content_string}{YELLOW}{border_character}{WHITE}'

        print(result_string)

    def _printList(self, items: list[str], *, clear: bool = False, enumerate_options: bool = True, end: str = '\n') -> None:
        '''
        Just print a list of items, if enumerate is set to True, it will enumerate the items

        Positional Arguments:
            items {list[str]} -- The list of items to print

        Keyword-Only Arguments:
            clear {bool} -- Whether to clear the terminal before printing the items (default: False)
            enumerate_options {bool} -- Whether to enumerate the items (default: True)
            end {str} -- The character to use when ending the print (default: '\\n')

        Examples:
            >>> items = ['a', 'bb', 'ccc']
            >>> _printList(items)
            0. a
            1. bb
            2. ccc

            >>> items = ['a', 'bb', 'ccc']
            >>> _printList(items, enumerate_options=False)
            a
            bb
            ccc

            >>> items = ['a', 'bb', 'ccc']
            >>> _printList(items, end='###')
            0. a
            1. bb
            2. ccc###
        '''
        if not items:
            return

        if clear:
            self._clearTerminal()

        result_lines = []
        for index, item in enumerate(items):
            prefix = f'{YELLOW}{index}. {WHITE}' if enumerate_options else ''
            result_lines.append(f'{prefix}{item}')

        result_string = '\n'.join(result_lines)
        print(result_string, end=end)

    def numericInput(self, input_msg:str, *, max:float = None, min:float = None, clear:bool = True, print_static:bool = False, return_int:bool = True) -> float | int:
        '''
        Gets a numeric input from the user and validates it

        If the user sets a max or min value, the input must be between the range min <= input <= max

        Positional Arguments:
            input_msg {str} -- The message to display to the user

        Keyword-Only Arguments:
            max {float} -- The maximum value the user can input (default: None)
            min {float} -- The minimum value the user can input (default: None)
            clear {bool} -- Whether to clear the terminal before displaying the message (default: True)
            print_static {bool} -- Whether to add the message to the static messages array (default: False)
            return_int {bool} -- Whether to return an integer value (default: True)

        Returns:
            float -- The numeric input from the user if valid and the return_int is False
            int -- The numeric input from the user if valid and the return_int is True

        Raises:
            ValueError: If the max value is less than the min value
            ValueError: If the user input is not a number
            ValueError: If the user input is not between the range min <= input <= max

        Examples:
            >>> numericInput('Enter a number')
            ? (numeric) Enter a number: 5
            5

            >>> numericInput('Enter a number', max=4)
            ? (numeric) Enter a number: 5
            ValueError: Invalid input

            >>> numericInput('Enter a number', min=4)
            ? (numeric) Enter a number: 3
            ValueError: Invalid input

            >>> numericInput('Enter a number', min=4, max=6)
            ? (numeric) Enter a number: 5
            5

            >>> numericInput('Enter a number', return_int=False)
            ? (numeric) Enter a number: 5
            5.0
        '''
        if max is None: max = float('inf')
        if min is None: min = 0

        if max < min: raise ValueError('Max must be greater than min')

        if clear: self._clearTerminal(print_static=print_static)
        user_input = input(f'{YELLOW}?{CYAN} (numeric) {WHITE}{input_msg}')

        # Validate the user input
        try:
            user_input = float(user_input)
        except ValueError:
            raise ValueError('Invalid input')

        if user_input < min or user_input > max: 
            raise ValueError('Invalid input')

        if return_int:
            user_input = int(user_input)

        return user_input

    def booleanInput(self, input_msg:str, *, clear:bool = True, print_static:bool = False) -> bool:
        '''
        Gets a boolean input from the user

        Positional Arguments:
            input_msg {str} - The message to display to the user

        Keyword-Only Arguments:
            clear {bool} - Whether to clear the terminal before displaying the message (default: True)
            print_static {bool} - Whether to add the message to the static messages array (default: False)

        Returns:
            bool - The boolean input from the user if valid

        Examples:
            >>> booleanInput('Enter a boolean')
            ? (yes/no) Enter a boolean: yes
            True

            >>> booleanInput('Enter a boolean')
            ? (yes/no) Enter a boolean: no
            False

            >>> booleanInput('Enter a boolean')
            ? (yes/no) Enter a boolean: y
            True

            >>> booleanInput('Enter a boolean')
            ? (yes/no) Enter a boolean: l
            False
        '''
        if clear: self._clearTerminal(print_static=print_static)
        user_input = input(f'{YELLOW}?{CYAN} (yes/no) {WHITE}{input_msg}').lower()

        return user_input in ['y', 'yes']

    def stringInput(self, input_msg:str, *, clear:bool = True, print_static:bool = False, obsure:bool = False, safe:bool = False, correct:bool = False) -> str:
        '''
        Gets a string input from the user, allowing for validation of the input and correction of invalid characters if needed

        Positional Arguments:
            input_msg {str} - The message to display to the user

        Keyword-Only Arguments:
            clear {bool} - Whether to clear the terminal before displaying the message (default: True)
            print_static {bool} - Whether to add the message to the static messages array (default: False)
            obsure {bool} - Whether to obsure the user input (default: False)
            safe {bool} - Whether to check the input for invalid characters (default: False)
            correct {bool} - Whether to correct the input if it contains invalid characters, if set to True it ignore the safe flag (default: False)

        Returns:
            str - The string input from the user if valid

        Raises:
            ValueError: If the user input is not a valid string and the safe flag is set to True and the correct flag is set to False

        Examples:
            >>> stringInput('Enter a string')
            ? (string) Enter a string: Hello World
            'Hello World'

            >>> stringInput('Enter a string', safe=True)
            ? (string) Enter a string: Hello World!
            ValueError: Invalid input

            >>> stringInput('Enter a string', correct=True)
            ? (string) Enter a string: Hello World!
            'Hello World'
        '''
        if clear: self._clearTerminal(print_static=print_static)

        if obsure: user_input = getpass(f'{YELLOW}?{CYAN} (string) {WHITE}{input_msg}')
        else: user_input = input(f'{YELLOW}?{CYAN} (string) {WHITE}{input_msg}')

        # Define a whitelist of allowed characters
        allowed_chars = set(string.ascii_letters + string.digits + string.punctuation + 'áéíóúüÁÉÍÓÚÜ' + ' ')

        # Remove any characters that are not in the whitelist
        if correct:
            user_input = ''.join(c for c in user_input if c in allowed_chars)
        # Check that the user input only contains characters from the whitelist
        elif safe and not all(c in allowed_chars for c in user_input):
            raise ValueError('Invalid input')

        return user_input

    def passwordInput(self, input_msg:str, *, clear:bool = True, print_static:bool = False) -> str:
        '''
        Gets a password input from the user, the input will be obsured

        Positional Arguments:
            input_msg {str} - The message to display to the user

        Keyword-Only Arguments:
            clear {bool} - Whether to clear the terminal before displaying the message (default: True)
            print_static {bool} - Whether to add the message to the static messages array (default: False)

        Returns:
            str - The password input from the user if valid

        Raises:
            ValueError: If the user input is not a valid string and the clear flag is set to False
        '''
        return self.stringInput(input_msg, clear=clear, print_static=print_static, obsure=True)

    def generateMenu(self, title:str, menu_options: list[str], *, returnable:bool = True, return_message:str = None, print_static:bool = False, clear:bool = True, max_errors:int = 10) -> int:
        '''
        Displays a menu to the user and returns the selected option

        If returnable is set to True, the option 0 will be reserved to the return to back menu option, so the options will be enumarated starting from 1

        Positional Arguments:
            title {str} - The title of the menu
            menu_options {list[str]} - The options to display to the user

        Keyword-Only Arguments:
            returnable {bool} - Whether to add the option to return to the menu (default: True)
            print_static {bool} - Whether to reprint the static messages (default: False)
            clear {bool} - Whether to clear the terminal before displaying the menu (default: True)
            max_errors {int} - The maximum number of errors the user can make before a ValueError is raised (default: 10)

        Returns:
            int - The user selected option index, or -1 if the user selected return and returnable is set to True

        Raises:
            ValueError: If the user input is not a valid option and the clear flag is set to False
            ValueError: If the maximum number of errors is reached

        Examples:
            >>> generateMenu('Menu', ['Option 1', 'Option 2', 'Option 3'])
            Menu

            0. Volver
            1. Option 1
            2. Option 2
            3. Option 3

            Seleccione una opción: 2
            2

            >>> generateMenu('Menu', ['Option 1', 'Option 2', 'Option 3'], returnable=False)
            Menu

            0. Option 1
            1. Option 2
            2. Option 3

            Seleccione una opción: 2
            2

            >>> generateMenu('Menu', ['Option 1', 'Option 2', 'Option 3'], returnable=False, clear=False)
            Menu

            0. Option 1
            1. Option 2
            2. Option 3

            Seleccione una opción: 3
            valueError: Invalid input
        '''
        error_counter:int = 0
        movement:int = returnable # As the boolean value is 0 or 1, this will add 0 or 1 to the user input to get the correct index

        # Adding the return option to the menu and the custom message if available
        if returnable:
            if return_message is None: return_message = 'Return to last menu'
            menu_options = [return_message] + menu_options

        while error_counter < max_errors:
            if clear: self._clearTerminal(print_static=print_static)
            if error_counter > 0:  print(f'{RED}! {YELLOW}Invalid option!{WHITE}\n')
            
            print(title, end='\n\n')

            # Printing the options
            self._printList(menu_options)

            # Getting the user selection among the options
            try:
                user_input = self.numericInput("Select an option: ", max=len(menu_options) - 1 + movement, clear=False)
            except ValueError as exep:
                if not clear: raise exep
                continue

            return user_input - movement
        
        raise ValueError('Invalid input')

    def matchStringArrays(self, source: list[str], target: list[str], *, prematch: list[str] = None, purge_empty:bool = True, return_message:str = None, max_errors:int = 10) -> dict[str, str]:
        '''
        Displays a menu to the user to map a column of options to another

        Positional Arguments:
            source {list[str]} - The columns of the source list
            target {list[str]} - The columns of the target list
        
        Keyword-Only Arguments:
            prematch {list[str]} - The columns of the target list that are already mapped to the source, must be the same length as the source list (default: None)
            purge_empty {bool} - Whether to remove empty values from the result map before returning it (default: True)

        Returns:
            dict[str, str] - A dictionary with the source and target columns mapped

        Raises:
            ValueError: If the source or target lists are not set or empty
            ValueError: If the prematch list is not the same length as the source list
            ValueError: If all the values of source are not completly maped to target and the flag purge_empty is set to False
            ValueError: If the user make the maximum number of errors consecutively

        Examples:
            >>> matchStringArrays(source=['Columna 1', 'Columna 2', 'Columna 3'], target=['Columna 1', 'Columna 2', 'Columna 3'])
            Mapee todas las columnas que desee usar:

            Columna 1 -> Empty
            Columna 2 -> Empty
            Columna 3 -> Empty

            Seleccione una opción: 1
            Mapee la columna Columna 1:

            0. Columna 1
            1. Columna 2
            2. Columna 3

            Seleccione una opción: 2

            >>> matchStringArrays(source=['Columna 1', 'Columna 2', 'Columna 3'], target=['Columna 1', 'Columna 2', 'Columna 3'], prematch=['Columna 1', 'Columna 2', 'Columna 3'])
            Mapee todas las columnas que desee usar:

            Columna 1 -> Columna 1
            Columna 2 -> Columna 2
            Columna 3 -> Columna 3

            Seleccione una opción: 1
            Mapee la columna Columna 1:
            
            0. Columna 1
            1. Columna 2
            2. Columna 3

            Seleccione una opción: 2
        '''
        if not source or not target: raise ValueError('Source and target must be set and not empty')
        if prematch is not None and len(prematch) != len(source): raise ValueError('Prematch must have the same length as source')
        
        result_map:dict[str, str] = {source[i]: prematch[i] if prematch is not None else '' for i in range(len(source))}

        while True:
            # Display the result map so the user can see the mapping progress
            options:list[str] = [f'{key} -> {value if value != "" else "Empty"}' for key, value in result_map.items()]

            # Choose a column from the source file to map
            user_input = self.generateMenu('Map all the columns to use: \n', options, return_message=return_message, max_errors=max_errors)
            if user_input == -1: break

            # Choose a column from the target file to map to the selected source column
            map_input = self.generateMenu(f'Map the column {YELLOW}{source[user_input - 1]}{WHITE}', target, max_errors=max_errors)
            if map_input == -1: continue

            result_map[source[user_input]] = target[map_input]

        # Remove the empty values from the result map and return it
        if not purge_empty and '' in result_map.values(): raise ValueError('There are empty values in the result map')

        return {key: value for key, value in result_map.items() if value != ''} if purge_empty else result_map

    def editableStringList(self, message:str, *, values:list[str] = None, clear:bool = True, max_errors:int = 10) -> list[str]:
        '''
        Displays a menu to the user to edit a list of options

        Positional Arguments:
            message {str} - The message to display before the list

        Keyword-Only Arguments:
            values {list[str]} - The array to edit (default: None)
            clear {bool} - Whether to clear the terminal before displaying the menu (default: True)
            max_errors {int} - The maximum number of errors the user can make before the function raises an error (default: 10)

        Returns:
            list[str] - The edited array

        Examples:
            >>> editableList('Lista de elementos', values = ['Elemento 1', 'Elemento 2', 'Elemento 3'])
            Lista de elementos

            Elemento 1
            Elemento 2
            Elemento 3

            Que desea hacer con la lista?: 

            0. Agregar elemento
            1. Eliminar elemento
            2. Finalizar edición

            ? (Numeric) Seleccione una opción: 0
        '''
        if values is None: values = []
        error_counter:int = 0
        error:bool = False

        while error_counter < max_errors:
            if clear: self._clearTerminal()
            if error: 
                print(f'{RED}!! {YELLOW}Invalid Option{WHITE}')
                error_counter += 1
                error = False

            options:list = ['Add an element', 'Remove an element', 'Finish editing']

            # Display the current array
            self.print(message)
            self._printList(values, enumerate_options=False)

            # Get the user selection
            try:
                user_input = self.generateMenu('\n\nWhat you want to do with the list?: ', options, returnable=False, clear=False)
            except ValueError:
                error = True
                continue
            
            # Reset the error counter if the user makes a valid selection
            error_counter = 0

            # Add an element to the array
            if user_input == 0:
                element:str = self.stringInput('Add the value of the new element: ', clear=False)
                values.append(element)

            # Remove an element from the array
            elif user_input == 1:
                delete_index:int = self.generateMenu('\nWhat element you want to remove?: ', values, returnable=False)
                values.pop(delete_index)

            # Finish editing the array
            elif user_input == 2: break

        return values

    def editableMap(self, map:dict = None, *, clear:bool = True) -> dict:
        '''
        Displays a menu to the user to edit a map of options

        Positional Arguments:
            map {dict} - The map to edit (default: None)

        Keyword-Only Arguments:
            clear {bool} - Whether to clear the terminal before displaying the menu (default: True)

        Returns:
            dict - The edited map

        Examples:
            >>> editableMap({'Elemento 1': 'Valor 1', 'Elemento 2': 'Valor 2', 'Elemento 3': 'Valor 3'})
            Elemento 1 -> Valor 1
            Elemento 2 -> Valor 2
            Elemento 3 -> Valor 3

            Que desea hacer con el mapa?:

            0. Agregar elemento
            1. Eliminar elemento
            2. Finalizar edición

            ? (Numeric) Seleccione una opción: 0
        '''
        if map is None: map = {}

        while True:
            if clear: self._clearTerminal()
            options:list = ['Add element', 'Remove element']

            # Display the current map
            self._printList([f'{key} -> {value}' for key, value in map.items()], enumerate_options=False)

            # Get the user selection
            user_input = self.generateMenu('What do you want to do with the map?: ', options, return_message='Finish editing', clear=False)
            if user_input == -1: break

            # Add an element to the map
            elif user_input == 0:
                key:str = self.stringInput('Insert the key for the new element to add: ')
                value:str = self.stringInput('Insert the value for the new element to add: ')
                map[key] = value

            # Remove an element from the map
            elif user_input == 1:
                delete_index:int = self.generateMenu('Wich element you want to remove?: ', [f'{key} -> {value}' for key, value in map.items()])
                if delete_index != 0: del map[list(map.keys())[delete_index]]

        return map

    def fileExplorer(self, *, clear:bool = True, text:str = None, extensions:list[str] = None, only_directories:bool = False, only_files:bool = False, print_static:bool = False) -> list:
        '''
        Generate a file system explorer, if a file is selected the path of the file is returned automatically, else wait for the user to select a directory manually

        The explorer add two options to the menu that all always first and second: 0 end the search and return the selected directory, 1 return to the parent directory

        When a path is a directory an slash is added at the end of the path name

        Keyword-only Arguments:
            clear {bool} - Whether to clear the terminal before displaying the menu (default: True)
            text {str} - The text to display at the top of the menu (default: None)
            extensions {list[str]} - The extensions of the files to show (default: None)
            only_directories {bool} - Whether to show only directories (default: False)
            print_static {bool} - Whether to print the menu staticly (default: False)

        Returns:
            list - The path of the directory or file selected by the user, and a number indicating if the selected path is a directory (0) or a file (1)

        Raises:
            ValueError: If the user inserts an invalid option 10 consecutive times
        '''
        TAGS:dict[str,str] = {'Directory': f'{PURPLE}Directory{WHITE}', 'File': f'{GREEN}File{WHITE}'}
        current_dir = Path(self._current_dir)

        while True:
            # Get all the files and directories in the current path and place them in a list with [name, type]
            files:list[str, str] = [[file.name, TAGS['Directory'] if file.is_dir() else TAGS['File']] for file in current_dir.iterdir()]
            # Get only the directories if the flag is set to True
            files = [[f_name, f_type] for f_name, f_type in files if not only_directories or f_type == TAGS['Directory']]
            # Get only the files with the specified extensions
            files = [[f_name, f_type] for f_name, f_type in files if f_type == TAGS['Directory'] or not extensions or Path(f_name).suffix in extensions]

            # Add the files to the options list
            options:list = ['Select this directory', 'Got to parent directory'] if not only_files else ['Go to parent directory']
            options += [f'{f_name} - {f_type}' for f_name, f_type in files] 

            user_input:int = self.generateMenu(f'{text}\nActually selecting in: {YELLOW}{os.path.abspath(current_dir)}{WHITE}\n', options, returnable=False, print_static=print_static, clear=clear)
            if only_files: user_input += 1

            # Static options: 0 end search, 1 parent directory
            if user_input == 0: 
                self._current_dir = str(current_dir)
                return [str(current_dir), 0]
            elif user_input == 1: 
                current_dir = current_dir.parent
                continue

            # If the user selected a file return the path of the file
            selected_file, selected_type = files[user_input - 2]
            if selected_type == TAGS['File']: 
                self._current_dir = str(current_dir)
                return [str(current_dir / selected_file), 1]
            
            current_dir /= selected_file

    def printTable(self, table:list[list[str]], *, headers:list[str] = None, print_static:bool = False, rows_per_page:int = 20) -> None:
        '''
        Print a matrix to the terminal in a pretty way adding a page system every 20 rows

        Positional Arguments:
            table {list[list[str]]} - The table to print

        Keyword-only Arguments:
            headers {list[str]} - The headers of the table (default: None)
            print_static {bool} - Whether to print the table staticly (default: False)
            rows_per_page {int} - The number of rows to print per page (default: 20)

        Raises:
            ValueError: If the table is empty or is None

        Examples:
            >>> printTable([['Name', 'Age'], ['John', '20'], ['Mary', '19']])
            Page 1 of 1

            |Name|Age|
            |----+---|
            |John|20 |
            |Mary|19 |

            0. Finish exploring
            ? (numerical) Select an option: 0
        '''
        if not table: raise ValueError('The table cannot be empty or None')

        # Set headers from the first row of the table if not provided
        if headers is None: 
            headers:list[str] = table[0]
            table = table[1:]

        selected_page = 1
        error = False

        page_number = len(table) // rows_per_page + 1
        pages:list = [table[i:i + rows_per_page] for i in range(0, len(table), rows_per_page)]

        while True:
            # Calculate each column width
            widths:list[int] = self._calculateTableWidth(headers, pages[selected_page - 1])

            self._clearTerminal(print_static=print_static)
            if error: 
                print(f'{RED}!! {YELLOW}Invalid option{WHITE}\n')
                error = False
            print(f'Page {YELLOW}{selected_page} of {WHITE}{page_number}\n')

            # Print the headers
            self._printTableRow(headers, widths=widths)

            # Print separator
            self._printTableRow(['-' * width for width in widths], widths=widths, middle_character='+')

            # Print the data
            for row in pages[selected_page - 1]:
                self._printTableRow(row, widths=widths)

            # Add interactive options
            options:list = []
            if selected_page != 1: options.append('Last page')
            if selected_page != page_number: options.append('Next page')
            options.append('Finish exoloring')

            try:
                user_input:int = self.generateMenu('\n', options, returnable=False, clear=False, print_static=print_static)
            except ValueError:
                error = True
                continue

            # Page selection logic
            if len(options) == 3:
                if user_input == 0: selected_page -= 1
                elif user_input == 1: selected_page += 1
                else: break

            elif len(options) == 2:
                if selected_page == 1 and user_input == 0: selected_page += 1
                elif selected_page == page_number and user_input == 0: selected_page -= 1
                else: break

            elif len(options) == 1 and user_input == 0: break
            else : error = True

    def multiselect(self, text:str, options:list, *, print_static:bool = False) -> list:
        '''
        Generate a multiselect menu

        Positional Arguments:
            text {str} - The text to display at the top of the menu
            options {list[str]} - The options to display

        Keyword-only Arguments:
            print_static {bool} - Whether to print the menu staticly (default: False)

        Returns:
            list - A list of the selected options

        Examples:
            >>> multiselect('Select the options you want', ['Option 1', 'Option 2', 'Option 3'])
            Select the options you want

            1.[ ] Option 1
            2.[ ] Option 2
            3.[ ] Option 3

            Insert the index you want to select: 1
            ...
            Select the options you want

            1.[X] Option 1
            2.[ ] Option 2
            3.[ ] Option 3

            Insert the index you want to select: 2
        '''
        is_selected:list = [False] * len(options)
        error:bool = False

        while True:
            self._clearTerminal(print_static=print_static)
            if error: 
                print(f'{RED}!! {YELLOW}Invalid option{WHITE}\n')
                error = False
            print(f'{text}\n\n', f'{YELLOW}0. {WHITE}Finish', sep='')

            for index, option in enumerate(options):
                print(f'{YELLOW}{index + 1}.[{GREEN}{"X" if is_selected[index] else " "}{YELLOW}] {WHITE}{option}')

            try:
                user_input:int = self.numericInput('Insert the index you want to select: ', max=len(options), clear= False, print_static=print_static)
                if user_input == 0: break
                is_selected[user_input - 1] = not is_selected[user_input - 1]
            except ValueError:
                error = True
                continue

        return [options[index] for index, option in enumerate(is_selected) if option]

    def print(self, text:str, *, static:bool = False) -> None:
        '''
        Print a message to the terminal

        Positional Arguments:
            text {str} - The message to print

        Keyword-only Arguments:
            static {bool} - Whether to print the message staticly (default: False)

        Examples:
            >>> print('This is a message')
            This is a message

            >>> print('This is a static message', static=True)
            ... This is a static message

            >>> print('This is a message')
            ... This is a static message
            This is a message
        '''
        if static: 
            self._static_messages.append(text)
            print(f'{CYAN}... {WHITE}{text}')
        else: print(text)
