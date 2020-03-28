#importing the important packages for our project
from flask import Flask, render_template, request, redirect,url_for
import pymongo
from bson import ObjectId

#with this single line of code, we will create a new Flask app!
#in technical speak, what we are doing is "instantiating a Flask object"...
app = Flask(__name__)

#here, we paste the code that MongoDB gave us to call our MongoDB Atlas cluster
client = pymongo.MongoClient("mongodb+srv://admin:zdEGl1wIgyJ47LVZ@hackplanner-ahnzl.gcp.mongodb.net/test?retryWrites=true&w=majority")
#then, we can pull out the database
db = client.hack_planner
#and the collections
hack_ideas=db.hack_ideas
cool_techs=db.cool_techs
lessons_learned=db.lessons_learned

#the purpose of this function is to make sure we always route to the home (index) page
def redirect_url():
    return request.args.get('next') or request.referrer or url_for('index')

#update our app with the latest data from MongoDB
def update():                   
    #here, we are retrieving the values from each collection
    hack_ideas_new=hack_ideas.find()
    cool_techs_new=cool_techs.find()
    lessons_learned_new=lessons_learned.find()
    #then, we return them to the webpage and reload
    return render_template('index.html', hack_ideas=hack_ideas_new, cool_techs=cool_techs_new, lessons_learned=lessons_learned_new)

#this command ensures that the update function will run every time we return home
app.add_url_rule("/", "update", update)


#add an idea for a hack to the list
@app.route('/add_idea', methods=['POST'])
def add_idea():
    #pull the new values from the form
    potential_title=request.values.get('potential_title')
    brief_description=request.values.get('brief_description')
    potential_collaborators=request.values.get('potential_collaborators')
    #aggregate the data from the form and insert into a new MongoDB document
    hack_ideas.insert({'potential_title':potential_title, 'brief_description':brief_description, 'potential_collaborators':potential_collaborators})
    #finally, returning to home will make sure that we update our page with the new database values
    return redirect('/')

#scrap an idea from the list
@app.route('/remove_idea')
def remove_idea():
    #this line of code gets the ID of the chosen document and removes it from the database
    hack_ideas.remove({'_id':ObjectId(request.values.get('_id'))})
    #return home (and update)
    return redirect('/')

#add technology you learned about to the list
@app.route('/add_tech', methods=['POST'])
def add_tech():
    #pull the new values from the form
    name=request.values.get('name')
    website_docs=request.values.get('website_docs')
    potential_use_cases=request.values.get('potential_use_cases')
    #aggregate and add the data
    cool_techs.insert({'name':name, 'website_docs':website_docs, 'potential_use_cases':potential_use_cases})
    #return home (and update)
    return redirect('/')

#scrap tech from the list
@app.route('/remove_tech')
def remove_tech():
    #remove a technology from the database
    cool_techs.remove({'_id':ObjectId(request.values.get('_id'))})
    #go home (and update)
    return redirect('/')

#add a lesson learned from a recent hackathon
@app.route('/add_lesson', methods=['POST'])
def add_lesson():
    #pull the new values from the form
    date=request.values.get('date')
    devpost_link=request.values.get('devpost_link')
    notes=request.values.get('notes')
    #aggregate and add the data
    lessons_learned.insert({'date':date, 'devpost_link':devpost_link, 'notes':notes})
    #return home (and update)
    return redirect('/')

#unlearn a lesson
@app.route('/remove_lesson')
def remove_lesson():
    #remove a lesson from the database
    lessons_learned.remove({'_id':ObjectId(request.values.get('_id'))})
    #return home (and update)
    return redirect('/')
