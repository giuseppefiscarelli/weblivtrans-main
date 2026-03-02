#!/bin/bash

venv_path="${HOME}/venv-lt_clear"
detach=0
log_file=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --detach|--daemon)
            detach=1
            ;;
        --log)
            log_file="$2"
            shift
            ;;
    esac
    shift
done

if command -v python3 > /dev/null 2>&1; then
    py_cmd='python3'
elif command -v python > /dev/null 2>&1; then
    py_cmd='python'
else
    echo 'Python not found.'
    echo 'Install Python 3 using the package manager provided by your distributions'
    exit
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
fi
source "${venv_path}/bin/activate"
# Always reinstall the local package to pick up updates after git pull
pip install -U "$(dirname "$(realpath "$0")")/.."

# Run server
# This is a dirty way to keep the server in the foreground and open the URL
#   after the server has been run.
# If the server is run first and sent in the background, this does not seem to
#   work, the page is black.
if [[ ${detach} -eq 1 ]]; then
    # Detach from terminal to avoid SIGHUP when the console closes.
    trap '' HUP
    if [[ -n "${log_file}" ]]; then
        nohup "${venv_path}/bin/lt_clear_app" >> "${log_file}" 2>&1 &
    else
        nohup "${venv_path}/bin/lt_clear_app" >/dev/null 2>&1 &
    fi
    echo $! > "${venv_path}/lt_clear_app.pid"
    exit 0
fi

(sleep 3; if command -v xdg-open > /dev/null 2>&1; then xdg-open "http://127.0.0.1:5000"; elif command -v open > /dev/null 2>&1; then open "http://127.0.0.1:5000"; fi) &
"${venv_path}/bin/lt_clear_app"
