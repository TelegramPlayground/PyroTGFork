# Contributing to this Pyrogram Fork

Welcome, and thank you for your interest in contributing to this Pyrogram Fork!

Pyrogram was (and hopefully should continue to be) an open source project that depends on the generous help of contributors who volunteer their time and skills. We appreciate your involvement and support.

You can contribute in many ways, not only by writing code. This document aims to give you a high-level overview of how you can get involved.

## What Can I Do?

In short: anything you find useful!

If you’re unsure whether your changes are welcome, open an issue on GitHub or preferably ask in the [Telegram chat](https://t.me/pyrotgfork/2).

In case you’d like to get some inspiration what we're working on, we have a [long list of issues across all repositories](https://github.com/issues?q=is%3Aissue%20is%3Aopen%20(repo%3ATelegramPlayground%2FPyroTGFork%20OR%20repo%3ATelegramPlayground%2Fpyrogram%20OR%20repo%3ATelegramPlayground%2Fpyrogram-tgcrypto)%20sort%3Acreated-desc) and there is usually also a [pinned issue](https://github.com/TelegramPlayground/PyroTGFork/issues) which tells you which issues need help.

## Asking Questions

If you have a question, please use the [Telegram Chat](https://t.me/pyrotgfork/2) instead of opening an issue. Simply start a message in the correct topic and our community will gladly answer.

## Providing Feedback

Feedback from the community is very important to us as the maintainers of this Pyrogram fork. If you have any suggestions, ideas, or concerns, please share them with us. You can use the [Telegram Chat](https://t.me/pyrotgfork/2) to start a conversation.

You might be wondering about the difference between asking questions, providing feedback, and making feature requests. Asking questions is about seeking help or clarification. Providing feedback involves sharing your thoughts and opinions on the existing features and the project as a whole. Feature requests, on the other hand, are about suggesting new features or improvements. See the next section for more details on feature requests.

## Creating Issues

Have you identified a reproducible problem in this Pyrogram fork? Do you have a feature request? Here is how you can report your issue as efficiently as possible.

### Look For an Existing Issue

Before creating a new issue, check the open issues to see if someone else has already reported the same problem or requested the same feature.

If you find an existing issue that is relevant to yours, you can comment on it and express your support or disagreement with a reaction:

- upvote 👍
- downvote 👎

If none of the open issues match your case, then create a new issue following the guidelines below.

### How to Write a Bug Report

A bug report should contain the following information:

- A clear and descriptive title that summarizes the problem.
- A brief description of what you were doing when the bug occurred, and what you expected to happen.
- A detailed description of the actual behavior and how it differs from the expected behavior.
- [Steps to reproduce the bug](https://stackoverflow.com/help/minimal-reproducible-example), preferably in as much detail as possible in text format.
- The version of Pyrogram and the operating system you are using. Kindly refrain from reporting issues noticed incase you are unable to reproduce it consistently with this Pyrogram fork.
- Any relevant error messages or logs.

### How to Write a Feature Request

A feature request should contain the following information:

- A clear and descriptive title that summarizes the feature.
- A brief explanation of why you need this feature and how it would benefit the project and the community.
- A detailed description of how the feature should work and what it should look like, preferably with examples.
- Optionally any relevant links or references to similar features in other projects or applications.

## Creating a Pull Request

To contribute code to this Pyrogram fork, simply open a pull request by following the guide below.

You can read more about pull requests in the [GitHub docs](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request).

### Setting Up Development Environment

1. Fork this Pyrogram repository to your GitHub account.
2. Clone your forked repository of Pyrogram to your computer:

```bash
git clone https://github.com/<your username>/pyrogram
cd pyrogram
```

4. Add a track to the original repository:

```bash
git remote add upstream https://github.com/TelegramPlayGround/PyroTGFork
```

5. Install dependencies:

```bash
pip install --force-reinstall .[dev]
```

### Run tests

All changes should be tested:

```bash
pytest tests
```

Remember to write tests for your new features or modify the existing tests to cover your code changes. Testing is essential to ensure the quality and reliability of your code.

### Docs

We use Sphinx to generate documentation in the [docs](https://github.com/TelegramPlayground/pyrogram) repository. You can edit the sources and preview the changes using a live-preview server with:

```bash
make docs-live
```

### Commit Messages

We use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/), which provide a standardized and structured format for commit messages. This helps ensure clear and consistent communication about the changes made in each commit. The commit messages should have the following structure:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

where:

- `<type>`: This is a keyword that indicates the kind of change that the commit introduces. It can be one of the following values: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, or `revert`.
- `[optional scope]`: This is an optional identifier that specifies the scope of the change. It can be a module, a component, a file, or any other logical unit of the project.
- `<description>`: This is a short and concise summary of the change in the present tense and imperative mood. It should not end with a period.
- `[optional body]`: This is an optional section that provides more details and context about the change. It should be separated from the summary by a blank line and wrapped at 72 characters.
- `[optional footer(s)]`: This is an optional section that provides additional information such as references to issues, breaking changes, or acknowledgments. It should be separated from the body by a blank line and follow the format `<key>: <value>`.

For example:

```
feat(storage): support multiple database using orm

This commit adds support for multiple databases using the tortoise-orm. It also updates the configuration file to allow the user to specify the database type and connection string.

BREAKING CHANGE: The database configuration has changed. The user must update the configuration file to specify the database type and connection string.

Closes #123
```

### Describing Changes

Write a concise summary of your changes in one or more sentences, so that bot developers can see what's new or updated in the library. 

## Thank You

Your contributions to open source, large or small, make great projects like this possible. Thank you for taking the time to contribute.
