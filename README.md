This is an experiment, with some very cool results!

It has very few components:

-   A [script](./chat-and-execute.py) that emulates the chat interface with ChatGPT, with the extra capability of [running arbitrary commands given by the AI on the host](#the-execute-directive) (of course the script itself was built with ChatGPT)
-   a [SudoLang](https://github.com/paralleldrive/sudolang-llm-support/blob/b477188820678cdedc7dcf0cc9b5e526be277532/sudolang.sudo.md) prompt ["CLI Coder"](./sudo/cli-coder.sudo)

When used together we effectively get a **TDD Machine**, that works in small steps, constantly verifying the previous steps using concrete commands on the host cli.

[Here's an example](./fizzbuzz-chat-readable) of the machine working on the fizzbuzz kata.

## The `execute:` Directive

The AI can respond with lines of the form `execute: {command}` - and these commands are automatically executed on the host as a child process.

This of course gives the AI access to any tool (e.g. `curl https://raw.githubusercontent.com/nitsanavni/tdd-machine/main/README.md`, `python -m pytest`, `cat main.py`).

example:

AI says:

```markdown
execute: git status
```

Automatic response:

```
executeResult {
  cmd: git status
  output: On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   current_chat.txt

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        git-status

no changes added to commit (use "git add" and/or "git commit -a")
  exit: 0
}
```
