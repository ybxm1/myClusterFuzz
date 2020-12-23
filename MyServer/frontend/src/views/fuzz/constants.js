export const PROTO_TITLE = {
  'modbus': 'Modbus/TCP',
  'siemens': 'Siemens S7',
  'iec104': 'IEC104',
  'profinet': 'ProfiNet',
  'omron': 'OMRON FINS',
  'tcp': 'TCP',
  'udp': 'UDP',
  'icmp': 'ICMP',
  'ip': 'IP',
  'arp': 'ARP',
  'cip': 'CIP',
  'ethernet/ip': 'EtherNet/IP',
  'hartip': 'HartIP',
  'dnp3': 'DNP3',
  'omron_fins': 'OmronFINS',
  'goose': 'IEC GOOSE',
  'mms': 'IEC MMS'
}

export const JobStatus = {
  CREATED: 0,
  SELECTED_CASE: 1,
  TO_FUZZ: 2,
  FUZZING: 3,
  FUZZ_COMPLETE: 4,
  ERROR: 5
}
