#!/usr/bin/env python3
"""Leo Agent Kit: local course, blueprint and delivery handoff."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
VENDOR = ROOT / 'vendor'


def project_path(base, name):
    if not re.fullmatch(r'[\w-]{1,64}', name, re.UNICODE):
        raise ValueError('项目名限 1–64 个中文、字母、数字、下划线或连字符')
    return base / name


def initialize(base, name):
    target = project_path(base, name)
    if target.exists():
        raise ValueError('项目已存在；初始化不会覆盖已有文件')
    base.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=base) as temp:
        stage = Path(temp) / name
        shutil.copytree(VENDOR / 'idea-to-launch-kit', stage,
                        ignore=shutil.ignore_patterns('projects', '.git', '__pycache__'))
        docs = stage / 'projects' / name / 'docs'
        for folder in ('PRD', '设计参考', '阶段文档', 'evidence'):
            (docs / folder).mkdir(parents=True)
        (docs / 'PRD' / '输入说明.md').write_text(
            '# 项目输入\n\n用 handoff 导入工坊的 PRD.md 和方案.md，或先与你的编码助手讨论需求。\n', encoding='utf-8')
        (stage / 'leo-project.json').write_text(json.dumps(
            {'name': name, 'version': 1, 'handoffs': []}, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        stage.rename(target)
    return target


def handoff(base, name, source):
    target = project_path(base, name)
    statefile = target / 'leo-project.json'
    state = json.loads(statefile.read_text(encoding='utf-8'))
    docs = target / 'projects' / name / 'docs' / 'PRD'
    files = ['PRD.md', '方案.md']
    content = {}
    for filename in files:
        src = source / filename
        if not src.is_file() or src.is_symlink():
            raise ValueError(f'缺少普通文件：{filename}')
        data = src.read_bytes()
        if not data.decode('utf-8').strip():
            raise ValueError(f'文件为空：{filename}')
        if (docs / filename).exists():
            raise ValueError(f'已有 {filename}；请先自行归档，工具不会覆盖')
        content[filename] = data
    # Validate the complete pair before writing either artifact.
    for filename, data in content.items():
        with (docs / filename).open('xb') as dest:
            dest.write(data)
    state['handoffs'].append({filename: hashlib.sha256(data).hexdigest()
                              for filename, data in content.items()})
    temp = statefile.with_suffix('.tmp')
    temp.write_text(json.dumps(state, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    temp.replace(statefile)
    return docs


def main():
    parser = argparse.ArgumentParser(description='Leo Agent Kit · 学习 → 架构 → 交付')
    parser.add_argument('--workspace', type=Path, default=ROOT / 'workspace')
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('doctor')
    course = commands.add_parser('learn'); course.add_argument('chapter', nargs='?', default='guide')
    init = commands.add_parser('init'); init.add_argument('name')
    transfer = commands.add_parser('handoff'); transfer.add_argument('name'); transfer.add_argument('source', type=Path)
    delivery = commands.add_parser('delivery'); delivery.add_argument('name')
    delivery.add_argument('action', choices=['task', 'status', 'check', 'accept'])
    delivery.add_argument('--confirmed', action='store_true', help='仅在用户明确验收通过后使用')
    delivery.add_argument('--next-stage')
    work = commands.add_parser('workshop'); work.add_argument('args', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    try:
        if args.command == 'doctor':
            lock = json.loads((ROOT / 'sources.lock.json').read_text())
            good = True
            for item in lock:
                path = VENDOR / item['repo'].split('/')[-1]
                ok = all((path / f).exists() for f in item['required'])
                print(('OK' if ok else 'MISSING'), path.name, item['commit'][:7]); good &= ok
            print('Python:', sys.version.split()[0], '| bash:', shutil.which('bash') or 'missing')
            return 0 if good and shutil.which('bash') else 1
        if args.command == 'learn':
            path = VENDOR / 'claude-code-harness-study'
            if args.chapter == 'guide':
                print((path / 'index.html').as_uri())
                print('选型指南:', path / 'guide' / 'README.md')
                return 0
            return subprocess.call([sys.executable, 'run.py', args.chapter], cwd=path)
        if args.command == 'init':
            print(initialize(args.workspace.resolve(), args.name)); return 0
        if args.command == 'handoff':
            print(handoff(args.workspace.resolve(), args.name, args.source.resolve())); return 0
        if args.command == 'workshop':
            rest = args.args[1:] if args.args[:1] == ['--'] else args.args
            return subprocess.call([sys.executable, '-m', 'blueprint', *rest], cwd=VENDOR / 'agent-workshop')
        if args.command == 'delivery':
            target = project_path(args.workspace.resolve(), args.name)
            if not (target / 'leo-project.json').is_file():
                raise ValueError('请先 init 项目')
            if args.action == 'accept' and not args.confirmed:
                raise ValueError('需要用户实际验收通过，再提供 --confirmed；自检成功不能替代人工验收')
            action = {'task': '任务', 'status': '状态', 'check': '自检', 'accept': '通过'}[args.action]
            command = ['bash', 'kit.sh', action, args.name]
            if args.next_stage:
                command.append(args.next_stage)
            return subprocess.call(command, cwd=target)
    except (OSError, ValueError) as error:
        print('错误:', error, file=sys.stderr); return 2


if __name__ == '__main__':
    sys.exit(main())
