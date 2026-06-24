# CH02 Prompts

Prompt blocks extracted from the current manuscript source.

## Vague summary request

````text
Summarize this document.
````

## Structured summary request

````text
Summarize this document in 3-5 bullet points.
Focus on actionable recommendations. Skip background information.
Each bullet should be one sentence.
````

## Step-by-step code review

````text
Review this code in three steps:
1. First, identify what the code accomplishes
2. Then, list any bugs with line numbers
3. Finally, propose fixes for each issue, explaining why each fix works
````

## Ask for a PR description

````text
Write a PR description for this diff:

[the staged git diff]
````

## Retry: JSON parse error

````text
That JSON was invalid: Expecting value: line 1 column 1 (char 0). Fix it to match the schema.
````

## Retry: schema validation error

````text
That JSON was invalid: ['Test invalid email'] is too short. Fix it to match the schema.
````
