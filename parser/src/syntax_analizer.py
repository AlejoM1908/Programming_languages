import re

class GrammarError(Exception):
    """
    Exception raised for errors in the provided grammar.
    """
    def __init__(self, message:str) -> None:
        super().__init__(message)

class GrammarRule:
    """
    Class that represents a grammar rule with the predictions groups for Descent Syntax Analizer.

    Attributes:
        exp (str): The lexeme that represents the non terminal of the rule.
        rules (list[list[str]]): The list of rules for the non terminal.
        predictions (list[set[str]]): The list of predictions groups for each rule.
    """
    def __init__(self, exp:str, rules:list[list[str]]) -> None:
        self.exp:str = exp
        self.rules:list[list[str]] = rules
        self.predictions:list[set[str]] = []

    def __str__(self) -> str:
        """
        If not prediction return the rule in the form:
            exp -> rule | rule2 | rule3 | ...
        If prediction return the rule in the form:
            exp -> rule : <pred1, pred2, pred3, ...>
            exp -> rule2 : <pred4, pred5, pred6, ...> 
            ...
        """
        if not self.predictions:
            return f"{self.exp} -> {' | '.join([' '.join(rule) for rule in self.rules])}"
        else: 
            final_rules = [(rule, pred) for rule, pred in zip(self.rules, self.predictions)]
            return '\n'.join([f"{self.exp} -> {' '.join(rule)} : <{','.join(pred)}>" for rule, pred in final_rules])

class SyntaxAnalizer:
    def __init__(self, grammar_path:str) -> None:
        self.path = grammar_path

        self._cleanGrammar()

    def _getInitialLexeme(self, raw_grammar:list[str]) -> tuple[str, int]:
        """
        Get the initial lexeme of the grammar.

        Returns:
            tuple[str, int]: The initial lexeme and the amount of lines to skip.
        """
        first_line = raw_grammar[0].strip().replace('\n', '')
        match = re.search(r'\S+ ->', first_line)

        if not match:
            return (first_line,1)
        else:
            return (match.group().replace(' ->', ''), 0)

    def _cleanGrammar(self) -> None:
        with open(self.path, 'r') as file:
            raw_grammar = file.readlines()

        # Remove comments and empty lines
        raw_grammar = [row for row in raw_grammar if row[0] != '\n' and not row.startswith('//') and not row.startswith('#')] 

        self.start_lexeme, skip = self._getInitialLexeme(raw_grammar)

        self.grammar:dict[str,GrammarRule] = {}
        for row in raw_grammar[skip:]:
            if row == '\n':
                continue
            exp, rule = row.split(' -> ')
            rule = rule.replace('\n', '').split(' ')

            if exp not in self.grammar:
                self.grammar[exp] = GrammarRule(exp, [rule])
            else:
                self.grammar[exp].rules.append(rule)

    def _computeFirsts(self, lexeme:str, first:dict[str,set[str]]) -> set[str]:
        # non terminal already computed
        if lexeme in first:
            return first[lexeme]
        
        # lexeme is epsilon
        if lexeme == 'epsilon':
            return {'#'}
        
        # lexeme is a terminal
        if lexeme not in self.grammar:
            return {lexeme}
        
        first[lexeme] = set()

        for rule in self.grammar[lexeme].rules:
            # Check for left recursion
            if rule[0] == lexeme:
                raise GrammarError(f"Grammar is not LL1, {lexeme} has left recursion")
            # Check for repeated firsts
            if rule[0] in first[lexeme] or (rule[0] == 'epsilon' and '#' in first[lexeme]):
                raise GrammarError(f"Grammar is not LL1, {lexeme} has multiple firsts")
            # Check for epsilon
            if rule[0] == 'epsilon':
                first[lexeme].add('#')
            # Check for terminal
            elif rule[0] not in self.grammar:
                first[lexeme].add(rule[0])
            # Check for non terminal
            else:
                next = self._computeFirsts(rule[0], first)

                # Check for epsilon in recursion
                if '#' in next:
                    first[lexeme].update(next - {'#'})
                    
                    if len(rule) > 1:
                        first[lexeme].update(self._computeFirsts(rule[1], first) - {'#'})
                    else:
                        first[lexeme].add('#')
                else:
                    first[lexeme].update(next)

        return first[lexeme]
    
    def _computeFollows(self, lexeme:str, follow:dict[str,set[str]]) -> dict[str,set[str]]:
        # non terminal already computed
        if lexeme in follow:
            return follow[lexeme]
        
        follow[lexeme] = set()

        if lexeme == self.start_lexeme:
            follow[lexeme].add('$')

        for exp, value in self.grammar.items():
            for rule in value.rules:
                for index, step in enumerate(rule):
                    if step == lexeme:
                        # Check if the step is the last one
                        if index != len(rule) - 1:
                            next_step = rule[index + 1]
                        else:
                            next_step = 'epsilon'
                            
                        follow[lexeme].update(self._computeFirsts(next_step, self.firsts) - {'#'})
                            
                        if '#' in self._computeFirsts(next_step, self.firsts):
                            follow[lexeme].update(self._computeFollows(exp, follow))
        
        return follow[lexeme]

    def _getPredictionGroups(self) -> None:
        self.firsts:dict[str,set[str]] = {}
        self.follows:dict[str,set[str]] = {}

        # Calculate firsts and follows groups
        for exp in self.grammar:
            # Calculate firsts
            self._computeFirsts(exp, self.firsts)

            # Calculate follows
            self._computeFollows(exp, self.follows)

        # Calculate predictions groups for each rule
        for exp, value in self.grammar.items():
            for rule in value.rules:
                value.predictions.append(set())

                for step in rule:
                    new_values = self._computeFirsts(step, self.firsts)
                    value.predictions[-1].update(new_values - {'#'})

                    if '#' not in new_values:
                        break
                    else:
                        value.predictions[-1].update(self._computeFollows(exp, self.follows))

            # Check for LL1 grammar rules
            for i in range(len(value.predictions) - 1):
                for j in range(i + 1, len(value.predictions)):
                    if value.predictions[i].intersection(value.predictions[j]):
                        raise GrammarError(f"Grammar is not LL1, {exp} has multiple predictions")

    def _convertToFunction(self, Grammar_rule:GrammarRule) -> str:
        if not Grammar_rule.predictions:
            return f"def {Grammar_rule.exp}(self) -> None:\n    pass\n"
        else:
            function = f"    def {Grammar_rule.exp}(self) -> None:\n"

            for rule, pred in zip(Grammar_rule.rules, Grammar_rule.predictions):
                function += f"        if self.token.token_type in {pred}:\n"
                
                for step in rule:
                    if step in self.grammar:
                        function += f"            self.{step}()\n"
                    elif step == 'epsilon':
                        break
                    else:
                        step_set = {step}
                        function += f'            self._match({step_set})\n'

                function += f"            return\n"

            function += f"        else:\n            self._raiseError({set().union(*Grammar_rule.predictions)})\n"

            return function
        
    def _convertToMain(self) -> str:
        main_str = f"    def compile(self) -> None:\n        self.{self.start_lexeme}()\n"
        
        main_str += f"        if self.token.token_type != '$':\n            self._raiseError({{'$'}})\n"

        main_str += "        else:\n            print('El analisis sintactico ha finalizado exitosamente.')\n"
        
        return main_str

    def generateAnalizer(self) -> None:
        self._getPredictionGroups()

        with open('src/assets/template.py', 'r') as file:
            template = file.read()

        functions = '\n'.join([self._convertToFunction(rule) for rule in self.grammar.values()])
        main = self._convertToMain()

        template = template.replace('$$FUNCTIONS$$', functions)
        template = template.replace('$$MAIN$$', main)

        with open('generated_compiler.py', 'w') as file:
            file.write(template)

    def test(self) -> None:
        try:
            self.generateAnalizer()

            print('\n'.join([str(rule) for rule in self.grammar.values()]))
            print("\n\nAnalizador sintactico generado exitosamente")
        except GrammarError as e:
            print(e.args[0])
            return
