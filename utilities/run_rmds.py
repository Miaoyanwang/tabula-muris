#!/usr/bin/env python3

import glob
from io import StringIO
import os
import shlex
import subprocess
import locale
locale.setlocale(locale.LC_ALL, 'en_US.utf8')

import click

"""
May need to set "locales" for Unicode because ASCII is stupid.

e.g. for a ENglish, US machine:

export LC_ALL=en_US.UTF-8 
export LANG=en_US.UTF-8
"""

@click.command()
@click.option('--folder', default='.')
def main(folder):
    """Run all *.Rmd files in a folder and render to HTML"""
    globber = os.path.join(folder, '*.Rmd')
    rmds = glob.iglob(globber)

    for rmd in rmds:
        # Skip the template because it won't work anyway due to syntax errors
        if rmd == "Template.Rmd":
            continue
        click.echo(f'Starting {rmd} ...')
        stdout = rmd + '.out'
        stderr = rmd + '.err'

        command = shlex.split(f"Rscript -e \"rmarkdown::render(\'{rmd}\', "
                              "clean=TRUE)\"  > {stdout} 2>{stderr}")
        print(command)
        with open(stdout, 'w') as file_out:
            with open(stderr, 'w') as file_err:
                subprocess.Popen(command, stdout=file_out, stderr=file_err)


if __name__ == "__main__":
    main()
