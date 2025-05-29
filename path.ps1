# Get the current directory
Clear-Host
$currentDirectory = Get-Location
## Write-Host "Current directory: $($currentDirectory.Path.ToLower()) `n"

# Get the current Path environment variable
$currentPath = [Environment]::GetEnvironmentVariable("Path", "Process")
## Write-Host "Current PATH: $($currentPath.ToLower()) `n"

# Check if the current directory is already in the Path to avoid duplicates
if (!$currentPath.ToLower().contains( $currentDirectory.Path.ToLower())) {
    # Add the current directory to the Path for the current process (session)
    ## [Environment]::SetEnvironmentVariable("Path", "$currentDirectory;$currentPath", "Process")
    Write-Host "Current directory '$($currentDirectory.Path)' added to PATH for this session. `n"
    # (Optional) Verify the Path
    Write-Host "`nUpdated PATH for this session:`n$([Environment]::GetEnvironmentVariable("Path", "Process"))  `n"
} else {
    Write-Host "Current directory '$($currentDirectory.Path)' is already in the PATH for this session. `n"
}



