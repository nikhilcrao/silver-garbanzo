import datetime
import re
import json


def parseAmount(part : str) -> str:
  return float(re.sub(',', '', part, count=4))


def parseMerchant(part : str) -> str:
  return re.sub(r'\s+', ' ', part.lower())


def parseDateTime(part : str) -> str:
  parsed_part = ''
  try:
    parsed_part = datetime.datetime.strptime(part, '%d/%m/%Y %H:%M:%S')
  except ValueError:
    parsed_part = datetime.datetime.strptime(part, '%d/%m/%Y')
  return parsed_part.strftime('%Y-%m-%d %H:%M:%S')


def parseDateTimeAccount(part : str) -> str:
  parsed_part = datetime.datetime.strptime(part, '%d/%m/%y')
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
      'date': parseDateTime(parts[2]),
      'merchant': parseMerchant(parts[3]),
      'raw_amount': parseAmount(parts[5]),
      'credit': -1 if parts[6] == 'Cr' else 1,
    }
    record['amount'] = record['credit'] * record['raw_amount']
    record['category'] = None
  except ValueError:
    print('Error parsing record: %s' % line)
    raise
  return record


# type='cc' --> cc
# type='acct' --> acct
def ImportRecords(filename : str, type : int, verbose=False) -> list[dict[str, str]]:
  if verbose:
    print('Importing records from %s' % filename)

  if type == 'cc':
    return ImportRecordsFromCreditCard(filename, verbose)
  elif type == 'acct':
    return ImportRecordsFromAccount(filename, verbose)


def parseAccountRecord(line : str) -> dict[str, str]:
  parts = line.split(',')

  if len(parts) == 0 or len(parts) != 7:
    return {}

  try:
    is_credit = True if parts[3].strip() == '0.00' else False
    record = {
      'type': None,
      'account': None,
      'date': parseDateTimeAccount(parts[2].strip()),
      'merchant': '|'.join([parts[1].strip(), parts[5].strip()]),
      'raw_amount': float(parts[4]) if is_credit else float(parts[3]),
      'credit': -1 if is_credit else 1,
    }
    record['amount'] = record['credit'] * record['raw_amount']
    record['category'] = None
  except ValueError:
    print('Error parsing record: %s' % line)
    raise
  return record


def ImportRecordsFromAccount(filename : str, verbose=False) -> list[dict[str, str]]:
  imported = []
  with open(filename) as file:
    scan_records = False
    for line in file.readlines():
      if line.strip().startswith('Date'):
        scan_records = True
        continue

      if scan_records:
        record = parseAccountRecord(line)
        if len(record) == 0:
          continue
        imported.append(record)
        if verbose:
          print(record)
          
  if verbose:
    print('Imported %d records' % len(imported))

  return imported


def ImportRecordsFromCreditCard(filename : str, verbose=False) -> list[dict[str, str]]:
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