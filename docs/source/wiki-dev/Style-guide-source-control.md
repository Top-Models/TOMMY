# Source control style guide

***"Merge early, merge often"***  
While you're working on your own branch, merge main into your branch regularly to stay up to date and avoid huge conflicts upon review.

## Branches
Syntax: `prefix/ticket-title`  
Example: `feat/135-pdf-support`  

Corresponding Jira ticket numbers will be used in the branch name.  
The branch title can be different from the ticket title.  

**Prefixes:**  
- `feat/` (features)
- `fix/` (bugfixes)
- `test/` (testing)
- `docs/` (documentation)
- `refactor/` (refactoring)

Further paths can be used if multiple branches are related, such as:
- `feat/181-input-validation`
- `feat/preprocessing/154-stopwords`  
- `feat/preprocessing/43-blacklisting`  
- `feat/preprocessing/43-blacklisting/blacklist-words`
- `feat/preprocessing/43-blacklisting/display-blacklist`

Paths can help organize multiple related branches, for example, multiple subtasks `blacklist-words` and `display-blacklist` may be working towards the same feature `43-blacklisting` which will be merged together before opening a pull request to `main`. This does not have to fully correspond to how it looks in Jira, organize source control in ways that make sense and stays clean.

If you need to build on top of code in another branch, merge the other branch into your branch or consider basing your new branch off of theirs (creating `display-blacklist` from `43-blacklisting`). Just make sure they merge into main before you do.
## Commits
Write descriptive commits in a way that make the change and purpose clear, the first word(s) being verbs such as `add` or `replace` already making the purpose of the commit clear is even better for readability. For example:
- `Add button to blacklist new word`
- `Test blacklisting words button`
- `Remove duplicate add_stopwords()`
- `Downgrade six to 1.12 to satisfy textract requirements`

If you can't describe it in a single commit, consider breaking it up into multiple commits.  
Do not write unclear commits that could mean anything.  
**Examples of bad commit descriptions:**
- `Small changes` (What changes?)
- `Bugfix` (Fix what? How?)
- `Added new function to display` (What function?)
- `aaaaa it won't woooork` (Not helpful) >:ᗡ

