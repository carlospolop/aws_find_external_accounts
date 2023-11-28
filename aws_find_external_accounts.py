import boto3
import argparse

def get_roles_assumable_by_external_accounts(session, known_accounts):
    iam = session.client("iam")

    assumable_roles = {}

    roles = iam.list_roles()
    for role in roles["Roles"]:
        current_account = role["Arn"].split(":")[4]
        role_name = role["RoleName"]
        assume_role_policy_document = role["AssumeRolePolicyDocument"]
        statements = assume_role_policy_document["Statement"]

        for statement in statements:
            if statement["Effect"] == "Allow" and "AWS" in statement["Principal"]:
                aws_account = statement["Principal"]["AWS"]
                if isinstance(aws_account, list):
                    for account in aws_account:
                        if not account.startswith("arn:aws:iam"):
                            continue

                        accountn = account.split(":")[4]
                        if current_account != accountn:
                            if role_name not in assumable_roles:
                                assumable_roles[role_name] = {"known": [], "unknown": []}
                            
                            if accountn in known_accounts:
                                assumable_roles[role_name]["known"].append(accountn)
                            else:
                                assumable_roles[role_name]["unknown"].append(accountn)
                else:
                    if not aws_account.startswith("arn:aws:iam"):
                        continue

                    accountn = aws_account.split(":")[4]
                    if current_account != accountn:
                        if role_name not in assumable_roles:
                            assumable_roles[role_name] = {"known": [], "unknown": []}
                        
                        if accountn in known_accounts:
                            assumable_roles[role_name]["known"].append(accountn)
                        else:
                            assumable_roles[role_name]["unknown"].append(accountn)

    return current_account, assumable_roles

def process_profiles(profiles, known_accounts):
    for profile in profiles:
        session = boto3.Session(profile_name=profile)
        current_account, assumable_roles = get_roles_assumable_by_external_accounts(session, known_accounts)

        if assumable_roles:
            print(f"Inside the account `{current_account}`, the following roles can be assumed by external accounts:")
            for role, from_account in assumable_roles.items():
                if from_account["unknown"]:
                    unknown = f""
                    print(f"- Role `{role}` can be accessed from external unknown account `{'`, `'.join(from_account['unknown'])}`")
        else:
            print(f"No roles found that can be assumed by external accounts for profile `{profile}`.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find external accounts with access to this one.")
    parser.add_argument("-p", "--profiles", required=True, nargs='+', help="Space-separated list of AWS profiles to check.")
    parser.add_argument("-k", "--known-accounts", help="One or more comma-separated AWS account IDs that are known and you want to filter from the results.")
    args = parser.parse_args()
    
    profiles = args.profiles
    known_accounts = [a.lower() for a in args.known_accounts.strip().split(",")] if args.known_accounts else []

    process_profiles(profiles, known_accounts)
