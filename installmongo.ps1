Write-Host "Installing MongoDB..."
msiexec.exe /q /i mongodb-win32-x86_64-2008plus-ssl-3.4.6-signed.msi "ADDLOCAL=ALL" | Out-Null
 
Write-Host "Create data folder"
$mongoDataFolder = "c:\MongoData"
md "$mongoDataFolder\data"
md "$mongoDataFolder\logs"
 
Write-Host "Create config file"
$cfg = @"
systemLog:
    destination: file
    path: $mongoDataFolder\logs\mongod.log
storage:
    dbPath: $mongoDataFolder\data
"@
$cfg | Out-File "$mongoDataFolder\mongod.cfg"
 
Write-Host "Install Service"
&"$Env:ProgramFiles\MongoDB\Server\3.0\bin\mongod.exe" --config "$mongoDataFolder\mongod.cfg" --install | Out-Null
 
Write-Host "Configure Service"
Set-Service -Name MongoDB -StartupType Automatic
Start-Service -Name MongoDB