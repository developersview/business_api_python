# run_fastapi.ps1

# Define paths
$projectPath = "<path>"
$venvPath = "$projectPath\myenv"
$scriptPath = "$projectPath\main.py"

# Navigate to the project directory
Set-Location -Path $projectPath

try {
    . "$venvPath\Scripts\Activate.ps1"
    #pip install -r requirements.txt
    uvicorn main:app --host 192.168.0.106 --port 8000 --reload
	#uvicorn main:app --reload

}
catch {
    Write-Error "An error occurred: $_"
}
