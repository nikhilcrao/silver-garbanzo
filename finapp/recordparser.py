import datetime
import re
import json


def parseAmount(part : str) -> str:
  return float(re.sub(',', '', part, count=4))


def parseMerchant(part : str) -> str:
  return re.sub(r'\s+', ' ', part.lower())


def parseDatetime(part : str) -> str:
  parsed_part = ''
  try:
    parsed_part = datetime.datetime.strptime(part, '%d/%m/%Y %H:%M:%S')
  except ValueError:
    parsed_part = datetime.datetime.strptime(part, '%d/%m/%Y')
  return parsed_part.strftime('%Y-%m-%d %H:%M:%S')


def parseRecord(line : str) -> dict[str, str]:
  parts = line.split('~')

  if len(parts) == 0 or len(parts) != 7:
    return {}

  if line.startswith('Transaction type'):
    return {}

  try:
    record = {
      'type': parts[0],
      'account': parts[1],
      'date': parseDatetime(parts[2]),
      'merchant': parseMerchant(parts[3]),
      'raw_amount': parseAmount(parts[5]),
      'credit': 1 if parts[6] == 'Cr' else -1,
    }
    record['amount'] = record['credit'] * record['raw_amount']
    record['category'] = None
  except ValueError:
    print('Error parsing record: %s' % line)
    raise
  return record


def ImportRecords(filename : str, verbose=False) -> list[dict[str, str]]:
  if verbose:
    print('Importing records from %s' % filename)

  imported = []
  with open(filename) as file:
    scan_records = False    
    for line in file.readlines():
      if line.startswith('Transaction type'):
        scan_records = True
      elif line.startswith('Opening'):
        scan_records = False

      if scan_records:
        record = parseRecord(line)
        if len(record) == 0:
          continue
        imported.append(record)
        if verbose:
          print(record)

    if verbose:
      print('Imported %d records' % len(imported))

    return imported