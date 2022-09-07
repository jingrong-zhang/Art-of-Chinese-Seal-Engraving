import dash
import copy
from dash import Dash, dcc, html, Input, Output, ClientsideFunction
import plotly.graph_objects as go
import plotly.express as px
import dash_daq as daq
import pandas as pd
import numpy as np
from pandas.api.types import CategoricalDtype
from textwrap import dedent
from PIL import Image
import requests
from io import BytesIO


app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "中国篆刻·方寸之间见真章"

server = app.server
app.config.suppress_callback_exceptions = True


# #########################################
# ##############  format  #################
# #########################################

layout = dict(
    margin=dict(l=20, r=20, b=50, t=20),
    hovermode="closest",
    plot_bgcolor="rgba(0, 0, 0, 0)",
    paper_bgcolor="rgba(0, 0, 0, 0)",
    legend=dict(font=dict(size=12), orientation="v"),
    yaxis = dict(tickfont = dict(size=12)),
    xaxis = dict(tickfont = dict(size=12)),
    yaxis_title = None,
    xaxis_title = None,
)

color__dict = {
                '图画印':'#ab3b3a',
                '边款':'#ab3b3a',
                '口':'#ab3b3a',
                '口口':'#AB63FA',
                '日':'#FFA15A',
                '田':'#19D3F3',
                '口口口':'#FF6692',
                '圆':'#B6E880',
                '圆+方':'#24936E',
                '日日日':'#FECB52',
                '井':'#7F7F7F',
                '亚':'#72B7B2',
                '特殊':'#F7C242',
                '日+口':'#24936E',
                '1':'#F7C242',
                '2':'#BEC23F',
                '3':'#3A8FB7',
                '4':'#ab3b3a',
                '5':'#E98B2A',
                '6':'#81C7D4',
                '7':'#70649A',
                '8':'#24936E',
                '9':'#0089A7',
                '>=10':'#9f9f9f',
                '方形':'#7F7F7F',
                '长方形':'#ab3b3a',
                '椭圆形':'#F7C242',
                '圆形':'#E98B2A',
                '多个':'#3A8FB7',
                '三角形':'#BEC23F',
                '其他':'#9f9f9f',
                '白文':'#9f9f9f',
                '朱文':'#ab3b3a',
                '朱白相间文':'#3A8FB7',
                '姓名印':'#ab3b3a',
                '收藏鉴赏印':'#F7C242',
                '斋馆别号印':'#BEC23F',
                '书简印':'#81C7D4',
                '无':'#9f9f9f',
                '榭稚柳':'#BEC23F',
                '余任天':'#E98B2A',
                '齐白石':'#24936E',
                '张大千':'#3A8FB7',
                '寿石工':'#70649A',
                '吴昌硕':'#ab3b3a',
                '弘旿':'#72B7B2',
                '陈衡恪':'#AB63FA',
                '陈半丁':'#FF6692',
                }

# #########################################
# #######  read the orginal data  #########
# #########################################

onwer_final = pd.read_csv(f"./data/onwer_final.csv",index_col=0)
classify = pd.read_csv(f"./data/classification.csv",index_col=0)
classify_list = ['作者', '图画印', '边款', '边框', '印文字数', '印形', '印文', '印面内容']
img_db_path = 'https://raw.githubusercontent.com/jingrong-zhang/Seals_Database/main/img/'

# #################################################
# #########  generate dashboard card  #############
# #################################################

def build_modal_info_overlay(id, side, content):
    """
    Build div representing the info overlay for a plot panel
    """
    div = html.Div(
        [  # modal div
            html.Div(
                [  # content div
                    html.Div(
                        [
                            html.H4(
                                [
                                    # "Info | Double-click on legend to isolate one trace.",
                                    html.Img(
                                        id=f"close-{id}-modal",
                                        src="assets/times-circle-solid.svg",
                                        n_clicks=0,
                                        className="info-icon",
                                    ),
                                ],
                                className='modal-title'
                            ),
                            dcc.Markdown(content),
                        ]
                    )
                ],
                className=f"modal-content {side}",
            ),
            html.Div(className="modal"),
        ],
        id=f"{id}-modal",
        style={"display": "none"},
    )
    return div

modal_1 = build_modal_info_overlay(
                    "left",
                    "bottom",
                    dedent(
                        """
            _**印章数据库过滤检索面板**_ 使用方法 
            
            步骤一 _**选择过滤类别**_
            
            选择印章的两个属性进行过滤检索。目前提供八种属性，分别是：作者，图画印，边款，边框，印文字数，印形，印文，印面内容。注意：两个属性不可以相同。

            步骤二 _**选择过滤具体条件**_
            
            基于第一步的属性选择，进一步选择具体的过滤条件。例如，若步骤一选择了“印形”与“印文”，在本步骤中，您将根据“印形”和“印文”的所有分类进行最终的交叉检索。您将最终检索出“印形”为“方形”且“印文”为“白文”的所有印章。

            _**过滤结果**_
            
            展示出基于您所选的过滤条件，数据库中满足要求的印章数量。

            步骤三 _**基于 ‘某条件数据库’ 选择印章**_
            
            本步骤将决定中间面板下拉菜单中的可选印章。若选择基于“过滤结果”，可选印章将与过滤结果一致；若选择“完整数据库”，可选印章将是完整的印章数据库，约一万个印章。       
            """
                    ),
                )

modal_2 = build_modal_info_overlay(
                    "right",
                    "bottom",
                    dedent(
                        """
            _**印章属性表**_
            
            本表格展示所选的两个印章的具体属性，包括上海图书馆数据库中的原有属性以及进一步的属性分析结果。

            _**作者具体信息**_
            
            本表格展示所选的两个印章的作者具体信息。
            """
                    ),
                )

modal_3 = build_modal_info_overlay(
                    "mid_up_left",
                    "bottom",
                    dedent(
                        """
            _**印章可视化展示面板**_
            
            打开下拉菜单，选择印章编号。面板将展示印章的文字内容，作者，及图像信息。

            注意：您可以用鼠标选择放大图像的某个区域来观察印章细节，双击图像恢复原始大小。
            """
                    ),
                )
                
modal_4 = build_modal_info_overlay(
                    "mid_up_right",
                    "bottom",
                    dedent(
                        """
            _**印章可视化展示面板**_
            
            打开下拉菜单，选择印章编号。面板将展示印章的文字内容，作者，及图像信息。

            注意：您可以用鼠标选择放大图像的某个区域来观察印章细节，双击图像恢复原始大小。
            """
                    ),
                )
modal_5 = build_modal_info_overlay(
                    "mid_down_left",
                    "top",
                    dedent(
                        """
            _**基于两个过滤类别的数据库数量统计分析面板**_
            
            本图表展示了根据过滤类别一和类别二的印章数量统计结果，纵轴为印章数量，横轴为类别一的具体属性，颜色基于类别二的具体属性。例如，在默认视图中，我们可以观察得出以下结论：本印章数据库中，印形为方形的印章数量最多，长方形印章中朱文比例较高。

            注意：双击具体图例可以隐藏其他图例内容，单击具体图例可以隐藏本图例内容。您可以用鼠标选择放大图表的某个区域来观察细节，双击恢复原始大小。
            """
                    ),
                )

modal_6 = build_modal_info_overlay(
                    "mid_down_right",
                    "top",
                    dedent(
                        """
            _**基于过滤类别一的印章朱色比例分析面板**_
            
            本图表展示了根据过滤类别一的朱色比例分析结果，纵轴为印章数量，横轴为朱色比例（0-1），颜色基于类别一的具体属性。上方图表展示了最小值，最大值，平均值等统计信息。例如，当类别一为“印文时”，我们可以观察得出以下结论：本印章数据库中，朱文印章朱色比例平均低于白文印章。

            注意：双击具体图例可以隐藏其他图例内容，单击具体图例可以隐藏本图例内容。您可以用鼠标选择放大图表的某个区域来观察细节，双击恢复原始大小。
            """
                    ),
                )




def banner():
    return html.Div(
        className="banner",
        children=[
            # Change App Name here
            html.Div(
                className="banner",
                children=[
                    html.H1("· 方寸之间见真章"),
                    html.A(
                        id="logo",
                        children=[
                            html.Img(src=app.get_asset_url("logo.png"))
                        ],
                        href="",
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
                            labelStyle={'display': 'block', 'color': 'lightgrey', 'font-size': 14, 'height': 26},
                            inputStyle={"margin-right": "5px"},
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
                            labelStyle={'display': 'block', 'color': 'lightgrey', 'font-size': 14, 'height': 26},
                            inputStyle={"margin-right": "5px"},
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
                                labelStyle={'display': 'block', 'color': 'lightgrey', 'font-size': 14, 'height': 26},
                                inputStyle={"margin-right": "5px"},
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
                                labelStyle={'display': 'block', 'color': 'lightgrey', 'font-size': 14, 'height': 26},
                                inputStyle={"margin-right": "5px"},
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
                                dcc.Dropdown(
                                    id='img_options_1',
                                    className="dcc_control",
                                    clearable=False,
                                ),   
                        ]
                )

img_options_2 = html.Div(
                    className="img_options_2",
                    children=[
                                dcc.Dropdown(
                                    id='img_options_2',
                                    className="dcc_control",
                                    clearable=False,
                                ),     
                        ]
                )


def seal_num():
    return html.Div(
                    className="seal_num_bigcard",
                    children=[
                        html.Div(
                            [
                                html.H3("过滤结果"),
                                html.Div(
                                    className="seal_num",
                                    children=[
                                        html.H2(id="seal_num_text"),
                                        html.P("个可选印章"),
                                    ]
                                ),
                                html.Br(), 
                                html.H3("3. 基于 [ ] 选择印章"),
                                dcc.RadioItems(
                                    id='img_options_choice',
                                    className="dcc_control",
                                    options=['完整数据库','过滤结果'],
                                    value='完整数据库',
                                    labelStyle={"padding-right": "30px", 'color': 'lightgrey'},
                                    inputStyle={"margin-right": "5px"},
                                ),                         
                            ],
                            className="mini_container",
                        )
                    ],
                )

 
img_selection_1 = html.Div(
                    id="mid_up_left-div",
                    className="img_selection_1 img_border",
                    children=[
                                html.Div(
                                    className="img_titlebar_1",
                                    children=[
                                    html.H3(id="seal_1_title_text"), 
                                    img_options_1,
                                    html.H3(
                                            [
                                                "",
                                                html.Img(
                                                    id="show-mid_up_left-modal",
                                                    src="assets/question-circle-solid.png",
                                                    n_clicks=0,
                                                    className="info-icon",
                                                ),
                                            ]
                                        ),
                                    ]
                                ),
                                dcc.Graph(id="img_1", config={"displayModeBar": False, 'doubleClick': 'reset'}),
                        ]
                )

img_selection_2 = html.Div(
                    id="mid_up_right-div",
                    className="img_selection_2 img_border",
                    children=[
                                html.Div(
                                    className="img_titlebar_2",
                                    children=[
                                    html.H3(id="seal_2_title_text"), 
                                    img_options_2,
                                    html.H3(
                                            [
                                                "",
                                                html.Img(
                                                    id="show-mid_up_right-modal",
                                                    src="assets/question-circle-solid.png",
                                                    n_clicks=0,
                                                    className="info-icon",
                                                ),
                                            ]
                                        ),                                    
                                    ]
                                ),
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
                        id="mid_down_left-div",    
                        className="classify_graphic graphic_border",
                        children=[
                                html.Div(
                                    className="graphic_titlebar_1",
                                    children=[                            
                                        html.H3(id="classify_graphic_title"), 
                                        html.H3(
                                                [
                                                    "",
                                                    html.Img(
                                                        id="show-mid_down_left-modal",
                                                        src="assets/question-circle-solid.png",
                                                        n_clicks=0,
                                                        className="info-icon",
                                                    ),
                                                ]
                                            ),                                           
                                    ]
                                ),                            
                            dcc.Graph(id="classify_graphic", config={"displayModeBar": False}),
                            ]
                    )

share_graphic = html.Div(
                        id="mid_down_right-div",       
                        className="share_graphic graphic_border",
                        children=[
                                html.Div(
                                    className="graphic_titlebar_1",
                                    children=[                            
                                        html.H3(id="share_graphic_title"), 
                                        html.H3(
                                                [
                                                    "",
                                                    html.Img(
                                                        id="show-mid_down_right-modal",
                                                        src="assets/question-circle-solid.png",
                                                        n_clicks=0,
                                                        className="info-icon",
                                                    ),
                                                ]
                                            ),                                           
                                    ]
                                ),    
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
                id="left-div",
                className="left_column sides",
                children=[
                    html.H3(
                        [
                            "1. 选择过滤类别",
                            html.Img(
                                id="show-left-modal",
                                src="assets/question-circle-solid.png",
                                n_clicks=0,
                                className="info-icon",
                            ),
                        ]
                    ),
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
                id="right-div",
                className="right_column sides",
                children=[
                    html.H3(
                        [
                            "印章属性表",
                            html.Img(
                                id="show-right-modal",
                                src="assets/question-circle-solid.png",
                                n_clicks=0,
                                className="info-icon",
                            ),
                        ]
                    ),
                    dcc.Graph(id="info_table_1", config={"displayModeBar": False}),
                    html.H3("作者信息"),
                    dcc.Graph(id="info_table_2", config={"displayModeBar": False}),
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
    modal_1,
    modal_2,
    modal_3,
    modal_4,
    modal_5,
    modal_6,
        ], 
        className="app_container"
    )


# #################################################
# ################    callback   ##################
# #################################################

# Create show/hide callbacks for each info modal
for id in ["left", "right", "mid_up_left", "mid_up_right", "mid_down_left", "mid_down_right"]:
    @app.callback(
        [Output(f"{id}-modal", "style"), Output(f"{id}-div", "style")],
        [Input(f"show-{id}-modal", "n_clicks"), Input(f"close-{id}-modal", "n_clicks")],
    )
    def toggle_modal(n_show, n_close):
        ctx = dash.callback_context
        if ctx.triggered and ctx.triggered[0]["prop_id"].startswith("show-"):
            return {"display": "block"}, {"zIndex": 1003}
        else:
            return {"display": "none"}, {"zIndex": 0}

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
    fig = px.histogram(classify, 
                        x="朱色比例", 
                        color=main_axis,
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
    wanted_keys = ("简体","繁体","作者_细节","图画印","边款","边框","印文字数","印形","印文","印面内容","朱色比例","--姓名印","--收藏鉴赏印","--书简印","--斋馆别号印")

    my_dict_1 = classify[classify['序号']==int(img_options_1)].to_dict(orient='records')[0]
    new_dict_1 = dictfilt(my_dict_1, wanted_keys)

    my_dict_2 = classify[classify['序号']==int(img_options_2)].to_dict(orient='records')[0]
    new_dict_2 = dictfilt(my_dict_2, wanted_keys)

    first_column = list(new_dict_1.keys())
    first_column = list(map(lambda x: x.replace('作者_细节', '作者'), first_column))
    second_column = list(new_dict_1.values())
    third_column = list(new_dict_2.values())
    values = [first_column, second_column, third_column]

    fig = go.Figure(data=[go.Table(
    columnorder = [1,2,3],
    columnwidth = [45,60,60],
    header = dict(
        values = [['<b>属性</b>'],['<b>印章（左）</b>'],['<b>印章（右）</b>']],
        line_color='grey',
        fill_color='black',
        align=['center','center','center'],
        font=dict(color='white', size=12),
        height=30
    ),
    cells=dict(
        values=values,
        line_color='grey',
        fill=dict(color=['rgba(0, 0, 0, 0)', 'rgba(0, 0, 0, 0)', 'rgba(0, 0, 0, 0)']),
        align=['left','left','left'],
        font=dict(color='lightgrey', size=12),
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
    Output('info_table_2', 'figure'),
    [
        Input("img_options_1", "value"), 
        Input("img_options_2", "value"),  
    ],
    )
def update_share_graphic(img_options_1,img_options_2):
    """
    https://plotly.com/python/table/
    """
    owner_1 = classify[classify['序号']==img_options_1]['作者_细节'].tolist()[0]
    owner_2 = classify[classify['序号']==img_options_2]['作者_细节'].tolist()[0]

    dictfilt = lambda x, y: dict([ (i,x[i]) for i in x if i in set(y)])
    wanted_keys = ("作者","生年","卒年","介绍")

    my_dict_1 = onwer_final[onwer_final['作者']==owner_1].to_dict(orient='records')[0]
    new_dict_1 = dictfilt(my_dict_1, wanted_keys)

    my_dict_2 = onwer_final[onwer_final['作者']==owner_2].to_dict(orient='records')[0]
    new_dict_2 = dictfilt(my_dict_2, wanted_keys)

    first_column = list(new_dict_1.keys())
    second_column = list(new_dict_1.values())
    third_column = list(new_dict_2.values())
    values = [first_column, second_column, third_column]

    fig = go.Figure(data=[go.Table(
                    columnorder = [1,2,3],
                    columnwidth = [45,60,60],
                    header = dict(
                        values = [['<b>属性</b>'],['<b>印章（左）</b>'],['<b>印章（右）</b>']],
                        line_color='grey',
                        fill_color='black',
                        align=['center','center','center'],
                        font=dict(color='white', size=12),
                        height=30
                    ),
                    cells=dict(
                        values=values,
                        line_color='grey',
                        fill=dict(color=['rgba(0, 0, 0, 0)', 'rgba(0, 0, 0, 0)', 'rgba(0, 0, 0, 0)']),
                        align=['left','left','left'],
                        font=dict(color='lightgrey', size=12),
                        font_size=12,
                        height=25,
                    ),
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
    img_url = img_db_path + str(img_fname)
    response = requests.get(img_url)
    img_path = Image.open(BytesIO(response.content))

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
    img_url = img_db_path + str(img_fname)
    response = requests.get(img_url)
    img_path = Image.open(BytesIO(response.content))

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
    img_onwer = classify[classify['序号']==img_id]['作者_细节'].unique()[0]
    return [img_label + " - " + img_onwer]


@app.callback(
    Output("seal_2_title_text", "children"),
    Input("img_options_2", "value"), 
    )
def update_seal_num_text(img_options_2):
    img_id = int(img_options_2)
    img_label = classify[classify['序号']==img_id]['简体'].unique()[0]
    img_onwer = classify[classify['序号']==img_id]['作者_细节'].unique()[0]
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


@app.callback(
    [
        Output('img_options_1', 'options'),
        Output('img_options_1', 'value'),
        Output('img_options_2', 'options'),
        Output('img_options_2', 'value'),        
    ],
    [
        Input('img_options_choice', 'value'),
        Input("main_axis", "value"),   
        Input("sub_axis", "value"),    
        Input("main_options", "value"),   
        Input("sub_options", "value"),    
    ]
    )
def update_main_options(img_options_choice,main_axis,sub_axis,main_options,sub_options):
    if img_options_choice=='完整数据库':
        options = classify['序号'].tolist()
        return options, options[2190], options, options[2508]
    else:
        options = classify[(classify[main_axis]==main_options)&(classify[sub_axis]==sub_options)]['序号'].tolist()
        return options, options[0], options, options[-1]      


# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)