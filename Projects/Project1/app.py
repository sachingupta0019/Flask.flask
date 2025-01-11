from flask import Flask, request, render_template

## Create a Flask app
#Step 1 : Create a Flask app.
app = Flask(__name__)
#Step 2 : Define the route
@app.route("/", methods = ['GET']) # Define the route
#step 3 : Define the function for the route
def home():
    return "Hello World!" # Return the response


@app.route("/about/<int:number>") # Define the route
def about(number):
    return "About Page"+ str(number)

# Display Form using template
@app.route('/form',methods = ['GET', 'POST'])
def form():
    if request.method == "GET":
        return render_template('form.html')
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        full_name = first_name + " " + last_name
        return render_template('form.html', Name = full_name)



if __name__ == "__main__":
    app.run(debug=True) # Run the app in debug mode