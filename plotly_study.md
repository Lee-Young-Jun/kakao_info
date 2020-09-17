#대강 plotly를 사용하는 방법

    import pandas as pd
    import plotly.graph_objs as go
    from plotly.offline import plot #오프라인에서 사용할 수 있도록

    trace1 = {
        "x" : [1,2,3,...,n]
        "y" : [1,2,3,...,n]
        "uid" : "   "  #일단 사용안함
        "line" : {    #라인디자인을 위해
            "color" : "rgb(111,111,111)",
            "shape" : "spline"    #어떤 선이 모양을 쓸 것인지
        }
        "name" : "이 라인의 이름",
        "type" : "scatter",    #scatter 는 선 그래프

    #이렇게 여러개의 trace를 생성시키고

    data = Data([trace1,trace2, .... ] )

    layout = {    #그래프의 틀을 만들어주는 layout 이라고 생각
        "font" : {
            "size" : 12,
            "color" : "#444",    #바탕색??
            "family" : ???
        },
        "smith" : False,    #평탄화인듯
        "title" : "그래프의 제목",
        "width" : 725,    #너비
        "xaxis" : {
            "type" :
            "dtick" :
            "range" : [1970,2011],
        },
        "yaxis": {
        

        },


이런식으로 진행하면 된다고 생각.