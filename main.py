import os
import time
from typing import List, Dict, Tuple, Any

import fritzconnection as fc
from fritzconnection.lib.fritzstatus import FritzStatus

from telegraf.client import TelegrafClient

# The fields to read out from the Fritzbox and put into telegraf
# (service_name, [action_name])
metrics_names : Tuple[str, List[str]] = [
    ("WANCommonIFC1", [
        "GetTotalBytesSent",
        "GetTotalBytesReceived",
        "GetTotalPacketsSent",
        "GetTotalPacketsReceived"
    ]),
    ("WLANConfiguration1", [
        #"GetStatistics", # GetStatistics and GetPacketStatistics are the same thing
        "GetPacketStatistics",
        "GetTotalAssociations"
    ]),
    ("WLANConfiguration2", [
        #"GetStatistics",
        "GetPacketStatistics",
        "GetTotalAssociations"
    ]),
    ("WLANConfiguration3", [
        #"GetStatistics",
        "GetPacketStatistics",
        "GetTotalAssociations"
    ]),
    ("LANEthernetInterfaceConfig1", [
        "GetStatistics"
    ]),
    ("WANDSLInterfaceConfig1", [
        "GetStatisticsTotal"
    ]),
    ("WANDSLLinkConfig1", [
        "GetStatistics"
    ]),
    ("WANIPConnection1", [
        "GetPortMappingNumberOfEntries"
    ])
]

def main() -> None:
    setting_keys: List[str] = [
        "FRITZ_ADDRESS",
        "FRITZ_USERNAME",
        "FRITZ_PASSWORD",
        "TELEGRAF_HOSTNAME",
        "TELEGRAF_PORT",
        "SAMPLE_PERIOD"
    ]
    # Check if all environment keys are suplied and if they aren't end the program via an exception
    missing_keys = [key for key in setting_keys if key not in os.environ]
    if len(missing_keys) > 0:
        raise Exception(f"You need to supply the environment variable(s): {', '.join(missing_keys)}")
    # Extract the settings into a dictionary
    settings: Dict[str, Any] = {key: os.environ[key] for key in setting_keys}

    # Add optional settings, they are
    settings["PRINT_DATA"] = "PRINT_DATA" in os.environ and os.environ["PRINT_DATA"] != "False"
    settings["FRITZ_USE_TLS"] = "FRITZ_USE_TLS" in os.environ and os.environ["FRITZ_USE_TLS"] != "False"

    # Print information about the current configuration
    print("Current configuration:")
    for key, value in settings.items():
        # The still leaks the length of the password to the log but I don't think that really matters
        censored_value = '*'*len(value) if "PASSWORD" in key else value
        print(f"\t{key}={censored_value}")
    print()

    # Create the fritz connection
    fritz_connection = fc.FritzConnection(
        address  = settings["FRITZ_ADDRESS"],
        user     = settings["FRITZ_USERNAME"],
        password = settings["FRITZ_PASSWORD"],
        use_tls  = settings["FRITZ_USE_TLS"])
    print(fritz_connection)
    print()

    # Create the telgraf client, this pip library doesn't really do much
    telegraf_client = TelegrafClient(
        host=settings["TELEGRAF_HOSTNAME"],
        port=int(settings["TELEGRAF_PORT"]))

    # Set the sample period variable
    SAMPLE_PERIOD = float(settings["SAMPLE_PERIOD"])

    # Print some debug info that goes to docker log
    print(f"Polling the following metrics from {settings['FRITZ_ADDRESS']}")
    for service, actions in metrics_names:
        print(f"\t{service}")
        for action in actions:
            print(f"\t\t{action}")
    print()
    print(f"Starting to poll metrics every {SAMPLE_PERIOD} seconds")

    # Record the start time
    start = time.time()
    # Start looping
    while True:
        # Retrieve the data from the fritzbox and put it in the data dictionary
        data = {}
        for service, actions in metrics_names:
            for action in actions:
                result = fritz_connection.call_action(service, action)
                for key, value in result.items():
                    # Remove new prefix from variable names
                    if key[0:3] == 'New':
                        key = key[3:]
                    data[f"{service}.{key}"] = value

        # Send the collected data to telegraf
        telegraf_client.metric("router", data)

        # Print the data depending on the settings
        if settings["PRINT_DATA"]:
            print(data)

        # Sleep the appropriate amount of time
        time.sleep(SAMPLE_PERIOD - (time.time()-start)%SAMPLE_PERIOD)

if __name__ == "__main__":
    main()
