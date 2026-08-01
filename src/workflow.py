#!/usr/bin/env python3

# see https://allofphysics.com/llm_workflow_documentation

import json
import os

# source: https://www.mindstudio.ai/blog/what-is-loop-engineering-autonomous-ai-agent-workflows

# these stages are a sequence of prompts to help guide a human through the ingest of a derivation into https://allofphysics.com/.


# stage 1: create detailed Latex derivation
# see prompts used on https://github.com/allofphysicsgraph/task-tracker/issues/167

# stage : create list of steps used in derivation
# see prompts used on https://github.com/allofphysicsgraph/task-tracker/issues/169


# stage : create list of symbols used in derivation
# see prompts used on https://github.com/allofphysicsgraph/task-tracker/issues/168

# stage : compare symbols to PDG
# see prompts used on https://github.com/allofphysicsgraph/task-tracker/issues/174


# stage : create list of operations used in derivation
# see prompts used on https://github.com/allofphysicsgraph/task-tracker/issues/172

# stage : compare operations to PDG
# see prompts used on https://github.com/allofphysicsgraph/task-tracker/issues/175


# stage : create list of expressions used in derivation
# see prompts used on https://github.com/allofphysicsgraph/task-tracker/issues/170

# stage : compare expressions to PDG
# see prompts used on https://github.com/allofphysicsgraph/task-tracker/issues/176




STAGES = {
    1: {
        "name": "conversion to latex",
        "instructions": """
You are an expert technical typesetter and Theoretical Physicist. Your task is to transform the user-provided text into a formal, pedagogically structured LaTeX document. The audience isn't familiar with the math operations, so be pedantic in both explanations and inserting additional steps where needed to be more explicit about the transformations. Make the logic as explicit as feasible even though that increases the length of the document. Explain each step since the audience lacks the experience and insight that you have.

Objective: Convert the mathematical physics derivation into a sequence of logical steps as a single Latex document. A derivation consists of a sequence of steps where each equation relates to others via specific mathematical operations (e.g., substitution, differentiation, algebraic rearrangement).

Derivation Specifications:
- To help the reader understand what transformation is being applied, explicitly state the mathematical operations performed between equations (e.g., "Substituting Eq.~\ref{x} into Eq.~\ref{y} yields...").
- If the source text implies a step that is mathematically non-trivial (like equating coefficients or using a trigonometric identity), explicitly break that out into a sub-step with its own equation and label.
- In addition to explicitly stating the transformations being applied between equations, guide the reader through the derivation.

Style
- focus on the mathematical and physical veracity
- uses declarative statements
- guide the reader through a logical sequence of ideas to reach a conclusion.
- use Scientific Impersonal Style, also known as Technical Expository Prose. Use Mathematical Imperatives to direct the reader's attention. The Impersonal Imperative should be used.
- be methodical and explicit
- be Precise and Technical

Document Specifications:
- use the document class and preamble provided below
- Strict ASCII Encoding: The entire .tex file must be ASCII. Do not use Unicode characters. For Greek letters, operators, or special symbols, use standard LaTeX commands.
- Every mathematical equation must be placed in a numbered `equation` environment.
- Use `\label{...}` for every equation.
- Labeling Convention: Labels must be unique, descriptive of the equation's physical or mathematical role, and contain no spaces. Use only lowercase letters and underscores
- Every equation should have a single relation (e.g., `=`) separating the left-hand side (LHS) from the right-hand side (RHS). If the source material uses short-hand of multiple relations to indicate a sequence of steps, break those into separate equations that each have a single relation.

Here is the starting point for the Latex file:

```
\documentclass{article}
\usepackage{amsmath}
\usepackage{amssymb}

% margins of 1 inch:
\setlength{\topmargin}{-.5in}
\setlength{\textheight}{9in}
\setlength{\oddsidemargin}{0in}
\setlength{\textwidth}{6.5in}

\usepackage[pdftex]{hyperref} % hyperlink equation and bibliographic citations
\author{Ben Payne, with Gemini 3 Flash}
\title{DERIVATION NAME HERE}

\begin{document}
\maketitle
\begin{abstract}
DESCRIPTION OF DERIVATION HERE
\end{abstract}

DERIVATION STEPS HERE

\end{document}
```

        """,
        "file_dependencies": ["DERIVATION_AS_LATEX.tex"],
    },
    2: {
        "name": "list of symbols",
        "instructions": """
Read the file `DERIVATION_AS_LATEX.tex` 

The latex file contains equations and symbols. Provide a list, formatted as JSON, of every unique symbol and a description of that symbol.

For each entry in the JSON list include a list of references to the labeled equations where each symbol is used.

For each symbol categorize the symbol as scalar, vector, or matrix

For each scalar symbol, categorize the symbol as variable or a constant.

For each scalar symbol, categorize the values the scalar can take as "real", "complex", "integer", or "arbitrary"

For each scalar symbol, categorize the scalar as "positive", "negative", "non-negative", or "any"

For each scalar symbol there are 7 dimensionality measurements: mass, time, length, temperature, electric charge, amount of substance, luminous intensity.
If the scalar is dimensionless, then the value for each of the 7 measures is zero.
If the scalar has non-zero dimensions, explicitly state the integer value of the dimensions.

Write out just the JSON list as your answer.

The output should comply with this schema:

```
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Physics Symbol Definition Set",
  "type": "array",
  "items": {
    "type": "object",
    "required": [
      "variable",
      "description",
      "references",
      "category_type",
      "scalar_type",
      "value_type",
      "sign_type",
      "dimensionality"
    ],
    "properties": {
      "variable": {
        "type": "string",
        "description": "The LaTeX representation of the physical variable."
      },
      "description": {
        "type": "string",
        "description": "A human-readable explanation of the variable."
      },
      "references": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "List of internal IDs or equation slugs where this variable is used."
      },
      "category_type": {
        "type": "string",
        "enum": [
          "scalar",
          "vector",
          "tensor"
        ],
        "description": "The mathematical nature of the quantity."
      },
      "scalar_type": {
        "type": "string",
        "enum": [
          "variable",
          "constant"
        ],
        "description": "Whether the value changes within the system context."
      },
      "value_type": {
        "type": "string",
        "enum": [
          "real",
          "complex",
          "integer"
        ],
        "description": "the numerical set the value belongs to."
      },
      "sign_type": {
        "type": "string",
        "enum": [
          "any",
          "positive",
          "negative",
          "non-negative",
          "non-positive"
        ],
        "description": "The physical constraints on the sign of the value."
      },
      "dimensionality": {
        "type": "object",
        "description": "The SI base dimensions exponents.",
        "additionalProperties": false,
        "required": [
          "mass",
          "time",
          "length",
          "temperature",
          "electric_charge",
          "amount_of_substance",
          "luminous_intensity"
        ],
        "properties": {
          "mass": {
            "type": "integer"
          },
          "time": {
            "type": "integer"
          },
          "length": {
            "type": "integer"
          },
          "temperature": {
            "type": "integer"
          },
          "electric_charge": {
            "type": "integer"
          },
          "amount_of_substance": {
            "type": "integer"
          },
          "luminous_intensity": {
            "type": "integer"
          }
        }
      }
    }
  }
}

```

""",
        "file_dependencies": ["DERIVATION_AS_LATEX.tex", "SYMBOLS.json"],
    },
    3: {
        "name": "scalar symbol comparison: missing and matching",
        "instructions": """Read the file `SYMBOLS.json` 

I have two input data sets:
- a set of symbols found in the derivation of the DERIVATION_NAME_HERE.
- a set of symbols in a database for physics derivations. Each symbol has a unique ID number.

The task is to create two JSON files: one for matches where symbols are in both inputs, and another JSON file for symbols in the DERIVATION_NAME_HERE derivation that are not in the physics derivations database. All symbols in the DERIVATION_NAME_HERE derivation should end up in one of the two JSON output files.

For the JSON that captures the matches (`matches.json`), for each match indicate
- the symbol Latex
- the ID from the database
- the list of equation labels from the derivation
- the description
- explanation of why the symbol is a match
- confidence level of the match

Here is the schema for `matches.json`:

```
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Physics Symbol Matches Schema",
  "type": "array",
  "items": {
    "type": "object",
    "required": [
      "symbol_latex",
      "db_id",
      "description",
      "explanation",
      "confidence"
    ],
    "properties": {
      "symbol_latex": {
        "type": "string",
        "minLength": 1,
        "description": "The LaTeX representation of the symbol from the derivation."
      },
      "db_id": {
        "type": "string",
        "pattern": "^[0-9]+$",
        "minLength": 8,
        "description": "The unique numerical ID from the physics database."
      },
      "equation_labels": {
        "type": "array",
        "description": "equations in the derivation that use the symbol"
      },
      "description": {
        "type": "string",
        "minLength": 1,
        "description": "A description of the symbol's role in the derivation."
      },
      "explanation": {
        "type": "string",
        "minLength": 1,
        "description": "Justification for why this derivation symbol matches the database entry."
      },
      "confidence": {
        "type": "string",
        "enum": [
          "high",
          "medium",
          "low"
        ],
        "description": "The certainty level of the match."
      }
    }
  }
}
```
For the JSON that captures the missing symbols (`missing.json`), for each symbol indicate
- the symbol Latex
- the description
- comments about symbols in the database that might be considered adjacent and what the ID number is

Here is the schema for `missing.json`:

```
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Missing Physics Symbols Schema",
  "type": "array",
  "items": {
    "type": "object",
    "required": [
      "symbol_latex",
      "description",
      "comments"
    ],
    "properties": {
      "symbol_latex": {
        "type": "string",
        "minLength": 1,
        "description": "The LaTeX representation of the symbol used in the derivation."
      },
      "description": {
        "type": "string",
        "minLength": 1,
        "description": "A description of what the symbol represents in the derivation."
      },
      "comments": {
        "type": "string",
        "minLength": 1,
        "description": "Notes regarding nearby symbols in the database or why a match was omitted."
      }
    }
  }
}
```
        """,
        "file_dependencies": ["SYMBOLS.json"],
    },
    4: {
        "name": "tex to operations.json",
        "instructions": """Read the `DERIVATION_AS_LATEX.tex` file """,
        "file_dependencies": ["operations.json", "DERIVATION_AS_LATEX.tex"],
    },
    5: {
        "name": "comparing operations in PDG DB",
        "instructions": """Based on reading the files `operations.json` """,
        "file_dependencies": ["operations.json"],
    },
    6: {
        "name": "expressions.json: split LHS, RHS; add Sympy",
        "instructions": "",
        "file_dependencies": [""],
    },
    7: {
        "name": "comparison of expressions with PDG: matches and missing",
        "instructions": "",
        "file_dependencies": [""],
    },
    8: {
        "name": "associating symbols with expressions",
        "instructions": "",
        "file_dependencies": [],
    },
    9: {
        "name": "associating operators with expressions ",
        "instructions": "",
        "file_dependencies": [""],
    },
    10: {
        "name": "rewriting expression SymPy using PDG IDs",
        "instructions": "",
        "file_dependencies": [],
    },
    11: {
        "name": "create steps.json",
        "instructions": "",
        "file_dependencies": ["steps.json"],
    },
}


class WorkflowManager:
    def __init__(self, state_file=".workflow_state.json"):
        self.state_file = state_file
        self.current_stage = 1
        self.load_state()

    def load_state(self):
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r") as f:
                    data = json.load(f)
                    self.current_stage = data.get("current_stage", 1)
            except Exception:
                self.current_stage = 1

    def save_state(self):
        try:
            with open(self.state_file, "w") as f:
                json.dump({"current_stage": self.current_stage}, f)
        except Exception as e:
            print(f"[Warning] Failed to save workflow state: {e}")

    def get_stage_prefix(self) -> str:
        stage_name = STAGES[self.current_stage]["name"]
        return f"[STAGE {self.current_stage}: {stage_name}]"

    def get_current_instructions(self) -> str:
        stage_info = STAGES[self.current_stage]
        deps = (
            f"\nFiles associated with this stage: {', '.join(stage_info['file_dependencies'])}"
            if stage_info["file_dependencies"]
            else ""
        )
        return f"CURRENT ACTIVE STAGE: {self.get_stage_prefix()}\nInstructions: {stage_info['instructions']}{deps}"

    def advance_stage(self) -> bool:
        if self.current_stage < len(STAGES):
            self.current_stage += 1
            self.save_state()
            return True
        return False

    def regress_stage(self) -> bool:
        if self.current_stage > 1:
            self.current_stage -= 1
            self.save_state()
            return True
        return False
