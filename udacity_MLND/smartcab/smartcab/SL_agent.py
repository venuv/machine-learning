import random
import math
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """ An agent that learns to drive in the Smartcab world.
        This is the object you will be modifying. """ 

    def __init__(self, env, learning=False, epsilon=1.0, alpha=0.5):
        super(LearningAgent, self).__init__(env)     # Set the agent in the evironment 
        self.planner = RoutePlanner(self.env, self)  # Create a route planner
        self.valid_actions = self.env.valid_actions  # The set of valid actions

        # Set parameters of the learning agent
        self.learning = learning # Whether the agent is expected to learn
        self.Q = dict()          # Create a Q-table which will be a dictionary of tuples
        self.epsilon = epsilon   # Random exploration factor
        self.alpha = alpha       # Learning factor

        ###########
        ## TO DO ##
        ###########
        # Set any additional class parameters as needed
        self.total_trials = 0
        
        #waypoints = ['forward', 'left', 'right']
        #lights = ['red', 'green']
        #oncomings = [None, 'forward', 'left', 'right']
        #for x in waypoints:
        #    for y in lights:
        #        for z in oncomings:
        #            self.Q[x, y, z] = {'left':0, 'right':0, 'forward':0, 'none':0}


    def reset(self, destination=None, testing=False):
        """ The reset function is called at the beginning of each trial.
            'testing' is set to True if testing trials are being used
            once training trials have completed. """

        # Select the destination as the new location to route to
        self.planner.route_to(destination)
        
        ########### 
        ## TO DO ##
        ###########
        # Update epsilon using a decay function of your choice
        # Update additional class parameters as needed
        # If 'testing' is True, set epsilon and alpha to 0
        
        #self.tolerance = 0.05
        ########### 
        ## TO DO ##
        ###########
        # Update epsilon using a decay function of your choice
        self.total_trials += 1
        self.a = 0.025
        #self.epsilon = 1-(0.05*self.total_trials)
        #self.epsilon = float(1)/float((self.total_trials)**2)
        #self.epsilon = float(self.alpha)**float(self.total_trials)
        #self.epsilon = float(math.cos(self.alpha*self.total_trials))
        #self.epsilon = float(1)/math.exp(float(self.alpha*self.total_trials))
        
        #if self.epsilon < 0:
        #    self.epsilon = 0
        #else:
        #    self.epsilon = 1-(0.05*self.total_trials)
        # Update additional class parameters as needed
        # If 'testing' is True, set epsilon and alpha to 0
        
        if testing is True: #self.epsilon < self.tolerance: # i.e. testing is true
            self.epsilon = 0
            self.alpha = 0
        else :
            #self.epsilon = 1-(0.01*self.total_trials)
            self.epsilon = 1- float(1)/math.exp(float(self.a*self.total_trials))
                
                
        #else :
        #    if self.total_trials < 101:
        #        self.epsilon = 1
        #    else:
        #        self.epsilon = 0

        return None

    def build_state(self):
        """ The build_state function is called when the agent requests data from the 
            environment. The next waypoint, the intersection inputs, and the deadline 
            are all features available to the agent. """

        # Collect data about the environment
        waypoint = self.planner.next_waypoint() # The next waypoint 
        inputs = self.env.sense(self)           # Visual input - intersection light and traffic
        deadline = self.env.get_deadline(self)  # Remaining deadline

        ########### 
        ## TO DO ##
        ###########
        # Set 'state' as a tuple of relevant data for the agent
        # When learning, check if the state is in the Q-table
        #   If it is not, create a dictionary in the Q-table for the current 'state'
        #   For each action, set the Q-value for the state-action pair to 0
        
        #state = None
        
        light = inputs['light']
        oncoming = inputs['oncoming']  
        left = inputs['left']
        #right = inputs['right']
        #state = (waypoint, light, oncoming)
        #state = (waypoint, light, oncoming, left, right)
        state = (waypoint, light, oncoming, left)
        
        return state


    def get_maxQ(self, state):
        """ The get_max_Q function is called when the agent is asked to find the
            maximum Q-value of all actions based on the 'state' the smartcab is in. """

        ########### 
        ## TO DO ##
        ###########
        # Calculate the maximum Q-value of all actions for a given state

        maxQ_key = max(self.Q[self.state], key=(lambda key: self.Q[self.state][key]))
        maxQ = self.Q[self.state][maxQ_key]
        
        return maxQ 


    def createQ(self, state):
        """ The createQ function is called when a state is generated by the agent. """

        ########### 
        ## TO DO ##
        ###########
        # When learning, check if the 'state' is not in the Q-table
        # If it is not, create a new dictionary for that state
        #   Then, for each action available, set the initial Q-value to 0.0
        
        if self.learning is True:
            if state not in self.Q.keys():
                self.Q[state] = {'left':0, 'right':0, 'forward':0, None:0}

        return


    def choose_action(self, state):
        """ The choose_action function is called when the agent is asked to choose
            which action to take, based on the 'state' the smartcab is in. """

        # Set the agent state and default action
        self.state = state
        self.next_waypoint = self.planner.next_waypoint()
        #action = None

        ########### 
        ## TO DO ##
        ###########
        # When not learning, choose a random action
        # When learning, choose a random action with 'epsilon' probability
        #   Otherwise, choose an action with the highest Q-value for the current state
        
        #from random import randint, uniform
        #random_number = randint(0,3)
        #action = self.valid_actions[random_number]
        p_random = random.uniform(0, 1)
        #maxQ = self.get_maxQ(state)
        
        #if self.learning is False:
        #    action = random.choice(self.valid_actions)
        
       
        if self.learning is True:
            if p_random <= 1-self.epsilon: #(1-epsilon probability choose random)
                
                maxQ_key = max(self.Q[self.state], key=(lambda key: self.Q[self.state][key]))
                maxQ_value = self.Q[self.state][maxQ_key]
                
                # forming new dictionary to store actions with the same highQ value
                top_actions = dict()

                # forming dictionary for current state so I can iterate through the action/rewards to find those that contain the highest
                # max q value and then append them to top_actions dictionary
                state_dict = self.Q[self.state]
                for action, reward in state_dict.iteritems():
                    if reward == maxQ_value:
                        top_actions[action] = reward 
                        
                action = random.choice(top_actions.keys()) # randomly select from multiple actions if they have the same max q value.
            else:
                action = random.choice(self.valid_actions)
                
        elif self.learning is False:
            action = random.choice(self.valid_actions)
 
        return action


    def learn(self, state, action, reward):
        """ The learn function is called after the agent completes an action and
            receives an award. This function does not consider future rewards 
            when conducting learning. """

        ########### 
        ## TO DO ##
        ###########
        # When learning, implement the value iteration update rule
        #   Use only the learning rate 'alpha' (do not use the discount factor 'gamma')
        
        ## get the next state,action Q(s',a')  
        #next_waypoint = self.planner.next_waypoint()  
        #next_inputs = self.env.sense(self)           
        #next_light = next_inputs['light']
        #next_oncoming = next_inputs['oncoming']    
        #next_left = next_inputs['left']
        #next_right = next_inputs['right']
        #next_state = (next_waypoint, next_light, next_oncoming, next_left, next_right)
        
        #self.Q[self.state][action] = (1-self.alpha)*self.Q[self.state][action] + self.alpha*(reward + self.gamma*self.Q[next_state][maxQ])
        self.Q[self.state][action] = (1-self.alpha)*self.Q[self.state][action] + self.alpha*(reward)
                
        return


    def update(self):
        """ The update function is called when a time step is completed in the 
            environment for a given trial. This function will build the agent
            state, choose an action, receive a reward, and learn if enabled. """

        state = self.build_state()          # Get current state
        self.createQ(state)                 # Create 'state' in Q-table
        action = self.choose_action(state)  # Choose an action
        reward = self.env.act(self, action) # Receive a reward
        self.learn(state, action, reward)   # Q-learn

        return
        

def run():
    """ Driving function for running the simulation. 
        Press ESC to close the simulation, or [SPACE] to pause the simulation. """

    ##############
    # Create the environment
    # Flags:
    #   verbose     - set to True to display additional output from the simulation
    #   num_dummies - discrete number of dummy agents in the environment, default is 100
    #   grid_size   - discrete number of intersections (columns, rows), default is (8, 6)
    #env = Environment(verbose=True)
    env = Environment()

    ##############
    # Create the driving agent
    # Flags:
    #   learning   - set to True to force the driving agent to use Q-learning
    #    * epsilon - continuous value for the exploration factor, default is 1
    #    * alpha   - continuous value for the learning rate, default is 0.5
    #agent = env.create_agent(LearningAgent, learning=True)
    agent = env.create_agent(LearningAgent, learning=True, alpha=0.33)
    
    ##############
    # Follow the driving agent
    # Flags:
    #   enforce_deadline - set to True to enforce a deadline metric
    env.set_primary_agent(agent, enforce_deadline=True)

    ##############
    # Create the simulation
    # Flags:
    #   update_delay - continuous time (in seconds) between actions, default is 2.0 seconds
    #   display      - set to False to disable the GUI if PyGame is enabled
    #   log_metrics  - set to True to log trial and simulation results to /logs
    #   optimized    - set to True to change the default log file name
    #sim = Simulator(env, update_delay=0.001, log_metrics=True)
    sim = Simulator(env, update_delay=0.001, log_metrics=True, optimized=True)
    
    
    ##############
    # Run the simulator
    # Flags:
    #   tolerance  - epsilon tolerance before beginning testing, default is 0.05 
    #   n_test     - discrete number of testing trials to perform, default is 0
    #sim.run(n_test=10)
    sim.run(n_test=100, tolerance=0.01)
    
if __name__ == '__main__':
    run()
