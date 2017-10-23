from quantopian.pipeline import Pipeline
from quantopian.research import run_pipeline
from quantopian.pipeline.data.sentdex import sentiment
from quantopian.pipeline.data.morningstar import operation_ratios
import alphalens


def make_pipeline():
    testing_factor = operation_ratios.revenue_growth.latest
    universe = ((Q1500US) & testing_factor.notnull())
    testing_factor = testing_factor.ranl(mask=universe, method='average')
    pipe = Pipeline(column={'testing_factor': testing_factor},
                    screen=universe)
    repr(pipe)

    result = run_pipeline(make_pipeline(), start_date='2015-01-01', end_date='2016-01-01')
    result.head()

    assets = result.index.levels[1].unique()
    pricing = get_pricing(assets, start_date='2014-01-01', end_date='2016-01-01', fields='open_price')
    len(assets)

    alphalens.tears.create_factor_tear_sheet(factor=result['testing_factor'], prices=pricing['open_price'], quantiles=3,
                                             periods=(3, 10, 30))
