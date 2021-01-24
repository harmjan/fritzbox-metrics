# Fritzbox metrics
A dockerizable python script to pull data from a Fritz!box and push the data into telegraf.

The values are mostly counters so to get meaningful graphs you'll have to take the derivative when plotting the data.

## Usage examples
The script is configured via environment variables, the name of the variable should explain its meaning. The variables `PRINT_DATA` and `FRITZ_USE_TLS` are optional, the others are mandatory.

### Without docker
```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
FRITZ_ADDRESS=192.168.178.1 FRITZ_USERNAME=metrics FRITZ_PASSWORD=supersecret TELEGRAF_HOSTNAME=192.168.178.40 TELEGRAF_PORT=8094 SAMPLE_PERIOD=10 python main.py
```

### With docker
```
sudo docker build . -t fritzbox-metrics
sudo docker run fritzbox-metrics
sudo docker run -e FRITZ_ADDRESS=192.168.178.1 -e FRITZ_USERNAME=metrics -e FRITZ_PASSWORD=supersecret -e TELEGRAF_HOSTNAME=192.168.178.40 -e TELEGRAF_PORT=8094 -e SAMPLE_PERIOD=10 fritzbox-metrics
```

### With docker compose
An example of how to use this container with docker compose:
```
version: "3.3"

networks:
  fritzbox-metrics:
    build: /opt/fritzbox-metrics/
    hostname: fritzbox-metrics
    container_name: fritzbox-metrics
    environment:
      - FRITZ_ADDRESS=192.168.178.1
      - FRITZ_USERNAME=metrics
      - FRITZ_PASSWORD=supersecret
      - FRITZ_USE_TLS=True
      - TELEGRAF_HOSTNAME=192.168.178.2
      - TELEGRAF_PORT=8094
      - SAMPLE_PERIOD=10
    restart: unless-stopped
```
If you also run telegraf as an docker container on the same host can you let this container depend on the telegraf docker container.

## Example output
The following is an example of what the script prints when `PRINT_DATA=True` passed in the environment. Without that option set is the startup information still printed but no information is printed each measurement cycle.
```
Current configuration:
	FRITZ_ADDRESS=192.168.178.1
	FRITZ_USERNAME=metrics
	FRITZ_PASSWORD=***********
	TELEGRAF_HOSTNAME=192.168.178.40
	TELEGRAF_PORT=8094
	SAMPLE_PERIOD=10
	PRINT_DATA=True
	FRITZ_USE_TLS=False

FRITZ!Box 7590 at http://192.168.178.1
FRITZ!OS: 7.21

Polling the following metrics from 192.168.178.1
	WANCommonIFC1
		GetTotalBytesSent
		GetTotalBytesReceived
		GetTotalPacketsSent
		GetTotalPacketsReceived
	WLANConfiguration1
		GetPacketStatistics
		GetTotalAssociations
	WLANConfiguration2
		GetPacketStatistics
		GetTotalAssociations
	WLANConfiguration3
		GetPacketStatistics
		GetTotalAssociations
	LANEthernetInterfaceConfig1
		GetStatistics
	WANDSLInterfaceConfig1
		GetStatisticsTotal
	WANDSLLinkConfig1
		GetStatistics
	WANIPConnection1
		GetPortMappingNumberOfEntries

Starting to poll metrics every 10.0 seconds
{'WANCommonIFC1.TotalBytesSent': 2988178631, 'WANCommonIFC1.TotalBytesReceived': 1937311528, 'WANCommonIFC1.TotalPacketsSent': 1842982, 'WANCommonIFC1.TotalPacketsReceived': 802129, 'WLANConfiguration1.TotalPacketsSent': 293109, 'WLANConfiguration1.TotalPacketsReceived': 251552, 'WLANConfiguration1.TotalAssociations': 0, 'WLANConfiguration2.TotalPacketsSent': 558708, 'WLANConfiguration2.TotalPacketsReceived': 322738, 'WLANConfiguration2.TotalAssociations': 1, 'WLANConfiguration3.TotalPacketsSent': 0, 'WLANConfiguration3.TotalPacketsReceived': 0, 'WLANConfiguration3.TotalAssociations': 0, 'LANEthernetInterfaceConfig1.BytesSent': 1031083879, 'LANEthernetInterfaceConfig1.BytesReceived': 24972131, 'LANEthernetInterfaceConfig1.PacketsSent': 3937778, 'LANEthernetInterfaceConfig1.PacketsReceived': 258788, 'WANDSLInterfaceConfig1.ReceiveBlocks': 18258286, 'WANDSLInterfaceConfig1.TransmitBlocks': 10790262, 'WANDSLInterfaceConfig1.CellDelin': 0, 'WANDSLInterfaceConfig1.LinkRetrain': 3, 'WANDSLInterfaceConfig1.InitErrors': 0, 'WANDSLInterfaceConfig1.InitTimeouts': 0, 'WANDSLInterfaceConfig1.LossOfFraming': 0, 'WANDSLInterfaceConfig1.ErroredSecs': 16300, 'WANDSLInterfaceConfig1.SeverelyErroredSecs': 17, 'WANDSLInterfaceConfig1.FECErrors': 0, 'WANDSLInterfaceConfig1.ATUCFECErrors': 0, 'WANDSLInterfaceConfig1.HECErrors': 0, 'WANDSLInterfaceConfig1.ATUCHECErrors': 0, 'WANDSLInterfaceConfig1.CRCErrors': 43606, 'WANDSLInterfaceConfig1.ATUCCRCErrors': 0, 'WANDSLLinkConfig1.ATMTransmittedBlocks': 2928470532, 'WANDSLLinkConfig1.ATMReceivedBlocks': 1796475453, 'WANDSLLinkConfig1.AAL5CRCErrors': 0, 'WANDSLLinkConfig1.ATMCRCErrors': 0, 'WANIPConnection1.PortMappingNumberOfEntries': 4}
{'WANCommonIFC1.TotalBytesSent': 2999720865, 'WANCommonIFC1.TotalBytesReceived': 1941246231, 'WANCommonIFC1.TotalPacketsSent': 1843038, 'WANCommonIFC1.TotalPacketsReceived': 802156, 'WLANConfiguration1.TotalPacketsSent': 293109, 'WLANConfiguration1.TotalPacketsReceived': 251552, 'WLANConfiguration1.TotalAssociations': 0, 'WLANConfiguration2.TotalPacketsSent': 558721, 'WLANConfiguration2.TotalPacketsReceived': 322738, 'WLANConfiguration2.TotalAssociations': 1, 'WLANConfiguration3.TotalPacketsSent': 0, 'WLANConfiguration3.TotalPacketsReceived': 0, 'WLANConfiguration3.TotalAssociations': 0, 'LANEthernetInterfaceConfig1.BytesSent': 1031102922, 'LANEthernetInterfaceConfig1.BytesReceived': 24972545, 'LANEthernetInterfaceConfig1.PacketsSent': 3937859, 'LANEthernetInterfaceConfig1.PacketsReceived': 258794, 'WANDSLInterfaceConfig1.ReceiveBlocks': 18258286, 'WANDSLInterfaceConfig1.TransmitBlocks': 10790262, 'WANDSLInterfaceConfig1.CellDelin': 0, 'WANDSLInterfaceConfig1.LinkRetrain': 3, 'WANDSLInterfaceConfig1.InitErrors': 0, 'WANDSLInterfaceConfig1.InitTimeouts': 0, 'WANDSLInterfaceConfig1.LossOfFraming': 0, 'WANDSLInterfaceConfig1.ErroredSecs': 16300, 'WANDSLInterfaceConfig1.SeverelyErroredSecs': 17, 'WANDSLInterfaceConfig1.FECErrors': 0, 'WANDSLInterfaceConfig1.ATUCFECErrors': 0, 'WANDSLInterfaceConfig1.HECErrors': 0, 'WANDSLInterfaceConfig1.ATUCHECErrors': 0, 'WANDSLInterfaceConfig1.CRCErrors': 43606, 'WANDSLInterfaceConfig1.ATUCCRCErrors': 0, 'WANDSLLinkConfig1.ATMTransmittedBlocks': 2938561477, 'WANDSLLinkConfig1.ATMReceivedBlocks': 1801245787, 'WANDSLLinkConfig1.AAL5CRCErrors': 0, 'WANDSLLinkConfig1.ATMCRCErrors': 0, 'WANIPConnection1.PortMappingNumberOfEntries': 4}
```
