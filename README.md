This is an experiment, with some very cool results!

It has very few components:

-   A [script](./chat-and-execute.py) that emulates the chat interface with ChatGPT, with the extra capability of running arbitrary commands given by the AI on the host (of course the script itself was built with ChatGPT)
-   a [SudoLang](https://github.com/paralleldrive/sudolang-llm-support/blob/b477188820678cdedc7dcf0cc9b5e526be277532/sudolang.sudo.md) prompt ["CLI Coder"](./sudo/cli-coder.sudo)

When used together we effectively get a **TDD Machine**, that works in small steps, constantly verifying the previous steps using concrete commands on the host cli.

[Here's an example](./fizzbuzz-chat-readable) of the machine working on the fizzbuzz kata.

# The `execute:` Directive

The AI can respond with lines of the form `execute: {command}` - and these commands are automatically executed on the host as a child process.

example:

```markdown
execute: git status
```
