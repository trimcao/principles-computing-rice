"""
Cookie Simulator
Name: Tri Cao
Email: trimcao@gmail.com
Date: September 2015

### ONLY WORKS WITH CODESKULPTOR ###
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
#    total_cookies = 0.0
#    current_cookies = 0.0
#    time = 0.0
#    cps = 1.0
#    history = [(0.0, None, 0.0, 0.0)]    

    def __init__(self):
        self._total_cookies = 0.0
        self._current_cookies = 0.0
        self._time = 0.0
        self._cps = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]    
        
    def __str__(self):
        """
        Return human readable state
        """
        return "\nCurrent Time:    " + str(self.get_time()) + \
               "\nCurrent Cookies: " + str(self.get_cookies()) + \
               "\nCPS:             " + str(self.get_cps()) + \
               "\nTotal Cookies:   " + str(self._total_cookies) + "\n"
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if (cookies <= self._current_cookies):
            return 0.0
        else:
            return math.ceil((cookies - self._current_cookies) / self._cps)
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if (time <= 0.0):
            pass
        else:
            produce = time * self._cps
            self._current_cookies += produce
            self._total_cookies += produce
            self._time += time
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if (self._current_cookies >= cost):
            self._current_cookies -= cost
            self._cps += additional_cps
            event = (self.get_time(), item_name, cost, self._total_cookies)
            self._history.append(event)           
        else:
            pass


def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    build = build_info.clone()
    state = ClickerState()
    while (state.get_time() <= duration):
        #print state
        #check current time against duration?
        # use strategy to get the next item to buy
        item_to_buy = strategy(state.get_cookies(), state.get_cps(), 
                               state.get_history(), duration - state.get_time(),
                               build)
        if item_to_buy == None:
            break
        else:
            #print state.get_cookies()
            time_needed = state.time_until(build.get_cost(item_to_buy))
            #print time_needed
            if ((state.get_time() + time_needed) > duration):
                break
            else:
                #print True
                state.wait(time_needed)
                #print "Current Cookies: ", state.get_cookies()
                #print "Cost: ", build.get_cost(item_to_buy)
                state.buy_item(item_to_buy, build.get_cost(item_to_buy), build.get_cps(item_to_buy))
                build.update_item(item_to_buy)
    
    # Check if there is still time left
    if (state.get_time() < duration):
        state.wait(duration - state.get_time())
        
    # Replace with your code
    return state


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    afford = affordable(cookies, cps, time_left, build_info)
    if (len(afford) > 0):
        return cheapest_item(afford, build_info)
    else:   
        return None

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    afford = affordable(cookies, cps, time_left, build_info)
    if (len(afford) > 0):
        return most_expensive_item(afford, build_info)
    else:   
        return None

def strategy_best_2(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    buy_item = strategy_best_helper_2(cookies, cps, history, time_left, build_info, BUY_LIST_BEST)
    return buy_item

def strategy_best_helper_2(cookies, cps, history, time_left, build_info, buy_list):
    """
    Helper method for strategy_best
    """
    if (len(buy_list) > 0):
        next_item = buy_list[0]
        
        # check if we can afford the item
        if ((cookies + cps * time_left) > build_info.get_cost(next_item)):
            buy_list.pop(0)
            return next_item
        else:
            return None
    else:
        return strategy_cheap(cookies, cps, history, time_left, build_info)

def strategy_best_3(cookies, cps, history, time_left, build_info):    
    """
    The Best Strategy to date
    """
    buy_item = strategy_best_helper(cookies, cps, history, time_left, build_info, BUY_LIST_ORIGINAL)
    return buy_item    

def strategy_best_helper_3(cookies, cps, history, time_left, build_info, buy_list):
    """
    Helper method: Buy the cheapest until it is not the cheapest anymore,
    then never buy it again
    """
    afford = affordable_list(cookies, cps, time_left, build_info, buy_list)
    
    if (len(afford) > 1):
        cheapest = cheapest_item(afford, build_info)    
        # Compare the cheapest item with the first item in the buy_list
        if (cheapest == buy_list[0]):
            # start checking for efficiency
            next_expensive = buy_list[1]
            cps_eff = build_info.get_cps(next_expensive) / build_info.get_cps(cheapest)
            cost_eff = build_info.get_cost(next_expensive) / build_info.get_cost(cheapest)
            # if the cost efficiency is no longer as good as cps_efficiency, remove it
            if (cost_eff < cps_eff):
                buy_list.pop(0)
        #print buy_list
        #print cheapest
        #print build_info.get_cost(cheapest)
        return cheapest
    elif (len(afford) == 1):
        #print afford[0]
        #print build_info.get_cost(afford[0])
        return afford[0]
    else:
        return None
        #return strategy_expensive(cookies, cps, history, time_left, build_info)

def strategy_best(cookies, cps, history, time_left, build_info):    
    afford = affordable(cookies, cps, time_left, build_info)
    if (len(afford) > 0):
        buy_item = most_efficient(afford, build_info)
        return buy_item
    else:
        return None
        
def most_efficient(items, build_info):
    """
    Determine the most efficient item to buy at a given moment
    """
    sum_eff_list = []

    for each_item in items:
        sum_eff = 0
        for another in items:
            if (each_item != another):
                cost_eff = build_info.get_cost(each_item) / build_info.get_cost(another)
                cps_eff = build_info.get_cps(each_item) / build_info.get_cps(another)
                eff_factor = cps_eff / cost_eff
                sum_eff += eff_factor
        sum_eff_list.append((each_item, sum_eff))
    # find the item with the maximum efficiency
    max_efficiency = -1
    max_item = ""
    for item in sum_eff_list:
        if (item[1] > max_efficiency):
            max_efficiency = item[1]
            max_item = item[0]
    return max_item
             
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state
    #print buy_list_original

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    #history = state.get_history()
    #history = [(item[0], item[3]) for item in history]
    #simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def cheapest_item(items, build_info):
    """
    Find the cheapest item in a list of items
    """
    # set min_cost to a good arbitrary value
    min_cost = float("inf")
    min_item = ""
    for item in items:
        if (build_info.get_cost(item) < min_cost):
            min_cost = build_info.get_cost(item)
            min_item = item
    return min_item

def most_expensive_item(items, build_info):
    """
    Find the most expensive item in a list of items
    """
    # set max_cost to a good arbitrary value
    max_cost = -1.0
    max_item = ""
    for item in items:
        if (build_info.get_cost(item) > max_cost):
            max_cost = build_info.get_cost(item)
            max_item = item
    return max_item

def affordable(cookies, cps, time_left, build_info):
    """
    Return a list of items that are affordable
    """
    total_possible = cookies + cps * time_left
    afford = []
    for item in build_info.build_items():
        if (build_info.get_cost(item) <= total_possible):
            afford.append(item)
    return afford

def affordable_list(cookies, cps, time_left, build_info, buy_list):
    """
    Return a list of affordable items from a list (not from build_info)
    """
    total_possible = cookies + cps * time_left
    afford = []
    for item in buy_list:
        if (build_info.get_cost(item) <= total_possible):
            afford.append(item)
    return afford    

def gen_buy_list(build_info, n_times):
    """
    Generate a buying list sorted by cost.
    Each item will appear n times.
    """
    # Generate a list of tuples of items
    first_list = []
    costs = []
    items = build_info.build_items()
    for item in items:
        costs.append(build_info.get_cost(item))
    
    for idx in range(len(items)):
        first_list.append((items[idx], costs[idx]))
    
    # Sort the first_list based on cost
    first_list = sorted(first_list, key=lambda x: x[1])
    
    # Generate the final list 
    final_list = []
    for item in first_list:
        for dummy_idx in range(n_times):
            final_list.append(item[0])
    
    return final_list
      

def run():
    """
    Run the simulator.
    """    
    #run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    #run_strategy("Cheap", SIM_TIME, strategy_cheap)
    #run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    #run_strategy("Best - 2", SIM_TIME, strategy_best_2)

BUILD_ORIGINAL = provided.BuildInfo()
BUY_LIST_BEST = gen_buy_list(BUILD_ORIGINAL, 90)
BUY_LIST_ORIGINAL = gen_buy_list(BUILD_ORIGINAL, 1)
    
#run()

#test = ClickerState()
#print test
#print math.ceil((6.0 - 1.0) / 2.0)

        
# test time_until()
#state = ClickerState()
#build = provided.BuildInfo()
#print build.get_cost("Cursor")
#time_needed = state.time_until(build.get_cost("Cursor") - state.get_cookies())
#print time_needed
#print build.get_cps("Cursor")
#print build.build_items()
#print cheapest_item(build)
#afford = affordable(1000, 2.0, 10000, build)
#print afford
#print most_expensive_item(afford, build)

#print gen_buy_list(build, 2)
#print build.get_cost('Antimatter Condenser')
#print build.get_cost('Time Machine')

# test helper method
#build = provided.BuildInfo()
#buy_list = gen_buy_list(build, 1)
#buy_list.pop(0)
#print strategy_best_helper(10000000, 1, [], 100, build, buy_list)
#build.update_item('Grandma')

#for item in build.build_items():
#    print item + ": " + str(build.get_cps(item))
#    print item + ": " + str(build.get_cost(item))

#print most_efficient(build.build_items(), build)

#def owl_test():
#    """ Test method for Owl Test
#    """
#    obj = ClickerState()
#    obj.wait(78.0)
#    obj.buy_item('item', 1.0, 1.0)
#    print obj.get_history()
#    
#    another = ClickerState()
#    print another.get_history()
#
#owl_test()
    
    
