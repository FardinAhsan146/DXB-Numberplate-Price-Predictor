echo off
set arg1=%1
shift
git pull origin main
git add -A
git commit -m "%arg1%"
git push origin main 