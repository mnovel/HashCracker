# HashCracker

HashCracker is a simple password hash cracker that supports various hash types and modes of attack, including wordlist and brute-force attacks.

## Features

- Supports multiple hash types: **MD5**, **SHA1**, **SHA256**, and **SHA512**.
- Two modes of attack: **wordlist** and **brute-force**.
- Configurable parameters for brute-force attacks, including character set and length range.
- Multi-threading support for faster cracking.

## Requirements

- **Python 3.x**
- Required libraries: `hashlib`, `itertools`, `threading`, `argparse`, `os`

## Download and Installation

1. **Clone the Repository:**

   Clone this repository to your local machine using the following command:

   ```bash
   git clone https://github.com/mnovel/HashCracker.git
   ```

2. **Navigate to the Directory:**

   Change into the project directory:

   ```bash
   cd HashCracker
   ```

## Usage

Run the script using Python with the following command line arguments:

```bash
python HashCracker.py -t {0,1,2,3} -m {0,1} hash_input [wordlist_or_charset] [--start_length START_LENGTH] [--end_length END_LENGTH] [--charset CHARSET] [--threads THREADS]
```

### Arguments:

- `-t`, `--hash_type`: Type of hash to crack (0=MD5, 1=SHA1, 2=SHA256, 3=SHA512)
- `-m`, `--mode`: Attack mode (0=wordlist, 1=brute-force)
- `hash_input`: The hash value or file path containing hash values to crack
- `wordlist_or_charset`: Path to the wordlist file (for wordlist mode) or charset (for brute-force mode)
- `--start_length START_LENGTH`: Starting length for brute-force (required for brute-force mode)
- `--end_length END_LENGTH`: Ending length for brute-force (required for brute-force mode)
- `--charset CHARSET`: Character set for brute-force mode (default is `abcdefghijklmnopqrstuvwxyz`)
- `--threads THREADS`: Number of threads for brute-force (default is 4)

## Examples

### 1. Wordlist Attack Example

To crack a hash using a wordlist:

1. Create a hash file `hash.txt` with the following content:

   ```
   d1c056a983786a38ca76a05cda240c7b86d77136
   ```

2. Create a wordlist file `wordlist.txt` with potential passwords:

   ```
   password
   123456
   tes
   admin
   ```

3. Run the wordlist attack:

   ```bash
   python HashCracker.py -t 0 -m 0 hash.txt wordlist.txt
   ```

**Expected Output:**

```
[INFO] Starting wordlist attack using: wordlist.txt
[+] Found: tes for hash d1c056a983786a38ca76a05cda240c7b86d77136
```

### 2. Brute-force Attack Example

To perform a brute-force attack on the same hash:

1. Ensure you have the `hash.txt` with the same content as before.

2. Run the brute-force attack with a character set of `abcd` and lengths from 1 to 4:

   ```bash
   python HashCracker.py -t 0 -m 1 hash.txt --start_length 1 --end_length 4 --charset "abcd"
   ```

**Expected Output:**

```
[INFO] Starting brute-force attack from length 1 to 4
[+] Found: tes for hash d1c056a983786a38ca76a05cda240c7b86d77136
```

## License

This project is licensed under the [MIT License](LICENSE).
