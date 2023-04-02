#!/user/bin/env powershell

[CmdletBinding()]

Param
(
    [Parameter(position=0)]
    [ValidateSet("Clean","All","BuildExe","UnitTest","Lint","BuildTestData","FunctionalTest","Test")]
    [String]
    $Action="All"
)

Function Clean {
    Write-Host "Clean" -b darkgreen -f white

    # Delete all __pycache__ folders
    Get-ChildItem -Filter __pycache__ -Recurse -Force | Remove-Item -Recurse -Force -Verbose

    # Delete all logs
    Get-ChildItem *.log -Recurse | foreach { Remove-Item -Path $_.FullName -Verbose }

    # Delete all spec files
    Get-ChildItem *.spec -Recurse | foreach { Remove-Item -Path $_.FullName -Verbose }

    # Delete compilation files
    if(Test-Path -Path "build"){
      Remove-Item "build" -Recurse -Verbose
    }

    if(Test-Path -Path "dist"){
      Remove-Item "dist" -Recurse -Verbose
    }

    # Delete test data
    if(Test-Path -Path "test_data"){
      Remove-Item "test_data" -Recurse -Verbose
    }
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
    [IO.File]::WriteAllLines("$($pwd)/test_data/.rmanifest", "file10.altered|file10.txt")

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

    New-Item -Path "test_data/order" -ItemType Directory
    [IO.File]::WriteAllLines("$($pwd)/test_data/order/a.txt", "Test data")
    [IO.File]::WriteAllLines("$($pwd)/test_data/order/b.txt", "Test data")
    [IO.File]::WriteAllLines("$($pwd)/test_data/order/c.txt", "Test data")
    [IO.File]::WriteAllLines("$($pwd)/test_data/order/d.txt", "Test data")
    [IO.File]::WriteAllLines("$($pwd)/test_data/order/e.txt", "Test data")
    [IO.File]::WriteAllLines("$($pwd)/test_data/order/f.txt", "Test data")
    [IO.File]::WriteAllLines("$($pwd)/test_data/order/g.txt", "Test data")
    [IO.File]::WriteAllLines("$($pwd)/test_data/order/not-me.csv", "Test data")
}

Function FunctionalTest {
    Write-Host "FunctionalTest" -b darkgreen -f white

    Write-Host "Test 1 - Pick 3" -b magenta -f white
    python .\src\file_randomizer.py .\test_data\ -pick 3 -r

    Write-Host "Test 2 - Pick 1 .csv" -b magenta -f white
    python .\src\file_randomizer.py .\test_data\ -pick 1 -r -re ".*csv"

    Write-Host "Test 3 - Pick 100 from \test_data\path3" -b magenta -f white
    python .\src\file_randomizer.py .\test_data\path3 -pick 100

    Write-Host "Test 4 - Pick 1 absolute" -b magenta -f white
    python .\src\file_randomizer.py "$($pwd)\test_data\path3\" -pick 1 -r

    Write-Host "Test 5 - Randomize test_data" -b magenta -f white
    python .\src\file_randomizer.py .\test_data\ -name -order

    Write-Host "Test 6 - Randomize \test_data\path3" -b magenta -f white
    python .\src\file_randomizer.py .\test_data\path3 -name -order

    Write-Host "Test 7 - Randomize order \test_data\order" -b magenta -f white
    python .\src\file_randomizer.py .\test_data\order -order -re ".+\.txt"

    Write-Host "Test 8 - Undo \test_data\path3" -b magenta -f white
    python .\src\file_randomizer.py .\test_data\path3 -undo

    Write-Host "Test 9 - Do nothing" -b magenta -f white
    python .\src\file_randomizer.py .\test_data\
}

Function Lint {
  Write-Host "Lint" -b darkgreen -f white

  pylint .\src
}

Function BuildExe {
  Write-Host "BuildExe" -b darkgreen -f white

  $version = Get-Content .\version.txt -First 1

  pyinstaller --onefile src/file_randomizer.py -n "file-randomizer-$($version).exe"
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
    "Test"{
      BuildTestData
      UnitTest
      BuildTestData
      FunctionalTest
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
    "BuildExe"
    {
        BuildExe
    }
    "All"
    {
        Clean
        BuildTestData
        UnitTest
        BuildTestData
        FunctionalTest
        BuildExe
    }
}
