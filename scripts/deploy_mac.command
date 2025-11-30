#!/bin/zsh

venv_path="${HOME}/venv-lt_clear"

if (( $+commands[python3] )); then
    py_cmd='python3'
elif (( $+commands[python] )); then
    py_cmd='python'
else
    echo 'Python command not found, will attempt to install it'
    if (( ! $+commands[brew] )); then
        echo 'Homebrew necessary to install Python, will install it.'
        xcode-select -p 2&>1 > /dev/null
        if [ $? -ne 0 ]; then
            echo 'Command Line Tools for XCode not found.  Attempting to install.'
            xcode-select --install
        fi
        echo 'NOTE: you need administrator level rights to install Homebrew'
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        rehash
    fi
    brew install python@3.12
    rehash
fi

py_ver=$(${py_cmd} -c "import sys; print(sys.version_info.major == 3 and sys.version_info.minor >= 8)")

if [[ ${py_ver} -ne 'True' ]]; then
    echo 'Error: the version of Python is not supported'
    exit
fi

# Now let us check if virtual environment installed
if [[ ! -e $venv_path ]]; then
    echo 'Virtual environment not found, installing it'
    mkdir ${venv_path}
    ${py_cmd} -m venv "${venv_path}"
    source "${venv_path}/bin/activate"
    rehash
    pip install ${0:a:h}/..
else
    source "${venv_path}/bin/activate"
fi
rehash

# Run server
# This is a dirty way to keep the server in the foreground and open the URL
#   after the server has been run.
# If the server is run first and sent in the background, this does not seem to
#   work, the page is black.
(sleep 4; open "http://127.0.0.1:5000") &
${venv_path}/bin/lt_clear_app
