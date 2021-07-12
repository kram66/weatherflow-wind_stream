import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from websocket import create_connection
import json


# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []

duration= 20

personal_token = "[TOKEN]"
tempest_ID = '[TOKEN]'
station_id = "[TOKEN]"




def opensocket():
	websock     	= create_connection('wss://ws.weatherflow.com/swd/data?api_key=' + personal_token)
	temp_rs     	=  websock.recv()
	websock.send('{"type":"listen_start",' + ' "device_id":' + tempest_ID + ',' + ' "id":"Tempest"}')
	temp_rs     	=  websock.recv()
	temp_rs     	=  websock.recv()
	websock.close()
	json_obj 	= json.loads(temp_rs)
	windspeed	= json_obj['obs'][0][3]
	return windspeed	

# This function is called periodically from FuncAnimation
def animate(i, xs, ys):

     winds = round(opensocket(), 2)

    # Add x and y to lists
    xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    ys.append(winds)

    # Limit x and y lists to 20 items
    xs = xs[-20:]
    ys = ys[-20:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Wind Speed')
    plt.ylabel('WindSpeed (KMpH)')

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), frames=duration, interval=2000)
plt.show()
