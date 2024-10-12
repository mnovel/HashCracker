import sys
import hashlib
import itertools
import threading
import argparse
import os

class HashCracker:
    def __init__(self, hash_values, hash_type, mode, wordlist=None, charset='abcdefghijklmnopqrstuvwxyz', start_length=1, end_length=6, threads=4):
        self.hash_values = hash_values if isinstance(hash_values, list) else [hash_values]
        self.hash_type = hash_type
        self.mode = mode
        self.wordlist = wordlist
        self.charset = charset
        self.start_length = start_length
        self.end_length = end_length
        self.threads = threads
        self.found_hashes = {}
        self.lock = threading.Lock()

    def crack(self):
        """Start the cracking process based on the selected mode."""
        try:
            if self.mode == '0':
                self.wordlist_attack()
            elif self.mode == '1':
                self.brute_force_attack()
            else:
                raise ValueError("Invalid mode specified. Use '0' for wordlist or '1' for brute-force.")
        except Exception as e:
            print(f"[ERROR] {e}")

    def wordlist_attack(self):
        """Perform a hash cracking attack using a wordlist."""
        if not os.path.isfile(self.wordlist):
            raise FileNotFoundError(f"Wordlist file '{self.wordlist}' not found.")
        
        print(f"[INFO] Starting wordlist attack using: {self.wordlist}")
        try:
            with open(self.wordlist, 'r') as file:
                for word in file:
                    word = word.strip()
                    if self.check_hash(word):
                        if len(self.found_hashes) == len(self.hash_values):
                            break
        except Exception as e:
            print(f"[ERROR] An error occurred during wordlist attack: {e}")

    def brute_force_attack(self):
        """Perform a brute-force attack on the hash values."""
        print(f"[INFO] Starting brute-force attack from length {self.start_length} to {self.end_length}")
        try:
            for length in range(self.start_length, self.end_length + 1):
                threads = [threading.Thread(target=self.generate_combinations, args=(length,)) for _ in range(self.threads)]
                for thread in threads:
                    thread.start()
                for thread in threads:
                    thread.join()
                if len(self.found_hashes) == len(self.hash_values):
                    break
        except Exception as e:
            print(f"[ERROR] An error occurred during brute-force attack: {e}")

    def generate_combinations(self, length):
        """Generate all possible combinations of the specified length using the charset."""
        for combo in itertools.product(self.charset, repeat=length):
            candidate = ''.join(combo)
            if self.check_hash(candidate):
                if len(self.found_hashes) == len(self.hash_values):
                    break

    def check_hash(self, candidate):
        """Check if the candidate matches any of the hash values."""
        for hash_value in self.hash_values:
            if hash_value not in self.found_hashes:
                if self.hash(self.hash_type, candidate) == hash_value:
                    with self.lock:
                        print(f"[+] Found: {candidate} for hash {hash_value}")
                        self.found_hashes[hash_value] = candidate
                    return True
        return False

    @staticmethod
    def hash(hash_type, value):
        """Hash the given value using the specified hash type."""
        hash_functions = {
            '0': hashlib.md5,
            '1': hashlib.sha1,
            '2': hashlib.sha256,
            '3': hashlib.sha512
        }
        if hash_type not in hash_functions:
            raise ValueError(f"Unsupported hash type '{hash_type}'.")
        return hash_functions[hash_type](value.encode()).hexdigest()

def load_hashes_from_file(file_path):
    """Load hashes from a file."""
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Hash file '{file_path}' not found.")
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except Exception as e:
        raise RuntimeError(f"Failed to read hash file: {e}")

def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description='HashCracker - A simple password hash cracker.')
    parser.add_argument('-t', '--hash_type', choices=['0', '1', '2', '3'],
                        help='Type of hash to crack (0=MD5, 1=SHA1, 2=SHA256, 3=SHA512)', required=True)
    parser.add_argument('-m', '--mode', choices=['0', '1'],
                        help='Attack mode: 0=wordlist, 1=brute', required=True)
    parser.add_argument('hash_input', help='The hash value or file path containing hash values to crack')
    parser.add_argument('wordlist_or_charset', help='Path to the wordlist file (for wordlist mode) or charset (for brute mode)', nargs='?', default=None)
    parser.add_argument('-s', '--start_length', type=int, help='Starting length for brute-force')
    parser.add_argument('-e', '--end_length', type=int, help='Ending length for brute-force')
    parser.add_argument('-c', '--charset', type=str, help='Character set for brute-force mode', default='abcdefghijklmnopqrstuvwxyz')
    parser.add_argument('-th', '--threads', type=int, default=4, help='Number of threads for brute-force')

    args = parser.parse_args()

    try:
        if args.mode == '0':
            if not args.wordlist_or_charset or not os.path.isfile(args.wordlist_or_charset):
                raise ValueError("For wordlist mode, a valid wordlist file is required.")
        elif args.mode == '1':
            if args.start_length is None or args.end_length is None or args.charset is None:
                raise ValueError("For brute-force mode, --start_length, --end_length, and --charset are required.")

        if args.hash_input.endswith('.txt'):
            hash_values = load_hashes_from_file(args.hash_input)
        else:
            hash_values = [args.hash_input]

        cracker = HashCracker(
            hash_values=hash_values,
            hash_type=args.hash_type,
            mode=args.mode,
            wordlist=args.wordlist_or_charset if args.mode == '0' else None,
            charset=args.charset if args.mode == '1' else 'abcdefghijklmnopqrstuvwxyz',
            start_length=args.start_length,
            end_length=args.end_length,
            threads=args.threads
        )

        cracker.crack()
    
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
