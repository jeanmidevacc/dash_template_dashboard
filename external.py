import os
import datetime
import decimal
import random

import dash_html_components as html

import boto3
from boto3.dynamodb.conditions import Key

import pandas as pd
import numpy as np


# Function to get the right symbol (the arrrow and associated color)
def get_symbol(value):
    if value<0:
        return ["fa fa-arrow-circle-down down fa-inverse"," "]
    elif value>0:
        return ["fa fa-arrow-circle-up up fa-inverse","+"]
    else:
        return ["fa fa-arrow-circle-right right fa-inverse","     "]

# Fucntion to get the key figures
def get_kf(param):
    a=random.randint(-5,5)
    b=random.randint(-5,5)
    c=random.randint(-5,5)
    list_elt=[
    [param,"NA",random.randint(-5,5)],
    ["Past week",get_symbol(a)[0],get_symbol(a)[1]+str(a)],
    ["Past month",get_symbol(b)[0],get_symbol(b)[1]+str(b)],
    ["Past year",get_symbol(c)[0],get_symbol(c)[1]+str(c)]
    ]

    return list_elt

# Function to creqte the key figures object
def get_keyindex(color,unit,list_elt):

    list_elt_display=[]

    for i,elt in enumerate(list_elt):
        if i==0:
            elt_li=html.Li(children=[elt[0]])
            elt_li2=html.Li(className="big-num",children=[html.H4("{} {}".format(elt[2],unit))])
            elt_ul=html.Ul(children=[elt_li,elt_li2])
            elt_header=html.Header(children=[elt_ul])

            elt_li=html.Li(children=[html.I(className="fa fa-fw fa-calendar-o"),elt[1]])
            elt_ul=html.Ul(children=[elt_li])
            elt_list=html.Li(className="list",children=[elt_ul])
            elt_sections=html.Ul(className="sections",children=[elt_list])
            elt_article=html.Article(children=[elt_sections])

            list_elt_display+=[elt_header,elt_article]
        else:
            elt_i2=html.I(className="fa fa-fw fa-clock-o")
            elt_li3=html.Li(children=[elt_i2,elt[0]])
            elt_i3=html.I(className=elt[1])

            elt_li4=html.Li(className="big-num",children=[elt_i3,"{} {}".format(elt[2],unit)])
            elt_group=html.Ul(className="sections",children=[elt_li3,elt_li4])
            elt_footer=html.Footer(children=elt_group)

            list_elt_display+=[elt_footer]

    elt_section=html.Section(className="bubble",style={"background-color": color},children=list_elt_display)
    return elt_section

# Function to create an html table that will contains the dataframe
def generate_table(dataframe):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr(children=[
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(len(dataframe))]
    )
