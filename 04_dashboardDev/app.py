import dash
import copy
from dash import Dash, dcc, html, Input, Output, ClientsideFunction
import plotly.graph_objects as go
import plotly.express as px
import dash_daq as daq
import pandas as pd
import geopandas as gpd
import shapely.geometry
import numpy as np
from pandas.api.types import CategoricalDtype
from textwrap import dedent
from PIL import Image


app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "中国篆刻，方寸之间大天地"

server = app.server
app.config.suppress_callback_exceptions = True


# #########################################
# #######  read the orginal data  #########
# #########################################

classify = pd.read_csv(f"../03_LabelProcessing/classification.csv",index_col=0)

classify_list = ['作者', '图画印', '边款', '边框', '印文字数', '印形', '印文', '印面内容']


# #################################################
# #########  generate dashboard card  #############
# #################################################


def classify_button():
    """
    https://dash.plotly.com/dash-html-components/button
    """
    return html.Div(
        id="classify_button_card",
        className = "classify_button_card",
        children=[
            html.H2("Commuting Scenario"),
            html.P("1. 选择主轴"),
            dcc.RadioItems(
                id='main_axis',
                className="dcc_control",
                options=[
                    {'label': classify_list[0], 'value': classify_list[0]},
                    {'label': classify_list[1], 'value': classify_list[1]},
                    {'label': classify_list[2], 'value': classify_list[2]},
                    {'label': classify_list[3], 'value': classify_list[3]},
                    {'label': classify_list[4], 'value': classify_list[4]},
                    {'label': classify_list[5], 'value': classify_list[5]},
                    {'label': classify_list[6], 'value': classify_list[6]},
                    {'label': classify_list[7], 'value': classify_list[7]},                   
                ],
                value="印文字数",
                labelStyle={'display': 'block'}
            ),
            html.P("2. 选择副轴"),
            dcc.RadioItems(
                id='sub_axis',
                className="dcc_control",
                options=[
                    {'label': classify_list[0], 'value': classify_list[0]},
                    {'label': classify_list[1], 'value': classify_list[1]},
                    {'label': classify_list[2], 'value': classify_list[2]},
                    {'label': classify_list[3], 'value': classify_list[3]},
                    {'label': classify_list[4], 'value': classify_list[4]},
                    {'label': classify_list[5], 'value': classify_list[5]},
                    {'label': classify_list[6], 'value': classify_list[6]},
                    {'label': classify_list[7], 'value': classify_list[7]},  
                ],
                value="印文",
                labelStyle={'display': 'block'}
            ),
        ],
    )

def classify_dropdown():
    """
    https://dash.plotly.com/dash-core-components/dropdown
    """
    return html.Div(
        id="classify_dropdown_card",
        className = "classify_dropdown_card",
        children=[
            html.H2("Commuting Scenario"),
            html.P("1. 选择主轴"),
            dcc.Dropdown(
                id='main_options',
                className="dcc_control",
            ),
            html.P("2. 选择副轴"),
            dcc.Dropdown(
                id='sub_options',
                className="dcc_control",
            ),
        ],
    )


def seal_num():
    return html.Div(
                    className="seal_num",
                    children=[
                        html.Div(
                            [
                                html.P("可选印章数量"), 
                                html.H3(id="seal_num_text"), 
                                html.P("3. 选择印章"),
                                dcc.Dropdown(
                                    id='img_options',
                                    options=[872,4253,4354,6,24],
                                    value=872,
                                    className="dcc_control",
                                ),     
                            ],
                            className="mini_container",
                        )
                    ],
                )


# #################################################
# #################    layout   ###################
# #################################################

app.layout = html.Div([
    classify_button(),
    classify_dropdown(),
    seal_num(),
    dcc.Graph(id="classify_graphic", config={"displayModeBar": False}),
    dcc.Graph(id="share_graphic", config={"displayModeBar": False}),
    dcc.Graph(id="img", config={"displayModeBar": False, 'doubleClick': 'reset'}),
    dcc.Graph(id="info_table", config={"displayModeBar": False}),
        ], 
        className="app_container"
    )


# #################################################
# ################    callback   ##################
# #################################################

@app.callback(
    Output('sub_axis', 'options'),
    Input('main_axis', 'value')
    )
def disable_options(main_axis):
    if main_axis==classify_list[0]:
        return [
                    {'label': classify_list[0], 'value': classify_list[0], 'disabled': True},
                    {'label': classify_list[1], 'value': classify_list[1], 'disabled': False},
                    {'label': classify_list[2], 'value': classify_list[2], 'disabled': False},
                    {'label': classify_list[3], 'value': classify_list[3], 'disabled': False},
                    {'label': classify_list[4], 'value': classify_list[4], 'disabled': False},
                    {'label': classify_list[5], 'value': classify_list[5], 'disabled': False},
                    {'label': classify_list[6], 'value': classify_list[6], 'disabled': False},
                    {'label': classify_list[7], 'value': classify_list[7], 'disabled': False},  
                ]
    if main_axis==classify_list[1]:
        return [
                    {'label': classify_list[0], 'value': classify_list[0], 'disabled': False},
                    {'label': classify_list[1], 'value': classify_list[1], 'disabled': True},
                    {'label': classify_list[2], 'value': classify_list[2], 'disabled': False},
                    {'label': classify_list[3], 'value': classify_list[3], 'disabled': False},
                    {'label': classify_list[4], 'value': classify_list[4], 'disabled': False},
                    {'label': classify_list[5], 'value': classify_list[5], 'disabled': False},
                    {'label': classify_list[6], 'value': classify_list[6], 'disabled': False},
                    {'label': classify_list[7], 'value': classify_list[7], 'disabled': False},  
                ]
    if main_axis==classify_list[2]:
        return [
                    {'label': classify_list[0], 'value': classify_list[0], 'disabled': False},
                    {'label': classify_list[1], 'value': classify_list[1], 'disabled': False},
                    {'label': classify_list[2], 'value': classify_list[2], 'disabled': True},
                    {'label': classify_list[3], 'value': classify_list[3], 'disabled': False},
                    {'label': classify_list[4], 'value': classify_list[4], 'disabled': False},
                    {'label': classify_list[5], 'value': classify_list[5], 'disabled': False},
                    {'label': classify_list[6], 'value': classify_list[6], 'disabled': False},
                    {'label': classify_list[7], 'value': classify_list[7], 'disabled': False},  
                ]                
    if main_axis==classify_list[3]:
        return [
                    {'label': classify_list[0], 'value': classify_list[0], 'disabled': False},
                    {'label': classify_list[1], 'value': classify_list[1], 'disabled': False},
                    {'label': classify_list[2], 'value': classify_list[2], 'disabled': False},
                    {'label': classify_list[3], 'value': classify_list[3], 'disabled': True},
                    {'label': classify_list[4], 'value': classify_list[4], 'disabled': False},
                    {'label': classify_list[5], 'value': classify_list[5], 'disabled': False},
                    {'label': classify_list[6], 'value': classify_list[6], 'disabled': False},
                    {'label': classify_list[7], 'value': classify_list[7], 'disabled': False},  
                ]
    if main_axis==classify_list[4]:
        return [
                    {'label': classify_list[0], 'value': classify_list[0], 'disabled': False},
                    {'label': classify_list[1], 'value': classify_list[1], 'disabled': False},
                    {'label': classify_list[2], 'value': classify_list[2], 'disabled': False},
                    {'label': classify_list[3], 'value': classify_list[3], 'disabled': False},
                    {'label': classify_list[4], 'value': classify_list[4], 'disabled': True},
                    {'label': classify_list[5], 'value': classify_list[5], 'disabled': False},
                    {'label': classify_list[6], 'value': classify_list[6], 'disabled': False},
                    {'label': classify_list[7], 'value': classify_list[7], 'disabled': False},  
                ]
    if main_axis==classify_list[5]:
        return [
                    {'label': classify_list[0], 'value': classify_list[0], 'disabled': False},
                    {'label': classify_list[1], 'value': classify_list[1], 'disabled': False},
                    {'label': classify_list[2], 'value': classify_list[2], 'disabled': False},
                    {'label': classify_list[3], 'value': classify_list[3], 'disabled': False},
                    {'label': classify_list[4], 'value': classify_list[4], 'disabled': False},
                    {'label': classify_list[5], 'value': classify_list[5], 'disabled': True},
                    {'label': classify_list[6], 'value': classify_list[6], 'disabled': False},
                    {'label': classify_list[7], 'value': classify_list[7], 'disabled': False},  
                ]
    if main_axis==classify_list[6]:
        return [
                    {'label': classify_list[0], 'value': classify_list[0], 'disabled': False},
                    {'label': classify_list[1], 'value': classify_list[1], 'disabled': False},
                    {'label': classify_list[2], 'value': classify_list[2], 'disabled': False},
                    {'label': classify_list[3], 'value': classify_list[3], 'disabled': False},
                    {'label': classify_list[4], 'value': classify_list[4], 'disabled': False},
                    {'label': classify_list[5], 'value': classify_list[5], 'disabled': False},
                    {'label': classify_list[6], 'value': classify_list[6], 'disabled': True},
                    {'label': classify_list[7], 'value': classify_list[7], 'disabled': False},  
                ]
    if main_axis==classify_list[7]:
        return [
                    {'label': classify_list[0], 'value': classify_list[0], 'disabled': False},
                    {'label': classify_list[1], 'value': classify_list[1], 'disabled': False},
                    {'label': classify_list[2], 'value': classify_list[2], 'disabled': False},
                    {'label': classify_list[3], 'value': classify_list[3], 'disabled': False},
                    {'label': classify_list[4], 'value': classify_list[4], 'disabled': False},
                    {'label': classify_list[5], 'value': classify_list[5], 'disabled': False},
                    {'label': classify_list[6], 'value': classify_list[6], 'disabled': False},
                    {'label': classify_list[7], 'value': classify_list[7], 'disabled': True},  
                ]


@app.callback(
    Output('main_axis', 'options'),
    Input('sub_axis', 'value')
    )
def disable_options(sub_axis):
    if sub_axis==classify_list[0]:
        return [
                    {'label': classify_list[0], 'value': classify_list[0], 'disabled': True},
                    {'label': classify_list[1], 'value': classify_list[1], 'disabled': False},
                    {'label': classify_list[2], 'value': classify_list[2], 'disabled': False},
                    {'label': classify_list[3], 'value': classify_list[3], 'disabled': False},
                    {'label': classify_list[4], 'value': classify_list[4], 'disabled': False},
                    {'label': classify_list[5], 'value': classify_list[5], 'disabled': False},
                    {'label': classify_list[6], 'value': classify_list[6], 'disabled': False},
                    {'label': classify_list[7], 'value': classify_list[7], 'disabled': False},  
                ]
    if sub_axis==classify_list[1]:
        return [
                    {'label': classify_list[0], 'value': classify_list[0], 'disabled': False},
                    {'label': classify_list[1], 'value': classify_list[1], 'disabled': True},
                    {'label': classify_list[2], 'value': classify_list[2], 'disabled': False},
                    {'label': classify_list[3], 'value': classify_list[3], 'disabled': False},
                    {'label': classify_list[4], 'value': classify_list[4], 'disabled': False},
                    {'label': classify_list[5], 'value': classify_list[5], 'disabled': False},
                    {'label': classify_list[6], 'value': classify_list[6], 'disabled': False},
                    {'label': classify_list[7], 'value': classify_list[7], 'disabled': False},  
                ]
    if sub_axis==classify_list[2]:
        return [
                    {'label': classify_list[0], 'value': classify_list[0], 'disabled': False},
                    {'label': classify_list[1], 'value': classify_list[1], 'disabled': False},
                    {'label': classify_list[2], 'value': classify_list[2], 'disabled': True},
                    {'label': classify_list[3], 'value': classify_list[3], 'disabled': False},
                    {'label': classify_list[4], 'value': classify_list[4], 'disabled': False},
                    {'label': classify_list[5], 'value': classify_list[5], 'disabled': False},
                    {'label': classify_list[6], 'value': classify_list[6], 'disabled': False},
                    {'label': classify_list[7], 'value': classify_list[7], 'disabled': False},  
                ]                
    if sub_axis==classify_list[3]:
        return [
                    {'label': classify_list[0], 'value': classify_list[0], 'disabled': False},
                    {'label': classify_list[1], 'value': classify_list[1], 'disabled': False},
                    {'label': classify_list[2], 'value': classify_list[2], 'disabled': False},
                    {'label': classify_list[3], 'value': classify_list[3], 'disabled': True},
                    {'label': classify_list[4], 'value': classify_list[4], 'disabled': False},
                    {'label': classify_list[5], 'value': classify_list[5], 'disabled': False},
                    {'label': classify_list[6], 'value': classify_list[6], 'disabled': False},
                    {'label': classify_list[7], 'value': classify_list[7], 'disabled': False},  
                ]
    if sub_axis==classify_list[4]:
        return [
                    {'label': classify_list[0], 'value': classify_list[0], 'disabled': False},
                    {'label': classify_list[1], 'value': classify_list[1], 'disabled': False},
                    {'label': classify_list[2], 'value': classify_list[2], 'disabled': False},
                    {'label': classify_list[3], 'value': classify_list[3], 'disabled': False},
                    {'label': classify_list[4], 'value': classify_list[4], 'disabled': True},
                    {'label': classify_list[5], 'value': classify_list[5], 'disabled': False},
                    {'label': classify_list[6], 'value': classify_list[6], 'disabled': False},
                    {'label': classify_list[7], 'value': classify_list[7], 'disabled': False},  
                ]
    if sub_axis==classify_list[5]:
        return [
                    {'label': classify_list[0], 'value': classify_list[0], 'disabled': False},
                    {'label': classify_list[1], 'value': classify_list[1], 'disabled': False},
                    {'label': classify_list[2], 'value': classify_list[2], 'disabled': False},
                    {'label': classify_list[3], 'value': classify_list[3], 'disabled': False},
                    {'label': classify_list[4], 'value': classify_list[4], 'disabled': False},
                    {'label': classify_list[5], 'value': classify_list[5], 'disabled': True},
                    {'label': classify_list[6], 'value': classify_list[6], 'disabled': False},
                    {'label': classify_list[7], 'value': classify_list[7], 'disabled': False},  
                ]
    if sub_axis==classify_list[6]:
        return [
                    {'label': classify_list[0], 'value': classify_list[0], 'disabled': False},
                    {'label': classify_list[1], 'value': classify_list[1], 'disabled': False},
                    {'label': classify_list[2], 'value': classify_list[2], 'disabled': False},
                    {'label': classify_list[3], 'value': classify_list[3], 'disabled': False},
                    {'label': classify_list[4], 'value': classify_list[4], 'disabled': False},
                    {'label': classify_list[5], 'value': classify_list[5], 'disabled': False},
                    {'label': classify_list[6], 'value': classify_list[6], 'disabled': True},
                    {'label': classify_list[7], 'value': classify_list[7], 'disabled': False},  
                ]
    if sub_axis==classify_list[7]:
        return [
                    {'label': classify_list[0], 'value': classify_list[0], 'disabled': False},
                    {'label': classify_list[1], 'value': classify_list[1], 'disabled': False},
                    {'label': classify_list[2], 'value': classify_list[2], 'disabled': False},
                    {'label': classify_list[3], 'value': classify_list[3], 'disabled': False},
                    {'label': classify_list[4], 'value': classify_list[4], 'disabled': False},
                    {'label': classify_list[5], 'value': classify_list[5], 'disabled': False},
                    {'label': classify_list[6], 'value': classify_list[6], 'disabled': False},
                    {'label': classify_list[7], 'value': classify_list[7], 'disabled': True},  
                ]


@app.callback(
    Output('main_options', 'options'),
    Input('main_axis', 'value')
    )
def update_main_options(main_axis):
    main_options = classify[main_axis].unique().tolist()
    return main_options


@app.callback(
    Output('sub_options', 'options'),
    Input('sub_axis', 'value')
    )
def update_sub_options(sub_axis):
    sub_options = classify[sub_axis].unique().tolist()
    return sub_options


@app.callback(
    Output("seal_num_text", "children"),
    [
        Input("main_axis", "value"),   
        Input("sub_axis", "value"),    
        Input("main_options", "value"),   
        Input("sub_options", "value"),
    ],
    )
def update_seal_num_text(main_axis,sub_axis,main_options,sub_options):
    df =  classify[(classify[main_axis]==main_options)&(classify[sub_axis]==sub_options)]
    return [len(df)]


@app.callback(
    Output('classify_graphic', 'figure'),
    [
        Input("main_axis", "value"),  
        Input("sub_axis", "value"),
     ],
    )
def update_classify_graphic(main_axis, sub_axis):
    df = classify.groupby(by=[main_axis,sub_axis]).agg({"数量":"sum"}).reset_index()
    df.sort_values(by=main_axis, ascending=True, inplace=True)
    fig = px.bar(df, x=main_axis, y="数量", color=sub_axis)
    return fig


@app.callback(
    Output('share_graphic', 'figure'),
    [
        Input("main_axis", "value"),  
     ],
    )
def update_share_graphic(main_axis):
    fig = px.histogram(classify, x="朱色比例", color=str(main_axis),
                   marginal="box", # box or violin, rug
                   opacity = 0.7,
                   nbins = 50,
                   barmode = "overlay")
    return fig

# info_table
@app.callback(
    Output('info_table', 'figure'),
    [
        Input("img_options", "value"),  
     ],
    )
def update_share_graphic(img_options):

    dictfilt = lambda x, y: dict([ (i,x[i]) for i in x if i in set(y)])
    my_dict = classify[classify['序号']==1].to_dict(orient='records')[0]
    wanted_keys = ("简体","繁体","作者","图画印","边款","边框","印文字数","印形","印文","印面内容","朱色比例")
    new_dict = dictfilt(my_dict, wanted_keys)

    first_column = list(new_dict.keys())
    second_column = list(new_dict.values())
    values = [first_column, second_column]

    fig = go.Figure(data=[go.Table(
    columnorder = [1,2],
    columnwidth = [30,60],
    header = dict(
        values = [['<b>属性</b>'],['<b>内容</b>']],
        line_color='darkslategray',
        fill_color='black',
        align=['left','center'],
        font=dict(color='white', size=12),
        height=30
    ),
    cells=dict(
        values=values,
        line_color='darkslategray',
        fill=dict(color=['white', 'white']),
        align=['left', 'center'],
        font_size=12,
        height=25)
        )
    ])
    return fig


@app.callback(
    Output('img', 'figure'),
    Input('img_options', 'value')
    )
def update_img(img_options):
    fig = go.Figure()

    img_id = int(img_options)
    img_label = classify[classify['序号']==img_id]['简体'].unique()[0]
    img_fname = classify[classify['序号']==img_id]['文件名'].unique()[0]
    img_x = classify[classify['序号']==img_id]['img_x'].unique()[0]
    img_y = classify[classify['序号']==img_id]['img_y'].unique()[0]
    img_path = "../png_crop/" + str(img_fname)
    img_path = Image.open(img_path)

    # Constants
    square = 400

    # Add invisible scatter trace.
    # This trace is added to help the autoresize logic work.
    fig.add_trace(go.Scatter(x=[0, square],y=[0, square],mode="markers",marker_opacity=0))

    # Configure axes
    fig.update_xaxes(visible=False, range=[0, square] )
    fig.update_yaxes(visible=False, range=[0, square], scaleanchor="x" )

    if img_x >= img_y:
        # Add image
        fig.add_layout_image(
            dict(
                x=0,
                y=(square+(square/img_x)*img_y)/2,
                sizex=square,
                sizey=(square/img_x)*img_y,
                xref="x",
                yref="y",
                opacity=1.0,
                layer="below",
                sizing="stretch",
                source=img_path)
        )
    else:
        fig.add_layout_image(
            dict(
                x=(square-(square/img_y)*img_x)/2,
                y=square,
                sizex=(square/img_y)*img_x,
                sizey=square,
                xref="x",
                yref="y",
                opacity=1.0,
                layer="below",
                sizing="stretch",
                source=img_path)
        )    

    # Configure other layout
    fig.update_layout(
        width=square,
        height=square,
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        plot_bgcolor="rgba(0, 0, 0, 1)",
        paper_bgcolor="rgba(0, 0, 0, 1)",  
    )

    return fig


























# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)