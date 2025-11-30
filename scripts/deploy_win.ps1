$py_check = python.exe --version 2>&1
$py_version = "3.12.7"
$py_arch = "amd64"
$py_exe = "python-${py_version}-${py_arch}.exe"
$py_downdir = "${HOME}/Downloads"
$venv_path = "${HOME}/venv-lt_clear"

# Check if we need to install Python
if ($py_check -like "* not found*") {
    Write-Output("Python is not installed.")
    Write-Output("Downloading version ${py_version} for ${py_arch} in ${py_downdir}...")
    Invoke-WebRequest -Uri https://www.python.org/ftp/python/$py_version/$py_exe `
                      -OutFile ${py_downdir}/${py_exe}
    Start-Process -NoNewWindow -FilePath "${py_downdir}/${py_exe}" `
                  -ArgumentList "/quiet", "PrependPath=1", "Include_test=0" -Wait
    # We now update the PATH environment variable for the current session
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") +
                ";" +
                [System.Environment]::GetEnvironmentVariable("Path","User")
} else {
    Write-Output("Python is installed.  Using ${py_check}")
}

# Now let us check that the version is OK, considering at least version 3.8
$py_ver = python -c "import sys; print(sys.version_info.major == 3 and sys.version_info.minor > 8)"

if (${py_ver} -ne 'True') {
    Write-Output('Error: the version of Python is not supported')
    Break
}

# Now let us check if virtual environment installed
if (-Not (Test-Path -Path $venv_path)) {
    Write-Output("Virtual environment not found, installing it")
    # Set-Location ${HOME}
    New-Item -Path ${venv_path} -ItemType Directory
    Start-Process -NoNewWindow "python.exe" -ArgumentList "-m", "venv", "${venv_path}" -Wait
    . "${venv_path}/Scripts/Activate.ps1"
    $dir_script = Split-Path -Parent $MyInvocation.MyCommand.Definition
    Start-Process -NoNewWindow "pip.exe" `
        -ArgumentList "install", (Get-Item $dir_script).Parent.FullName -Wait
} else {
    . "${venv_path}/Scripts/Activate.ps1"
    # # We update the PATH environment variable with the programs from the script
    # $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") +
    #             ";" +
    #             [System.Environment]::GetEnvironmentVariable("Path","User")
}

# Run server
Start-Process -NoNewWindow "lt_clear_app.exe"
Start-Process "http://127.0.0.1:5000"
