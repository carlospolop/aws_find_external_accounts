# AWS Find External Accounts

This script allows to help you finding external AWS accounts that have access to roles inside the account of the indicated profile.

## Quick Start

```bash
pip3 install -r requirements.txt

# Help
python3 aws_find_external_accounts.py -h
usage: aws_find_external_accounts.py [-h] -p PROFILE [-k KNOWN_ACCOUNTS]

Find external accounts with access to this one.

options:
  -h, --help            show this help message and exit
  -p PROFILE, --profile PROFILE
                        AWS profile to check.
  -k KNOWN_ACCOUNTS, --known-accounts KNOWN_ACCOUNTS
                        One or more comma separated AWS acoounds id that are known and you want
                        to filter from the results.

# Run example
python3 aws_sensitive_permissions.py -p profile-name [--known-accounts "123123123123,456456456456"]
```