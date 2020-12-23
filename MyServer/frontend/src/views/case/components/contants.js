export const Filters = [
  { text: 'ARP', value: 'arp' },
  { text: 'Siemens S7', value: 'siemens' },
  { text: 'Modbus/TCP', value: 'modbus' },
  { text: 'IEC104', value: 'iec104' },
  { text: 'Hart-IP', value: 'hartip' },
  { text: 'DNP3', value: 'dnp3' },
  { text: 'CIP', value: 'cip' },
  { text: 'IEC-MMS', value: 'mms' },
  { text: 'IEC-GOOSE', value: 'goose' },
  { text: 'OMRON-FINS', value: 'omron_fins' },
  { text: 'ProfiNet', value: 'profinet' },
  { text: 'EthernetIP', value: 'ethernet/ip' },
  { text: 'ICMP', value: 'icmp' },
  { text: 'IP', value: 'ip' },
  { text: 'TCP', value: 'tcp' },
  { text: 'UDP', value: 'udp' }
]

export const PROTO_MAP = {
  'arp': 'ARP',
  'ip': 'IP',
  'tcp': 'TCP',
  'udp': 'UDP',
  'icmp': 'ICMP',
  'profinet': 'ProfiNet',
  'omron_fins': 'OMRON-FINS',
  'goose': 'IEC-GOOSE',
  'mms': 'IEC-MMS',
  'cip': 'CIP',
  'dnp3': 'DNP3',
  'hartip': 'Hart-IP',
  'iec104': 'IEC104',
  'modbus': 'Modbus/TCP',
  'siemens': 'Siemens S7',
  'ethernet/ip': 'EthernetIP'
}
