import requests
from collections import defaultdict
from ordered_set import OrderedSet
import click

@click.command()
@click.option('--segments-to-servers', default=False, help='Show segments to server mapping')
@click.option('--partitions-to-servers', default=True, help='Show partititions to servers mapping')
@click.option('--servers-to-partitions', default=True, help='Show servers to partitions mapping')
def view_segments(segments_to_servers, partitions_to_servers, servers_to_partitions):
    table_name = "events3"

    segment_metadata_response = requests.get(f"http://localhost:9000/segments/{table_name}/servers").json()

    server_to_segment_map = segment_metadata_response[0]["serverToSegmentsMap"]

    if segments_to_servers:
        print("Segment to Servers")
        segment_ids_to_server_names = defaultdict(list)
        for server_url, segment_ids in server_to_segment_map.items():
            server_name, *_ = server_url.split(".")
            for segment_id in segment_ids:
                segment_ids_to_server_names[segment_id].append(server_name)

        sorted_segment_ids = sorted(
            segment_ids_to_server_names.items(), 
            key=lambda segment_id: (segment_id[0].split("__")[1], int(segment_id[0].split("__")[2]))
        )
        for segment_id, server_names in sorted_segment_ids: 
            print(f'{segment_id: <35}', server_names)
        print("")

    if partitions_to_servers:
        print("Partition to Servers")
        partition_ids_to_server_names = defaultdict(OrderedSet)
        for server_url, segment_ids in server_to_segment_map.items():
            server_name, *_ = server_url.split(".")
            for segment_id in segment_ids:
                partition_id = segment_id.split("__")[1]
                partition_ids_to_server_names[partition_id].add(server_name)

        for partition_id, server_names in sorted(partition_ids_to_server_names.items()): 
            print(f'{partition_id: <5}', server_names)
        print("")


    if servers_to_partitions:
        print("Server to Partitions")
        server_to_partitions_map = {
            server.split(".")[0]: OrderedSet(segment.split("__")[1] for segment in segments) 
            for server, segments in server_to_segment_map.items()
        }

        for partition, servers in sorted(server_to_partitions_map.items()): 
            print(f'{partition: <5}', servers)
        print("")


if __name__ == '__main__':
    view_segments()
