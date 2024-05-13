
# ntdsSearch

This project implements a console tool for loading, searching, and managing data extracted from ntds.dit (SecretsDump output).

## Features
-   **Data Loading**: Loads output files from `secretsdump`.
-   **Search Functionality**: Enables searches by username, hash, and password.
-   **Search History**: Maintains a history of the most recently executed commands.
-   **Results Export**: Allows exporting the results of the last executed command to a file.
-   **Include Historical Hashes**: Option to include or exclude historical hashes in searches.

## Requirements

-   Python 3.x
-   `readline` module (on Unix-based systems)
-   `pyreadline` module (on Windows, if necessary)

### Usage
```
python3 ntdsSearch.py
```
### Available Commands

-   `load <filename>`: Loads data from a specified file.
-   `search_username <username>`: Searches for a user by username.
-   `search_hash <hash>`: Searches for all users with a specific hash.
-   `search_password <password>`: Searches for all users with a specific password.
-   `list_repeated_hashes`: Lists hashes that are repeated among users.
-   `toggle_history`: Toggles the inclusion of historical hashes in searches.
-   `export <filename>`: Exports the results of the last used command to a file.
-   `clear`: Clears the console screen.
-   `exit`: Exits the application.

### Usage Example

To load a file and search for a specific hash:

```
(ntdsSearch) load example_ntds_output.txt
(ntdsSearch: example_ntds_output.txt) search_hash e19ccf75ee54e06b
```
To list repetitions between users
```
(ntdsSearch: example_ntds_output.txt) search_password password1
```

To enable the inclusion of old hashes and list all repeated hashes:

```
(ntdsSearch: example_ntds_output.txt) toggle_history
(ntdsSearch: example_ntds_output.txt) list_repeated_hashes
```
