from quantopian.pipeline import Pipeline
from quantopian.research import run_pipeline
from quantopian.pipeline.data.sentdex import sentiment
from quantopian.pipeline.data.morningstar import operation_ratios
import alphalens


def make_pipeline():
    testing_factor1 = operation_ratios.operation_margin.latest
    testing_factor2 = operation_ratios.revenue_growth.latest
    testing_factor3 = sentiment.sentiment_signal.latest

    universe = (Q1500US() &
                testing_factor1.notnull() &
                testing_factor2.notnull() &
                testing_factor3.notnull()
                )
    testing_factor1 = testing_factor1.ranl(mask=universe, method='average')
    testing_factor2 = testing_factor2.ranl(mask=universe, method='average')
    testing_factor3 = testing_factor3.ranl(mask=universe, method='average')
    testing_factor = testing_factor1 + testing_factor2 + testing_factor3
    testing_quantiles = testing_factor.quantiles(2)

    pipe = Pipeline(column={
        'testing_factor': testing_factor,
        'shorts': testing_quantiles.eq(0),
        'longs': testing_quantiles.eq(1)},
        screen=universe)
    repr(pipe)

    result = run_pipeline(make_pipeline(), start_date='2015-01-01', end_date='2016-01-01')
    result.head()

    assets = result.index.levels[1].unique()
    pricing = get_pricing(assets, start_date='2014-01-01', end_date='2016-01-01', fields='open_price')
    len(assets)

    alphalens.tears.create_factor_tear_sheet(factor=result['testing_factor'], prices=pricing['open_price'], quantiles=3,
                                             periods=(3, 10, 30))
