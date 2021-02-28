from environment import Environment
import numpy as np
from PIL import Image
import os

TOTAL_TIME = 0
NUM_LOCS = 20

UNIFORM_PROBABILITY = 0.1
CENTER_PROBABILITY = 0.5

def update_locs(width, height):
    global locs
    locs = [(np.random.uniform(50, width - 50), np.random.uniform(50, height - 50)) for i in range(NUM_LOCS)]


class Demand():

    def __init__(self, environment):

        self.environment = environment

    def generate_random_demand(self, current_time):

        # How many will request a car at this time?
        num_people = int(3 * np.sin((current_time % 1440) / 110 - 3) + 3)
        num_people = 1 if num_people == 0 else num_people


        self.centres_of_demand = [np.random.multivariate_normal([width/2, height/2], 6000*np.eye(2)) for i in range(num_people)]
        # self.centres_of_demand = [(np.random.uniform(0, width), np.random.uniform(0, height)) for i in range(num_people)]
        return self.centres_of_demand

    def activate_demand(self):
        for demand_centre in self.centres_of_demand:
            for agent in agents:
                if np.linalg.norm(agent.state - demand_centre) < 10 and agent.status == 'Parked':
                    agent.change_status('In demand')
                    break



# The Agent class allows the agent to interact with the environment.
class Agent():

    # The class initialisation function.
    def __init__(self, environment):
        '''
        :param environment:
        '''

        super().__init__()
        # Set the agent's environment.
        self.environment = environment

        self.env_width, self.env_height = self.environment.width, self.environment.height

        self.status = 'Active' # 'Parked', 'In demand'
        self.colour = (0, 0, 255)

        # Create the agent's current state
        self.state = np.array([np.random.uniform(0, self.env_width),
                               np.random.uniform(0, self.env_height)])

        self.initial_position = self.state

        self.destination = None

        self.speed_vector = None
        self.travel_time = np.random.uniform(6, 7)      # optimal speed
        self.wait_time = np.random.randint(0, 1)


    # Function to make the agent take one step in the environment.
    def step(self):



        if self.status == 'In demand' and self.wait_time != 0:
            self.wait_time -= 1

        elif self.status == 'Parked':
            pass

        else:
            self.change_status('Active')
            # 4. Make the step
            self.state += self.speed_vector
            self.state = np.array([self.state[0], self.state[1]])

            if abs(self.state[0] - self.destination[0]) < 5 and abs(self.state[1] - self.destination[1]) < 5:
                self.change_status('Parked')
                # self.hide_destination()
                self.wait_time = self.generate_random_wait_time()
                self.sample_random_destination()


    def generate_random_wait_time(self):
        return np.random.randint(250, 750)


    def get_int_state(self):
        return np.array([int(self.state[0]), int(self.state[1])])

    def get_int_initial_state(self):
        return np.array([int(self.initial_position[0]), int(self.initial_position[1])])


    def change_status(self, new_status):
        self.status = new_status
        self.change_colour()

        if self.status == 'Active':
            self.show_destination()
        elif self.status == 'In demand':
            self.hide_destination()
            self.wait_time = 25
        else:
            self.hide_destination()


    def change_colour(self):

        if self.status == 'Active':
            self.colour = (0, 0, 255)
        elif self.status == 'In demand':
            self.colour = (0, 0, 0)
        else:
            self.colour = (0, 255, 0)
        # self.colour = (255, 255, 255)

    def get_colour(self):
        return self.colour


    def sample_random_destination(self):

        # Record intial position
        self.initial_position = self.state

        # Sample a random destination
        # x_dest = np.random.randint(0, 500)
        # y_dest = np.random.randint(0, 500)

        # 1. Choose which mode to go to
        p = [(1 - (CENTER_PROBABILITY+UNIFORM_PROBABILITY))/(NUM_LOCS) for num in range(NUM_LOCS)]
        p.append(UNIFORM_PROBABILITY) # proba of grabbing uniformly
        p.append(CENTER_PROBABILITY) # probability of grabbing the middle


        mode = np.random.choice([i for i in range(NUM_LOCS+2)], p=p)

        # 2.
        if mode == NUM_LOCS:
            x_dest, y_dest = np.random.randint(0, self.env_width), np.random.randint(0, self.env_height)
        elif mode == NUM_LOCS+1:
            x_dest, y_dest = np.random.multivariate_normal((width/2, height/2), 1000 * np.eye(2))
        else:
            # print(len(locs), mode)
            x_dest, y_dest = np.random.multivariate_normal(locs[mode], 100*np.eye(2))

        x_dest, y_dest = int(x_dest), int(y_dest)

        self.direction_of_travel = np.array([(x_dest - self.state[0]), (y_dest - self.state[1])])
        self.direction_of_travel = self.direction_of_travel / (self.direction_of_travel ** 2).sum() ** 0.5

        self.speed_vector = np.array([self.direction_of_travel[0] * self.travel_time,
                                      self.direction_of_travel[1] * self.travel_time])

        self.destination = np.array([x_dest, y_dest])


    def hide_destination(self):
        self.destination_colour = (255, 255, 255)

    def show_destination(self):
        self.destination_colour = (255, 0, 0)

    def get_destination_colour(self):
        return self.destination



def track_time(current_time):
    '''
    Updates the current time
    :param current_time: tuple (hours, minutes)
    :return: new_time: tuple (hours, minutes)
    '''
    hours, minutes = current_time
    minutes += 1
    if minutes % 60 == 0:
        minutes = 0
        hours += 1
    if hours % 24 == 0:
        hours = 0
    return (hours, minutes)



# Main entry point
if __name__ == "__main__":

    # # Set the random seed for both NumPy and Torch
    # # You should leave this as 0, for consistency across different runs (Deep Reinforcement Learning is highly sensitive to different random seeds, so keeping this the same throughout will help you debug your code).
    CID = 123456
    np.random.seed(CID)
    times_locs_were_changed = 0
    # Create an environment.
    # If display is True, then the environment will be displayed after every agent step. This can be set to False to speed up training time. The evaluation in part 2 of the coursework will be done based on the time with display=False.
    # Magnification determines how big the window will be when displaying the environment on your monitor. For desktop PCs, a value of 1000 should be about right. For laptops, a value of 500 should be about right. Note that this value does not affect the underlying state space or the learning, just the visualisation of the environment.
    width, height = 600, 350
    environment = Environment(display=True, magnification=2, width=width, height=height)
    demand = Demand(environment)

    update_locs(width, height)

    # Create agents
    agents = []
    _ = [agents.append(Agent(environment)) for i in range(500)]

    # Initialise random destinations
    _ = [agent.sample_random_destination() for agent in agents]

    demand_centres = None
    current_time = (0, 0)
    # Loop over episodes
    while True:

        for agent in agents:
            agent.step()
        environment.update_agents(agents)

        environment.draw(current_time, locs, demand_centres, total_time=TOTAL_TIME)
        TOTAL_TIME += 1
        current_time = track_time(current_time)

        demand_centres = demand.generate_random_demand(TOTAL_TIME)
        demand.activate_demand()

        # if TOTAL_TIME % 100 == 0:
        #     demand_centres = demand.generate_random_demand(150)
        #     # environment.display_demand(demand_centres)
        #     demand.activate_demand()

        if track_time(current_time) == (5, 0):
            NUM_LOCS = np.random.randint(10, 20)
            update_locs(width, height)
            print(f'Change NUM_LOCS to {NUM_LOCS}')
            times_locs_were_changed += 1
            UNIFORM_PROBABILITY = 0.1
            CENTER_PROBABILITY = 0.9

        if track_time(current_time) == (16, 0):

            NUM_LOCS = np.random.randint(10, 20)
            update_locs(width, height)
            print(f'Change NUM_LOCS to {NUM_LOCS}')
            times_locs_were_changed += 1
            UNIFORM_PROBABILITY = 0.5
            CENTER_PROBABILITY = 0.1

        if TOTAL_TIME == 500:
            print('release')
            # environment.cap.release()

            # try:
            # Create the frames
            frames = []
            imgs = [d for d in os.listdir(f'./video/')]
            imgs.sort(key=lambda path: int(path[6:11]), reverse=False)

            for i in imgs:
                new_frame = Image.open(f'./video/' + i)
                frames.append(new_frame)

            # Save into a GIF file that loops forever
            frames[0].save(f'./video.gif', format='GIF',
                           append_images=frames[1:],
                           save_all=True,
                           duration=50, loop=0)
            # except:
            #     print('No video is made.')
