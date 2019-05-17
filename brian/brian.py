import boto3
import botocore
import click


session = boto3.Session(profile_name='brian')
ec2=session.resource('ec2')

def filter_instances(project,instance):
    instances = []
    if instance is not None:
        instance = [instance]

    if project:
        filters = [{'Name':'tag:Project','Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)

    elif instance:
        print("Test")
        instances = ec2.instances.filter(InstanceIds=instance)

    else:
        instances = ec2.instances.all()

    return instances

def has_pending_snapshot(volume):
        snapshots = list(volume.snapshots.all())
        return snapshots and snapshots[0].state == 'pending'

@click.group()
@click.option('--profile', default = None, help = 'enter your profile')

def cli(profile):
        """Brian manages snapshots"""

@cli.group('snapshots')
def snapshots():
    """Commands for snapshots"""

@snapshots.command('list')
@click.option('--project', default=None,
    help="Only Snapshots for project (tag Project:<name>)")
@click.option('--all', 'list_all', default=False, is_flag=True,
help = "List all snapshots for each volume, not just te most recent one")

def list_snapshots(project, list_all):
    "List EC2 Snapshots"

    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(",".join((
                    s.id,
                    v.id,
                    i.id,
                    s.state,
                    s.progress,
                    s.start_time.strftime("%c")
                )))

                if s.state =='completed' and not list_all: break

    return

@cli.group('volumes')
def volumes():
        """Commands for volumes"""

@volumes.command('list')
@click.option('--project', default=None,
    help="Only volumes for project (tag Project:<name>)")


def list_volumes(project):
    "List EC2 volumes"

    instances = filter_instances(project)

    for i in instances:

        for v in i.volumes.all():
            print(", ".join((
            v.id,
            i.id,
            v.state,
            str(v.size)+ "GiB",
            v.encrypted and "Encrypted" or "Not Encrypted"
            )))
    return

@cli.group('instances')

def instances():
        """Commands for instances"""

@instances.command('snapshot',
    help="Create snapshots of all volumes")

@click.option('--project', default=None,
    help="Only instances for project (tag Project:<name>)")
@click.option('--force', default = False, is_flag=True,
    help='Forces functions')
@click.option('--instance', default=None, help = "Only one instance")

def create_snapshots(project,instance,force):
    "Create snapshots for EC2 instances"

    if force == False and project == None:
        print("ERROR: please give up a project first or use force command")
        return

    instances = filter_instances(project, instance)

    stopped = []
    for i in instances:
        if i.state['Name'] == 'stopped':
            stopped.append(i.id)

        if i.id not in stopped:
            print("Stopping {0}...".format(i.id))
            i.stop()
            i.wait_until_stopped()
        else:
            print(i.id + " was already stopped")

        for v in i.volumes.all():
            if has_pending_snapshot(v):
                print("  Skipping {0}, snapshot already in progress".format(v.id))
                continue

            try:
                print("   Creating snapshot of {0}".format(v.id))
                v.create_snapshot(Description="Created by SnapshotAlyzer 30000")

            except botocore.exceptions.ClientError as e:
                print(" Could not create snapshot of {0}. ".format(i.id) + str(e))
                continue

        if i.id not in stopped:
            print("Starting {0}...".format(i.id))
            i.start()
            i.wait_until_running()
        else:
            print(i.id + " was already stopped, so will not be started")

    print("Job's done!")

    return


@instances.command('list')
@click.option('--project', default=None,
    help="Only instances for project (tag Project:<name>)")
##@click.option('--force', default = False, is_flag=True,
    ##help='Forces functions')
@click.option('--instance', default=None, help = "Only one instance")

def list_instances(project,instance):
    "List EC2 instances"

    #if force == False and project == None:
    ##    print('Please try force or enter your project')
    ##    return


    instances = filter_instances(project, instance)
    for i in instances:
        tags = { t['Key']:t['Value'] for t in  i.tags or []}
        print(', '.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            tags.get('Project', '<no project')
            )))

    return

@instances.command('stop')
@click.option('--project', default =None,
    help='Only instances for project')
@click.option('--force', default = False, is_flag=True,
    help='Forces functions')

def stop_instances(project, force):
    "Stop EC2 instances"

    if force == False and project == None:
        print('Please try force or enter your project')
        return

    instances = filter_instances(project)
    for i in instances:
        print("Stopping {0}...".format(i.id))
        try:
            i.stop()
        except botocore.exceptions.ClientError as e:
            print("Could not stop {0}. ".format(i.id) + str(e))
            continue
    return

@instances.command('start')
@click.option('--project', default =None,
    help='Only instances for project')
@click.option('--force', default = False, is_flag=True,
    help='Forces functions')


def start_instances(project, force):
    "Start EC2 instances"

    if force == False and project == None:
        print('Please try force or enter your project')
        return

    instances = filter_instances(project)
    for i in instances:
        print("Starting {0}...".format(i.id))
        try:
            i.start()
        except botocore.exceptions.ClientError as e:
                print("Could not start {0}. ".format(i.id) + str(e))
                continue

    return

@instances.command('reboot')
@click.option('--project', default =None,
    help='Only instances for project')
@click.option('--force', default = False, is_flag=True,
    help='Forces functions')

def reboot_instances(project,force):
    "Reboot EC2 instances"

    if force == False and project == None:
        print('Please try force or enter your project')
        return

    instances = filter_instances(project)
    for i in instances:
        print("Reboot {0}...".format(i.id))
        try:
            i.reboot()
        except botocore.exceptions.ClientError as e:
            print("Could not stop {0}. ".format(i.id) + str(e))
            continue
    return

if __name__ =='__main__':
    cli()
