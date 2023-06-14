import requests
import click
import json

@click.command()
@click.option('--table_name', default="events", help='Table name')
def run_rebalance(table_name):
    base_url = f"http://localhost:9000/tables/{table_name}/rebalance"
    params = {
        'type': 'realtime',
        'dryRun': 'false',
        'reassignInstances': 'true',
        'includeConsuming': 'true',
        'bootstrap': 'false',
        'downtime': 'true',
        'minAvailableReplicas': '1',
        'bestEfforts': 'true',
        'externalViewCheckIntervalInMs': '1000',
        'externalViewStabilizationTimeoutInMs': '3600000',
        'updateTargetTier': 'false',
    }

    response = requests.post(base_url, params=params)

    print(response.url)
    print(response.status_code)
    print(json.dumps(response.json(), indent=4))

if __name__ == '__main__':
    run_rebalance()
