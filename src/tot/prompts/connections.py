standard_prompt = '''What's the connection between the following four things?

{input}

First provide your reasoning, then provide your answer as the last line.
'''

# propose_prompt = '''What's the connection between the following four things?

# {input}

# Answer:
# {output}

# Refine this answer. First provide your reasoning, then provide your answer as the last line.'''

value_prompt = ''' What's the connection between the following four things?

{input}

Answer:
{output}

Evaluate if the given answer is correct (sure/likely/impossible). First provide your reasoning, then provide your rating (sure/likely/impossible) in the last line.
'''