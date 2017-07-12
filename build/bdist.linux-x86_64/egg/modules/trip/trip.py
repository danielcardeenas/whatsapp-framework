from app.mac import mac
from modules.trip.person import Person
import sqlite3

conn = sqlite3.connect('modules/trip/db/gdl.db')

def get_debters():
    people = []
    for row in conn.execute('select name, airbnb, vuelo from debters'):                                                                                                                                           
        people.append(Person(row[0], row[1], row[2]))
    
    return people
    

def print_debts():
    people = get_debters()
    print("Peeps: ", people)
    text = ''
    for person in people:
        text += '*' + person.name + '*: '
        text += '🏡 $'+ airbnb_debt(person.airbnb) + ' '
        text += '✈ $' + flight_debt(person.flight)
        text += '\n'
    
    print("Text: ", text)
    return text
        
def airbnb_debt(money):
    if money == None:
        return '-'
    
    return str(1330 - money)
    
def flight_debt(money):
    if money == None:
        return '-'
        
    return str(2000 - money)