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
# ##############  format  #################
# #########################################

layout = dict(
    margin=dict(l=20, r=20, b=20, t=20),
    hovermode="closest",
    plot_bgcolor="rgba(0, 0, 0, 0)",
    paper_bgcolor="rgba(0, 0, 0, 0)",
    legend=dict(font=dict(size=12), orientation="v"),
    yaxis = dict(tickfont = dict(size=12)),
    xaxis = dict(tickfont = dict(size=12)),
)

color__dict = {
                '图画印':'#636EFA',
                '边款':'#EF553B',
                '口':'#00CC96',
                '口口':'#AB63FA',
                '日':'#FFA15A',
                '田':'#19D3F3',
                '口口口':'#FF6692',
                '圆':'#B6E880',
                '圆+方':'#FF97FF',
                '日日日':'#FECB52',
                '井':'#7F7F7F',
                '亚':'#72B7B2',
                '特殊':'lightgrey',
                '日+口':'lightgrey',
                '1':'lightgrey',
                '2':'lightgrey',
                '3':'lightgrey',
                '4':'lightgrey',
                '5':'lightgrey',
                '6':'lightgrey',
                '7':'lightgrey',
                '8':'lightgrey',
                '9':'lightgrey',
                '>=10':'lightgrey',
                '方形':'lightgrey',
                '长方形':'lightgrey',
                '椭圆形':'lightgrey',
                '多个':'lightgrey',
                '三角形':'lightgrey',
                '其他':'lightgrey',
                '白文':'#9f9f9f',
                '朱文':'#ab3b3a',
                '朱白相间文':'#3A8FB7',
                '姓名印':'lightgrey',
                '收藏鉴赏印':'lightgrey',
                '斋馆别号印':'lightgrey',
                '书简印':'lightgrey',
                '无':'lightgrey',
                '*':'black',
                }

# #########################################
# #######  read the orginal data  #########
# #########################################

classify = pd.read_csv(f"../03_LabelProcessing/classification.csv",index_col=0)
classify_list = ['作者', '图画印', '边款', '边框', '印文字数', '印形', '印文', '印面内容']


# #################################################
# #########  generate dashboard card  #############
# #################################################

def banner():
    return html.Div(
        className="banner",
        children=[
            # Change App Name here
            html.Div(
                className="banner",
                children=[
                    html.H1(
                        id="banner_title",
                        children=[
                            html.A(
                                "中国篆刻：方寸之间大有天地",
                                href="https://github.com/plotly/dash-svm",
                                style={"text-decoration": "none", "color": "inherit"},
                            )
                        ],
                    ),
                    html.A(
                        id="logo",
                        children=[
                            html.Img(src=app.get_asset_url("GitHub_Logo.png"))
                        ],
                        href="https://plot.ly/products/dash/",
                    ),
                ],
            )
        ],
    )

axis_1 = html.Div(
                    className="axis_1",
                    children=[
                        html.P("类别一"),
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
                            value="印形",
                            labelStyle={'display': 'block'}
                        ),
                        ]
                )

axis_2 = html.Div(
                    className="axis_1",
                    children=[
                        html.P("类别二"),
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
                        ]
                )


def classify_button():
    """
    https://dash.plotly.com/dash-html-components/button
    """
    return html.Div(
        id="classify_button_card",
        className = "classify_button_card",
        children=[
            axis_1,
            axis_2,
        ],
    )

main_options = html.Div(
                    className="main_options",
                    children=[
                            html.P(id='class_1_text'),
                            dcc.RadioItems(
                                id='main_options',
                                className="dcc_control",
                                labelStyle={'display': 'block'},
                            ), 
                        ]
                )

sub_options = html.Div(
                    className="sub_options",
                    children=[
                            html.P(id='class_2_text'),
                            dcc.RadioItems(
                                id='sub_options',
                                className="dcc_control",
                                labelStyle={'display': 'block'},
                            ),
                        ]
                )


def classify_dropdown():
    """
    https://dash.plotly.com/dash-core-components/dropdown
    """
    return html.Div(
        id="classify_dropdown_card",
        className = "classify_dropdown_card",
        children=[
            main_options,
            sub_options,
        ],
    )

img_options_1 = html.Div(
                    className="img_options_1",
                    children=[
                                html.H4("印章一"),
                                dcc.Dropdown(
                                    id='img_options_1',
                                    options=[872,4253,4354,6,24],
                                    value=872,
                                    className="dcc_control",
                                    clearable=False,
                                ),   
                        ]
                )

img_options_2 = html.Div(
                    className="img_options_2",
                    children=[
                                html.H4("印章二"),   
                                dcc.Dropdown(
                                    id='img_options_2',
                                    options=[872,4253,4354,6,24],
                                    value=4354,
                                    className="dcc_control",
                                    clearable=False,
                                ),     
                        ]
                )

img_options = html.Div(
                    className="img_options",
                    children=[
                                img_options_1,   
                                img_options_2,  
                        ]
                )


def seal_num():
    return html.Div(
                    className="seal_num",
                    children=[
                        html.Div(
                            [
                                html.H3("过滤结果 - 可选印章数量"),
                                html.H2(id="seal_num_text"), 
                                html.H3("3. 选择印章"),
                                dcc.RadioItems(
                                    id='img_options_choice',
                                    className="dcc_control",
                                    options=['完整数据库','过滤结果'],
                                    value='完整数据库',
                                    labelStyle={'display': 'block'},
                                ),
                                html.Br(),
                                img_options,                              
                            ],
                            className="mini_container",
                        )
                    ],
                )


img_selection_1 = html.Div(
                    className="img_selection_1 img_border",
                    children=[
                                html.H3(id="seal_1_title_text"), 
                                dcc.Graph(id="img_1", config={"displayModeBar": False, 'doubleClick': 'reset'}),
                        ]
                )

img_selection_2 = html.Div(
                    className="img_selection_2 img_border",
                    children=[
                                html.H3(id="seal_2_title_text"), 
                                dcc.Graph(id="img_2", config={"displayModeBar": False, 'doubleClick': 'reset'}),
                        ]
                )

mid_column_imgs = html.Div(
                        className="mid_column_imgs",
                        children=[
                            img_selection_1,
                            img_selection_2,
                            ]
                    )

classify_graphic = html.Div(
                        className="classify_graphic",
                        children=[
                            html.H3(id="classify_graphic_title"), 
                            dcc.Graph(id="classify_graphic", config={"displayModeBar": False}),
                            ]
                    )

share_graphic = html.Div(
                        className="share_graphic",
                        children=[
                            html.H3(id="share_graphic_title"), 
                            dcc.Graph(id="share_graphic", config={"displayModeBar": False}),
                            ]
                    )


mid_column_graphs = html.Div(
                        className="mid_column_graphs",
                        children=[
                            classify_graphic,
                            share_graphic,
                            ]
                    )


left_column = html.Div(
                className="left_column sides",
                children=[
                    html.H3("1. 选择过滤类别"),
                    classify_button(),
                    html.Br(),
                    html.H3("2. 选择过滤具体条件"),
                    classify_dropdown(),
                    html.Br(),
                    seal_num(),
                    html.Br(),
                    ]
            )

right_column = html.Div(
                className="right_column sides",
                children=[
                    html.H3("可选印章数量"), 
                    dcc.Graph(id="info_table_1", config={"displayModeBar": False}),                
                    ]
            )

mid_column = html.Div(
                className="mid_column",
                children=[
                    mid_column_imgs,
                    mid_column_graphs,
                    ]
            )

app_body = html.Div(
                className="app_body",
                children=[
                    left_column,
                    mid_column,
                    right_column,
                    ]
            )


# #################################################
# #################    layout   ###################
# #################################################

app.layout = html.Div([
    banner(),
    app_body,
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
    [
        Output('main_options', 'options'),
        Output('main_options', 'value'),
    ],
    Input('main_axis', 'value')
    )
def update_main_options(main_axis):
    main_options = classify[main_axis].unique().tolist()
    return main_options, main_options[0]


@app.callback(
    [
        Output('sub_options', 'options'), 
        Output('sub_options', 'value'),
    ],
    Input('sub_axis', 'value')
    )
def update_sub_options(sub_axis):
    sub_options = classify[sub_axis].unique().tolist()
    return sub_options, sub_options[0]


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
    fig = px.bar(df, 
                x=main_axis, 
                y="数量", 
                color=sub_axis, 
                color_discrete_map=color__dict)
    fig.update_layout(layout)  
    return fig


@app.callback(
    Output('share_graphic', 'figure'),
    Input("main_axis", "value"), 
    )
def update_share_graphic(main_axis):
    column_y = main_axis
    fig = px.histogram(classify, 
                        x="朱色比例", 
                        color="印文",
                        marginal="box", # box or violin, rug
                        opacity = 0.7,
                        nbins = 50,
                        color_discrete_map=color__dict, 
                        barmode = "overlay")
    fig.update_layout(layout)  
    return fig


@app.callback(
    Output('info_table_1', 'figure'),
    [
        Input("img_options_1", "value"), 
        Input("img_options_2", "value"),  
    ],
    )
def update_share_graphic(img_options_1,img_options_2):
    """
    https://plotly.com/python/table/
    """
    dictfilt = lambda x, y: dict([ (i,x[i]) for i in x if i in set(y)])
    wanted_keys = ("简体","繁体","作者","图画印","边款","边框","印文字数","印形","印文","印面内容","朱色比例")

    my_dict_1 = classify[classify['序号']==int(img_options_1)].to_dict(orient='records')[0]
    new_dict_1 = dictfilt(my_dict_1, wanted_keys)

    my_dict_2 = classify[classify['序号']==int(img_options_2)].to_dict(orient='records')[0]
    new_dict_2 = dictfilt(my_dict_2, wanted_keys)

    first_column = list(new_dict_1.keys())
    second_column = list(new_dict_1.values())
    third_column = list(new_dict_2.values())
    values = [first_column, second_column, third_column]

    fig = go.Figure(data=[go.Table(
    columnorder = [1,2,3],
    columnwidth = [30,60,60],
    header = dict(
        values = [['<b>属性</b>'],['<b>印章（左）</b>'],['<b>印章（右）</b>']],
        line_color='darkslategray',
        fill_color='black',
        align=['center','center','center'],
        font=dict(color='white', size=12),
        height=30
    ),
    cells=dict(
        values=values,
        line_color='darkslategray',
        fill=dict(color=['rgba(0, 0, 0, 0)', 'rgba(0, 0, 0, 0)', 'rgba(0, 0, 0, 0)']),
        align=['left','left','left'],
        font_size=12,
        height=25)
        )
    ])

    fig.update_layout(
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",  
    )

    return fig



@app.callback(
    Output('img_1', 'figure'),
    Input('img_options_1', 'value')
    )
def update_img(img_options_1):
    fig = go.Figure()

    img_id = int(img_options_1)
    img_label = classify[classify['序号']==img_id]['简体'].unique()[0]
    img_fname = classify[classify['序号']==img_id]['文件名'].unique()[0]
    img_x = classify[classify['序号']==img_id]['img_x'].unique()[0]
    img_y = classify[classify['序号']==img_id]['img_y'].unique()[0]
    img_path = "../png_crop/" + str(img_fname)
    img_path = Image.open(img_path)

    # Constants
    square = 460

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
        margin={"l": 30, "r": 30, "t": 30, "b": 30},
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",  
    )
    return fig

@app.callback(
    Output('img_2', 'figure'),
    Input('img_options_2', 'value')
    )
def update_img(img_options_2):
    fig = go.Figure()

    img_id = int(img_options_2)
    img_label = classify[classify['序号']==img_id]['简体'].unique()[0]
    img_fname = classify[classify['序号']==img_id]['文件名'].unique()[0]
    img_x = classify[classify['序号']==img_id]['img_x'].unique()[0]
    img_y = classify[classify['序号']==img_id]['img_y'].unique()[0]
    img_path = "../png_crop/" + str(img_fname)
    img_path = Image.open(img_path)

    # Constants
    square = 460

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
        margin={"l": 30, "r": 30, "t": 30, "b": 30},
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",  
    )
    return fig


@app.callback(
    Output("seal_1_title_text", "children"),
    Input("img_options_1", "value"), 
    )
def update_seal_num_text(img_options_1):
    img_id = int(img_options_1)
    img_label = classify[classify['序号']==img_id]['简体'].unique()[0]
    img_onwer = classify[classify['序号']==img_id]['作者'].unique()[0]
    return [img_label + " - " + img_onwer]


@app.callback(
    Output("seal_2_title_text", "children"),
    Input("img_options_2", "value"), 
    )
def update_seal_num_text(img_options_2):
    img_id = int(img_options_2)
    img_label = classify[classify['序号']==img_id]['简体'].unique()[0]
    img_onwer = classify[classify['序号']==img_id]['作者'].unique()[0]
    return [img_label + " - " + img_onwer]


@app.callback(
    Output("class_1_text", "children"),
    Input("main_axis", "value"), 
    )
def update_seal_num_text(main_axis):
    return [main_axis]


@app.callback(
    Output("class_2_text", "children"),
    Input("sub_axis", "value"), 
    )
def update_seal_num_text(sub_axis):
    return [sub_axis]

@app.callback(
    Output("classify_graphic_title", "children"),
    [
        Input("main_axis", "value"), 
        Input("sub_axis", "value"), 
    ]
    )
def update_seal_num_text(main_axis,sub_axis):
    return ["基于 ["+main_axis+"] 和 ["+sub_axis+"] 对印章数据库进行交叉分析"]

@app.callback(
    Output("share_graphic_title", "children"),
    Input("main_axis", "value"),
    )
def update_seal_num_text(main_axis):
    return ["基于 ["+main_axis+"] 的印章朱色比例分布"]


# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)