import math
import random
import numpy as np
from numpy.random import RandomState
import bpy

a = 1,2
b= 9,15
list(np.array(a)-np.array(b))

def calculate_action_probability(state):
  exponentiated_potential = np.exp(-theta[state[0]][state[1]])
  action_probability = 1/(exponentiated_potential+1)
  return action_probability
     

def transition(state, action_probability):
  rand = np.random.random()
  
  if state[0] > 19:
    action = 0
    action_probability = 1
  elif state[0] < 1:
    action = 1
    action_probability = 1
  else:
    if rand < action_probability:
      action = 1
      action_probability = action_probability
    else:
      action = 0
      action_probability = 1-action_probability
  return action, action_probability
     

def untrained_transition(state, action_probability):
  rand = np.random.random()
  z, pplus, pminus = dynamics(0.5, 5, 1)
  
  if state[0] > 19:
    action = 0
    action_probability = 1
  elif state[0] < 1:
    action = 1
    action_probability = 1
  else:
    if rand < pplus[state[0]]:
      action = 1
      action_probability = pplus[state[0]]
    else:
      action = 0
      action_probability = 1-pplus[state[0]]
  return action, action_probability
     

def update_state(state, action):
  state[0] += 2*action - 1
  state[1] += 1
  return state
     

def generate_reward(state):

   if state[1] == T:
     reward = -1*abs(state[0]-16)
   else:
     reward = 0

   return reward
     

def calculate_eligibility(state, action, action_probability):
  if action == 1:
    eligibility = 1 - action_probability
  else:
    eligibility = -action_probability
  return eligibility
     

def find_value(state):
  return value_table[state[0]][state[1]]
     

def update_value(state, next_state, reward, learning_rate_beta):
  past_value = find_value(state)
  current_value = find_value(next_state)
  td_error = current_value + reward - past_value
  value_table[state[0]][state[1]] += learning_rate_beta * td_error
  return value_table
     

def update_theta(state, next_state, reward, learning_rate, eligibility):
  past_value = find_value(state)
  current_value = find_value(next_state)
  td_error = current_value + reward - past_value
  theta[state[0]][state[1]] += learning_rate * td_error * eligibility
  return theta
     

def gaussian_derivative(x,sigma):
  Gaussian = -np.exp(-x**2/sigma**2)*x/(2*sigma**2)
  return Gaussian
     

def dynamics(a,zlim,sigma):
  N = 2*a
  z = np.arange(-zlim,zlim,(2*zlim)/21)
  f = gaussian_derivative(z,sigma)

  pminus = (-f+a)/N
  pplus = (f+a)/N

  pminus[0] = 0.0001
  pplus[0] = 1

  pminus[-1] = 1
  pplus[-1] = 0.0001

  return z, pminus, pplus
     

def kl_regularisation(state, action, action_probability):

  z, pminus, pplus = dynamics(0.5, 5, 0.75)
  
  if action == 1:
    prob = pplus[state[0]]
  else:
    prob = pminus[state[0]]
  #print(prob)

  return -math.log(action_probability/prob)

z, p1, p2 = dynamics(0.5, 5, 0.75)

T = 30
dimensions = (2*T+1,T+1)
theta = np.zeros(dimensions)
state = [0,0]
     

def generate_samples_untrained(N):
  trajectories = []
  average_return = 0
  for i in range(0, N):
    state = [0,0]
    trajectory = [state.copy()]
    trajectory_reward = 0
    for i in range (0,T):
      action_probability = calculate_action_probability(state.copy())
      action, action_probability = untrained_transition(state.copy(), action_probability)
      next_state = update_state(state.copy(), action)
      reward = generate_reward(next_state.copy())
      trajectory_reward += reward
      state = next_state
      trajectory.append(state.copy())
    trajectories.append(trajectory.copy())
    average_return += (trajectory_reward - average_return)/(i+1)
  return trajectories, average_return
     

untrained, avg = generate_samples_untrained(30)
     

min_y = np.min(np.array(untrained)[:,:,0]) - 1
max_y = np.max(np.array(untrained)[:,:,0]) + 1

T = 30
N = 10000
dimensions = (2*T+1,T+1)
theta = np.zeros(dimensions)
value_table = np.zeros(dimensions)
learning_rate = 0.01
learning_rate_beta = 0.6
return_learning_rate = 0.1
     

def actor_critic(N, avg):
  trajectories = []
  trajectory_rewards = [] #stores trajectory rewards
  running_average_return = [] #store running average return
  for i in range(0, N):
    state = [0,0]
    trajectory = [state.copy()]
    actions = []
    rewards = []
    eligibilities = []
    action_probabilities = []
    trajectory_reward = 0
    for i in range (0,T):
      action_probability = calculate_action_probability(state.copy())

      action, action_probability = transition(state.copy(), action_probability)
      actions.append(action) #store actions
      action_probabilities.append(action_probability) #store action probabilities

      eligibility = calculate_eligibility(state.copy(), action, action_probability)
      eligibilities.append(eligibility) #store eligibilities
      
      next_state = update_state(state.copy(), action)
  
      reward = generate_reward(next_state.copy())+ kl_regularisation(state, action, action_probability)
      rewards.append(reward) #store rewards

      trajectory_reward += reward 

      #update the value for past state
      update_value(state, next_state, reward, learning_rate_beta)

      #update theta
      update_theta(state, next_state, reward, learning_rate, eligibility)

      state = next_state #set next state as state
      trajectory.append(state.copy()) #add next state to trajectory

    trajectories.append(trajectory.copy()) #append trajectory to global list
    trajectory_rewards.append(trajectory_reward) # append reward for trajectory

    #average_return
    avg += return_learning_rate * (trajectory_reward - avg)
    running_average_return.append(avg)

  return trajectory_rewards, running_average_return
     

ac_rewards, ac_running_return = actor_critic(N, avg)

def generate_samples_trained(N):
  trajectories = []
  trajectory_rewards = []
  average_return = 0
  for i in range(0, N):
    state = [0,0,0]
    trajectory = [state.copy()]
    trajectory_reward = 0
    for i in range (0,T):
      action_probability = calculate_action_probability(state.copy())
      action, action_probability = transition(state.copy(), action_probability)
      next_state = update_state(state.copy(), action)
      reward = generate_reward(next_state.copy())
      trajectory_reward += reward
      state = next_state
      trajectory.append(state.copy())
    trajectories.append(trajectory.copy())
    trajectory_rewards.append(trajectory_reward)
    #average_return += (trajectory_reward - average_return)/(i+1)
    
  return trajectories, trajectory_rewards
     

sample, traj_rewards = generate_samples_trained(30)
     

min_y = - 1
max_y = 21

bpy.ops.mesh.primitive_uv_sphere_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(0.5, 0.5, 0.5))
bpy.ops.anim.keyframe_insert_by_name(type="LocRotScale")

for time in range(0,30):
    x = np.array(sample)[0,time,0].T
    bpy.data.scenes["Scene"].frame_set(2*time)
    sphere = bpy.data.objects["Sphere"]
    sphere.location = (x,0,0)
    bpy.ops.anim.keyframe_insert_by_name(type="LocRotScale")
