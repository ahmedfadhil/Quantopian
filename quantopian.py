from quantopian.pipeline import Pipeline
from quantopian.research import run_pipeline
import blaz
from quantopian.interactive.data.sentdex import sentiment
from quantopian.pipeline.data.sentdex import sentiment
from quantopian.pipeline.filters.morningstar import Q1500US
import alphalens
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import pandas as pd

from . import plotting
from . import performance as perf
from . import utils

def make_pipeline():
    sentiment_factor = sentiment.sentiment_signal.last
    universe = (Q1500US()&sentiment_factor.not_null())
    pipe = Pipeline(columns={'sentiment':sentiment_factor,
                             'longs':(sentiment_factor>=4),
                             'shorts':(sentiment_factor<=-2)},
                             screen = universe)
    return pipe
result = run_pipeline(make_pipeline(),start_date = '2015-05-05',end_date = '2016-05-05')
type(result)

result.head()
len(result)

assets = result.index.levels[1].unique()
len(assets)

pricing = =get_pricing(assets,start_date = '2014-05-05',end_date = '2016-05-05',fields = 'open_price')

alphalens.tears.create_factor_tear_sheet(factor = result['sentiment'],
prices =pricing,
quantiles = 2,
periods = (1,5,10))