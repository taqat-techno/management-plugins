#!/usr/bin/env python3
"""Plugin Health Check — validates pm-guidelines plugin integrity.

Checks:
1. hooks.json entries point to existing .py files
2. Agent skill references resolve to existing SKILL.md files
3. Orphaned .py files in hooks/ not registered in hooks.json
4. global_lessons.md lesson count matches plugin.json claims
5. All skill directories have SKILL.md
6. plugin.json is valid JSON with required fields
7. Every SKILL.md has a model: declaration

Usage: py hooks/health_check.py
"""

import json
import os
import re
import sys
from pathlib import Path


def find_plugin_root():
    """Find plugin root from env var or script location."""
    env_root = os.environ.get('CLAUDE_PLUGIN_ROOT')
    if env_root and os.path.isdir(env_root):
        return Path(env_root)
    # Fallback: script is in hooks/, go up one level
    return Path(__file__).parent.parent


def check_hooks_json(plugin_root):
    """Verify all hooks.json entries point to existing files."""
    hooks_file = plugin_root / 'hooks' / 'hooks.json'
    if not hooks_file.exists():
        return 'FAIL', 'hooks.json not found'

    try:
        data = json.loads(hooks_file.read_text(encoding='utf-8'))
    except json.JSONDecodeError as e:
        return 'FAIL', f'hooks.json is invalid JSON: {e}'

    hooks = data.get('hooks', {})
    missing = []
    total = 0

    for event_type, matchers in hooks.items():
        for matcher_group in matchers:
            for hook in matcher_group.get('hooks', []):
                cmd = hook.get('command', '')
                # Extract .py filename from command
                match = re.search(r'hooks/(\w+\.py)', cmd)
                if match:
                    total += 1
                    py_file = plugin_root / 'hooks' / match.group(1)
                    if not py_file.exists():
                        missing.append(match.group(1))

    if missing:
        return 'FAIL', f'{len(missing)} hook file(s) missing: {", ".join(missing)}'
    return 'PASS', f'{total} hooks, all files exist'


def check_agent_skills(plugin_root):
    """Verify all skills referenced by agents exist on disk."""
    agents_dir = plugin_root / 'agents'
    if not agents_dir.exists():
        return 'FAIL', 'agents/ directory not found'

    issues = []
    total_refs = 0

    for agent_file in agents_dir.glob('*.md'):
        content = agent_file.read_text(encoding='utf-8', errors='replace')
        # Extract skills from YAML frontmatter
        in_skills = False
        for line in content.split('\n'):
            if line.strip() == 'skills:':
                in_skills = True
                continue
            if in_skills:
                match = re.match(r'\s+-\s+(\S+)', line)
                if match:
                    skill_name = match.group(1)
                    total_refs += 1
                    skill_dir = plugin_root / skill_name / 'SKILL.md'
                    if not skill_dir.exists():
                        issues.append(f'{agent_file.name} -> {skill_name}')
                elif not line.strip().startswith('-'):
                    in_skills = False

    if issues:
        return 'FAIL', f'Missing skills: {", ".join(issues)}'
    return 'PASS', f'{total_refs} skill references across agents, all exist'


def check_orphaned_hooks(plugin_root):
    """Find .py files in hooks/ not registered in hooks.json."""
    hooks_dir = plugin_root / 'hooks'
    hooks_file = hooks_dir / 'hooks.json'

    if not hooks_file.exists():
        return 'FAIL', 'hooks.json not found'

    hooks_json_text = hooks_file.read_text(encoding='utf-8')

    skip = {'pm_utils.py', 'health_check.py', '__init__.py'}
    orphaned = []

    for py_file in sorted(hooks_dir.glob('*.py')):
        name = py_file.name
        if name in skip or name.startswith('__'):
            continue
        # Check if this file is referenced in hooks.json
        stem = py_file.stem  # e.g., "pat_token_guard"
        if stem not in hooks_json_text:
            orphaned.append(name)

    if orphaned:
        return 'WARNING', f'{len(orphaned)} file(s) not in hooks.json: {", ".join(orphaned)}'
    return 'PASS', 'No orphaned hook files'


def check_lesson_count(plugin_root):
    """Verify global_lessons.md lesson count matches plugin.json claims."""
    # Find global_lessons.md at repo root
    project_root = plugin_root.parent.parent
    lessons_file = project_root / 'global_lessons.md'

    if not lessons_file.exists():
        return 'WARNING', f'global_lessons.md not found at {lessons_file}'

    content = lessons_file.read_text(encoding='utf-8', errors='replace')
    # Count numbered lessons: lines starting with "N. **"
    lesson_count = len(re.findall(r'^\d+\.\s+\*\*', content, re.MULTILINE))

    # Read plugin.json claim
    plugin_json = plugin_root / '.claude-plugin' / 'plugin.json'
    if plugin_json.exists():
        pdata = json.loads(plugin_json.read_text(encoding='utf-8'))
        desc = pdata.get('description', '')
        match = re.search(r'(\d+)\s+guidelines', desc)
        claimed = int(match.group(1)) if match else 0

        if claimed != lesson_count:
            return 'FAIL', f'plugin.json claims {claimed} guidelines but global_lessons.md has {lesson_count}'
        return 'PASS', f'{lesson_count} lessons in global_lessons.md, matches plugin.json'

    return 'WARNING', f'{lesson_count} lessons found but plugin.json missing'


def check_skill_directories(plugin_root):
    """Verify all skill directories have SKILL.md."""
    skill_dirs = []
    for d in sorted(plugin_root.iterdir()):
        if d.is_dir() and (d / 'SKILL.md').exists():
            skill_dirs.append(d.name)

    if not skill_dirs:
        return 'FAIL', 'No skill directories found'
    return 'PASS', f'{len(skill_dirs)} skills: {", ".join(skill_dirs)}'


def check_plugin_json(plugin_root):
    """Verify plugin.json is valid with required fields."""
    plugin_json = plugin_root / '.claude-plugin' / 'plugin.json'
    if not plugin_json.exists():
        return 'FAIL', 'plugin.json not found'

    try:
        data = json.loads(plugin_json.read_text(encoding='utf-8'))
    except json.JSONDecodeError as e:
        return 'FAIL', f'Invalid JSON: {e}'

    required = ['name', 'version', 'description']
    missing = [f for f in required if f not in data]
    if missing:
        return 'FAIL', f'Missing fields: {", ".join(missing)}'

    return 'PASS', f'v{data["version"]} — {data["name"]}'


def check_model_declarations(plugin_root):
    """Verify every SKILL.md has a model: declaration."""
    missing = []
    total = 0

    for d in sorted(plugin_root.iterdir()):
        skill_file = d / 'SKILL.md'
        if d.is_dir() and skill_file.exists():
            total += 1
            content = skill_file.read_text(encoding='utf-8', errors='replace')
            if not re.search(r'model:\s*(sonnet|opus|haiku)', content):
                missing.append(d.name)

    if missing:
        return 'WARNING', f'{len(missing)} skill(s) missing model declaration: {", ".join(missing)}'
    return 'PASS', f'{total} skills, all have model declarations'


def main():
    plugin_root = find_plugin_root()
    print(f'Plugin Root: {plugin_root}')
    print(f'{"=" * 50}')
    print()

    checks = [
        ('Hooks Configuration', check_hooks_json),
        ('Agent Skill References', check_agent_skills),
        ('Orphaned Hook Files', check_orphaned_hooks),
        ('Lesson Count', check_lesson_count),
        ('Skill Directories', check_skill_directories),
        ('Plugin Metadata', check_plugin_json),
        ('Model Declarations', check_model_declarations),
    ]

    results = {'PASS': 0, 'WARNING': 0, 'FAIL': 0}
    icons = {'PASS': '+', 'WARNING': '!', 'FAIL': 'X'}

    for name, check_fn in checks:
        try:
            status, detail = check_fn(plugin_root)
        except Exception as e:
            status, detail = 'FAIL', f'Check crashed: {type(e).__name__}: {e}'
        results[status] += 1
        print(f'  [{icons[status]}] {name}: {status} — {detail}')

    print()
    print(f'Summary: {results["PASS"]} PASS, {results["WARNING"]} WARNING, {results["FAIL"]} FAIL')

    if results['FAIL'] > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
