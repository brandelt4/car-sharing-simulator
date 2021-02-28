# Car Sharing Simulator

<div align="center"> 

<img src="https://github.com/brandelt4/car-sharing-simulator/blob/main/video.gif" />
</div>

## Idea
Car sharing is one of the earliest implementations of a *shared economy* and promises to be a very useful and eco-friendly way for individual transportation. There are, however, certain challenges that impede the acceptance of this service. One such challenge is an incorrect distribution of cars in a city, in which the geolocational 
demand for cars does not coincide with their actual locations. 

## Implementation
Certainly, this is just one problem out of many. In order to account for these problems and simulate the dynamics 
of car sharing in a city, it is handy to simulate it in a computer programme, where one could apply interesting interventions to change people's behaviour, guiding them 
to leave/re-distribute cars to more optimal locations in a city. For instance, one could think of providing small nudges (e.g. monetary incentives) for leaving a 
shared car in a sub-optimal location for an individual's purpose, yet in a more optimal location for matching public demand. 

### Run the simulation
```
cd car-sharing-simulator
python3 agent.py
``` 

### Changing simulation parameters
All parameters of the simulation can be found in `./agent.py`. I will be improving the presentation of these in future versions. 

### Visualisation components
1. *Green dots*: available cars
2. *Red dots*: in-use cars
3. *Black dots*: reserved cars
4. *Black circle*: destination demand hotspots (people tend to go there more often during certain parts of the day, e.g. shopping mall)
5. *Purple circle*: individual car demand (radius of the circle determines how far a person is willing to walk to get to a car)


In this repo, I provide some code for simulating car sharing within a city. 
For any questions about the functions of the code, feel free to contact me or raise suggestions in this repo. 

