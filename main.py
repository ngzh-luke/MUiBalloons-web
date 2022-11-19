# The project is developed by Kittipich "Luke" Aiumbhornsin
# Created on November 19, 2022

from myBalloons import systemInfo, create_app

print("SystemInfo -> ", systemInfo)

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=8614)
