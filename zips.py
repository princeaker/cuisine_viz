import json
import pandas as pd
import altair as alt

def createChart(data, name):
    color_expression    = "highlight._vgsid_==datum._vgsid_"
    color_condition     = alt.ConditionalPredicateValueDef(color_expression, "SteelBlue")
    highlight_selection = alt.selection_single(name="highlight", empty="all", on="mouseover")
    rating_selection    = alt.selection_single(name="rating", empty="all", encodings=['y'])
    maxCount            = int(data['total'].value_counts().max())

    barMean = alt.Chart() \
        .mark_bar(stroke="Black") \
        .encode(
            alt.X("total:Q", axis=alt.Axis(title="Total")),
            alt.Y('cuisine:O', axis=alt.Axis(title="{} Cuisine Name".format(name)),
                  sort=alt.SortField(field="total", op="mean", order='descending')),
            alt.ColorValue("LightGrey", condition=color_condition),
        ).properties(
            selection = highlight_selection+rating_selection,
        )


    return alt.hconcat(barMean,
        data=data,
        title="{} Cuisine Counts".format(name)
    )


def getData(z):
    import os
    cur_dir = os.path.dirname(__file__)
    #nyc_cuisines = json.load(open('nyc_restaurants_by_cuisine.json', 'r'))
    nyc_cuisines = json.load(open(os.path.join(cur_dir,'nyc_restaurants_by_cuisine.json'), 'r'))

    df = pd.DataFrame([(nyc_cuisines[i].get('cuisine'), nyc_cuisines[i].get('perZip').get(z))
                       for i in range(len(nyc_cuisines))],
                      columns=['cuisine', 'total'])
    df = df.dropna()
    return df