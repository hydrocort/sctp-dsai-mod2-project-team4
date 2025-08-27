# Cursor Project Rules

This directory contains Project Rules for the Olist E-commerce Data Pipeline project, using Cursor's new Project Rules system.

## What are Project Rules?

Project Rules provide system-level instructions to Cursor's Agent and Inline Edit features. They give persistent context, preferences, and workflows for your project.

## Rule Files

### 1. `olist-pipeline.mdc` - Core Project Rules
- **Type**: Always (applies to entire project)
- **Scope**: All files (`**/*`)
- **Purpose**: Core project context, architecture decisions, and general guidelines

### 2. `dbt-guidelines.mdc` - dbt Development Rules
- **Type**: Auto Attached (applies when working with dbt files)
- **Scope**: SQL files, dbt config files, schema files
- **Purpose**: dbt-specific development patterns and best practices

### 3. `python-guidelines.mdc` - Python Development Rules
- **Type**: Auto Attached (applies when working with Python files)
- **Scope**: Python files (`**/*.py`)
- **Purpose**: Python coding standards and project-specific patterns

## How It Works

1. **Always Rules**: The main `olist-pipeline.mdc` rule is always included in model context
2. **Auto Attached Rules**: Specialized rules automatically attach when working with relevant file types
3. **Scoped Application**: Rules only apply to files matching their glob patterns

## Benefits Over Legacy .cursorrules

- **Version Controlled**: Rules are stored in `.cursor/rules` and can be committed to git
- **Scoped**: Different rules for different file types and contexts
- **Organized**: Multiple focused rule files instead of one large file
- **Maintainable**: Easy to update specific aspects without affecting others

## Migration from .cursorrules

The legacy `.cursorrules` file has been renamed to `.cursorrules.legacy` and should not be used going forward. All project guidance is now provided through the new Project Rules system.

## Adding New Rules

To add new rules:
1. Create a new `.mdc` file in `.cursor/rules/`
2. Use proper MDC metadata format at the top
3. Choose appropriate rule type (Always, Auto Attached, Agent Requested, or Manual)
4. Define glob patterns for scoping

## Rule Types

- **Always**: Always included in model context
- **Auto Attached**: Included when files matching glob patterns are referenced
- **Agent Requested**: Available to AI, which decides whether to include
- **Manual**: Only included when explicitly mentioned using @ruleName
