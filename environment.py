import numpy as np
import cv2
from PIL import ImageGrab
from PIL import Image



# The Environment class defines the "world" within which the agent is acting
class Environment:

    # Function to initialise an Environment object
    def __init__(self, display, magnification, width, height):

        # Set whether the environment should be displayed after every step
        self.display = display
        # Set the magnification factor of the display
        self.magnification = magnification

        # Set the initial state of the agent
        # self.init_state = np.array([0.15, 0.15], dtype=np.float32)
        # # Set the initial state of the goal
        # self.goal_state = np.array([0.75, 0.85], dtype=np.float32)
        # # Set the space which the obstacle occupies
        # self.obstacle_space = np.array([[0.3, 0.5], [0.3, 0.6]], dtype=np.float32)

        self.width, self.height = width, height

        # Create an image which will be used to display the environment
        self.image = np.zeros((self.height * self.magnification, self.width * self.magnification, 3))

        # Camera
        # self.f = cv2.VideoWriter_fourcc(*"MJPG")
        # self.cap = cv2.VideoWriter('new3.avi', self.f, 30, (self.height * self.magnification, self.width * self.magnification))

        # self.image = cv2.imread('buda.jpg', 1)
        # self.image = cv2.resize(self.image, (500 * self.magnification, 500 * self.magnification), interpolation = cv2.INTER_AREA)
        print('Created space of shape: ', self.image.shape)

        self.agents = None


    def update_agents(self, agents):
        self.agents = agents


    def display_time(self, current_time):

        # font
        font = cv2.FONT_HERSHEY_SIMPLEX

        # org
        org = (25, 40)

        # fontScale
        fontScale = 1

        # Blue color in BGR
        color = (0, 0, 0)

        # Line thickness of 2 px
        thickness = 1

        hours, minutes = current_time
        if current_time[0] < 10:
            hours = f'0{current_time[0]}'
        if current_time[1] < 10:
            minutes = f'0{current_time[1]}'

        # Using cv2.putText() method
        cv2.putText(self.image, f'Time is {hours}:{minutes}', org, font, fontScale, color, thickness, cv2.LINE_AA)


    def draw_hotspots(self, locs):

        for loc in locs:
            state = loc
            agent_centre = (int(state[0]) * self.magnification, int(state[1]) * self.magnification)
            agent_radius = 10
            agent_colour = (0, 0, 0)
            cv2.circle(self.image, agent_centre, agent_radius, agent_colour, 1)


    def display_demand(self, locs):
        for loc in locs:
            agent_centre = (int(loc[0]) * self.magnification, int(loc[1]) * self.magnification)
            agent_radius = 15
            agent_colour = (255, 0, 255)
            cv2.circle(self.image, agent_centre, agent_radius, agent_colour, 1)


            # Function to draw the environment and display it on the screen, if required
    def draw(self, time, locs, demand_centres=None, total_time=0):
        '''
        :param agents: all agents currently active
        '''

        # Create a white background
        self.image.fill(255)

        # self.image = cv2.imread('buda.jpg', 1)
        # self.image = cv2.resize(self.image, (500 * self.magnification, 500 * self.magnification), interpolation = cv2.INTER_AREA)
        # # Draw the obstacle
        # obstacle_left = int(self.magnification * self.obstacle_space[0, 0])
        # obstacle_top = int(self.magnification * (1 - self.obstacle_space[1, 1]))
        # obstacle_width = int(self.magnification * (self.obstacle_space[0, 1] - self.obstacle_space[0, 0]))
        # obstacle_height = int(self.magnification * (self.obstacle_space[1, 1] - self.obstacle_space[1, 0]))
        # obstacle_top_left = (obstacle_left, obstacle_top)
        # obstacle_bottom_right = (obstacle_left + obstacle_width, obstacle_top + obstacle_height)
        # cv2.rectangle(self.image, obstacle_top_left, obstacle_bottom_right, (150, 150, 150), thickness=cv2.FILLED)
        for agent in self.agents:

            # Draw the agent
            state = agent.get_int_state()
            agent_centre = (state[0] * self.magnification, state[1] * self.magnification)
            agent_radius = 2
            agent_colour = agent.get_colour()
            cv2.circle(self.image, agent_centre, agent_radius, agent_colour, cv2.FILLED)

            # Draw the destination
            if agent.status == 'Active':
                dest_centre = (agent.destination[0] * self.magnification, agent.destination[1] * self.magnification)
                dest_radius = 1
                dest_colour = (255, 0, 0)
                cv2.circle(self.image, dest_centre, dest_radius, dest_colour, cv2.FILLED)

            # # Draw a line path
            # initial_state = agent.get_int_initial_state()
            # cv2.line(self.image,
            #          (initial_state[0] * self.magnification, initial_state[1] * self.magnification),
            #          (state[0] * self.magnification, state[1] * self.magnification),
            #          (10, 250, 0),
            #          1, lineType=8)

        # print(self.image.shape)
        # self.overlay = self.image.copy()
        self.display_time(time)
        self.draw_hotspots(locs)

        if demand_centres is not None:
            self.display_demand(demand_centres)


        # Show the image
        cv2.imshow("Environment", self.image)

        # This line is necessary to give time for the image to be rendered on the screen
        cv2.waitKey(1)

        cv2.imwrite(f'./video/Frame_' + str(total_time).zfill(5) + '.png',
                    self.image)

        # self.cap.write(self.image.astype(np.uint8))

