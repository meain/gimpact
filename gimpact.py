'''Simple module to get git stats'''

import subprocess
import fire
import progressbar


class bcolors:
    '''Colors for printing'''
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def get_authors(folder):
    names = subprocess.check_output(["git log --format='%aN' | sort -u"], cwd=folder, shell=True)
    names = names.split('\n')[:-1]
    return names

def get_stats(folder):
    '''Get stats for a for all users'''
    bar = progressbar.ProgressBar()
    print 'Generating stats'
    names = get_authors(folder)
    stats = []
    for name in bar(names):
        command = 'git log --shortstat --no-merges --branches --author=\"' + name + '\" | grep -E "fil(e|es) changed" | awk \'{files+=$1; inserted+=$4; deleted+=$6} END {print files,inserted,deleted}\''
        command = command.decode('utf-8')
        per_auth_stat = subprocess.check_output([command], cwd=folder, shell=True)[:-1].split(' ')
        author_stat = {}
        author_stat['name'] = name
        author_stat['files_changed'] = per_auth_stat[0]
        author_stat['insertions'] = per_auth_stat[1]
        author_stat['deletions'] = per_auth_stat[2]
        stats.append(author_stat)
    return stats


def print_stas(folder):
    stats = get_stats(folder)
    print("{:<45}{:<30}{:<30}{:<30}\n".format(bcolors.UNDERLINE+'Author name'+bcolors.ENDC, bcolors.UNDERLINE+'Files changed'+bcolors.ENDC,\
            bcolors.UNDERLINE+'Insertions'+bcolors.ENDC, bcolors.UNDERLINE+'Deletions'+bcolors.ENDC))
    for stat in stats:
        name = bcolors.BOLD+stat['name']+bcolors.ENDC
        files_changed = bcolors.YELLOW+stat['files_changed']+bcolors.ENDC
        insertions = bcolors.GREEN+stat['insertions']+bcolors.ENDC
        deletions = bcolors.RED+stat['deletions']+bcolors.ENDC
        print("{:<50}{:<30}{:<30}{:<30}\n".format(name, files_changed, insertions, deletions))


class GitStats(object):
    '''Gitstats module for fire'''
    def authorstat(self, folder):
        print_stas(folder)
if __name__ == '__main__':
  fire.Fire(GitStats)
