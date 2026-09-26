#!/usr/bin/env python3
import json
import datetime
import subprocess

# Get scoreboard data
result = subprocess.run(['/srv/rodion/projects/venv_builder/bin/rodion', 'scoreboard', '--json'], capture_output=True, text=True)
if result.returncode != 0:
    raise RuntimeError(f"rodion scoreboard failed: {result.stderr}")
scoreboard = json.loads(result.stdout)

# Convert to the format build.py expects
venture_data = {
    'generated_at': datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00', 'Z'),
    'source': 'rodion scoreboard --json',
    'ventures': [],
    'summary': {
        'total_ventures': len(scoreboard),
        'active_ventures': sum(1 for v in scoreboard if v.get('status') == 'active'),
        'probes': sum(1 for v in scoreboard if v.get('stage') == 'probe'),
        'tracks': {},
        'money_in_usd': 0,
        'money_out_usd': 0,
        'ventures_at_kill_gate': sum(1 for v in scoreboard if v.get('kill_allowed', False))
    }
}

for v in scoreboard:
    track = v.get('track', 'unknown')
    venture_data['summary']['tracks'][track] = venture_data['summary']['tracks'].get(track, 0) + 1
    
    # Get last iteration
    last_iter = v.get('last_iteration', {})
    
    venture_data['ventures'].append({
        'id': v.get('id'),
        'name': v.get('name'),
        'track': v.get('track'),
        'stage': v.get('stage', 'probe'),
        'owner': v.get('owner'),
        'hypothesis': v.get('hypothesis'),
        'metric_name': v.get('metric_name'),
        'metric_value': v.get('metric_value', 0),
        'kill_criteria': v.get('kill_criteria'),
        'status': v.get('status', 'active'),
        'days_alive': v.get('days_alive', 0),
        'iterations': v.get('iterations', 0),
        'min_iterations': v.get('min_iterations', 3),
        'min_days': v.get('min_days', 14),
        'kill_allowed': v.get('kill_allowed', False),
        'last_iteration': last_iter,
        'review_in_days': v.get('review_in_days', 0),
        'project_dir': (v.get('project_dir') or '').replace('/srv/rodion/projects/', ''),
        'repo': v.get('repo', ''),
        'jurisdiction': v.get('jurisdiction', '')
    })

with open('/srv/rodion/projects/showcase/venture-status.json', 'w') as f:
    json.dump(venture_data, f, indent=2)

print('venture-status.json updated')