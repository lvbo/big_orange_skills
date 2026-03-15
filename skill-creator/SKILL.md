---
name: skill-creator
description: Guide for creating Claude Skills following Anthropic best practices. Use when user asks to create a new skill, improve an existing skill, or needs help with skill structure, YAML frontmatter, testing, or troubleshooting.
metadata:
  author: Claude Assistant
  version: 1.0.0
  category: development
  tags: [skills, claude, best-practices, development, guide]
---

# Skill Creator Guide

Build effective Claude Skills following Anthropic's official best practices.

## When to Use

- User wants to create a new skill
- User needs to improve/refactor an existing skill
- User asks about skill structure or YAML frontmatter
- User needs help with skill testing or troubleshooting

## Core Principles

### What is a Skill?

A skill is a folder containing instructions that teach Claude how to handle specific tasks or workflows. It enables:
- Consistent, repeatable outputs
- Domain expertise without re-explaining
- Multi-step workflow automation
- Integration with MCP servers

### Progressive Disclosure (Three Levels)

1. **Level 1 (YAML Frontmatter)**: Always loaded - tells Claude when to use the skill
2. **Level 2 (SKILL.md Body)**: Loaded when relevant - full instructions
3. **Level 3 (Linked Files)**: Loaded on demand - detailed references

## Skill Structure

```
skill-name/
├── SKILL.md          # Required - main skill file with YAML frontmatter
├── scripts/          # Optional - executable code (Python, Bash, etc.)
├── references/       # Optional - documentation loaded as needed
└── assets/           # Optional - templates, fonts, icons
```

**CRITICAL RULES:**
- Folder name: kebab-case (no spaces, no capitals, no underscores)
- File name: exactly `SKILL.md` (case-sensitive)
- No README.md inside skill folder

## YAML Frontmatter

### Required Fields

```yaml
---
name: skill-name-in-kebab-case
description: What it does. Use when user [specific trigger phrases].
---
```

### Field Requirements

**name:**
- kebab-case only (e.g., `todoist-task-manager`)
- ❌ No: `My Skill`, `my_skill`, `MySkill`
- ✅ Yes: `my-skill`

**description:**
- MUST include BOTH:
  - What the skill does
  - When to use it (trigger conditions)
- Under 1024 characters
- Include specific phrases users might say
- Mention file types if relevant

### Good vs Bad Descriptions

✅ **Good:**
```yaml
description: Analyzes Figma design files and generates developer handoff documentation. 
  Use when user uploads .fig files, asks for "design specs", "component documentation", 
  or "design-to-code handoff".
```

❌ **Bad:**
```yaml
description: Helps with projects.                    # Too vague
description: Creates sophisticated multi-page docs.  # Missing triggers
description: Implements the Project entity model.    # Too technical
```

### Optional Fields

```yaml
---
name: my-skill
description: [required description]
license: MIT                          # For open-source skills
compatibility: Requires Python 3.8+   # Environment requirements
metadata:                             # Custom key-value pairs
  author: Your Name
  version: 1.0.0
  mcp-server: server-name
  category: productivity
  tags: [project-management, automation]
---
```

### Security Restrictions

**FORBIDDEN in frontmatter:**
- XML angle brackets (`<` or `>`)
- Skills named with "claude" or "anthropic" prefix (reserved)

## Writing SKILL.md

### Recommended Structure

```markdown
# Skill Name

Brief description of what the skill does.

## When to Use

- Trigger condition 1
- Trigger condition 2

## Instructions

### Step 1: [First Major Step]

Clear explanation of what happens.

```bash
python scripts/process.py --input {filename}
```

Expected output: [describe success]

### Step 2: [Second Major Step]

...

## Examples

### Example 1: [Common Scenario]
**User says:** "..."

**Actions:**
1. Step one
2. Step two

**Result:** Expected outcome

## Error Handling

### Error: [Common Error]
**Cause:** Why it happens
**Solution:** How to fix

## Configuration

**Required Environment Variables:**
```bash
export API_TOKEN='your_token'
```

## Important Notes

**CRITICAL:** 
- Key point 1
- Key point 2

## Technical Details

- API endpoints used
- Script paths
- Dependencies
```

## Best Practices

### Be Specific and Actionable

✅ **Good:**
```markdown
Run `python scripts/validate.py --input {filename}` to check data format.
If validation fails:
- Missing required fields → add them to CSV
- Invalid date formats → use YYYY-MM-DD
```

❌ **Bad:**
```markdown
Validate the data before proceeding.
```

### Use Progressive Disclosure

- Keep SKILL.md focused on core instructions
- Move detailed docs to `references/` folder
- Link to references: `See references/api-guide.md for rate limiting`

### Include Error Handling

```markdown
## Common Issues

### MCP Connection Failed
If you see "Connection refused":
1. Verify MCP server running: Settings > Extensions
2. Confirm API key valid
3. Try reconnecting: Settings > Extensions > [Service] > Reconnect
```

### Reference Bundled Resources

```markdown
Before writing queries, consult `references/api-patterns.md` for:
- Rate limiting guidance
- Pagination patterns
- Error codes
```

## Testing Strategy

### 1. Trigger Tests

Goal: Ensure skill loads at right times

**Should trigger:**
- "Help me set up a new ProjectHub workspace"
- "I need to create a project in ProjectHub"

**Should NOT trigger:**
- "What's the weather in San Francisco?"
- "Help me write Python code"

### 2. Functional Tests

Goal: Verify correct outputs

**Test case format:**
```
Test: Create project with 5 tasks
Given: Project name "Q4 Planning", 5 task descriptions
When: Skill executes workflow
Then:
- Project created in ProjectHub
- 5 tasks created with correct properties
- All tasks linked to project
- No API errors
```

### 3. Performance Comparison

Metrics to track:
- Tool calls with vs without skill
- Token consumption
- User correction needed

## Common Patterns

### Pattern 1: Sequential Workflow

Use when: Multi-step processes in specific order

```markdown
## Workflow: Onboard New Customer

### Step 1: Create Account
Call MCP: `create_customer`
Parameters: name, email, company

### Step 2: Setup Payment
Call MCP: `setup_payment_method`
Wait for: verification

### Step 3: Create Subscription
Call MCP: `create_subscription`
```

### Pattern 2: Multi-MCP Coordination

Use when: Workflows span multiple services

```markdown
### Phase 1: Design Export (Figma MCP)
1. Export assets
2. Generate specs

### Phase 2: Asset Storage (Drive MCP)
1. Create folder
2. Upload assets

### Phase 3: Task Creation (Linear MCP)
1. Create tasks
2. Attach asset links
```

### Pattern 3: Iterative Refinement

Use when: Output quality improves with iteration

```markdown
### Initial Draft
1. Fetch data
2. Generate draft

### Quality Check
Run: `scripts/check.py`
Identify: missing sections, formatting issues

### Refinement Loop
1. Address issues
2. Regenerate sections
3. Re-validate
4. Repeat until threshold met
```

## Troubleshooting

### Skill Won't Upload

**Error:** "Could not find SKILL.md"
- Cause: Wrong file name
- Fix: Rename to exactly `SKILL.md` (case-sensitive)

**Error:** "Invalid frontmatter"
- Cause: YAML formatting issue
- Fix: Check for unclosed quotes, missing `---` delimiters

**Error:** "Invalid skill name"
- Cause: Spaces or capitals in name
- Fix: Use kebab-case only

### Skill Doesn't Trigger

**Symptom:** Skill never loads automatically

**Checklist:**
1. Is description too generic? ("Helps with projects" won't work)
2. Does it include trigger phrases?
3. Does it mention relevant file types?

**Debugging:** Ask Claude "When would you use the [skill name] skill?" and adjust based on response.

### Skill Triggers Too Often

**Symptom:** Skill loads for irrelevant queries

**Solutions:**
1. Add negative triggers:
```yaml
description: Advanced data analysis for CSV. Do NOT use for simple exploration.
```

2. Be more specific:
```yaml
# Too broad
description: Processes documents

# Better
description: Processes PDF legal documents for contract review
```

### Instructions Not Followed

**Symptom:** Skill loads but Claude doesn't follow instructions

**Causes:**
1. Instructions too verbose → Keep concise, use bullet points
2. Instructions buried → Put critical instructions at top
3. Ambiguous language → Be specific

**Advanced:** For critical validations, bundle a script instead of relying on language.

## Quick Checklist

### Before Upload
- [ ] Folder named in kebab-case
- [ ] SKILL.md exists (exact spelling)
- [ ] YAML frontmatter has `---` delimiters
- [ ] name field: kebab-case, no spaces/capitals
- [ ] description includes WHAT and WHEN
- [ ] No XML tags (`<` or `>`)
- [ ] Instructions clear and actionable
- [ ] Error handling included
- [ ] Examples provided

### After Upload
- [ ] Test triggering on obvious tasks
- [ ] Test triggering on paraphrased requests
- [ ] Verify doesn't trigger on unrelated topics
- [ ] Functional tests pass
- [ ] Monitor for under/over-triggering

## Example: Complete Skill

```yaml
---
name: notion-project-setup
description: Sets up complete Notion project workspaces with pages, databases, and templates. 
  Use when user says "set up Notion project", "create Notion workspace", "initialize Notion workspace", 
  or mentions "Notion project template".
metadata:
  author: Claude Assistant
  version: 1.0.0
  category: productivity
  tags: [notion, project-management, workspace]
---

# Notion Project Setup

Creates complete project workspaces in Notion.

## When to Use

- "Set up a Notion project"
- "Create Notion workspace"
- "Initialize Notion workspace"

## Instructions

### Step 1: Gather Requirements
Ask user:
- Project name
- Team size
- Required databases (tasks, docs, meetings)

### Step 2: Create Structure
Use Notion MCP:
1. Create project page
2. Create databases
3. Set up relations

### Step 3: Apply Templates
Copy from `assets/project-templates/`

## Examples

### Example 1: Marketing Campaign
**User:** "Set up Notion project for Q4 marketing campaign"

**Result:** 
- Project page created
- Tasks, Calendar, Docs databases
- Campaign timeline template applied

## Configuration

Requires `NOTION_API_TOKEN` environment variable.

## Important Notes

**CRITICAL:** Always verify database relations are properly configured before applying templates.
```

## Resources

- Anthropic Skills Documentation
- Example Skills: github.com/anthropics/skills
- MCP Documentation
