# -*- coding: utf-8 -*-
"""
@author: cleartonic
@author: vex
"""
import random
import csv
import yaml
import traceback
import datetime
import time
import pickle
import socket
import re, logging, sys
import os
from collections import Counter 

# try:
#     THIS_FILEPATH = os.path.dirname( sys.executable)
#     THIS_FILENAME = os.path.basename(sys.executable)
# except:
THIS_FILEPATH = os.path.dirname( __file__ )
THIS_FILENAME = os.path.basename(__file__)


try:
    logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    filename=os.path.join(THIS_FILEPATH,'config','output_log.log'),
                    filemode='a',
                    level=logging.DEBUG)
except:
    THIS_FILEPATH = os.path.dirname( __file__ )
    THIS_FILENAME = os.path.basename(__file__)
    logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    filename=os.path.join(THIS_FILEPATH,'config','output_log.log'),
                    filemode='a',
                    level=logging.DEBUG)


VERSION_NUM = "2.2.3"
# INFO_MESSAGE = 'Twitch Trivia Bot loaded. Version %s. Developed by cleartonic. %s' % (VERSION_NUM, random.randint(0,10000))
INFO_MESSAGE = 'Twitch Trivia Bot loaded.'

if not os.path.exists(os.path.abspath(os.path.join(THIS_FILEPATH,'config'))):
    os.makedirs(os.path.abspath(os.path.join(THIS_FILEPATH,'config')))
if not os.path.exists(os.path.abspath(os.path.join(THIS_FILEPATH,'config','scores'))):
    os.makedirs(os.path.abspath(os.path.join(THIS_FILEPATH,'config','scores')))
if not os.path.exists(os.path.abspath(os.path.join(THIS_FILEPATH,'config','music'))):
    os.makedirs(os.path.abspath(os.path.join(THIS_FILEPATH,'config','music')))

    with open(os.path.abspath(os.path.join(THIS_FILEPATH,'config','music','track.txt')),'w') as f:
        f.write('Null track')
    with open(os.path.abspath(os.path.join(THIS_FILEPATH,'config','music','artist.txt')),'w') as f:
        f.write('Null artist')

class MainLoop():

    def __init__(self):
        self.connection_active = False
        self.bot_status_dict = {"connect_status":"Inactive",
                                "trivia_status":"Inactive"}
        self.bot_status_dict_init = {"connect_status":"Inactive",
                                "trivia_status":"Inactive"}

        self.tb = None


    def connect(self):
        self.tb = TriviaBot()  
        if self.tb.valid:
            #self.connect_button.setText("Disconnect")
            self.connection_active = True
            logging.debug("Starting connect loop")
            iternum = 0
            while self.tb.valid:
                iternum += 1
                if iternum % 1200 == 0:
                    # only update once every second
                    self.update_console() 
                self.tb.main_loop(command_line_mode = True)
                #QtCore.QCoreApplication.processEvents()
                time.sleep(1/120)
        else:
            #msg = QMessageBox()
            #msg.setWindowTitle("Error message")
            #msg.setText("Error message:\n%s" % self.tb.error_msg)
            print("Error message:\n%s" % self.tb.error_msg)
            #msg.exec_()

    def update_console(self):
        print("Connection status: %s" % self.bot_status_dict['connect_status'])
        print("Trivia status: %s" % self.bot_status_dict['trivia_status'])


"""
class MainWindow(QWidget):

    def update_gui(self):
        '''
        This takes all variables from the active tb 
        '''
        self.connect_status.setText(self.bot_status_dict['connect_status'])
        if self.bot_status_dict['connect_status'] == 'Active':
            self.connect_status.setStyleSheet("QLabel { color : green; }");    
        else:
            self.connect_status.setStyleSheet("QLabel { color : red; }");    

            
        try:
            self.bot_status_dict['trivia_status'] = self.tb.active_session.trivia_status
        except:
            self.bot_status_dict['trivia_status'] = "Inactive"
        self.trivia_status.setText(self.bot_status_dict['trivia_status'])
        if self.bot_status_dict['trivia_status'] == 'Active':
            self.trivia_status.setStyleSheet("QLabel { color : green; }");    
        elif self.bot_status_dict['trivia_status'] == 'Finished':
            self.trivia_status.setStyleSheet("QLabel { color : blue; }");    
        else:
            self.trivia_status.setStyleSheet("QLabel { color : red; }");    
            
        
        
        if self.tb:
            self.trivia_start_button.setVisible(True)
            if self.tb.trivia_active:
                self.category_label.setVisible(True)
                self.question_label.setVisible(True)
                self.answer_label.setVisible(True)
                self.top3_label.setVisible(True)
                self.top3_variable_text.setText(self.tb.active_session.check_top(3))
                if str(self.tb.active_session.session_config['music_mode']) == 'true' or self.tb.active_session.session_config['music_mode'] == True:
                    self.trivia_startq_button.setVisible(True)
                else:
                    self.trivia_skip_button.setVisible(True)
                if self.tb.active_session.session_config['mode'] == 'poll' or self.tb.active_session.session_config['mode'] == 'poll2':    
                    self.trivia_endq_button.setVisible(True)
                if self.tb.active_session.questionasked:
                    self.category_variable_text.setVisible(True)
                    self.question_variable_text.setVisible(True)
                    self.answer_variable_text.setVisible(True)
                    self.top3_variable_text.setVisible(True)
                    self.question_no_variable_text.setVisible(True)
                    self.category_variable_text.setText(self.tb.active_session.active_question.category)
                    self.question_variable_text.setText(self.tb.active_session.active_question.question)
                    self.answer_variable_text.setText(', '.join(self.tb.active_session.active_question.answers))
                    self.question_no_variable_text.setText(self.tb.active_session.report_question_numbers())
                else:
                    self.category_variable_text.setVisible(False)
                    self.question_variable_text.setVisible(False)
                    self.answer_variable_text.setVisible(False)
                    self.question_no_variable_text.setVisible(False)
                    self.category_variable_text.setText("")
                    self.question_variable_text.setText("")
                    self.answer_variable_text.setText("")
                    self.top3_variable_text.setText("")
                    self.question_no_variable_text.setText("")

        else:
            self.set_all_invisible()
            
        # special cases
        if self.bot_status_dict['trivia_status'] == "Finished":
            self.trivia_start_button.setText("Start Trivia")
            self.trivia_skip_button.setVisible(False)
            self.trivia_endq_button.setVisible(False)
            
    def set_all_invisible(self):
        self.category_label.setVisible(False)
        self.question_label.setVisible(False)
        self.answer_label.setVisible(False)            
        self.top3_label.setVisible(False)
        self.category_variable_text.setVisible(False)
        self.question_variable_text.setVisible(False)
        self.question_no_variable_text.setVisible(False)
        self.answer_variable_text.setVisible(False)
        self.top3_variable_text.setVisible(False)
        self.trivia_start_button.setVisible(False)
        self.trivia_skip_button.setVisible(False)
        self.trivia_startq_button.setVisible(False)
        self.trivia_endq_button.setVisible(False)
    
    def toggle_connect(self):
        logging.debug("Connect %s " % self.connection_active)
        if self.connection_active:
            self.bot_status_dict['connect_status'] = 'Inactive'
            self.bot_status_dict = self.bot_status_dict_init
            self.set_all_invisible()
            self.update_gui()
            self.end_connection()
        else:
            self.bot_status_dict['connect_status'] = 'Active'
            self.connect()
            
    def toggle_start_trivia(self):
        if not self.tb.active_session.trivia_active:
            self.trivia_start_button.setText("Stop Trivia")
            self.tb.start_session()
        else:
            self.trivia_start_button.setText("Start Trivia")
            self.tb.active_session.force_end_of_trivia()
        
    def skip_question(self):
        if self.tb.active_session.trivia_active:
            try:
                self.tb.active_session.skip_question()
            except:
                logging.debug("Error on skipping question : %s" % traceback.print_exc())
                
    def start_question(self):
        if self.tb.active_session.trivia_active:
            try:
                self.tb.active_session.start_question()
            except:
                logging.debug("Error on starting question : %s" % traceback.print_exc())
                
    def end_question(self):
        if self.tb.active_session.trivia_active:
            try:
                logging.info("Ending question")
                self.tb.active_session.end_question()
            except:
                logging.debug("Error on ending question : %s" % traceback.print_exc())
        
    def connect(self):
        self.tb = TriviaBot()  
        if self.tb.valid:
            self.connect_button.setText("Disconnect")
            self.connection_active = True
            logging.debug("Starting connect loop")
            iternum = 0
            while self.tb.valid:
                iternum += 1
                if iternum % 120 == 0:
                    # only update once every second
                    self.update_gui() 
                self.tb.main_loop(command_line_mode = False)
                QtCore.QCoreApplication.processEvents()
                time.sleep(1/120)
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Error message")
            msg.setText("Error message:\n%s" % self.tb.error_msg)
            msg.exec_()
            
    def hide_other_buttons(self):
        self.trivia_start_button.setVisible(False)
        self.trivia_skip_button.setVisible(False)
        self.trivia_endq_button.setVisible(False)
        self.trivia_startq_button.setVisible(False)
        self.trivia_start_button.setText("Start Trivia")
    def end_connection(self):
        logging.debug("Ending connection.")
        self.connection_active = False
        self.connect_button.setText("Connect")
        self.hide_other_buttons()
        self.tb.stop_bot()
"""


# SETTINGS
# TriviaBot object sets up and manages Session objects

class TriviaBot(object):

    def __init__(self):
        logging.debug("Begin setting up Trivia Bot...")
        self.valid = True
        self.trivia_active = False
        self.error_msg = ""
        self.active_session = NullSession()
        with open(os.path.join(THIS_FILEPATH,'config','trivia_config.yml'),'r') as f:
            temp_config = yaml.safe_load(f)
            self.validate_trivia_config(temp_config)
        with open(os.path.join(THIS_FILEPATH,'config','auth_config.yml'),'r') as f:
            temp_config = yaml.safe_load(f)
            self.validate_auth_config(temp_config)

        if self.valid:
            try:
                logging.debug("Setting up Chat Bot...")
                self.cb = ChatBot(self.auth_config)
            except:
                logging.debug("Failure to connect to Twitch chat. Check auth config and retry")
                self.valid = False
            self.admin_commands_list = {'!triviastart':self.start_session,
                                  '!stopbot':self.stop_bot,
                                  '!loadsession':self.load_trivia_session,
                                  '!savesession':self.save_trivia_session}

            self.commands_list = {'!score':self.check_active_session_score,
                                  '!scores':self.check_active_session_scores,
                                  '!flag':self.flag_current_question,
                                  '!stats':self.display_stats
                                }
            self.admins = [i.strip() for i in self.trivia_config['admins'].split(",")]
            self.ignore_users = [i.strip() for i in self.trivia_config['ignore_users'].split(",")]

            logging.debug("Finished setting up Trivia Bot.")
        else:
            logging.debug("Invalid setup - please check trivia_config.yml file")


    def validate_trivia_config(self,temp_config):
        for k, v in temp_config.items():
            if k == 'filename':
                if not v.endswith(".csv"):
                    self.error_msg = "Config error: Filename %s does not end with .csv" % v
                    logging.debug(self.error_msg)
                    self.valid = False
            elif k in ['question_count','hint_time1','hint_time2','skip_time','question_delay','question_bonusvalue']:
                if type(v) != int:
                    self.error_msg = "Config error: Error with %s -> %s not being an integer" % (k,v)
                    logging.debug(self.error_msg)
                    self.valid = False
            elif k == 'mode':
                if v not in ['single','poll','poll2']:
                    self.error_msg = "Config error: Mode must be 'single', 'poll', 'poll2'"
                    logging.debug(self.error_msg)
                    self.valid = False
            elif k == 'admins':
                if type(v) != str:
                    self.error_msg = "Config error: Admins must be text only, separated by commas"
                    logging.debug(self.error_msg)
                    self.valid = False
            elif k == 'order':
                if v not in ['random','ordered']:
                    self.error_msg = "Config error: Order must be 'ordered' or 'random' only"
                    logging.debug(self.error_msg)
                    self.valid = False
            elif k == 'music_mode':
                if type(v) != bool:
                    self.error_msg = "Config error: Music mode must be set to true or false"
                    logging.debug(self.error_msg)
                    self.valid = False
                if v == True:
                    if "poll2" not in temp_config['mode']:
                        self.error_msg = "Config error: When using music mode, mode 'poll2' must be chosen"
                        logging.debug(self.error_msg)
                        self.valid = False
                    if "infinite" not in temp_config['length']:
                        self.error_msg = "Config error: When using music mode, length 'infinite' must be chosen"
                        logging.debug(self.error_msg)
                        self.valid = False


        if self.valid:
            logging.debug("Passed trivia_config validation.")
            self.trivia_config = temp_config

    def validate_auth_config(self,temp_config):
        for k, v in temp_config.items():
            if k == 'host':
                if v != 'irc.twitch.tv':
                    logging.debug("Config issue: Host name %s is not default irc.twitch.tv - change at discretion only" % v)
            elif k == 'port':
                if int(v) != 6667:
                    logging.debug("Config issue: Port %s is not default 6667 - change at discretion only" % v)
            elif k == 'nick':
                if type(k) != str:
                    self.error_msg = "Config error: Bot name %s should be text string only" % v
                    logging.debug(self.error_msg)
                    self.valid = False
            elif k == 'pass':
                if "oauth:" not in v:
                    self.error_msg = "Config error: Invalid password %s. Password should be in format 'oauth:xxx'" % v
                    logging.debug(self.error_msg)
                    self.valid = False
            elif k == 'chan':
                if "#" in v or type(v) != str:
                    self.error_msg = "Config error: Invalid channel name %s. Channel name should be text only with NO number sign" % v
                    logging.debug(self.error_msg)
                    self.valid = False

        if self.valid:
            logging.debug("Passed auth_config validation.")
            self.auth_config = temp_config

    def start_session(self, start_new_override=True):
        logging.debug("Starting session...")
        if not self.trivia_active:
            if not self.active_session or start_new_override: #if there's already a session, ignore, unless from command
                self.active_session = Session(self.cb, self.trivia_config)
            self.active_session.trivia_status = "Active"
            logging.debug(self.active_session.trivia_status)
            self.cb.s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))

            # setup
            try:
                if self.active_session.question_count < 1:
                    self.cb.send_message("No questions were loaded. Check log for issue reporting and restart the trivia bot.")
                else:
                    if self.trivia_config['length'] == 'infinite':
                        self.cb.send_message("Trivia has begun! Infinite question mode. Trivia will start in %s seconds." % (self.active_session.session_config['question_delay']))
                    else:
                        self.cb.send_message("Trivia has begun! Question Count: %s. Trivia will start in %s seconds." % (self.active_session.question_count, self.active_session.session_config['question_delay']))

                    time.sleep(1)
                    self.cb.send_message("Hints will occur after %s seconds and %s seconds." % (self.active_session.session_config['hint_time1'], self.active_session.session_config['hint_time2']))

                    time.sleep(self.active_session.session_config['question_delay'])
                    # get first question, ask, then begin loop
                    self.active_session.trivia_active = True
                    self.trivia_active = True
                    self.active_session.call_question()

            except:
                logging.debug("Error on session %s" % traceback.print_exc())
        else:
            logging.debug("Trivia active - ignoring command to begin session.")

    def save_trivia_session(self):
        '''
        dump trivia session to pickle file
        '''
        if self.active_session and self.trivia_active:
            if self.active_session.trivia_active:
                save_session = self.active_session
                save_session.cb = None
                with open('latest_session.p', 'wb') as p:
                    pickle.dump(save_session,p)
                self.active_session.cb = self.cb
                logging.debug("Latest trivia session saved.")
        else:
            logging.debug("No trivia session saved.")

    def load_trivia_session(self):
        '''
        load trivia session to pickle file
        '''
        if not self.trivia_active:
            try:
                with open('latest_session.p', 'rb') as p:
                    load_session = pickle.load(p)
                    load_session.cb = self.cb
                    self.active_session = load_session

                logging.debug("Latest trivia session loaded.")
                self.cb.send_message("Latest trivia session loaded. Beginning trivia...")
            except:
                logging.debug("Unable to load session, file not found.")
                self.cb.send_message("No previous session found.")
            self.start_session(False)

        else:
            if self.trivia_active:
                logging.debug("Trivia session active, cannot load during session.")
            else:
                logging.debug("No trivia session loaded.")

    def stop_bot(self):
        self.cb.send_message("Ending trivia bot. See you next trivia session!")
        self.valid = False
        try:
            self.active_session.valid = False
            self.active_session.trivia_active = False
        except:
            pass


    def handle_triviabot_message(self,username, message):
        '''
        This is the main function that decides what to do based on the latest message that came in
        For the TRIVIA BOT, primarily used for commands
        '''
        if message:
#            user = self.check_user(username) ########## TO DO

            # Split out the message into "<COMMAND> <ARGS>", assume a command starts the message, and all commands that we respond to starte with !
            words = message.split()

            if words[0].startswith('!'):
                # Potential command
                cmd = words[0]
                msg = " ".join(words[1:])

                #print("Command %s message %s" % (cmd, msg))

                if cmd in self.admin_commands_list.keys() and username in self.admins:
                    func = self.admin_commands_list[cmd]

                    if cmd == '!score':
                        func(username)
                    else:
                        func()

                if cmd in self.commands_list.keys():
                    func = self.commands_list[cmd]
                    if cmd == '!flag':
                        func(username, msg)
                    elif cmd == '!score':
                        func(username)
                    else:
                        func()

    def check_active_session_score(self, username):
        '''
        If there's an active session that has not yet been replaced (meaning, the last active 
        session after a game is over), this will allow users to call their scores
        '''
        if self.active_session != None and not self.active_session.trivia_active:
            user = self.active_session.check_user(username)
            # anti spam measure
            if user.validate_message_time():
                if user:
                    self.active_session.check_user_score(user, from_trivia_bot=True)
                else:
                    self.cb.send_message("%s had no points in the last game." % (username))

    def check_active_session_scores(self):
        '''
        If there's an active session that has not yet been replaced (meaning, the last active 
        session after a game is over), this will allow users to call their scores
        '''
        if self.active_session != None and not self.active_session.trivia_active:
            user = self.active_session.check_user(username)
            # anti spam measure
            if user.validate_message_time():
                self.active_session.check_top_scores()

    def flag_current_question(self, username, msg):
        if self.active_session != None and self.active_session.trivia_active:
            logging.debug("Q#%d: %s - flagged by user %s comment: %s" % (self.active_session.questionno, self.active_session.active_question.question_string, username, msg))

    def display_stats(self):
        if self.active_session != None and self.active_session.trivia_active:
            stats = "Trivia Session: Active Questions: %d Asked: %d Answered: %d Players: %d" % ( len(self.active_session.questions),
                                                                        int(self.active_session.questionno),
                                                                        len(self.active_session.answered_questions),
                                                                        len(self.active_session.users) )
        else:
            stats = "Trivia Session: Inactive"

        self.cb.send_message(stats)

    def handle_active_session(self):
        username, message, clean_message = self.cb.retrieve_messages()

        self.handle_triviabot_message(username, clean_message)
        if message and username !='tmi' and username not in self.ignore_users:
            logging.debug(username)
            logging.debug(self.cb.bot_config['nick'])
            logging.debug("Message received:\n%s " % message)
        self.active_session.check_actions()
        if self.active_session.session_config['mode'] == 'poll' or self.active_session.session_config['mode'] == 'poll2':
            self.active_session.manage_poll_question()
        self.active_session.handle_session_message(username, clean_message)

    def main_loop(self, command_line_mode = True):
        '''
        The main loop is always running from the start
        While trivia is not active, it will check only handle_triviabot_message for incoming messages
        While trivia is active, it will delegate to the active session
        '''

        if command_line_mode:
            iternum = 0
            while self.valid:
                iternum += 1
                if iternum % 1200 == 0:
                    try:
                        logging.debug("Iternum %s : trivia_active %s active_session.trivia_active %s" % (iternum, self.trivia_active, self.active_session.trivia_active))
                    except:
                        logging.debug("Iternum %s : %s" % (iternum, self.trivia_active))

                if self.active_session.trivia_active:
                    self.handle_active_session()
                else:
                    username, message, clean_message = self.cb.retrieve_messages()

                    if message and username !='tmi' and username not in self.ignore_users:
                        logging.debug(username)
                        logging.debug(self.cb.bot_config['nick'])
                        logging.debug("Message received:\n%s " % message)


                    if message:
                        if not self.trivia_active: #when a session is NOT running
                            self.handle_triviabot_message(username, clean_message)


                    if self.trivia_active: # when a session is running
                        # check every iteration if trivia is active or not, to set the trivia bot to be inactive
                        if not self.active_session.trivia_active:
                            logging.debug("Setting trivia to inactive based on active_session...")
                            self.trivia_active = False
                        pass




                time.sleep(1 / 120)
            logging.debug("Trivia bot no longer valid, ending program.")
        else:
            # when not in command line mode, the window program will handle the looping
            if self.active_session.trivia_active:
                self.handle_active_session()
            else:
                username, message, clean_message = self.cb.retrieve_messages()

                if message and username !='tmi':
                    logging.debug(username)
                    logging.debug(self.cb.bot_config['nick'])
                    logging.debug("Message received:\n%s " % message)


                if message:
                    if not self.trivia_active: #when a session is NOT running

                        # if theres a command thats recognized, the loop may happen elsewhere
                        # this happens with !triviastart
                        self.handle_triviabot_message(username, clean_message)


                if self.trivia_active: # when a session is running
                    # check every iteration if trivia is active or not, to set the trivia bot to be inactive
                    if not self.active_session.trivia_active:
                        logging.debug("Setting trivia to inactive based on active_session...")
                        self.trivia_active = False
                    pass



class NullSession():
    trivia_active = False
    trivia_status = "Inactive"

class Session(object):

    def __init__(self, cb, trivia_config):
        logging.debug("Begin setting up Session...")
        logging.debug("Setting up session constants...")
        self.cb = cb
        self.userscores = {}                         # Dictionary holding user scores, kept in '!' and loaded/created upon trivia. [1,2,3] 1: Session score 2: Total trivia points 3: Total wins
        self.SWITCH = True                           # Switch to keep bot connection running
        self.trivia_active = False                   # Switch for when trivia is being played
        self.questionasked = False            # Switch for when a question is actively being asked
        self.questionasked_time = 0           # Time when the last question was asked (used for relative time length for hints/skip)
        self.questionno = 1                  # Question # in current session
        self.answervalue = 1                 # How much each question is worth (altered by BONUS only)
        self.question_count = 0
        self.questions = []
        self.answered_questions = []
        self.active_question = None
        self.trivia_status = "Inactive"
        self.users = []
        self.admin_commands_list = {'!triviaend':self.force_end_of_trivia,
                                    '!skip':self.skip_question,
                                    '!start':self.start_question,
                                    '!endquestion':self.end_question,
                                    '!next':self.skip_question,
                                    '!bonus':self.toggle_bonus_mode}
        self.commands_list       = {'!score':self.check_user_score,
                                    '!scores':self.check_top_scores,
                                    '!flag':self.flag_current_question}
        self.session_actions = {'hint1':self.call_hint1,
                                'hint2':self.call_hint2,
                                'skip':self.skip_question}

        self.TIMER = 0                               # Ongoing active timer
        self.bonus_round = False


        logging.debug("Loading config...")
        self.session_config = trivia_config
        self.admins = [i.strip() for i in trivia_config['admins'].split(",")]
        self.ignore_users = [i.strip() for i in trivia_config['ignore_users'].split(",")]
        out_str = ''
        for k, v in self.session_config.items():
            out_str += "   " + "{:<20}".format(k)+ " " + str(v) + "\n"
        logging.debug(out_str)
        self.valid = True
        try:
            if self.session_config['music_mode']:
                # in music mode, do not load a trivia set, instead do nothing
                self.question_count = 99999
                self.ts = {}
                self.ss = {}

            else:
                logging.debug("Loading trivia data...")
                try:
                    with open(os.path.join(THIS_FILEPATH,'config',self.session_config['file_name']),'r',encoding=self.session_config['csv_encoding']) as f:
                        data_source = f.read()
                    data = csv.reader(data_source.splitlines(),quotechar='"', delimiter=',',quoting=csv.QUOTE_ALL, skipinitialspace=True)
                except:
                    logging.debug("Error on reading csv file. Check encoding format set in trivia_config is the same as csv file")
                self.ts = {}
                for idx, i in enumerate(data):
                    try:
                        answer, answer2, answer3, answer4, answer5 = None, None, None, None, None
                        if len(i) == 8:
                            category, question, answer, answer2, answer3, answer4, answer5, creator = i
                        elif len(i) == 5:
                            category, question, answer, answer2, creator = i
                        else:
                            category, question, answer = i
                            creator = 'Anon'
                        if question.lower() == 'question':
                            logging.debug("Data line was ignored for csv header")
                        elif answer != '' and category != '' and question != '':
                            self.ts[idx] = {'category':category, 'question':question, 'answer':answer,'answer2':answer2, 'answer3':answer3, 'answer4':answer4, 'answer5':answer5,'creator':creator}
                        else:
                            logging.debug("Data line was ignored, make sure category, question and answer are non null fields: %s" % i)
                    except Exception as e:
                        logging.debug("Error on data line, check number of fields: %s" % i)
                        logging.debug("Exception: %s " % e)

                if self.session_config['mode'] == 'poll2':
                    logging.debug("Mode set to poll2, only taking questions with valid answer/answer2...")
                    valid_keys = [i for i in self.ts if self.ts[i]['answer2'] != '']
                    new_ts = {}
                    for i in valid_keys:
                        new_ts[i] = self.ts[i]
                    self.ts = new_ts

                self.tsrows = len(self.ts.keys())


                if self.tsrows < self.session_config['question_count']:
                    self.session_config['question_count'] = int(self.tsrows)
                    logging.debug("Warning: Trivia questions for session exceeds trivia set's population. Setting session equal to max questions.")

                logging.debug("Creating session set data. Population %s, session %s" % (self.tsrows, self.session_config['question_count']))

                if self.session_config['category_distribution'] == 'random':
                    self.create_random_trivia_set()
                elif self.session_config['category_distribution'] == 'distributed':
                    self.create_distributed_trivia_set()
                try:

                    for k, v in self.ss.items():
                        try:
                            self.questions.append(Question(v, self.session_config))
                        except Exception as e:
                            logging.debug("Error %s -> %s on question creation: %s" % (k,v,e))
                except Exception as e:
                    logging.debug("Error %s on question creation" % e)
                if self.session_config['length'] == 'infinite':
                    self.question_count = 999999
                else:
                    self.question_count = len(self.questions)

                logging.debug("Finished setting up Session.")

        except Exception as e:
            logging.debug("Error on data load. Check trivia set and make sure file_name matches in config, and that file matches columns/headers correctly\nError code:\n>> %s" % e)
            self.valid = False

        if str(self.session_config['output']).lower() == 'true' or self.session_config['output'] == True:
            for i in ['1_place_username','1_place_score','2_place_username','2_place_score','3_place_username','3_place_score','scoreboard']:
                with open(os.path.join(THIS_FILEPATH,'config','scores','%s.txt' % i),'w') as f:
                    f.write('')

    def create_random_trivia_set(self):
        chosen_idx = random.sample(list(self.ts.keys()), int(self.session_config['question_count']))
        if self.session_config['order'] == 'ordered':
            chosen_idx.sort()
        self.ss = {}
        for i in chosen_idx:
            self.ss[i] = self.ts[i]

    def create_distributed_trivia_set(self):

        # with open('temp.pickle','rb') as p:
        #     data = pickle.load(p)

        # determine how much to first sample the data
        data = self.ts
        data_len = len(data)

        if self.session_config['length'] == 'infinite':
            question_count = data_len
        else:
            question_count = self.session_config['question_count']
            if question_count > data_len:
                question_count = data_len

        order = self.session_config['order']

        print("Trivia Set: %d, Question Count: %d " % (data_len, question_count))

        first_sample = 0
        if (question_count / data_len) < .3:
            first_sample = int(data_len / 3)
        elif (question_count / data_len) < .5:
            first_sample = int(data_len / 2)
        if first_sample < question_count:
           first_sample = question_count


        print("LEN %s" % first_sample)

        data_set = {}
        category_counts = {}
        # first initialize each category for 0 count

        def report_mean(c):
            return float(sum(c.values()) / len(c.values())) + 1


        # create first sampled set
        data_set_sample1 = {}
        chosen_idx = random.sample(list(data.keys()), int(first_sample))
        # print("LEN 2 %s" % len(chosen_idx))
        if order == 'ordered':
            chosen_idx.sort()
        for i in chosen_idx:
            data_set_sample1[i] = data[i]

        for k, v in data_set_sample1.items():
            category_counts[v['category']] = 0

        iter_num = 0
        placed_num = 0
        while iter_num < 10000 and placed_num < question_count:
            for k, v in data_set_sample1.items():
                # get category_count
                reported_mean = report_mean(category_counts)
                category_report = category_counts[v['category']]
                flag_a = category_report <= reported_mean
                flag_b = category_report == 0
                # print("%s %s %s %s" % (category_report, reported_mean, flag_a, flag_b))
                if flag_a or flag_b:
                    print("adding category %s" % v['category'])
                    if k not in data_set.keys():
                        data_set[k] = v
                        category_counts[v['category']] = category_counts[v['category']] + 1
                        placed_num += 1
                        if placed_num >= question_count:
                            print("Break by placed_num >= question_count")
                            break

                iter_num += 1
                if iter_num >= 10000:
                    print("Break by iter_num")
                    break
        print("ITER %s PLACED %s" % (iter_num,placed_num))
        # final shuffle
        data_set_final = {}
        data_set_keys = list(data_set.keys())
        random.shuffle(data_set_keys)
        # data_set_keys = random.sample(data_set_keys,int(self.session_config['question_count']))

        for i in data_set_keys:
            data_set_final[i] = data_set[i]


        self.ss = data_set_final
        print(len(data_set_final.keys()))
        logging.debug("Category counts breakdown:")
        for k, v in category_counts.items():
            logging.debug("%s %s" % ("{:50}".format("%s:" % k), v))


    def flag_current_question(self, user):
        try:
            return self.cb.flag_current_question(self, user)
        except:
            pass

    def call_current_time(self):
        return datetime.datetime.now()

    def report_question_numbers(self):
        if self.session_config['length'] == 'infinite':
            return "%s / %s" % (self.questionno, "inf")
        else:
            return "%s / %s" % (self.questionno, self.question_count)

    def call_question(self):
        if self.session_config['music_mode']:
            try:
                # create the question based on config/music/ contents each time
                with open(os.path.join(THIS_FILEPATH,'config','music','artist.txt'),'r') as f:
                    artist = f.read()
                with open(os.path.join(THIS_FILEPATH,'config','music','track.txt'),'r') as f:
                    track = f.read()
                self.active_question = Question([artist,track],self.session_config,music_mode=True)
                self.active_question.activate_question(self.bonus_round, int(self.session_config['question_bonusvalue']))
                self.questionasked = True
                self.cb.send_message("Question %s: %s" % (self.questionno, self.active_question.question_string))
                logging.debug(self.active_question)
            except Exception as e:
                logging.debug("Error on calling next question, ending trivia...%s" % str(e))
                self.force_end_of_trivia()
        else:
            try:
                self.active_question = self.questions.pop()
                if self.session_config['length'] == 'infinite':
                    # add the question back, to the start of the index (so its not popped next)
                    self.questions = [self.active_question] + self.questions
                self.active_question.activate_question(self.bonus_round, int(self.session_config['question_bonusvalue']))
                self.questionasked = True
                self.cb.send_message("Q#%s: %s" % (self.questionno, self.active_question.question_string))
                logging.debug(self.active_question)
            except:
                logging.debug("Error on calling next question, ending trivia...")
                self.force_end_of_trivia()
        self.write_question_variable()


    def question_answered(self, user, answer_slot=None):
        if self.session_config['mode'] == 'single':
            user.points += self.active_question.point_value
            self.active_question.active = False
            self.answered_questions.append(self.active_question)
            self.cb.send_message(self.active_question.answer_string(user, self.questionno))
            self.questionno += 1
            self.questionasked = False
            time.sleep(self.session_config['question_delay'])
            if self.questionno < self.question_count + 1:
                try:
                    self.call_question()
                except:
                    logging.debug("Error on question call %s" % traceback.print_exc() )
            else:
                self.force_end_of_trivia()

        elif self.session_config['mode'] == 'poll':
            if user not in self.active_question.answered_user_list:
                self.active_question.answered_user_list.append(user)
        elif self.session_config['mode'] == 'poll2':
            if answer_slot == 1:
                if user not in self.active_question.answered_user_list:
                    self.active_question.answered_user_list.append(user)
            elif answer_slot == 2:
                if user not in self.active_question.answered_user_list2:
                    self.active_question.answered_user_list2.append(user)
        if str(self.session_config['output']).lower() == 'true' or self.session_config['output'] == True:
            self.output_session_variables()

        self.clear_question_variable()


    def write_question_variable(self):
        try:
            with open(os.path.join(THIS_FILEPATH,'config','scores','question.txt'),'w') as f:
                f.write(self.active_question.question_string)
        except:
            logging.error("Error on write question to file")


    def clear_question_variable(self):
        try:
            with open(os.path.join(THIS_FILEPATH,'config','scores','question.txt'),'w') as f:
                f.write("")
        except:
            logging.error("Error on write question to file")


    def output_session_variables(self):
        try:
            user_dict = {}
            for u in self.users:
                user_dict[u.username] = u.points
            if user_dict:
                k = Counter(user_dict)
                top3 = k.most_common(3)
                for idx, i in enumerate(top3):
                    with open(os.path.join(THIS_FILEPATH,'config','scores','%s_place_username.txt' % (int(idx) + 1)),'w') as f:
                        f.write(str(i[0]))
                    with open(os.path.join(THIS_FILEPATH,'config','scores','%s_place_score.txt' % (int(idx) + 1)),'w') as f:
                        f.write(str(i[1]))

                return_str = ''
                for k, v in user_dict.items():
                    return_str += '%s: %s\n' % (k,v)
                with open(os.path.join(THIS_FILEPATH,'config','scores','scoreboard.txt'),'w') as f:
                    f.write(return_str)


        except:
            logging.debug("Error on output session variables method (score txt files) %s" % traceback.print_exc())

    def check_user(self,username):
        '''
        This checks the username and returns the User object that matches
        '''
        for user in self.users:
            if user.username == username:
                logging.debug("Returning found user %s" % username)
                return user
        else:
            logging.debug("Creating new user %s" % username)
            new_user = User(username)
            self.users.append(new_user)
            return new_user

    def check_user_score(self, user, from_trivia_bot = False):
        if not from_trivia_bot:
            if user.validate_message_time():
                self.cb.send_message("User %s has %s points." % (user.username, user.points))
        else:
            self.cb.send_message("User %s had %s points last game." % (user.username, user.points))


    def check_top_scores(self):
        self.cb.send_message("Top scores in current game: %s" % self.check_top(5))


    def check_top(self, num = 3):
        user_dict = {}
        for u in self.users:
            user_dict[u.username] = u.points
        if user_dict:
            k = Counter(user_dict)
            top = k.most_common(num)
            return_str = ''
            for i in top:
                return_str += '%s: %s ' % (i[0], i[1])
            return return_str
        else:
            return "No users playing"


    def force_end_of_trivia(self):
        self.check_end_of_trivia(end_trivia_flag=True)


    def check_end_of_trivia(self, end_trivia_flag = False):
        if (self.questionno > self.question_count and self.trivia_active) or end_trivia_flag:
            self.write_question_variable()
            logging.debug("Ending trivia...")
            self.trivia_active = False
            self.find_winner()
            if self.winners:
                try:
                    if len(self.winners) > 1:
                        winners_string = ', '.join([i.username for i in self.winners])
                        self.cb.send_message("Trivia is over - a tie between %s for %s points!" % (winners_string, self.winners[0].points))
                    else:
                        winner = self.winners[0]
                        self.cb.send_message("Trivia is over - %s wins with %s points!" % (winner.username, winner.points))
                except:
                    self.cb.send_message("Error on calculating winners: %s" % (self.winners))
            else:
                self.cb.send_message("Trivia is over - no winner found.")
            time.sleep(.5)
            self.cb.send_message("Thanks for playing!")
            self.trivia_status = "Finished"
            return True
        else:
            return False

    def find_winner(self):
        top_score = 0
        for user in self.users:
            if user.points > top_score:
                top_score = user.points

        # now check if there's more than 1 winner
        winners = [user for user in self.users if user.points == top_score]

        if not winners or top_score == 0:
            winners = None

        self.winners = winners

    def call_hint1(self):
        try:
            if self.questionasked and self.active_question.hint_1:
                self.cb.send_message("Hint: %s " % self.active_question.hint_1)
        except:
            logging.debug("Error on hint 1 %s" % traceback.print_exc())
    def call_hint2(self):
        try:
            if self.questionasked and self.active_question.hint_2:
                self.cb.send_message("Hint: %s " % self.active_question.hint_2)
        except:
            logging.debug("Error on hint 1 %s" % traceback.print_exc())


    def skip_question(self):
        try:

            ans = ''
            if self.session_config['skip_show_answer']:
                ans = "The answer was  ** %s **." % self.active_question.answers[0]

            self.cb.send_message("Question being skipped. %s" % ans)
            self.active_question.active = False
            self.answered_questions.append(self.active_question)
            self.questionno += 1
            self.questionasked = False
            time.sleep(self.session_config['question_delay'])
            if self.questionno < self.question_count + 1:
                try:
                    self.call_question()
                except:
                    logging.debug("Error on question call %s" % traceback.print_exc() )
            else:
                self.force_end_of_trivia()

        except:
            logging.debug("Error on skip question %s" % traceback.print_exc())

    def start_question(self):
        try:
            if not self.active_question.active:
                self.call_question()
            else:
                logging.debug("Question already active, ignoring Start Q command")
        except:
            logging.debug("Error on start question %s" % traceback.print_exc())

    def end_question(self):
        try:
            self.active_question.question_time_start = datetime.datetime(1990,1,1)


        except:
            logging.debug("Error on skip question %s" % traceback.print_exc())

    def manage_poll_question(self):
        adjuster = datetime.timedelta(seconds = self.session_config['skip_time'])
        adj_time = self.active_question.question_time_start + adjuster
        cur_time = self.call_current_time()
        if adj_time < cur_time and self.active_question.active:
            logging.debug("Scoring current question for poll")
            self.active_question.find_poll_score()
            self.active_question.active = False
            self.answered_questions.append(self.active_question)
            if self.active_question.point_dict:
                first_user = list(self.active_question.point_dict.keys())[0]
                for user in self.active_question.point_dict:
                    user.points += self.active_question.point_dict[user]
                self.answered_questions.append(self.active_question)
                self.cb.send_message(self.active_question.answer_string_poll(first_user, self.active_question.point_dict[first_user], self.questionno))
            else:
                ans = ''
                if self.session_config['skip_show_answer']:
                    ans = "The answer was  ** %s **." % self.active_question.answers[0]
                self.cb.send_message("Question not answered in time. %s" % ans)

            if self.active_question.session_config['mode'] == 'poll2':

                time.sleep(.25)
                # first score second question
                if self.active_question.point_dict2:
                    try:
                        first_user = list(self.active_question.point_dict2.keys())[0]
                        for user in self.active_question.point_dict2:
                            user.points += self.active_question.point_dict2[user]
                        time.sleep(.5)
                        self.cb.send_message(self.active_question.answer_string_poll2(first_user, self.active_question.point_dict2[first_user], self.questionno))
                    except:
                        logging.debug("Error on second question poll, ignoring.")
                else:
                    self.cb.send_message("2nd category question not answered in time. The answer was ** %s **." % self.active_question.answers[1])

                # then bonus points for both

                bonus_users = []
                for user in self.active_question.point_dict.keys():
                    if user in self.active_question.point_dict2.keys():
                        bonus_users.append(user)
                        user.points += 2

                if bonus_users:
                    time.sleep(.25)
                    if len(bonus_users) > 3:
                        self.cb.send_message("More than 3 players answered both prompts correctly, yielding +2 bonus points!")
                    else:
                        self.cb.send_message("%s answered both prompts correctly, yielding +2 bonus points!" % ', '.join([user.username]))
            self.questionno += 1
            self.questionasked = False

            # if music_mode is True, then do nothing after a question is answered
            if self.session_config['music_mode']:
                pass
            else:
                time.sleep(self.session_config['question_delay'])
                if self.questionno < self.question_count + 1:
                    try:
                        self.call_question()
                    except:
                        logging.debug("Error on question call %s" % traceback.print_exc() )
                else:
                    self.force_end_of_trivia()

    def check_actions(self):
        try:
            # first check the question object by seeing if a hint or timeout needs to occur
            action = self.active_question.check_actions()
            if action:
                if action in self.session_actions.keys():
                    func = self.session_actions[action]
                    func()
        except:
            logging.debug("Error on check_actions: %s" % traceback.print_exc())

    def toggle_bonus_mode(self):
        if self.bonus_round:
            self.bonus_round = False
            self.active_question.point_value = 1
            self.cb.send_message("Bonus round disabled. Trivia questions worth 1 point." )
        else:
            self.bonus_round = True
            self.active_question.point_value = int(self.session_config['question_bonusvalue'])
            self.cb.send_message("Bonus round is active! Bonus questions are worth ** %s ** points!" % (self.session_config['question_bonusvalue']))

    def handle_session_message(self,username, message):
        '''
        This is the main function that decides what to do based on the latest message that came in
        For the SESSION
        '''
        self.check_end_of_trivia()
        if message:
            logging.debug("Session vars trivia_active: %s questionasked: %s" % (self.trivia_active, self.questionasked))


            # handle commands first
            if message in self.admin_commands_list.keys() and username in self.admins:
                func = self.admin_commands_list[message]
                func()


            if username not in self.ignore_users:

                user = self.check_user(username)

                if message in self.commands_list:
                    func = self.commands_list[message]

                    if message == '!score' or message == '!flag':
                        func(user)
                    else:
                        func()

                # trivia active
                if self.trivia_active:
                    if self.questionasked:
                        if self.session_config['mode'] == 'poll2':
                            match, answer_slot = self.active_question.check_match(message)
                            if match:
                                self.question_answered(user, answer_slot)
                        else:
                            match = self.active_question.check_match(message)
                            if match:
                                self.question_answered(user)

        else:
            return None




class Question(object):
    '''
    Takes a row from the session set dataframe and converts into object
    '''
    def __init__(self, row, session_config,music_mode=False):
        self.session_config = session_config
        self.active = False
        if music_mode:
            self.question = "Listen to audio..."
            self.answers = [row[0],row[1]]
            self.answers = [i for i in self.answers if i != '']
            self.category = "Music"
            self.creator = ''
        else:
            self.question = str(row['question'][0]).upper() + row['question'][1:]
            self.answers = [row['answer'],row['answer2'],row['answer3'],row['answer4'],row['answer5']]
            self.answers = [i for i in self.answers if i != '' and i is not None]
            self.answers = [i for i in self.answers if i == i]
            self.category = row['category']
            if 'category' in row:
                self.creator = row['creator']

        if self.session_config['mode'] == 'poll2':
            try:
                answers_temp = [self.answers[0], self.answers[1]]
            except:
                logging.debug("ERROR ON PARSING QUESTION WITH ANSWER/ANSWER2, CHECK TRIVIA SOURCE")

        self.question_string = "%s: %s" % (self.category, self.question)
        self.point_value = 1
        self.set_hints()
        self.hint1_asked = False
        self.hint2_asked = False
        self.skipped = False
        self.answered_user_list =[] # this is an ordered list used for polling multiple answers as they come in
        self.answered_user_list2 =[] # same, but for 2nd during 'poll2' mode

    def activate_question(self, bonus_flag, bonus_amount):
        self.active = True
        self.question_time_start = datetime.datetime.now() # datetime object
        if bonus_flag:
            self.point_value = bonus_amount

    def __str__(self):
        return "{:<10}".format("Category:") + str(self.category) + "\n" +\
                "{:<10}".format("Question:") + str(self.question) + "\n" +\
                "{:<10}".format("Answers:") + str(self.answers) + "\n" +\
                "{:<10}".format("Hints:") + str(self.hint_1) + " - " + str(self.hint_2)

    def check_match(self, cleanmessage, mode=None):
        if self.session_config['mode'] != 'poll2':

            try:
                for answer in self.answers:
                    #logging.debug("Checking user response %s against stored answer: %s" % (cleanmessage, re.escape(answer)))
                    # Match answer, allow trailing comments
                    if bool(re.match(r"\b%s(\b|$)*" % re.escape(answer), cleanmessage, re.IGNORECASE)):
                        logging.debug("Answer recognized: %s" % answer)
                        return True
                return False
            except:
                logging.debug("No match on %s to %s" % (cleanmessage, answer))
                return False

        else:
            # for poll2, we check each answer for a match and return
            try:
                if bool(re.match("\\b%s\\b" % self.answers[0],cleanmessage,re.IGNORECASE)):   # strict new matching
                    logging.debug("Answer recognized: %s" % self.answers[0])
                    return True, 1 # answer_slot 1
                elif bool(re.match("\\b%s\\b" % self.answers[1],cleanmessage,re.IGNORECASE)):   # strict new matching
                    logging.debug("Answer recognized: %s" % self.answers[0])
                    return True, 2 # answer_slot 1
                return False, None
            except:
                logging.debug("Try/except error, no match on %s to %s" % (cleanmessage, answer))
                return False, None

    def answer_string(self,user, trivia_num):
        return "%s answers question #%s correctly! The answer is ** %s ** with a %s point value. %s has %s points!" % (user.username, trivia_num ,self.answers[0], self.point_value, user.username, user.points)

    def answer_string_poll(self,user, point_val, trivia_num):
        if self.answered_user_list_remaining:
            return "%s answers question #%s first correctly! The answer is ** %s ** with a %s point value. %s has %s points! Others who answered: %s" % (user.username, trivia_num ,self.answers[0], point_val, user.username, user.points, ', '.join(self.answered_user_list_remaining))
        else:
            return "%s answers question #%s first correctly! The answer is ** %s ** with a %s point value. %s has %s points!" % (user.username, trivia_num ,self.answers[0], point_val, user.username, user.points)

    def answer_string_poll2(self,user, point_val, trivia_num):
        if self.answered_user_list_remaining:
            return "%s answers question (2nd category) #%s first correctly! The answer is ** %s ** with a %s point value. %s has %s points! Others who answered: %s" % (user.username, trivia_num ,self.answers[1], point_val, user.username, user.points, ', '.join(self.answered_user_list_remaining))
        else:
            return "%s answers question (2nd category) #%s first correctly! The answer is ** %s ** with a %s point value. %s has %s points!" % (user.username, trivia_num ,self.answers[1], point_val, user.username, user.points)

    def set_hints(self):
    # type 0, replace 2 out of 3 chars with _
        prehint = str(self.answers[0])
        listo = []
        hint = ''
        counter = 0
        for i in prehint:
            if counter % 3 >= 0.7 and i != " ":
                listo += "▯"
            else:
                listo += i
            counter += 1
        for i in range(len(listo)):
            hint += hint.join(listo[i])

        if hint != prehint:
            self.hint_1 = hint
        else:
            self.hint_1 = ''

        hint2 = re.sub('[aeiou]','▯',prehint,flags=re.I)

        if hint2 != prehint:
            self.hint_2 = hint2
        else:
            self.hint_2 = ''

    def check_actions(self):
        time_since_question_asked = (datetime.datetime.now() - self.question_time_start).seconds

        if (time_since_question_asked >= self.session_config['hint_time1']) and not self.hint1_asked:
            self.hint1_asked = True
            return 'hint1'

        elif (time_since_question_asked >= self.session_config['hint_time2']) and not self.hint2_asked:
            self.hint2_asked = True
            return 'hint2'

        elif (time_since_question_asked >= self.session_config['skip_time']) and not self.skipped and self.session_config['mode'] == 'single':
            # do not skip on mode 'poll', other process handles
            self.skipped = True
            return 'skip'

        else:
            return None
    def find_poll_score(self):
        '''
        for 'poll'/'poll2' mode, this takes the answered_user_list and translates into points

        first gets n + 2 points
        second gets n + 1 points
        all others get n points
        where
        n = original point value
        '''
        self.point_dict = {}
        self.answered_user_list_remaining = []
        try:
            if self.answered_user_list:
                self.answered_user_list = self.answered_user_list[::-1]
                self.point_dict = {self.answered_user_list.pop():self.point_value + 2}
                self.answered_user_list_remaining = [i.username for i in self.answered_user_list]
                try:
                    self.point_dict[self.answered_user_list.pop()] = self.point_value + 1
                except:
                    pass
                try:
                    for k in self.answered_list:
                        self.point_dict[k] = self.point_value
                except:
                    pass
            else:
                pass
        except:
            logging.debug("Error on find_poll_score: %s" % traceback.print_exc())


        # do additional scoring if mode is poll2
        if self.session_config['mode'] == 'poll2':
            self.point_dict2 = {}
            self.answered_user_list_remaining2 = []
            try:
                if self.answered_user_list2:
                    self.answered_user_list2 = self.answered_user_list2[::-1]
                    self.point_dict2 = {self.answered_user_list2.pop():self.point_value + 2}
                    self.answered_user_list_remaining2 = [i.username for i in self.answered_user_list2]
                    try:
                        self.point_dict2[self.answered_user_list2.pop()] = self.point_value + 1
                    except:
                        pass
                    try:
                        for k in self.answered_list2:
                            self.point_dict2[k] = self.point_value
                    except:
                        pass
                else:
                    pass
            except:
                logging.debug("Error on find_poll_score: %s" % traceback.print_exc())


class User(object):
    def __init__(self,username):
        self.points = 0
        self.username = username
        self.last_msg_time = datetime.datetime.now()
    def validate_message_time(self):
        if self.last_msg_time + datetime.timedelta(seconds=1) < datetime.datetime.now():
            self.last_msg_time = datetime.datetime.now()
            logging.debug("Validate message time and reset")
            return True
        else:
            return False


class ChatBot(object):
    '''
    ChatBot is solely responsible for sending and reporting messages
    '''
    def __init__(self, auth_config):
        self.infomessage = INFO_MESSAGE
        try:
            self.valid = True
            self.bot_config = auth_config

            self.connect()

        except Exception as e:
            logging.debug("Connection failed. Check config settings and reload bot.\nError code:\n%s" % str(e))
            self.valid = False
        logging.debug("Finished setting up Chat Bot.")

    def connect(self):
        try:
            self.s = socket.socket()
            self.s.connect((self.bot_config['host'], self.bot_config['port']))
            self.s.send("PASS {}\r\n".format(self.bot_config['pass']).encode("utf-8"))
            self.s.send("NICK {}\r\n".format(self.bot_config['nick']).encode("utf-8"))
            self.s.send("JOIN #{}\r\n".format(self.bot_config['chan']).encode("utf-8"))
            time.sleep(1)
            self.send_message(self.infomessage)
            self.s.setblocking(0)
        except:
            self.s = socket.socket()
            self.s.connect((self.bot_config['host'], self.bot_config['port']))
            self.s.send("PASS {}\r\n".format(self.bot_config['pass']).encode("utf-8"))
            self.s.send("NICK {}\r\n".format(self.bot_config['nick']).encode("utf-8"))
            self.s.send("JOIN #{}\r\n".format(self.bot_config['chan'].lower()).encode("utf-8"))
            time.sleep(1)
            self.send_message(self.infomessage)
            self.s.setblocking(0)


    ### Chat message sender func
    def send_message(self, msg):
        sendmsg = ":"+self.bot_config['nick']+"!"+self.bot_config['nick']+"@"+self.bot_config['nick']+".tmi.twitch.tv PRIVMSG #"+self.bot_config['chan']+" : "+msg+"\r\n"
        if 'iso' in self.bot_config['encoding'].lower():
            sendmsg2 = sendmsg.encode(self.bot_config['encoding'])
        else:
            sendmsg2 = sendmsg.encode("utf-8")
        try:
            self.s.send(sendmsg2)
            logging.debug("Sending msg: %s" % sendmsg2)
        except (BrokenPipeError, TimeoutError):
            time.sleep(1)
            self.connect()

    def retrieve_messages(self):
        username, message, cleanmessage = None, None, None
        try:
            response = self.s.recv(1024).decode("utf-8")
            logging.debug("Response:\n%s" % response)
            if response == "PING :tmi.twitch.tv\r\n":
                self.s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
                logging.debug("Pong sent")
            else:
                username = re.search(r"\w+", response).group(0) 
                if username == self.bot_config['nick']:  # Ignore this bot's messages
                    pass
                else:
                    message = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :").sub("", response)
                    cleanmessage = re.sub(r"\s +", "", message, flags=re.UNICODE).replace("\n","").replace("\r","")

#                    logging.debug("USER RESPONSE: " + username + " : " + message)
#                    if cleanmessage in var.COMMANDLIST:
#                        logging.debug("Command recognized.")
#                        trivia_commandswitch(cleanmessage,username)
#                        time.sleep(1)
        except: 
#            logging.debug(traceback.print_exc())

            pass
        return username, message, cleanmessage

def main():
    #main_window = MainWindow()
    #main_window.window.show()
    #main_window.app.exec_()
    mainloop = MainLoop()
    mainloop.connect()
if __name__ == '__main__':
    main()
