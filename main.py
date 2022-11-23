# The project is developed by Kittipich "Luke" Aiumbhornsin
# Created on November 19, 2022

from myBalloons import systemInfo, create_app
from decouple import config as en_var # import the environment var
# import pytz

print("SystemInfo -> ", systemInfo)
print("Environment Variable: "+ en_var('myBalloonsAppSecretKey'))

# print(pytz.all_timezones) # List out all the timezone available
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=8614)


