# requirements: pip3 install pyyaml
import os
import yaml

subnet = "192.168.104.0"
subnet_mask = '24'
route_gateway = "192.168.104.1"
eth_name = 'bond0'


# This function will be listed all routes
def getroutes(bond_name):
    netplan_path = '/opt/netplan/'
    netplan_path1 = ''
    files = []
    # Find .yaml files
    # r=root, d=directories, f = files
    for r, d, f in os.walk(netplan_path):
        for file in f:
            if bond_name + '.yaml' in file:
                files.append(os.path.join(r, file))
    # Find Netplan configuration path
    netplan_path1 = files[0]
    # Get route to netplan file.
    with open(netplan_path1, 'r') as file:
        documents = yaml.full_load(file)
        routes = documents['network']['bonds'][bond_name].get('routes')
        for item in routes:
            print('Route subnet is: ' + str(item['to']) + ' and route gateway is: ' + str(item['via']))


# This function will be added routes to the netplan file and will be applied it
def addroute(route_ip, route_gateway, netmask, bond_name):
    netplan_path = '/opt/netplan/'
    netplan_path1 = ''
    files = []
    route_ip1 = [f'{route_ip}/{netmask}']
    # Find .yaml files
    # r=root, d=directories, f = files
    for r, d, f in os.walk(netplan_path):
        for file in f:
            if bond_name + '.yaml' in file:
                files.append(os.path.join(r, file))
    # Find Netplan configuration path
    netplan_path1 = files[0]
    print(netplan_path1)
    # Backup from Netplan configuration file in /etc/netplan/ with netplan.bak name before changing it
    os.system('sudo -i cp ' + netplan_path1 + ' /etc/netplan/netplan.bak')
    # Add to route to netplan file.
    with open(netplan_path1, 'r') as file:
        documents = yaml.full_load(file)
        routes = documents['network']['bonds'][bond_name].get('routes')
        # If routes section isn't in netplan file then create it.
        if not routes:
            documents['network']['bonds'][bond_name]['routes'] = []
        # If route section exist in netplan file then append key,value(ip : value, via : value) in routes section
        documents['network']['bonds'][bond_name]['routes'].append({'to': route_ip1, 'via': route_gateway})
        route_list = documents['network']['bonds'][bond_name].get('routes')
        for item in route_list:
            print('Route subnet is: ' + str(item['to']) + ' and route gateway is: ' + str(item['via']))

    # Convert "documents" dictionary to YAML format and dumt it into netplan file.
    with open(netplan_path1, 'w') as file:
        yaml.dump(documents, file)
    # Run "netplan generate" and "netplan apply" command for finalizing task.
    os.system('sudo -i netplan generate && netplan apply')
    # List all of routes
    #os.system('ip route list')


# This function will be deleted route from the netplan file and will be applied it
def delroute(route_ip, route_gateway, netmask, bond_name):
    netplan_path = '/opt/netplan/'
    netplan_path1 = ''
    files = []
    route_ip1 = [f'{route_ip}/{netmask}']
    print(route_ip1)
    # Find .yaml files
    # Find Netplan configuration path
    # r=root, d=directories, f = files
    for r, d, f in os.walk(netplan_path):
        for file in f:
            if bond_name + '.yaml' in file:
                files.append(os.path.join(r, file))

    netplan_path1 = files[0]
    print(netplan_path1)
    # Backup from Netplan configuration file in /etc/netplan/ with netplan.bak name before changing it
    os.system('sudo -i cp ' + netplan_path1 + ' /etc/netplan/netplan.bak')
    # Convert netplan yaml file to dictionary format.
    with open(netplan_path1, 'r') as file:
        documents = yaml.full_load(file)
        routes = documents['network']['bonds'][bond_name].get('routes')
        print(routes)
        # If routes section isn't in netplan file then raise error.
        if not routes:
            print("Section routes is not exist and is not any route to deleting")
        # If route section exist in netplan file then delete it in routes section
        else:
            for item in documents['network']['bonds'][bond_name]['routes']:
                if item['to'] == route_ip1:
                    documents['network']['bonds'][bond_name]['routes'].remove(item)
                    route_list = documents['network']['bonds'][bond_name].get('routes')
                    for item in route_list:
                        print('Route subnet is: ' + str(item['to']) + ' and route gateway is: ' + str(item['via']))

    # Convert "documents" dictionary to YAML format and dumt it into netplan file.
    with open(netplan_path1, 'w') as file:
        yaml.dump(documents, file)
    # Run "netplan generate" and "netplan apply" command for finalizing task.
    os.system('sudo -i netplan generate && netplan apply')
    # List all of routes for output view.
    os.system('ip route list')


def main():
    getroutes(bond_name)
    addroute(route_ip, route_gateway, netmask, bond_name)
    delroute(route_ip, route_gateway, netmask, bond_name)



if __name__ == '__main__':
    main()
