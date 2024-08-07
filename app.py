from flask import Flask, render_template, request, redirect, url_for
import ezgmail

app = Flask(__name__)

# Function to read inbox
def read_inbox():
    # Use ezgmail to read inbox
    unread_threads = ezgmail.unread()
    inbox_emails = []
    for thread in unread_threads:
        # Extract necessary information from each email thread
        email_info = {
            'sender': thread.messages[0].sender,
            'subject': thread.messages[0].subject,
            'snippet': thread.messages[0].snippet,
            'timestamp': thread.messages[0].timestamp,
            'message': thread.messages[0].body,  # Fetch full message body
        }
        inbox_emails.append(email_info)
    return inbox_emails

# Landing Page
@app.route('/')
def index():
    return render_template('index.html')

# Inbox Page
@app.route('/inbox')
def inbox():
    inbox_emails = read_inbox()
    return render_template('inbox.html', emails=inbox_emails)

# Send Email Page
@app.route('/send_email')
def send_email():
    return render_template('send_email.html')

# Send Bulk Email Page
@app.route('/send_bulk_email')
def send_bulk_email():
    return render_template('send_bulk_email.html')

# Send Email Functionality
@app.route('/send', methods=['POST'])
def send():
    recipient = request.form['recipient']
    subject = request.form['subject']
    message = request.form['message']
    ezgmail.send(recipient, subject, message)
    return redirect(url_for('index'))

# Send Bulk Email Functionality
@app.route('/send_bulk', methods=['POST'])
def send_bulk():
    recipients = request.form['recipients'].split(',')
    subject = request.form['subject']
    message = request.form['message']
    ezgmail.send(recipients, subject, message)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
