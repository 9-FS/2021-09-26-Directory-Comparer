# Copyright (c) 2023 구FS, all rights reserved. Subject to the MIT licence in `licence.md`.
import copy
import KFS.log
import logging
import os


@KFS.log.timeit
def main() -> None:
    dirs_entries: list[list[str]] = []                          # directory 1 and 2 entries all
    DIRS_LEN: int = 2                                           # number of directories
    dirs_path: list[str] = []                                   # directory absolute paths
    dirs_uniques: list[list[str]] = []                          # directory 1 and 2 entries unique
    result: str = ""                                            # result with all deviations, ready for saving in file
    RESULT_FILENAME: str = "Directory Differences.txt"          # result file
    user_input: str                                             # user input, temporary variable
    
    i = 0
    while i<DIRS_LEN:                                           # get user input for all directories
        logging.info(f"Directory {i+1} path: ")
        user_input = input()                                    # path input, crash if user is stupid and gives wrong path
                                                                # user_input="C:/Users/Felix/Dropbox/Musik/Bibliothek"
        logging.info(user_input)
        try:
            dirs_entries.append(os.listdir(user_input))         # try to generate entry list, will fail if path can't be found
        except FileNotFoundError:
            logging.error(f"Directory with path \"{user_input}\" could not be found.")
            continue                                            # try again
        dirs_path.append(os.path.abspath(user_input))           # append absolute path
        logging.info(f"Found directory at: \"{dirs_path[-1]}\"")
        
        dirs_uniques.append(copy.deepcopy(dirs_entries[-1]))    # initialise uniques with deep copy of all entries
        i += 1
    
    result += "--------------------------------------------------\n"
    for i, dir_entries in enumerate(dirs_entries):              # for all directories
        for j, dir_entries in enumerate(dirs_entries):          # go through all other directories
            if i==j:                                            # skip same directory
                continue
            for dir_entry in dir_entries:                       # and remove their entries in own unique list
                try:
                    dirs_uniques[i].remove(dir_entry)
                except ValueError:
                    pass
        
        result += f"Directory \"{dirs_path[i]}\" uniques:\n"    # generate result for this directory
        if len(dirs_uniques[i])==0:                             # placeholder
            result += "-"
        else:
            result += "\n".join(dirs_uniques[i])                # uniques
        result += "\n--------------------------------------------------\n"
    logging.info(f"{sum([len(dir_uniques) for dir_uniques in dirs_uniques])} deviations found.")
    logging.info(result)
    
    logging.info(f"Writing results into file \"{RESULT_FILENAME}\"...")
    with open(RESULT_FILENAME, "wt", encoding="utf-8") as result_file:
        result_file.write(result)
    logging.info(f"\rWrote results into file \"{RESULT_FILENAME}\".")
    
    return