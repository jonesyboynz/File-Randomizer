#!/user/bin/env powershell

[CmdletBinding()]

Param
(
    [Parameter(position=0)]
    [ValidateSet("Clean","All","Build","UnitTest","Lint","BuildTestData","FunctionalTest")]
    [String]
    $Action="All"
)

Function Clean {
    Write-Host "Clean" -b darkgreen -f white

    # Delete all __pycache__ folders
    Get-ChildItem -Filter __pycache__ -Recurse -Force | Remove-Item -Recurse -Force -Verbose

    # Delete all logs
    Get-ChildItem *.log -Recurse | foreach { Remove-Item -Path $_.FullName -Verbose }
}

Function UnitTest {
    Write-Host "UnitTest" -b darkgreen -f white

    python -m unittest discover -s .\src -p "*_tests.py"
}

Function BuildTestData {
    Write-Host "BuildTestData" -b darkgreen -f white

    Write-Host "Removing exiting test data" -b magenta -f white
    if(Test-Path -Path "test_data"){
      Remove-Item "test_data" -Recurse -Verbose
    }

    Write-Host "Generating test data" -b magenta -f white
    New-Item -Path "test_data" -ItemType Directory
    [IO.File]::WriteAllLines("$($pwd)/test_data/file1.txt", "Test data")
    [IO.File]::WriteAllLines("$($pwd)/test_data/file2.csv", "Test data")
    [IO.File]::WriteAllLines("$($pwd)/test_data/file10.altered", "Test data")
    [IO.File]::WriteAllLines("$($pwd)/test_data/.rmanifestlog", "file10.altered|file10.txt")

    New-Item -Path "test_data/path1" -ItemType Directory
    [IO.File]::WriteAllLines("$($pwd)/test_data/path1/file3.txt", "Test data")

    New-Item -Path "test_data/path1/path2" -ItemType Directory
    [IO.File]::WriteAllLines("$($pwd)/test_data/path1/path2/file4.txt", "Test data")
    [IO.File]::WriteAllLines("$($pwd)/test_data/path1/path2/file5.txt", "Test data")
    [IO.File]::WriteAllLines("$($pwd)/test_data/path1/path2/file6.csv", "Test data")
    [IO.File]::WriteAllLines("$($pwd)/test_data/path1/path2/file7", "Test data")

    New-Item -Path "test_data/path3" -ItemType Directory
    [IO.File]::WriteAllLines("$($pwd)/test_data/path3/file8.txt", "Test data")
    [IO.File]::WriteAllLines("$($pwd)/test_data/path3/file9.data", "Test data")
}

Function FunctionalTest {
    Write-Host "FunctionalTest" -b darkgreen -f white

    Write-Host "Test 1 - Pick 3" -b magenta -f white
    python .\src\file_randomizer.py .\test_data\ -pick 3 -r

    Write-Host "Test 2 - Pick 1 .csv" -b magenta -f white
    python .\src\file_randomizer.py .\test_data\ -pick 1 -r -re ".*csv"

    Write-Host "Test 3 - Pick 100 from path3" -b magenta -f white
    python .\src\file_randomizer.py .\test_data\path3 -pick 100

    Write-Host "Test 4 - Randomize test_data" -b magenta -f white
    python .\src\file_randomizer.py .\test_data\ -name -order

    Write-Host "Test 5 - Undo test_data" -b magenta -f white
    Write-Host "todo"

    Write-Host "Test 6 - Do nothing" -b magenta -f white
    python .\src\file_randomizer.py .\test_data\
}

Function Lint {
  Write-Host "Lint" -b darkgreen -f white

  pylint .\src
}

Function Build {
  Write-Host "Build" -b darkgreen -f white

  pyinstaller --onefile src/file_randomizer.py
}


if (!(Test-Path -Path .filename-randomizer-project-anchor)){
  Write-Host "run-app.ps1 must be invoked from the project directory" -b red -f black
  exit 1
}

Switch($Action)
{
    "Clean"
    {
        Clean
    }
    "UnitTest"
    {
        BuildTestData
        UnitTest
    }
    "BuildTestData"
    {
        BuildTestData
    }
    "FunctionalTest"{
      BuildTestData
      FunctionalTest
    }
    "Lint"
    {
        Lint
    }
    "Build"
    {
        Build
    }
    "All"
    {
        Clean
        BuildTestData
        UnitTest
        BuildTestData
        FunctionalTest
        Build
    }
}
