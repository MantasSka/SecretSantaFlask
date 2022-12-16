from flask import Flask, render_template, request
import random
import smtplib

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def secret_santa():
    if request.method == 'POST':
        # Get the list of participants and email addresses from the form
        participants = request.form.get('participants').strip().split('\n')
        email_addresses = request.form.get(
            'email_addresses').strip().split('\n')

        # Zip the participants and email addresses into a list of tuples
        participant_emails = list(zip(participants, email_addresses))

        # Shuffle the list of participant emails
        random.shuffle(participant_emails)

        # Create a list of pairs
        pairs = list(
            zip(participant_emails, participant_emails[1:] + [participant_emails[0]]))

        # Get the email server and sender address from the form
        email_server = request.form.get('email_server')
        sender_address = request.form.get('sender_address')

        # Connect to the email server
        server = smtplib.SMTP(email_server)
        server.starttls()
        server.login(sender_address, request.form.get('sender_password'))

        # Send an email to each participant with their Secret Santa pair
        for (participant, email), secret_santa in pairs:
            message = f"""\
            Subject: Your Secret Santa Pair

            Hi {participant},

            Your Secret Santa for this year is {secret_santa[0]}!

            We hope you have a great time with this gift exchange.

            Best regards,
            The Secret Santa Organizer - Mantas Skara"""
            server.sendmail(sender_address, email, message)

        # Close the connection to the email server
        server.quit()

        # Render the template with the pairs
        return render_template('secret_santa.html', pairs=pairs)
    else:
        # Render the form template
        return render_template('form.html')
