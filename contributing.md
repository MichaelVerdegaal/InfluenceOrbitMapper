## Submitting an issue

- Use the templates as much as possible, for consistency sake.
- If a bug, please explain properly the steps you took before the issue happened
- if a feature request/change, describe why you think that change will improve the product

## Pull request guidelines

- Fork from the develop branch, not main.
- Make sure your request is only targeted at a single issue
- Make sure your commit messages are clear and concise. If you need help with this, check
  out [this blog post](https://chris.beams.io/posts/git-commit/).

## Python guidelines

- Adhere to [PEP-8](https://www.python.org/dev/peps/pep-0008/) wherever Python is written
- Adhere to [PEP-257](https://www.python.org/dev/peps/pep-0257/) and
  [PEP-287](https://www.python.org/dev/peps/pep-0287/) for docstrings
- Update requirements.txt if you include a new package
- If you do plan to add a new package, make sure that it's absolutely necessary. In case of doubt post an issue.
- When it comes to single vs double quotes (' and ") for strings, use single quotes as much as possible. Use double
  quotes for strings meant to be readable to a user, or general long messages. Double quotes is also of course permitted
  when string escaping is needed.
  
## Javascript guidelines
- Add proper JSDoc comments to Javascript functions
