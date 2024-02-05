from flask_app import app
from flask import render_template, redirect, flash, session, request
from flask_app.models.show import Show
from flask_app.models.user import User
from datetime import datetime
from flask_app.models.comment import Comment 

@app.route('/shows')
def books():
    if 'user_id' in session:
        user_id = session['user_id']
        shows = Show.get_all()
        logged_user = User.get_user_by_id({'id': user_id})
        return render_template('shows.html', shows=shows, loggedUser=logged_user)
    return redirect('/')

@app.route('/shows/new')
def addShow():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('create.html')





@app.route('/shows/new', methods=['POST'])
def createShow():
    if 'user_id' not in session:
        return redirect('/login')
    
    form_data = request.form
    
    # Validate form data
    if not form_data.get('title') or not form_data.get('network') or not form_data.get('comments') or not form_data.get('release_date'):
        flash('All fields are required', 'createShowError')
        return redirect(request.referrer)
    if len(form_data.get('title')) < 3 or len(form_data.get('network')) < 3 or len(form_data.get('comments')) < 3:
        flash('Title, Network, and Comments must be at least 3 characters', 'createShowError')
        return redirect(request.referrer)
    
    # Convert release_date to suitable format
    release_date = datetime.strptime(form_data['release_date'], '%Y-%m-%d').date()

    data = {
        'title': form_data['title'],
        'network': form_data['network'],
        'release_date': release_date,
        'comments': form_data['comments'],
        'user_id': session['user_id']
    }
    
    Show.create(data)
    return redirect('/shows')
   

@app.route('/shows/<int:id>')
def viewShow(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': id,
        'show_id': id
    }
    show = Show.get_show_by_id(data)
 
    return redirect('/')


@app.route('/shows/delete/<int:id>')
def deleteShow(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': id,
    }
    show = Show.get_show_by_id(data)
    if show and show['user_id'] == session['user_id']:
        
        Show.delete(data)
    return redirect('/')

@app.route('/shows/edit/<int:id>')
def editShow(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': id
    }
    show = Show.get_show_by_id(data)
    if show and show['user_id'] == session['user_id']:
        return render_template('edit.html', show=show)
    return redirect('/')

@app.route('/shows/update/<int:id>', methods=['POST'])
def updateShow(id):
    if 'user_id' not in session:
        return redirect('/')
    
    # Retrieve the show data from the form
    form_data = request.form
    
    # Validate form data
    if not form_data.get('title') or not form_data.get('network') or not form_data.get('comments') or not form_data.get('release_date'):
        flash('All fields are required', 'updateShowError')
        return redirect(request.referrer)
    if len(form_data.get('title')) < 3 or len(form_data.get('network')) < 3 or len(form_data.get('comments')) < 3:
        flash('Title, Network, and Comments must be at least 3 characters', 'updateShowError')
        return redirect(request.referrer)
    
    # Convert release_date to suitable format
    release_date = datetime.strptime(form_data['release_date'], '%Y-%m-%d').date()

    # Prepare the data for updating the show
    data = {
        'id': id,
        'title': form_data['title'],
        'network': form_data['network'],
        'release_date': release_date,
        'comments': form_data['comments']
    }
    
    # Update the show in the database
    Show.update(data)
    
    # Redirect to the dashboard
    return redirect('/shows')




@app.route('/shows/view/<int:id>')
def ShowInfo(id):
    if 'user_id' not in session:
        return redirect('/login')  # Redirect to login if user is not logged in

    # Retrieve the show information from the database
    data = {
        'id': id
    }
    show = Show.get_show_by_id(data)
    if not show:
        flash('Show not found', 'showInfoError')
        return redirect('/shows')  # Redirect to shows list if show not found

    # Get the logged-in user's information
    logged_user = User.get_user_by_id({'id': session['user_id']})
    comments = Comment.get_comments_for_show(id)

    return render_template('view_show.html', show=show, logged_user=logged_user, comments=comments)
    # Render the template with the show details
   




# Update Flask Routes for Comment Submission and Deletion
@app.route('/shows/comment/<int:show_id>', methods=['POST'])
def add_comment(show_id):
    if 'user_id' not in session:
        return redirect('/login')

    form_data = request.form

    if not form_data.get('comment'):
        flash('Comment cannot be empty', 'commentError')
        return redirect(request.referrer)

    data = {
        'comment': form_data['comment'],
        'user_id': session['user_id'],
        'show_id': show_id
    }

    Comment.create_comment(data)
    return redirect(f'/shows/view/{show_id}')

@app.route('/shows/comment/<int:show_id>', methods=['POST'])
def addcomment(show_id):
    if 'user_id' not in session:
        return redirect('/login')  # Redirect to login if user is not logged in

    # Get comment data from form
    comment_text = request.form.get('comment')

    # Ensure comment text is not empty
    if not comment_text:
        flash('Comment cannot be empty', 'error')
        return redirect(f'/shows/view/{show_id}')

    # Save the comment to the database
    comment_data = {
        'comment': comment_text,
        'user_id': session['user_id'],
        'show_id': show_id
    }
    Comment.create(comment_data)  # Assuming you have a Comment model with a create method

    # Redirect back to the show view page after adding the comment
    return redirect(f'/shows/view/{show_id}')

@app.route('/shows/comment/delete/<int:comment_id>')
def delete_comment(comment_id):
    if 'user_id' not in session:
        return redirect('/login')

    comment = Comment.get_comment_by_id(comment_id)

    if comment and comment['user_id'] == session['user_id']:
        Comment.delete_comment(comment_id)

    return redirect(request.referrer)







