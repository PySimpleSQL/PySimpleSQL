#!/usr/bin/python3
import PySimpleGUI as sg
import pysimplesql as ss                               # <=== PySimpleSQL lines will be marked like this.  There's only a few!
import logging
logger=logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)               # <=== You can set the logging level here (NOTSET,DEBUG,INFO,WARNING,ERROR,CRITICAL)

# Here are our callback functions
def enable(db,win):
    res=sg.popup_get_text('Enter password for edit mode.\n(Hint: it is 1234)')
    return True if res=='1234' else False
def disable(db,win):
    res = sg.popup_yes_no('Are you sure you want to disabled edit mode?')
    return True if res == 'Yes' else False

# Define our layout. We will use the ss.record convenience function to create the controls
layout = [
    ss.record('Restaurant.name'),
    ss.record('Restaurant.location'),
    ss.record('Restaurant.fkType', sg.Combo, size=(30,10), auto_size_text=False)]
sub_layout = [
    ss.selector('selector1','Item',size=(35,10))+
    [sg.Col([ss.record('Item.name'),
         ss.record('Item.fkMenu', sg.Combo, size=(30,10), auto_size_text=False),
         ss.record('Item.price'),
         ss.record('Item.description', sg.MLine, (30, 7))
    ])],
    ss.actions('act_item','Item', edit_protect=False,navigation=False,save=False, search=False)
]
layout += [[sg.Frame('Items', sub_layout)]]
layout += [ss.actions('act_restaurant','Restaurant')]

# Initialize our window and database, then bind them together
win = sg.Window('places to eat', layout, finalize=True)
db = ss.Database(':memory:', win,sql_script='example.sql')      # <=== load the database and bind it to the window
# NOTE: ":memory:" is a special database URL for in-memory databases

# Set our callbacks
# See documentation for a full list of callbacks supported
db.set_callback('edit_enable',enable)
db.set_callback('edit_disable',disable)

while True:
    event, values = win.read()

    if db.process_events(event, values):                  # <=== let PySimpleSQL process its own events! Simple!
        logger.info('PySimpleDB event handler handled the event!')
    elif event == sg.WIN_CLOSED or event == 'Exit':
        db=None              # <= ensures proper closing of the sqlite database and runs a database optimization at close
        break
    else:
        logger.info(f'This event ({event}) is not yet handled.')





