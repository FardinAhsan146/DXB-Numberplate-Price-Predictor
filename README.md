# Predicting the price of license plates using ML and non ML methods

The price of license plates in Dubai follow a pattern. The less number of digits it has and the less number of unique digits it has the higher in price it tends to be.

The end goal is to create a function `predict_pricce(num: str) -> int` that can accept a license plate and return its predicted price.

So far I am testing with Xtreme Gradient Boosting as the ML algorithm and a Levenshtein distance function as a non ML reference point to see what kind of performance to expect. 
