"""MC1-P2: Optimize a portfolio.  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
Atlanta, Georgia 30332  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
All Rights Reserved  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
Template code for CS 4646/7646  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
works, including solutions to the projects assigned in this course. Students  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
and other users of this template code are advised not to share it with others  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
or to make it available on publicly viewable websites including repositories  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
such as github and gitlab.  This copyright statement should not be removed  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
or edited.  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
We do grant permission to share solutions privately with non-students such  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
as potential employers. However, sharing with other current or future  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
GT honor code violation.  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
-----do not edit anything above this line---  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
Student Name: Tucker Balch (replace with your name)  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
GT User ID: tb34 (replace with your User ID)  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
GT ID: 900897987 (replace with your GT ID)  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
"""  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
import pandas as pd  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
import matplotlib.pyplot as plt  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
import numpy as np  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
import datetime as dt  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
from util import get_data, plot_data
from scipy.optimize import minimize  		  	   		     			  		 			 	 	 		 		 	 		 		 	 				  	 
  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
# This is the function that will be tested by the autograder  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
# The student must update this code to properly implement the functionality


def optimize_portfolio(sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 1, 1),syms=['GOOG', 'AAPL','GLD', 'XOM'], gen_plot=False):
    sv = 1.0
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)
    prices = prices_all[syms]
    prices_SPY = prices_all['SPY']
    
    stocks = prices
    log_ret = np.log(stocks/stocks.shift(1))
    
    def get_ret_vol_sr(weights): 
        weights = np.array(weights)
        ret = np.sum(log_ret.mean() * weights) * 252
        vol = np.sqrt(np.dot(weights.T, np.dot(log_ret.cov()*252, weights)))
        sr = ret / vol 
        return np.array([ret, vol, sr])
    
    def neg_sharpe(weights):
        return get_ret_vol_sr(weights)[2] * -1
    
    def check_sum(weights):
        return np.sum(weights) - 1
    
    cons = ({'type':'eq', 'fun':check_sum})
    bounds = [(0.0, 1.0) for i in stocks.columns]
    init_guess = np.asarray([1 / len(syms)] * len(syms))
    opt_results = minimize(neg_sharpe, init_guess, method='SLSQP', bounds=bounds, constraints=cons)
    allocs = opt_results.x
    sddr = opt_results.fun
    sr = get_ret_vol_sr(allocs)[2]
    
    normed = prices/prices.values[0]
    alloced = normed.multiply(allocs)
    pos_vals = alloced.multiply(sv)
    
    port_val = pos_vals.sum(axis=1)
    dr = (port_val / port_val.shift(1)) - 1
    cr = (port_val[-1] / port_val[0]) - 1
    adr = dr.mean()
    
    if gen_plot:
        port_val = port_val/port_val[0]
        prices_SPY = prices_SPY/prices_SPY[0]
        df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        plot_data(df_temp, title="Daily portfolio value and SPY")
    
    return allocs, cr, adr, sddr, sr
    	  	 
  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
def test_code():  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
    # This function WILL NOT be called by the auto grader  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
    # Do not assume that any variables defined here are available to your function/code  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
    # It is only here to help you set up and test your code  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
    # Define input parameters  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
    # Note that ALL of these values will be set to different values by  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
    # the autograder!  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
    start_date = dt.datetime(2009,1,1)  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
    end_date = dt.datetime(2010,1,1)  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
    symbols = ['GOOG', 'AAPL', 'GLD', 'XOM', 'IBM']  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
    # Assess the portfolio  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        gen_plot = False)  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
    # Print statistics  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
    print(f"Start Date: {start_date}")  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
    print(f"End Date: {end_date}")  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
    print(f"Symbols: {symbols}")  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
    print(f"Allocations:{allocations}")  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
    print(f"Sharpe Ratio: {sr}")  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
    print(f"Volatility (stdev of daily returns): {sddr}")  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
    print(f"Average Daily Return: {adr}")  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
    print(f"Cumulative Return: {cr}")  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
if __name__ == "__main__":  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
    # This code WILL NOT be called by the auto grader  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
    # Do not assume that it will be called  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
    test_code()  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
