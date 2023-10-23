import tools
prompt1 = '''suppose you are using calendar app on a smartphone, given a GUI screen described in html, please summarize the function of this UI screen in some phrases with verb and noun. Just return the function, do not tell me which button to click or which textbox to input, do not include 'go back to the front page', or 'scroll up/down' or any thing that you need to jump to another ui screen.  
For example:\nGUI:\n<button checked=True>No repetition</button>\n<button checked=False>Daily</button>\n<button checked=False>Weekly</button>\n<button checked=False>Monthly</button>\n<button checked=False>Yearly</button>\n<button checked=False>Custom</button>
You should answer:\nSet event reminder to non-recurring, daily, weekly, monthly, yearly and custom.\n
Now please summarize the function of this GUI screen:
<button id=0 checked=False>Algeria</button>\n<button id=1 checked=False>Argentina</button>\n
<button id=2 checked=False>Australia</button>\n<button id=3 checked=False>Belgi\xEB
</button>\n<button id=4 checked=False>Bolivia</button>\n<button id=5 checked=False>Brasil</button>\n
<button id=6 checked=False>Canada</button>\n<button id=7 checked=False>China</button>\n
<button id=8 checked=False>Colombia</button>\n<button id=9 checked=False>\u010C
esk\xE1 republika</button>\n<button id=10 checked=False>Danmark</button>\n<button
\ id=11 checked=False>Deutschland</button>\n<button id=12 checked=False>Eesti</button>\n
<button id=13 checked=False>Espa\xF1a</button>\n<button id=14 class='ImageButton'>go
\ back</button>\n<button id=15 checked=False>\xC9ire</button>\n<button id=16 checked=False>France</button>\n
<button id=17 checked=False>Hanguk</button>\n<button id=18 checked=False>Hellas</button>\n
<button id=19 checked=False>Hrvatska</button>\n<button id=20 checked=False>India</button>\n
<button id=21 checked=False>Indonesia</button>\n<button id=22 checked=False>\xCD
sland</button>\n<button id=23 checked=False>Italia</button>\n<button id=24 checked=False>Latvija</button>\n
<button id=25 checked=False>Lietuva</button>\n<button id=26 checked=False>Luxemburg</button>\n
<button id=27 checked=False>Makedonija</button>\n<button id=28 checked=False>Magyarorsz\xE1
g</button>\n<button id=29 checked=False>M\xE9xico</button>\n<button id=30 checked=False>Nederland</button>\n
<button id=31 checked=False>\u65E5\u672C</button>\n<button id=32 checked=False>Norge</button>\n
<button id=33 checked=False>\xD6sterreich</button>\n<button id=34 checked=False>P\u0101
kist\u0101n</button>\n<button id=35 checked=False>Polska</button>\n<button id=36
\ checked=False>Portugal</button>\n<button id=37 checked=False>\u0420\u043E\u0441
\u0441\u0438\u044F</button>\n<button id=38 checked=False>Rom\xE2nia</button>\n
<button id=39 checked=False>Schweiz</button>\n<button id=40 checked=False>Srbija</button>\n
<button id=41 checked=False>Slovenija</button>\n<button id=42 checked=False>Slovensko</button>\n
<button id=43 checked=False>South Africa</button>\n<button id=44 checked=False>Suomi</button>\n
<button id=45 checked=False>Sverige</button>\n<button id=46 checked=False>Ukraine</button>\n
<button id=47 checked=False>United Kingdom</button>\n<button id=48 checked=False>United
\ States</button>
please answer the phrases. Note that if there are a series of  countries, place names, names, time, dates, or any semantically repetitive sentence or words on buttons or texts, do not list them, summarize them in there category.'''

prompt2 = '''suppose you are using calendar app on a smartphone, given a GUI screen described in html, please summarize the function of this UI screen in some  phrases with verb and noun. 
For example:\nGUI:\n<button checked=True>No repetition</button>\n<button checked=False>Daily</button>\n<button checked=False>Weekly</button>\n<button checked=False>Monthly</button>\n<button checked=False>Yearly</button>\n<button checked=False>Custom</button>
You should answer:\nSet event reminder to non-recurring, daily, weekly, monthly, yearly and custom.\n
Now please summarize the function of this GUI screen:
<button id=0 class=''Navigate up'' checked=False></button>

    <p id=1>Settings</p>

    <button id=2 checked=False>Customize colors</button>

    <button id=3 checked=False>Manage event types</button>

    <button id=4 checked=False>Use 24-hour time format OFF</button>

    <button id=5 checked=True>Start week on Sunday ON</button>

    <button id=6 checked=False>Avoid showing What''s New on startup OFF</button>

    <button id=7 checked=False>Delete all events</button>

    <p id=8>EVENT REMINDERS</p>

    <button id=9 checked=False>Vibrate on reminder notification OFF</button>

    <button id=10 checked=False>Reminder sound<br>Default (Pixie Dust)</button>

    <button id=11 checked=True>Always use same snooze time ON</button>

    <button id=12 checked=False>Snooze time<br>10 minutes</button>

    <button id=13 class=''ImageButton''>go back</button>

    <p id=14>CALDAV</p>

    <button id=15 checked=False>CalDAV sync OFF</button>

    <p id=16>WEEKLY VIEW</p>

    <button id=17 checked=False>Start day at<br>07:00</button>

    <button id=18 checked=False>End day at<br>23:00</button>

    <p id=19>MONTHLY VIEW</p>

    <button id=20 checked=False>Show week numbers OFF</button>

    <button id=21 checked=False>Show a grid OFF</button>

    <p id=22>EVENT LISTS</p>

    <button id=23 checked=False>Replace event description with location OFF</button>

    <button id=24 checked=False>Display events from the past<br>Never</button>

    <p id=25>WIDGETS</p>

    <button id=26 checked=False>Font size<br>Medium</button>
please answer the phrases. Note that if there are a series of  countries, place names, names, time, dates, or any semantically repetitive sentence or words on buttons or texts, do not list them, summarize them in there category. Just return the phrases, do not tell me which button to click or which textbox to input, do not include 'go back to the front page', or 'scroll up/down' or any thing that you need to jump to another ui screen. '''


print(tools.query_gpt('hello'))