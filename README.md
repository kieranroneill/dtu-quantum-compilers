<h1 align="center">
  DTU: Quantum Compilers
</h1>

<p align="center">
  Contains the code and documentation of assignments for the Quantum Compilers course at DTU.
</p>

---

### Table of contents

* [1. Overview](#-1-overview)
  - [1.1. Project structure](#11-project-structure)
* [2. Usage](#-2-usage)
  - [2.1. Requirements](#21-requirements)
  - [2.2. Setup](#22-setup)
  - [2.3. Project-level setup](#23-project-level-setup)
* [3. Appendix](#-3-appendix)
  - [3.1. Projects](#31-projects)
  - [3.2. Useful commands](#32-useful-commands)

## 🔭 1. Overview

### 1.1. Project structure

This repo is a Python-based monorepo that uses the following structure:

```text
.
├─ projects/
│   ├── <project_name>/
│   │   ├── LICENSE
│   │   ├── main.py             <-- project entrypoint
│   │   ├── Makefile            <-- project-level scripts
│   │   ├── pyproject.toml      <-- project-level configuration file
│   │   ├── README.md
│   │   ├── requirements.txt    <-- project-level dependencies
│   │   └── ...
│   └── ...
├── dev-requirements.txt        <-- root-level Python dependencies
├── Makefile                    <-- root-level scripts
├── pip-requirements.txt        <-- defines the pip version
├── pyproject.toml              <-- root-level configuration file
├── README.md
└── ...
```

<sup>[Back to top ^][table-of-contents]</sup>

## 🪄 2. Usage

### 2.1. Requirements

* [Python v3.10.12+](https://www.python.org/downloads/)
* [Make](https://www.gnu.org/software/make/)

<sup>[Back to top ^][table-of-contents]</sup>

### 2.2. Setup

1. Install the root-level dependencies and tools:
```bash
$ make install
```

<sup>[Back to top ^][table-of-contents]</sup>

### 2.3. Project-level setup

For each project in the `projects/` directory, there will be a separate `Makefile` that can be used to install the project-specific dependencies and tools.

Refer to the `README.md` of each project for more information.

<sup>[Back to top ^][table-of-contents]</sup>

## 📑 3. Appendix

### 3.1. Projects

| Name                                                                                                                   | Description                                                           |
|------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------|
| [`assignment_001`](https://github.com/kieranroneill/dtu-quantum-compilers/blob/main/projects/assignment_001/README.md) | Assignment 001: A lexer, parser, and interpreter for CQ-expressions.m |

### 3.2. Useful commands

| Name              | Description                                         |
|-------------------|-----------------------------------------------------|
| `make format`     | Formats all nested Python code.                     |
| `make install`    | Installs all the root-level dependencies and tools. |
| `make lint`       | Runs the Python linter on all nested code.          |

<sup>[Back to top ^][table-of-contents]</sup>

<!-- links -->
[table-of-contents]: #table-of-contents
