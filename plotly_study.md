#�밭 plotly�� ����ϴ� ���

    import pandas as pd
    import plotly.graph_objs as go
    from plotly.offline import plot #�������ο��� ����� �� �ֵ���

    trace1 = {
        "x" : [1,2,3,...,n]
        "y" : [1,2,3,...,n]
        "uid" : "   "  #�ϴ� ������
        "line" : {    #���ε������� ����
            "color" : "rgb(111,111,111)",
            "shape" : "spline"    #� ���� ����� �� ������
        }
        "name" : "�� ������ �̸�",
        "type" : "scatter",    #scatter �� �� �׷���

    #�̷��� �������� trace�� ������Ű��

    data = Data([trace1,trace2, .... ] )

    layout = {    #�׷����� Ʋ�� ������ִ� layout �̶�� ����
        "font" : {
            "size" : 12,
            "color" : "#444",    #������??
            "family" : ???
        },
        "smith" : False,    #��źȭ�ε�
        "title" : "�׷����� ����",
        "width" : 725,    #�ʺ�
        "xaxis" : {
            "type" :
            "dtick" :
            "range" : [1970,2011],
        },
        "yaxis": {
        

        },


�̷������� �����ϸ� �ȴٰ� ����.