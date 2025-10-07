@echo off
echo Setting up Node.js environment...
set PATH=C:\Program Files\nodejs;%PATH%
echo Node.js has been added to PATH for this session
echo You can now use 'node' and 'npm' commands directly
echo.
echo Current versions:
node -v
npm -v
echo.
echo Navigate to your project directory and run:
echo   npm run dev    (to start development server)
echo   npm run build  (to build for production)
echo.
pause
