## Chapter 3 - Snapshotaalyzer
------------------------------------------------------------------------------
##aanroepen van een script uit atom >>
print("Hello, world")

for x in range(10):
    print(str(2**x))
## in je command prompt > python3 naam bestand.py

## als je een gitmapje (in Git) wilt clonen op je schijf
> git clone en dan de link van de git site (SSH)

##Updaten git
 >> git status, git add, git commit -am "beschrijving", push
----------------------------------------------------------------------------
##Als je iets wilt installeren - een package
pip3 install (vb) requests of pipenv
als je pipenv doet kun je daarna pipenv --three doen (dan open je python 3 in een virtual machine)
checken voor versie >> pipenv --version of pipenv run python -V
je moet packages ook installeren in je VM > pipenv install (vb) requests
- pipenv install boto3
- pipenv install -d ipython

en als je dat hebt gedaan >>
- pipenv run iptyhon <<bestandsnaam>>
en kun je python starten als shell >> pipenv run ipython

##Importeren script in VM
pipenv run ipython
from (mapnaam) import (bestand)
------------------------------------------------------------------------------
## Boto3
Toevoeging:
als je in python zit (VM):
import boto3
session = boto3.Session(profile_name='naamvandeuser')
ec2 = session.resource('ec2')
for i in ec2.instances.all():
    print(i):

Als je dit wilt opslaan:
%history en dan je script past in je atom file
---------------------------------------------------------------------------
##functie aanroepen
Nu kun je functies aanroepen
bestandsnaam.naam_functie(gegevens)
----------------------------------------------------------------------------
##handige tip
Note: if __name__ == '__main__': >> onderaan functie
Zorgt ervoor dat je op basis van je script de bijbehorende functies kan laten uitvoeren
- specificeren waar de functies beginnen
----------------------------------------------------------------------------
##AWS instance aanmaken
- heb je je publieke en private sleutel voor nodig in de .ssh map

import key pair (network & security)
Launch instance via AWS
Die connecten met je keypair -check op locatie
dan heb je onderaan een link die je in je command prompt pasten
>> ssh ec2-user@(link) & sudo yum update

Tags aanmaken om te kunnen refereren in je script (let op hoofdletters)

User aanmaken - voor toegang
aws configure --profile shotty
en dan de sleutel pasten die je uit AWS heb gehaald
-----------------------------------------------------------------------------
Starten van een bijbehorend script bij een AWS instances
pipenv run ipython bestandsnaam.py
import boto3
import click

session = boto3.Session(profile_name='naambestand')
ec2 = session.resource('ec2')

-------------------------------------------------------------filter aanmaken
def filter_instances(project):
        instances[]

        if project:                                     -- filter toepassen
            filters = [{'Name':'tag:Project', 'Values':["project"]}]
            instances = ec2.instances.filter(Filters=filters)
        else: ec2.instances.all():

        return instances

def filter_instances(id):
    instances[]

        if id:
            filters = [{'id':["InstanceId"}]
            instances = ec2.instances.filter(Filters=filters)

        else: ec2.instances.all():

        return instances

@click.group()
def instances():
    """Commands for instances"""

@instances.command('list')
@click.option('--project', default=None,               -- filter aanmaken
    help="Only instances for project (tag Project:<name>)")
@click.option('--id', default=None, help ='Only instance with id i-05d65eed478bb126a')

def list_instances(project,id):
    "List EC2 instances"                            -- functie beschrijving

    instances = filter_instances(project,id)

    for i in instances:                           -- funtie(uitvoering)
        tags = {t['Key']: t['Value'] for ti in i.tags or []}
        print(','.join((
        i.id,
        i.instance_type,
        i.placement['AvailabilityZone'],
        i.state['Name'],
        i.public_dns_name,
        tags.get('Project','<no project>'))))
    return
------------------------------------------------------------ zorg je ervoor dat een instance stopt
@instances.command('stop')
@click.option('--project', default=None,
    help='Only instances for project')
    def stop_instances(project):
        "Stop EC2 instances"
        instance = instances(project)

        for i in instances:
            print("stopping {0}...".format(i.id))
            i.stop ()

-----------------------------------------------------------------------
@instances.command('start')                                 -- zorg je ervoor dat een instance start
@click.option('--project', default=None,
    help='Only instances for project')
    def start_instances(project):
        "Start EC2 instances"
        instances[]

        if project:                                     -- filter toepassen
            filters = [{'Name':'tag:Project', 'Values':["project"]}]
            instances = ec2.instances.filter(Filters=filters)
        else:
            ec2.instances.all():

        for i in instances:
            print("Starting {0}...".format(i.id))
            i.start ()

------------------------------------------------------------------------- instance rebooten

@instances.command('reboot')
@click.option('--project', default =None,
    help='Only instances for project')
@click.option('--force', default =None,
    help='Forces script when --project isnt' set')

def reboot_instances(project, force):
    "Reboot EC2 instances"

    instances = filter_instances(project)
    for i in instances:
        print("Reboot {0}...".format(i.id))
        try:
            i.reboot()
        except botocore.exceptions.ClientError as e:
            print("Could not stop {0}. ".format(i.id) + str(e))
            continue
    return


if __name__ == '__main__':
    instances()
(als je dit opslaat)>> pipenv run iptyhon bestandsnaam
OF pipenv run ipython bestandsnaam instances top --project=(naam")
(als je pipenv run python bestandsnaam --help >> krijg je te zien wat de beschrijvin van de functies is)
--------------------------------------------------------------------------------
-- als je bovenstaand wil toepassen in je VM python shell
pipenv run ipython
import boto3


session = boto3.Session(profile_name='naambestand')
ec2 = session.resource('ec2')

--inst= ec2.instances.all
--inst (enter)>>resultaat is je instance collectie

--list(inst)
(output van je functie)
als je dan bijv de eerste instance wilt zien dan doe je
--list(inst)[0]
--i = list(inst)[0]
--i.id (enter)
krijg je je de id te zien van je eerste instance

als je wilt dat er een lijst wordt gemaakt je instancesm
>> pipenv run python bestandsnaam list --project=Tagnaam"
als je wilt dat je instance stopt
>> pipenv run python bestandsnaam stop --project=Tagnaam"
