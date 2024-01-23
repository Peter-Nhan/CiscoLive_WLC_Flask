from flask import Flask, render_template, send_from_directory
from netmiko import ConnectHandler
import os

app = Flask(__name__)

def grab_cli_output(cli):
    wlc = {
        'device_type': 'cisco_wlc',
        'ip': '192.168.1.1',
        'username': 'admin',
        'password': 'cisco123',
        'secret': 'cisco123',
    }
    # Connect to the WLC
    net_connect = ConnectHandler(**wlc)
    net_connect.enable()
    output = net_connect.send_command(cli)
    # Disconnect from the WLC
    net_connect.disconnect()

    return output

@app.route('/')
def index():
    return render_template('index.html')


# show ap summary
@app.route('/ap_sum')
def show_ap_summary():
    output = grab_cli_output('show ap summary')
    # Split the command output into lines
    lines = output.splitlines()
    # Grab total APs
    total_ap = lines[0]

    # Remove all lines to the actual AP listing
    # Staging-9800-CL#show ap summary
    # Number of APs: 1

    # CC = Country Code
    # RD = Regulatory Domain

    # AP Name                          Slots AP Model             Ethernet MAC   Radio MAC      CC   RD   IP Address                                State        Location
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # CW9166_LOANER                    3     CW9166I-Z            6849.9263.a160 ac2a.a1a6.90c0 AU   -Z   10.66.128.225                             Registered   default location
    lines = lines[7:]

    # Parse the AP details
    ap_details = []
    for line in lines:
        ap_info = line.split()
        ap_details.append({
            'ap_name': ap_info[0],
            'slots': ap_info[1],
            'ap_model': ap_info[2],
            'ether_mac': ap_info[3],
            'radio_mac': ap_info[4],
            'country_code': ap_info[5],
            'radio_domain': ap_info[6],
            'ip_address': ap_info[7],
            'state': ap_info[8],
            'location': ap_info[9]
        })

    # Render the template with the AP details
    return render_template('ap_summary.html', ap_details=ap_details, total_ap=total_ap)

# show ap summary sort descending client-count
@app.route('/ap_sum_client')
def ap_sum_client():
    output = grab_cli_output('show ap summary sort descending client-count')

    # Split the command output into lines
    lines = output.splitlines()
    # Grab total APs
    lines = lines[3:]

    # Parse the AP details
    ap_details = []
    for line in lines:
        ap_info = line.split()
        ap_details.append({
            'ap_name': ap_info[0],
            'ap_mac': ap_info[1],
            'client_count': ap_info[2],
            'data_usage': ap_info[3],
            'throughput': ap_info[4],
            'admin_state': ap_info[5],
        })

    # Render the template with the AP details
    return render_template('ap_summary_client_count.html', ap_details=ap_details)

# show ap summary sort descending data-usage 
@app.route('/ap_sum_data')
def ap_sum_data():
    output = grab_cli_output('show ap summary sort descending data-usage')

    # Split the command output into lines
    lines = output.splitlines()
    # Grab total APs
    lines = lines[3:]

    # Parse the AP details
    ap_details = []
    for line in lines:
        ap_info = line.split()
        ap_details.append({
            'ap_name': ap_info[0],
            'ap_mac': ap_info[1],
            'client_count': ap_info[2],
            'data_usage': ap_info[3],
            'throughput': ap_info[4],
            'admin_state': ap_info[5],
        })

    # Render the template with the AP details
    return render_template('ap_summary_data_usage.html', ap_details=ap_details)

# show wlan all | include Network Name|Number of Active Clients
@app.route('/wlan_all')
def wlan_all():
    output = grab_cli_output('show wlan all | include Network Name|Number of Active Clients')

    # Split the command output into lines
    lines = output.splitlines()
    # Parse the AP details
    wlan_details = []
    SSID = True
    
    for line in lines:
        ap_info = line.split(":")
    
        if SSID:
            wlan_details.append({'ssid': ap_info[1]})
            SSID = False
        else:
            wlan_details.append({'active': ap_info[1]})
            SSID = True
    
    ssid = []
    for i in range(0, len(wlan_details),2):
        ssid.append([wlan_details[i],wlan_details[i+1]])
    
    # Render the template with the AP details
    return render_template('wlan_all.html', ssid=ssid)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
