'''
EA Automation UI Scrapper

This script allows the user to capture content of UI through
API call. It has following Api url-
    GET <base url>/test/init, Request [laneName: String]
    GET <base url>/test/stop, Request [sessionId: String]
    POST <base url>/api/ea/ui/update
    POST <base url> is configurable. for more info check out README.txt.

This script requires that 'flask', 'flask_restful' and 'selenium' be installed
within the Python environment you are running this script in.

This file can also be imported as a module.

API call examples:
http://127.0.0.1:5000/test/init?laneId=Lane 1
http://127.0.0.1:5000/test/stop?sessionId=lane 1

'''

import sys
import re
import os
from threading import Thread
from time import sleep, time
from configparser import ConfigParser

import requests

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

app = Flask(__name__)
api = Api(app)
# Selenium section*************


class EmployeeAssist:
    '''
    A class used to represent Employee Assist interface.

    Attributes
    ----------
    cfg : object
        Object of ConfigParser. Load configurable parameter from "config.ini"
    id_thread : None
        Condition for Thread 't1' to be activated.

    Methods
    -------
    laneSel()
        Select the recent lane.
    dataScrape()
        Scrape information from EmployeeAssist Window.
    UiChange()
        Check UI change and notify.
    '''

    def __init__(self):
        '''
        Load EmployeeAssist url on Chrome browser and wait for Customer call.

        '''

        self.cfg = ConfigParser()
        self.cfg.read('config.ini')
        self.id_thread = None
        self.uistatus = list()

        arg = sys.argv[0]          # change of directory
        arg = arg.split('/')
        arg.pop()
        path = os.path.join("/".join(arg), 'chromedriver')
        URL = "https://eademo.sandbox.conversenow.ai/empAssist"
        self.driver = webdriver.Chrome(executable_path=path)
        self.driver.get(URL)
        while True:
            try:
                WebDriverWait(self.driver, 2).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.date-time')))
            except TimeoutException:
                self.driver.refresh()
                continue
            else:
                break

    def laneSel(self, laneName):
        '''
        Class method to select recent available lane.

        Argument
        ---------
        laneName : str
            Name of lane (example- Lane 1).

        Parameters
        ----------
        selected_Lane : WebElement
            Selenium WebElement of selected lane.
        t1 : Thread
            Thread for auto UI update notification.

        Returns
        -------
        idOfselectedlane : str
            Id of selected lane.

        '''

        laneName = laneName.lower()
        try:
            lane = self.driver.find_element_by_xpath('//p[contains(text(), "{}")]'.format(laneName))
        except NoSuchElementException:
            idOfselectedlane = None
        else:
            selected_Lane = lane
            selected_Lane.find_element_by_xpath('../..').click()  # Click event
            idOfselectedlane = laneName  # laneId
            self.id_thread = idOfselectedlane    # Thread
            t1 = Thread(target=self.UiChange, name='t1', daemon=True)
            t1.start()
        return idOfselectedlane

    def dataScrape(self):
        '''
        Class method to scrape information from EmployeeAssist UI.

        Parameters
        ----------
        symbol : str
            Store symbol (+,-,/)
        item_list : list
            Store system detected info of a dish available on UI.
        itemCust_list : list
            Store customization info of a dish available on UI.

        Returns
        -------
        utterance : str
            Utterance available on UI.
        systemDetected_list : list
            A list of system detected content.
            Format- [[diah 1], [dish 2], ...]
        custAvl_list : list
            A list of customization to be done of dish.
            Format- [[customizations of dish 1], [customizations of dish 2], ...]
        choiceAvl_dict : list
            Options available of customizations for dish 1.

        '''

        utterance = self.driver.find_element_by_class_name('utterance').text
        cart = self.driver.find_elements_by_class_name('dish')
        systemDetected_list = list()
        custAvl_list = list()
        for dish in cart:
            item_list = list()
            symbol_Div = dish.find_element_by_class_name('dish-status')
            symbol = symbol_Div.get_attribute('ng-reflect-ng-class')
            flag = re.search(r'Addition|Deletion|CheckOut', symbol).group()
            if flag == 'Addition':
                symbol = '+'
            elif flag == 'Deletion':
                symbol = '-'
            elif flag == 'CheckOut':
                symbol = '/'
            item_list.append(symbol)
            systemDetected = dish.find_elements_by_class_name('dish-item')
            for option in systemDetected:
                class_name = option.get_attribute('class')
                if 'trash' not in class_name:
                    item_list.append(option.text)

            systemDetected_list.append(item_list)

            itemCust_list = list()
            custAvl = dish.find_elements_by_class_name('item1')  # Customization
            for option in custAvl:
                itemCust_list.append(option.text)
            custAvl_list.append(itemCust_list)

        choiceAvl = self.driver.find_elements_by_class_name('current-option-type')
        choiceAvl_dict = dict()  # Current choice available
        for option in choiceAvl:
            key = option.find_element_by_class_name('option-name').text
            value = [itemOption.text for itemOption in
                     option.find_elements_by_class_name('option-items')]
            choiceAvl_dict[key] = value
        # print(utterance, systemDetected_list, custAvl_list, choiceAvl_dict, sep='\n')  # Debug
        return (utterance, systemDetected_list, custAvl_list, choiceAvl_dict)

    def UiChange(self):
        '''
        Method to auto detect UI change and post recent content on API .

        Parameters
        ----------
        ui_data : tuple
            Use to store previos UI info.
        uistatus : list
            Flag for keeping track of UI change.
        content : tuple
            Recent UI information.
        current_milli_time: time
            UI scrape time in milliseconds epoch.

        '''

        try:
            ui_data = tuple()
            uistatus = []
            while self.id_thread != None:
                symbol_Div = self.driver.find_elements_by_class_name('dish-status')
                if (uistatus != symbol_Div):
                    uistatus = symbol_Div
                    content = self.dataScrape()
                    if ui_data != content[1:]:
                        ui_data = content[1:]
                        current_milli_time = int(round(time()*1000))
                        print('\n\n****UI Change****\n\n')
                        print("\nScrape data -\nutterance: {0}\nselected_keywords: {1}\nupcoming_keywords: {2}\ncurrent_options: {3}\n".format(*content))  # Debug
                        UIdata = {'status': 'SUCCESS',
                                  'sessionId': self.id_thread,
                                  'updateTime': current_milli_time,
                                  'data': {'utterance': content[0],
                                            'selected_keywords': content[1],
                                            'upcoming_keywords': content[2],
                                            'current_options': content[3]}}
                        # requests.post(url='http://127.0.0.1:5000/test/dummy', json=UIdata)  # POST API testing purpose. Just a Dummy.
                        URL = self.cfg.get('configData', 'url')
                        requests.post(url=URL+'/api/ea/ui/update', json=UIdata)  # Post UIdata on API.
        except Exception:
            print('\n\nWarning!!\nAbrupt close')

    def laneClose(self):
        '''
        Method to abort tracking of UI.

        '''

        self.id_thread = None  # close thread t1.


emp_obj = EmployeeAssist()


# Api Endpoints ************

class Init(Resource):
    '''
    Api class for selecting lane.

    Attribute
    ---------
    parser : object
            Object of RequestParser.

    Method
    ------
    get()
        GET method for establishing connection (Lane selection).
    post()
        POST method to emulate POST Api.

    '''

    def __init__(self):
        '''
        Parameter
        ---------
        parser : object
            Object of RequestParser.

        '''

        self.parser = reqparse.RequestParser()

    def get(self):
        '''
        Method for establishing connection (Lane selection).

        Parameter
        ---------
        laneId : str, required
            unique Lane Id.
        idOflane : str
            Unique id of selected lane

        Return
        ------
        dict
            unique Id for connection and Success/Error message.
        '''

        self.parser.add_argument('laneId', required=True, type=str,
                                 help='Missing required parameter!')
        args = self.parser.parse_args()
        print(args)  # Debug
        if len(args['laneId']):
            global idOflane
            idOflane = emp_obj.laneSel(args['laneId'])
            if idOflane is None:
                return {'status': 'ERROR', 'messege': 'Invalid Lane name!!'}, 404
            else:
                return {'status': 'SUCCESS', 'id': idOflane}, 200

        else:
            return {'status': 'ERROR',
                    'messege': 'laneId may not be empty!'
                    }, 400

    def post(self):    # POST API testing purpose. Just a Dummy.
        records = request.json
        print('\n****INSIDE POST API***\n')
        print(records)
        return {'status': 'SUCCESS'}, 200


class Stop(Resource):
    '''
    Api class for closing connection.

    Attribute
    ---------
    parser : object
        Object of RequestParser.

    Method
    ------
    get()
        GET method for abort connection.

    '''

    def __init__(self):
        '''
        Parameter
        ---------
        parser : object
            Object of RequestParser.

        '''

        self.parser = reqparse.RequestParser()

    def get(self):
        '''
        Method to abort connection.

        Parameter
        ---------
        sessionId : str, required
            session Id of active connection.

        Return
        ------
        dict
            Success/Error message.
        '''

        self.parser.add_argument('sessionId', required=True, type=str, help='Missing required parameter!')
        args = self.parser.parse_args()
        print(args)  # Debug
        global idOflane
        try:
            if args['sessionId'] == idOflane:
                idOflane = None
                emp_obj.laneClose()
                return {'status': 'SUCCESS'}, 200
            else:
                return {'status': 'ERROR', 'message': 'Invalid sessionId!'}, 403
        except NameError:
            return {'status': 'ERROR', 'message': 'Establish connection first!'}, 400

api.add_resource(Init, '/test/init', endpoint='init')
api.add_resource(Stop, '/test/stop', endpoint='stop')
api.add_resource(Init, '/test/dummy', endpoint='dummy')

if __name__ == '__main__':
    app.run()  # run flask app
