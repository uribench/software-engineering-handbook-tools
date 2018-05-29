# Tools

A collection of automation scripts to build and maintain the [Software Engineering Handbook][1].

## Handbook Structure

The [Software Engineering Handbook][1] has the following structure and conventions:

```
Repository Root/                      https://github.com/uribench/software-engineering-handbook
├──Handbook/                          Root of the automatically generated handbook hierarchy
├──Guides/                            Collection of guides to be consumed by the handbook            
├──Topics/                            Collection of canonical topics
├──config/                            Root of configuration files for the handbook
|  └──navigation/                     Navigation related configuration files for the handbook
├──images/                            Collection of images for the handbook
├──_config.yml                        Required by GitHub Pages
└──README.md                          Main readme file for the handbook (the starting point)
```

The Handbook directory hierarchy represents an instance of a handbook, which is created 
automatically based on the `*.yml` configuration files in config/navigation/ directory.

The idea is to isolate the actual content of the handbook, given under Guides and Topics directories,
from the navigation experience. This makes a robust and easily maintained repository, 
which supports relatively easy changes to the handbook structure and the navigation experiences.

The Handbook directory hierarchy includes directories and README.md files. All the directories under
the Handbook directory have capitalized names with spaces, which represent the exact names of the
Handbook chapters and sections.

We distinguish between **intermediate Handbook directories** (i.e., directories having one or more 
child directories) and **terminal Handbook directories** (i.e., directories having no child 
directories).

Each intermediate Handbook directory contains a README.md file that includes, among other optional 
parts, a local Table of Contents (TOC) pointing to the child directories of the hosting intermediate 
Handbook directory (i.e., next level of the Handbook directory hierarchy).

Each terminal Handbook directory contains a README.md file pointing to one or more guides or topics
that are relevant to the hosting terminal Handbook directory (i.e., in the context of the entire 
navigation path leading from the Handbook root to the hosting terminal Handbook directory).

The entire content of the Handbook directory (i.e., directory hierarchy and all the README.md files)
is automatically generated and maintained by the automation scripts in the [tools repository][2],
based on the configuration files under the config directory.

---

[1]: https://github.com/uribench/software-engineering-handbook
[2]: https://github.com/uribench/software-engineering-handbook-tools