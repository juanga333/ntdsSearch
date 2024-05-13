import cmd
import hashlib
import binascii
import os
import sys
import signal
import readline

def get_ntlm(password):
    genhash = hashlib.new('md4', password.encode('utf-16le')).digest()
    return binascii.hexlify(genhash).decode()

def load_data(file_path, include_history):
    user_dict = {}
    try:
        with open(file_path, "r", encoding='utf-8', errors='ignore') as file:
            for line in file:
                parts = line.strip().split(":")
                if len(parts) > 3:
                    if include_history or "_history" not in parts[0]:
                        user_dict[parts[0]] = parts[3]
        return user_dict
    except FileNotFoundError:
        print("File not found. Please check the file path.")
        return None

class NtdsSearchCmd(cmd.Cmd):
    intro = 'Welcome to ntdsSearch shell. Type help or ? to list commands.\n'
    prompt_base = '(ntdsSearch) '
    prompt = prompt_base
    file = None
    user_dict = None
    history_file = 'command_history.txt'
    include_history = False  
    last_results = []

    def __init__(self):
        super().__init__()
        readline.set_completer_delims(' \t\n;')
        readline.parse_and_bind("tab: complete")
        self.load_history()

    def load_history(self):
        if os.path.exists(self.history_file):
            readline.read_history_file(self.history_file)

    def save_history(self):
        readline.write_history_file(self.history_file)

    def do_load(self, arg):
        """Load secretsdump output from a file: LOAD filename"""
        if arg:
            self.user_dict = load_data(arg, self.include_history)
            if self.user_dict is not None:
                self.file = arg
                self.prompt = f'(ntdsSearch: {self.file}) '
                print(f"Loaded data from {arg}")
            else:
                self.file = None
                self.prompt = self.prompt_base
        else:
            print("Filename is required. Usage: load <filename>")

    def do_toggle_history(self, line):
        """Toggle the inclusion of historical hashes: TOGGLE_HISTORY"""
        self.include_history = not self.include_history
        print(f"Inclusion of historical hashes is now {'enabled' if self.include_history else 'disabled'}.")


    def do_search_username(self, username):
        """Search hash by username: SEARCH_USERNAME username"""
        if not username:
            print("Username is required. Usage: search_username <username>")
            return
        if self.user_dict is None:
            print("ntds.dit is required. Please, use load function first")
            return
        found = False
        username = username.split('\\')[-1]
        for user, hash in self.user_dict.items():
            if user.endswith('\\' + username):
                result = f"{user} hash: {hash}"
                self.last_results.append(result)
                print(result)
                found = True
        if not found:
            print(f"{username} not in dump")

    def do_search_hash(self, hash_val):
        """Search usernames by hash and count occurrences: SEARCH_HASH hash"""
        self.last_results = []
        if not hash_val:
            print("Hash is required. Usage: search_hash <hash>")
            return
        if self.user_dict is None:
            print("ntds.dit is required. Please, use load function first")
            return
        found = False
        count = 0
        for username, hash in self.user_dict.items():
            if hash == hash_val:
                result = username
                self.last_results.append(result)
                print(result)
                found = True
                count += 1
        if not found:
            print("No users found with this hash.")
        else:
            print(f"{count} users found with this hash.")
            self.last_results.append(f"{count} users found with this hash")

    def do_search_password(self, password):
        """Search usernames by password and count occurrences: SEARCH_PASSWORD password"""
        self.last_results = []
        if not password:
            print("Password is required. Usage: search_password <password>")
            return
        if self.user_dict is None:
            print("ntds.dit is required. Please, use load function first")
            return
        hash_val = get_ntlm(password)
        result = f"Hash for {password}: {hash_val}"
        print(result)
        self.last_results.append(result)
        self.do_search_hash(hash_val)

    def do_list_repeated_hashes(self, line):
        """List all users that have their hash repeated and show total users with shared hashes."""
        self.last_results = []
        if not self.user_dict:
            print("No data loaded. Please load a file first.")
            return
        if self.user_dict is None:
            print("ntds.dit is required. Please, use load function first")
            return
        hash_count = {}
        for hash in self.user_dict.values():
            hash_count[hash] = hash_count.get(hash, 0) + 1

        repeated_hashes = {hash: count for hash, count in hash_count.items() if count > 1}
        total_users_with_repeats = sum(count for count in repeated_hashes.values())  

        if not repeated_hashes:
            print("No repeated hashes found.")
            return

        result = f"Total users with repeated hashes: {total_users_with_repeats}"
        print(result)
        self.last_results.append(result)
        for hash, count in repeated_hashes.items():
            result = f"Hash: {hash} is repeated {count} times."
            print(result)
            self.last_results.append(result)
            users_with_hash = [user for user, user_hash in self.user_dict.items() if user_hash == hash]
            for user in users_with_hash:
                result = f"\t{user}"
                print(result)
                self.last_results.append(result)


    def do_export(self, filename):
        """Export the last command results to a file."""
        if not self.last_results:
            print("No results to export.")
            return
        if not filename:
            print("Error: A filename is required. Usage: export <filename>")
            return
        try:
            with open(filename, 'w') as f:
                for line in self.last_results:
                    f.write(line + '\n')
            print(f"Results exported to {filename}")
        except IOError as e:
            print(f"Error writing to file: {e}")


    def do_exit(self, line):
        """Exit the shell"""
        self.save_history()
        return True
    
    def do_clear(self, line):
        "Clear the screen: CLEAR"
        os.system('cls' if os.name == 'nt' else 'clear')

    def emptyline(self):
        pass  # Do nothing on empty input line

    def postloop(self):
        print('Exiting ntdsSearch shell.')

if __name__ == '__main__':
    def handle_sigint(signum, frame):
        print("\nUse 'exit' to quit the shell.")
        sys.stdout.write(str(cmd_instance.prompt))  
        sys.stdout.flush()

    cmd_instance = NtdsSearchCmd()
    signal.signal(signal.SIGINT, handle_sigint)
    cmd_instance.cmdloop()
