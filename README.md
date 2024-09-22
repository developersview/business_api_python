# Business API using Python and FastAPI library
### Create the Virtual Environment:
```bash
python -m venv myenv
```
### Activate the Virtual Environment On Windows:
```bash
venv\Scripts\activate
```
### Install Dependencies
```bash
pip install fastapi uvicorn pyodbc
```
### Create requirement.txt
```bash
pip freeze > requirements.txt
```
### Run the FastAPI application
```bash
uvicorn main:app --reload
```
### Deactivate the Virtual Environment
```bash
deactivate
```
### Create an Powershell script to run the app directly
```ps
# run_fastapi.ps1

# Define paths
$projectPath = "<path_to_the_project>"
$venvPath = "$projectPath\myenv"
$scriptPath = "$projectPath\main.py"

# Navigate to the project directory
Set-Location -Path $projectPath

try {
    . "$venvPath\Scripts\Activate.ps1"
    #pip install -r requirements.txt
    uvicorn main:app --host <ip_address> --port <address> --reload
	#uvicorn main:app --reload

}
catch {
    Write-Error "An error occurred: $_"
}
```
## For create a public IP from own machine, Follow this
### 1. Download ngrok
### 2. Login using Github
### 3. Add the authentication
```bash
ngrok config add-authtoken <auth_token>
```
### 4. Run ngrok
```bash
ngrok http http://127.0.0.1:8000/